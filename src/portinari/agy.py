"""Wrapper do `agy` (Antigravity CLI) para gerar imagens. Ver docs/agy.md.

Fatos em que isto se apoia (docs/agy.md): não há comando de imagem — `agy -p` pede ao agente que
chame a ferramenta `generate_image(Prompt, ImageName, AspectRatio, ImagePaths)`; um LLM de texto
fica no meio e pode reescrever o prompt; `status` do JSON não é confiável (pode ser ERROR com
exit 0). Por isso o resultado é lido do transcript (`GENERATE_IMAGE`), e o prompt que a ferramenta
recebeu de fato é comparado com o pretendido.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from PIL import Image
from pydantic import BaseModel, Field

HOME = Path(os.environ.get("PORTINARI_AGY_HOME", "~/.gemini/antigravity-cli")).expanduser()
# Enum de AspectRatio que a ferramenta declara ao modelo (docs/agy.md §3.1).
PROPORCOES = {"1:1": 1.0, "2:3": 2 / 3, "3:2": 3 / 2, "3:4": 3 / 4, "4:3": 4 / 3, "9:16": 9 / 16, "16:9": 16 / 9}
# Escada de orquestradores: começa barato; se o prompt for reescrito/falhar, sobe (mitiga R1).
ESCADA_MODELOS = ("gemini-3.8-flash-low", "gemini-3.8-flash-medium", "gemini-3.8-flash-high")
MAX_GERACOES = 12


class AgyErro(Exception):
    pass


class TetoDeGeracoes(AgyErro):
    pass


class Geracao(BaseModel):
    k: int
    tentativa: int
    comando: list[str]
    modelo_orquestrador: str
    conversation_id: str | None = None
    status_agy: str | None = None
    erro: str | None = None
    proporcao: str
    nome: str
    origem: str = "agy"  # "agy" | "manual" (imagem gerada fora e importada)
    modelo_imagem: str | None = None  # só declarado na importação manual (ex.: nano-banana-pro)
    referencias: list[str] = Field(default_factory=list)
    imagem: str | None = None
    largura: int | None = None
    altura: int | None = None
    sha256: str | None = None
    fiel: bool = False  # prompt efetivo == pretendido (espaços normalizados)
    hex_ausentes: list[str] = Field(default_factory=list)  # hex do pretendido que sumiram
    inicio: str = ""
    duracao_s: float = 0.0


def melhor_proporcao(largura: int, altura: int) -> str:
    """Proporção do enum mais próxima do alvo (menos corte/ampliação depois)."""
    alvo = math.log(largura / altura)
    return min(PROPORCOES, key=lambda p: abs(math.log(PROPORCOES[p]) - alvo))


def montar_prompt(criativo: str, bloco: str, largura: int, altura: int) -> str:
    """Parte criativa + bloco de marca injetado por código (o LLM nunca o reescreve)."""
    tecnico = (
        f"## Technical\nTarget final size {largura}x{altura}. Render at the highest resolution and "
        "level of detail the generator supports; keep every edge crisp."
    )
    return f"{criativo.strip()}\n\n{bloco.strip()}\n\n{tecnico}\n"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _instrucao(prompt: str, proporcao: str, nome: str, refs: list[str], tentativa: int) -> str:
    linhas = [
        "Use your built-in generate_image tool exactly once, with these arguments:",
        "- Prompt: the text between the lines <<<PROMPT and PROMPT>>> below, copied VERBATIM, character "
        "for character. Do not translate, summarize, shorten, reorder, add or remove anything.",
        f'- AspectRatio: "{proporcao}"',
        f'- ImageName: "{nome}"',
    ]
    if refs:
        linhas.append(f"- ImagePaths: {json.dumps(refs)}")
    linhas += ["Do not call any other tool. Do not describe the image. When the tool finishes, reply only: DONE"]
    if tentativa > 1:
        linhas.append("WARNING: a previous attempt changed the prompt. Copy it EXACTLY, every line.")
    return "\n".join(linhas) + f"\n\n<<<PROMPT\n{prompt.strip()}\nPROMPT>>>\n"


def passos_imagem(conversation_id: str, home: Path = HOME) -> list[dict]:
    """Passos de geração do transcript: [{prompt, caminho}] (prompt = o que a ferramenta recebeu).
    Não filtra pelo `type` do passo: no agy 1.2.7 em headless ele vem como GENERIC (S1), nas sessões
    antigas como GENERATE_IMAGE — o que identifica o passo é o conteúdo."""
    p = home / "brain" / conversation_id / ".system_generated" / "logs" / "transcript_full.jsonl"
    if not p.is_file():
        return []
    passos = []
    for linha in p.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(linha)
        except ValueError:
            continue
        if r.get("status") != "DONE":
            continue
        m = re.search(r"Using prompt: (.*?)\n\s*\nGenerated image is saved at (\S+?\.(?:jpe?g|png|webp))\.", r.get("content", ""), re.S)
        if m:
            passos.append({"prompt": m.group(1), "caminho": m.group(2)})
    return passos


def _hex(s: str) -> set[str]:
    return {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", s)}


def _contar(saida: Path) -> int:
    log = saida / "geracoes.jsonl"
    return len(log.read_text().splitlines()) if log.is_file() else 0


def _transitorio(cp: subprocess.CompletedProcess) -> bool:
    """exit 3 + AGY_ERROR com retryable != false (changelog 1.2.6)."""
    m = re.search(r"AGY_ERROR:\s*(\{.*\})", cp.stderr or "")
    if not m:
        return False
    try:
        return json.loads(m.group(1)).get("retryable", True) is not False
    except ValueError:
        return True


def gerar(
    prompt: str,
    proporcao: str,
    saida: Path,
    iteracao: int,
    *,
    referencias: list[str] | None = None,
    max_geracoes: int = MAX_GERACOES,
    tentativas: int = 3,
    modelo: str | None = None,
    timeout: int = 300,
    dormir: Callable[[float], None] = time.sleep,
    folga: int = 30,
    home: Path | None = None,
) -> Geracao:
    """Gera UMA imagem (com retentativas). Grava gen_K.{jpg,prompt.md,efetivo.md,json} em
    `saida/iteracoes/NN/` e uma linha em `saida/geracoes.jsonl` por tentativa.
    Devolve a primeira tentativa fiel; senão a última (com fiel=False para o chamador decidir)."""
    saida, home = Path(saida), home or HOME
    pasta = saida / "iteracoes" / f"{iteracao:02d}"
    pasta.mkdir(parents=True, exist_ok=True)
    base = shlex.split(os.environ.get("PORTINARI_AGY", "agy"))
    refs = [str(Path(r).resolve()) for r in (referencias or [])]
    ultima: Geracao | None = None
    erros: list[str] = []
    for tentativa in range(1, tentativas + 1):
        if _contar(saida) >= max_geracoes:
            if ultima:  # já temos uma imagem (paga): devolve em vez de perdê-la
                return ultima
            raise TetoDeGeracoes(f"teto de {max_geracoes} gerações atingido em {saida}")
        k = len(list(pasta.glob("gen_*.json"))) + 1
        nome = f"gen_{k:02d}"
        mod = modelo or ESCADA_MODELOS[min(tentativa - 1, len(ESCADA_MODELOS) - 1)]
        cmd = [*base, "-p", _instrucao(prompt, proporcao, nome, refs, tentativa), "--output-format", "json",
               "--model", mod, "--print-timeout", f"{timeout}s", "--add-dir", str(pasta.resolve()),
               *[a for r in refs for a in ("--add-dir", str(Path(r).parent))]]
        g = Geracao(k=k, tentativa=tentativa, comando=cmd,
                    modelo_orquestrador=mod, proporcao=proporcao, nome=nome, referencias=refs,
                    inicio=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        (pasta / f"{nome}.prompt.md").write_text(prompt, encoding="utf-8")
        t0 = time.monotonic()
        transitorio = False
        try:
            cp = subprocess.run(cmd, capture_output=True, text=True, cwd=pasta, timeout=timeout + folga)
        except subprocess.TimeoutExpired:
            g.erro, transitorio = f"timeout de {timeout}s", True
        else:
            try:
                j = json.loads(cp.stdout.strip().splitlines()[-1])
            except (ValueError, IndexError):
                j = {}
            g.conversation_id, g.status_agy = j.get("conversation_id"), j.get("status")
            g.erro = j.get("error") or (cp.stderr.strip()[:500] or None if cp.returncode else None)
            if cp.returncode and not _transitorio(cp):
                g.duracao_s = round(time.monotonic() - t0, 1)
                _registrar(saida, iteracao, g, pasta, prompt, "")
                raise AgyErro(f"agy saiu com {cp.returncode} (não transitório): {g.erro}")
            transitorio = bool(cp.returncode)
            # o status do JSON não é confiável: vale o passo de geração do transcript
            efetivo = coletar(g, prompt, pasta, home)
            if efetivo is not None:
                g.duracao_s = round(time.monotonic() - t0, 1)
                _registrar(saida, iteracao, g, pasta, prompt, efetivo)
                ultima = g
                if g.fiel:
                    return g
                continue  # prompt reescrito: tenta de novo com modelo mais forte
            g.erro = g.erro or "nenhuma imagem gerada (sem passo GENERATE_IMAGE no transcript)"
            transitorio = True
        g.duracao_s = round(time.monotonic() - t0, 1)
        _registrar(saida, iteracao, g, pasta, prompt, "")
        erros.append(f"tentativa {tentativa}: {g.erro}")
        if not transitorio:
            break
        if tentativa < tentativas:
            dormir(5 * 2 ** (tentativa - 1))
    if ultima:
        return ultima
    raise AgyErro("sem imagem após retentativas — " + " | ".join(erros))


def coletar(g: Geracao, prompt: str, pasta: Path, home: Path) -> str | None:
    """Copia a imagem da conversa para a pasta da iteração e preenche `g`. Devolve o prompt efetivo
    (o que a ferramenta recebeu) ou None se a conversa não gerou imagem."""
    passos = passos_imagem(g.conversation_id, home) if g.conversation_id else []
    if not (passos and Path(passos[-1]["caminho"]).is_file()):
        return None
    passo = passos[-1]
    destino = pasta / f"{g.nome}{Path(passo['caminho']).suffix}"
    shutil.copy2(passo["caminho"], destino)
    with Image.open(destino) as im:
        g.largura, g.altura = im.size
    g.imagem, g.sha256 = str(destino), hashlib.sha256(destino.read_bytes()).hexdigest()
    g.fiel = _norm(passo["prompt"]) == _norm(prompt)
    g.hex_ausentes = sorted(_hex(prompt) - _hex(passo["prompt"]))
    g.erro = None if g.fiel else g.erro
    return passo["prompt"]


def _registrar(saida: Path, iteracao: int, g: Geracao, pasta: Path, pretendido: str, efetivo: str) -> None:
    (pasta / f"{g.nome}.efetivo.md").write_text(efetivo or "(a ferramenta não recebeu prompt)", encoding="utf-8")
    (pasta / f"{g.nome}.json").write_text(g.model_dump_json(indent=2), encoding="utf-8")
    with (saida / "geracoes.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"iteracao": iteracao, **g.model_dump()}, ensure_ascii=False) + "\n")


def importar(
    imagens: list[Path],
    prompt: str,
    saida: Path,
    iteracao: int,
    *,
    modelo: str | None = None,
    max_geracoes: int = MAX_GERACOES,
) -> list[Geracao]:
    """Traz para a execução imagens geradas à mão (ex.: no Nano Banana Pro colando `prompt_final.md`).
    Cada imagem vira gen_KK.<ext> + prompt completo + gen_KK.json (origem "manual") e conta como
    uma geração. Valida que é imagem antes de gravar qualquer coisa."""
    saida = Path(saida)
    pasta = saida / "iteracoes" / f"{iteracao:02d}"
    validas = []
    for img in map(Path, imagens):
        try:
            with Image.open(img) as im:
                im.verify()
            with Image.open(img) as im:
                validas.append((img, im.size))
        except Exception as e:
            raise AgyErro(f"{img} não é uma imagem válida") from e
    if _contar(saida) + len(validas) > max_geracoes:
        raise TetoDeGeracoes(f"importar {len(validas)} imagem(ns) passaria do teto de {max_geracoes} gerações")
    pasta.mkdir(parents=True, exist_ok=True)
    feitas = []
    for img, (w, h) in validas:
        k = len(list(pasta.glob("gen_*.json"))) + 1
        nome = f"gen_{k:02d}"
        destino = pasta / f"{nome}{img.suffix.lower()}"
        shutil.copy2(img, destino)
        g = Geracao(k=k, tentativa=1, comando=[], modelo_orquestrador="manual", modelo_imagem=modelo,
                    origem="manual", proporcao=melhor_proporcao(w, h), nome=nome, imagem=str(destino),
                    largura=w, altura=h, sha256=hashlib.sha256(destino.read_bytes()).hexdigest(),
                    fiel=True, inicio=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        (pasta / f"{nome}.prompt.md").write_text(prompt, encoding="utf-8")
        _registrar(saida, iteracao, g, pasta, prompt, "(geração manual: prompt colado pelo autor no gerador; não verificável)")
        feitas.append(g)
    return feitas
