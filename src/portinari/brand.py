"""Resolve a marca em runtime a partir de brand/ (nunca duplicada) → brand_snapshot.json.

Autoridade (docs/PLANO.md §2.1): tokens (valor) > DESIGN.md (regra) > _bloco-marca.md (bloco
operacional) > meta-prompt. Decisão do autor (A2): o pedido vence a marca, EXCETO a paleta — por
isso a paleta é a única parte vinculante; o resto entra como padrão sobreponível.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path

from .brief import RAIZ

BRAND = RAIZ / "brand"
MODOS = ("dark", "light")
ARQUIVOS = (
    "tokens/syntaxis.tokens.json",
    "DESIGN.md",
    "ILUSTRACOES/_bloco-marca.md",
    "ILUSTRACOES/meta-prompt-collage-paper-cut.md",
)
# Seções de _bloco-marca.md por prefixo de título (sem acento/caixa).
INJETAR = ("borda e reticula", "escala pequena", "sem texto renderizado")  # verbatim
LINT = "descritores proibidos"  # não entra no prompt: só lint da parte criativa
# "A escada" fica de fora: é a parte anti-sombra e o autor decidiu que o pedido vence (A2).
DESCARTADAS = ("a escada",)
GERADAS = ("paleta", "tetos numericos")  # regeneradas dos tokens (nunca hex do .md)
NOMES_MODO = {"dark": "escura", "light": "clara"}


class BrandError(Exception):
    pass


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _plano(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def _res(tokens: dict, valor: str) -> str:
    """Resolve aliases DTCG `{a.b.c}` até chegar ao hex."""
    while isinstance(valor, str) and valor.startswith("{"):
        alias = valor.strip("{}")
        no = tokens
        for parte in alias.split("."):
            try:
                no = no[parte]
            except KeyError as e:
                raise BrandError(f"alias de token inexistente: {alias}") from e
        valor = no["$value"]
    return str(valor).upper()


def paleta(tokens: dict, modo: str) -> dict:
    """Paleta do modo, toda derivada dos tokens."""
    ill = tokens["illustration"]
    camadas = []
    for nome in sorted((k for k in ill["stack"][modo] if k.startswith("layer")), key=lambda k: int(k[5:])):
        bruto = ill["stack"][modo][nome]["$value"]
        camadas.append(
            {"token": f"illustration.stack.{modo}.{nome}", "alias": bruto.strip("{}"), "hex": _res(tokens, bruto)}
        )
    figura = [
        {"token": f"illustration.figure.{k}", "alias": ill["figure"][k]["$value"].strip("{}"),
         "hex": _res(tokens, ill["figure"][k]["$value"])}
        for k in ("primary", "secondary")
    ]
    # brand/ILUSTRACOES/_bloco-marca.md: Lime 500 na pilha escura; Lime 700 se o fundo for a pilha
    # clara. lime.700 não tem alias em illustration.* (docs/PLANO.md C8), então lê color.lime.700.
    if modo == "light":
        acento = {"token": "color.lime.700", "alias": "color.lime.700", "hex": _res(tokens, "{color.lime.700}")}
    else:
        acento = {"token": "illustration.accent", "alias": ill["accent"]["$value"].strip("{}"),
                  "hex": _res(tokens, ill["accent"]["$value"])}
    return {"camadas": camadas, "figura": figura, "acento": acento}


def tetos(tokens: dict) -> dict:
    ill = tokens["illustration"]
    return {
        "max_matizes": ill["maxHues"]["$value"],
        "max_cores": ill["maxColors"]["$value"],
        "fundo_minimo": ill["minBackground"]["$value"],
        "acento_max": ill["accentMaxCoverage"]["$value"],
        "granulacao_max": ill["grainMaxLuminanceAmplitude"]["$value"],
        "tamanho_minimo_px": ill["minSizePx"]["$value"],
    }


def _secoes(md: str) -> dict[str, str]:
    """`## Título` -> corpo. Chave: título sem acento/caixa."""
    partes = re.split(r"^## (.+)$", md, flags=re.M)
    return {_plano(partes[i]): partes[i + 1].strip("\n") for i in range(1, len(partes), 2)}


def _achar(secoes: dict[str, str], prefixo: str) -> str:
    for k, v in secoes.items():
        if k.startswith(prefixo):
            return v
    raise BrandError(f"_bloco-marca.md não tem a seção '{prefixo}' (o bloco mudou de estrutura?)")


def _secao_paleta(p: dict, modo: str) -> str:
    """Só hex, em prosa. Nada de tabela nem nome de token: no S2 o gerador desenhou uma legenda de
    amostras com os nomes dos tokens que estavam na tabela (texto espúrio na imagem)."""
    cor = NOMES_MODO[modo]
    niveis = ", ".join(
        f"nível {i} {c['hex']}" + (" (a mais escura)" if i == 1 else " (a mais clara)" if i == len(p["camadas"]) else "")
        for i, c in enumerate(p["camadas"], 1)
    )
    figura = " e ".join(f["hex"] for f in p["figura"])
    return "\n".join(
        [
            f"## Paleta — pilha {cor} (a única desta peça)",
            "",
            "Pinte só com estes hex, um por folha de papel (âncora absoluta: nunca compare uma folha com outra,",
            f"nunca aproxime uma cor). Nunca misture a pilha escura com a clara. Não desenhe amostras de cor,",
            "legendas, códigos hex nem nenhum texto na imagem: os hex abaixo são instrução, não conteúdo.",
            "",
            f"- Folhas da pilha {cor}: {niveis}.",
            f"- Figura, sobre a pilha (nunca empilha): {figura}.",
            f"- Acento único, só na virada/conquista/ação: {p['acento']['hex']}.",
        ]
    )


def _secao_tetos(t: dict) -> str:
    return "\n".join(
        [
            "## Tetos numéricos (diretrizes; o pedido do autor pode sobrepor)",
            "",
            f"- Matizes de pilha por peça: {t['max_matizes']}, mais um neutro estrutural.",
            f"- Cores ≥1% do quadro: no máximo {t['max_cores']}.",
            f"- Fundo mínimo do quadro: {t['fundo_minimo']:.0%}.",
            f"- Acento do quadro: até {t['acento_max']:.0%}.",
            f"- Granulação (só no fundo), amplitude de luminância: abaixo de {t['granulacao_max']}.",
        ]
    )


def montar_bloco(bloco_md: str, tokens: dict, modo: str, texto: bool = False) -> str:
    """Bloco injetável do modo. `texto=True` = o pedido exige texto na imagem (dropa 'sem texto')."""
    sec = _secoes(bloco_md)
    partes = [f"# Bloco de marca Syntaxis — modo {modo} (pilha {NOMES_MODO[modo]})", "", _secao_paleta(paleta(tokens, modo), modo), "", _secao_tetos(tetos(tokens))]
    for prefixo in INJETAR:
        if texto and prefixo == "sem texto renderizado":
            continue
        partes += ["", f"## {prefixo_titulo(bloco_md, prefixo)}", _achar(sec, prefixo)]
    for prefixo in GERADAS + (LINT,) + DESCARTADAS:  # falha alto se o .md perdeu alguma seção
        _achar(sec, prefixo)
    return "\n".join(partes).strip() + "\n"


def prefixo_titulo(bloco_md: str, prefixo: str) -> str:
    """Título original (com acento) da seção, para o bloco sair como está no .md."""
    for t in re.findall(r"^## (.+)$", bloco_md, flags=re.M):
        if _plano(t).startswith(prefixo):
            return t
    raise BrandError(f"_bloco-marca.md não tem a seção '{prefixo}'")


def descritores_proibidos(bloco_md: str) -> list[str]:
    return re.findall(r"`([^`]+)`", _achar(_secoes(bloco_md), LINT))


def lint_descritores(texto: str, proibidos: list[str]) -> list[str]:
    """Descritores proibidos presentes no texto (palavra inteira, sem caixa). Aviso, não erro (A2)."""
    return [d for d in proibidos if re.search(rf"(?<![\w-]){re.escape(d)}(?![\w-])", texto, re.I)]


def _drift(tokens: dict, arquivos: dict[str, str]) -> list[str]:
    """Hex do .md que os tokens não conhecem (e vice-versa)."""
    esperados = set()
    for modo in MODOS:
        p = paleta(tokens, modo)
        esperados |= {c["hex"] for c in p["camadas"] + p["figura"]} | {p["acento"]["hex"]}
    esperados.add(_res(tokens, "{color.lime.500}"))
    avisos = []
    for nome, md in arquivos.items():
        achados = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", md)}
        for h in sorted(achados - esperados):
            avisos.append(f"deriva: {nome} cita {h}, que os tokens não têm (tokens vencem).")
        for h in sorted(esperados - achados):
            avisos.append(f"deriva: {nome} não cita {h}, que os tokens têm.")
    return avisos


def git_status(brand: Path, fetch: bool = True) -> dict:
    """Estado do git de brand/. Nunca faz pull/merge/checkout."""

    def git(*a: str, timeout: int = 30) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(brand), *a], capture_output=True, text=True, timeout=timeout)

    out: dict = {"repositorio": None, "remotos": [], "alteracoes_locais": [], "atras": None, "avisos": []}
    top = git("rev-parse", "--show-toplevel")
    if top.returncode:
        out["avisos"].append("brand/ não está num repositório git: versão só pelos tokens.")
        return out
    out["repositorio"] = top.stdout.strip()
    out["remotos"] = git("remote").stdout.split()
    out["alteracoes_locais"] = [l for l in git("status", "--porcelain", "--", str(brand)).stdout.splitlines() if l]
    if out["alteracoes_locais"]:
        out["avisos"].append(f"brand/ tem {len(out['alteracoes_locais'])} alteração(ões) não commitada(s).")
    if not out["remotos"]:
        out["avisos"].append("repositório sem remoto: não há como saber se brand/ está atrás.")
    elif fetch:
        try:
            git("fetch", "--quiet", timeout=60)
            n = git("rev-list", "--count", "HEAD..@{u}", "--", str(brand))
            out["atras"] = int(n.stdout.strip()) if n.returncode == 0 else None
        except (subprocess.TimeoutExpired, ValueError):
            out["avisos"].append("git fetch não concluiu; não sei se brand/ está atrás.")
        if out["atras"] is None and not any("fetch" in a for a in out["avisos"]):
            out["avisos"].append("branch sem upstream: não sei se brand/ está atrás.")
    return out


def resolver(brand: Path = BRAND, verificar_git: bool = True, texto: bool = False) -> dict:
    """Lê a marca agora e devolve o snapshot (dict serializável)."""
    brand = Path(brand)
    lidos: dict[str, bytes] = {}
    for rel in ARQUIVOS:
        p = brand / rel
        if not p.is_file():
            raise BrandError(f"arquivo de marca ausente: {p}")
        lidos[rel] = p.read_bytes()
    tokens = json.loads(lidos[ARQUIVOS[0]])
    bloco_md = lidos["ILUSTRACOES/_bloco-marca.md"].decode()
    try:
        versao_tokens = tokens["$extensions"]["br.com.syntaxis"]["version"]
    except KeyError as e:
        raise BrandError("tokens sem $extensions.br.com.syntaxis.version") from e
    m = re.search(r"\*\*v(\d+(?:\.\d+)*)\*\*", lidos["DESIGN.md"].decode())
    hashes = {k: _sha(v) for k, v in lidos.items()}
    return {
        "versao_tokens": versao_tokens,
        "versao_design": m.group(1) if m else None,
        "fingerprint": _sha(json.dumps(hashes, sort_keys=True).encode()),
        "arquivos": hashes,
        "vinculante": ["paleta"],
        "sobreponivel": ["sombra", "granulacao", "frame", "angulo de corte", "tetos numericos", "descritores proibidos"],
        "paletas": {m: paleta(tokens, m) for m in MODOS},
        "tetos": tetos(tokens),
        "descritores_proibidos": descritores_proibidos(bloco_md),
        "bloco": {m: montar_bloco(bloco_md, tokens, m, texto) for m in MODOS},
        "avisos": _drift(
            tokens,
            {k: lidos[k].decode() for k in ARQUIVOS[2:]},
        ),
        "git": git_status(brand, verificar_git) if verificar_git else None,
    }


def gravar(snapshot: dict, saida: Path) -> Path:
    destino = Path(saida) / "brand_snapshot.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    return destino
