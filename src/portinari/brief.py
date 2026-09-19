"""Pedido de ilustração (Markdown escrito à mão) → `Brief` validado.

O parser tolera o ruído típico de pedido manuscrito (`16:9]`, `2560 × 1440 `, campos vazios) e
registra cada correção em `avisos`. O que não dá para corrigir sem chutar vira `perguntas`
(ao autor), nunca correção silenciosa.
"""

from __future__ import annotations

import re
import unicodedata
import urllib.request
from datetime import date
from io import BytesIO
from math import gcd
from pathlib import Path

from PIL import Image
from pydantic import BaseModel, Field

RAIZ = Path(__file__).resolve().parents[4]  # monorepo Syntaxis
PIPELINE = Path(__file__).resolve().parents[2]  # pipelines/portinari

# chave canônica -> apelidos (já normalizados: sem acento, maiúsculas, espaço simples)
CHAVES = {
    "titulo": ("TITLE", "TITULO"),
    "uso": ("USO",),
    "aspect_ratio": ("ASPECT RATIO", "ASPECTRATIO", "PROPORCAO", "RAZAO DE ASPECTO"),
    "resolucao": ("RESOLUTION", "RESOLUCAO"),
    "tamanho": ("SIZE", "TAMANHO", "DIMENSOES"),
    "descricao": ("DESCRIPTION", "DESCRICAO"),
    "estilo": ("STYLE", "ESTILO"),
    "contexto": ("CONTEXT", "CONTEXTO"),
    "referencias": ("REFERENCE IMAGES", "IMAGENS DE REFERENCIA", "REFERENCIAS"),
}
APELIDO = {a: k for k, v in CHAVES.items() for a in v}
OBRIGATORIOS = ("titulo", "uso", "descricao")

# Só o que tem fonte (docs/PLANO.md §5). (regex sobre o USO normalizado, tamanho | None).
# tamanho None = USO reconhecido, mas sem tamanho definido em brand/ nem no pedido do autor.
PRESETS = [
    ("substack-email", r"substack.*(e-?mail|cabecalho)|(e-?mail|cabecalho).*substack", None),
    ("substack-capa", r"substack", (2560, 1440)),  # fonte: exemplo do autor; brand/ não define
    ("youtube-thumb", r"youtube.*(thumb|miniatura)|(thumb|miniatura).*youtube", None),
    ("linkedin-destaque", r"linkedin", (1200, 627)),  # brand/SOCIAL/README.md
    ("instagram-story", r"instagram.*(story|stories|reels|destaque)", (1080, 1920)),
    ("instagram-post", r"instagram", (1080, 1080)),  # brand/INSTAGRAM.md §2
]
ESTILOS = {"papercut": r"paper\s*-?\s*cut|collage|colagem|recorte"}
ESTILO_PADRAO = "papercut"  # brand/ILUSTRACOES/: hoje só existe collage / paper cut
LIMITE_REF = 25 * 1024 * 1024


class Referencia(BaseModel):
    origem: str
    caminho: str
    largura: int
    altura: int
    formato: str


class Brief(BaseModel):
    titulo: str = ""
    slug: str = ""
    pedido: str = ""
    saida: str = ""
    uso: str = ""
    preset: str | None = None
    descricao: str = ""
    estilo: str = ESTILO_PADRAO
    estilo_padrao: bool = True
    aspect_ratio: str | None = None
    resolucao: str | None = None
    tamanho: tuple[int, int] | None = None
    contexto: str = ""
    contexto_arquivos: list[str] = Field(default_factory=list)
    referencias: list[Referencia] = Field(default_factory=list)
    avisos: list[str] = Field(default_factory=list)
    perguntas: list[str] = Field(default_factory=list)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[\s_-]+", " ", s).strip().upper()


def _slug(s: str) -> str:
    s = _norm(s).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60].strip("-") or "sem-titulo"


# **CHAVE**: v | **CHAVE:** v | CHAVE: v | # CHAVE: v  (início de linha, até 3 espaços)
_LINHA_CHAVE = re.compile(
    r"^[ \t]{0,3}(?:#{1,6}[ \t]+)?(?:\*\*|__)?([^:*\n]{1,40}?)[ \t]*(?:\*\*|__)?[ \t]*:"
    r"[ \t]*(?:\*\*|__)?[ \t]*(.*)$"
)


def _campos(texto: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Separa o texto em campos. Retorna (campos, avisos, perguntas)."""
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    campos: dict[str, list[str]] = {}
    avisos, perguntas = [], []
    atual: str | None = None
    cerca = False
    preambulo = False
    for i, linha in enumerate(texto.splitlines(), 1):
        if linha.lstrip().startswith(("```", "~~~")):
            cerca = not cerca
        m = None if cerca else _LINHA_CHAVE.match(linha)
        chave = APELIDO.get(_norm(m.group(1))) if m else None
        if chave:
            if chave in campos:
                perguntas.append(
                    f"A chave {chave.upper()} aparece mais de uma vez (linha {i}). "
                    "Se for texto do CONTEXT, renomeie o começo dessa linha."
                )
            campos[chave] = [m.group(2)]
            atual = chave
        elif atual:
            campos[atual].append(linha)
        elif linha.strip():
            preambulo = True
    if preambulo:
        avisos.append("Texto antes da primeira chave foi ignorado.")
    return {k: "\n".join(v).strip() for k, v in campos.items()}, avisos, perguntas


def _vazio(v: str) -> bool:
    """Vazio ou placeholder `<...>` do _TEMPLATE.md."""
    return not v or bool(re.fullmatch(r"<[^>]*>", v.strip()))


def _razao_str(w: int, h: int) -> str:
    g = gcd(w, h)
    return f"{w // g}:{h // g}"


def _faixa(w: int, h: int) -> str:
    n = max(w, h)
    return "1k" if n <= 1536 else "2k" if n <= 3071 else "4k"


def _resolver_arquivos(contexto: str, raiz: Path, perguntas: list[str]) -> tuple[str, list[str]]:
    """Linhas `@caminho` (relativas à raiz do monorepo) são substituídas pelo conteúdo."""
    saida, lidos = [], []
    for linha in contexto.splitlines():
        m = re.fullmatch(r"\s*@(\S+)\s*", linha)
        if not m:
            saida.append(linha)
            continue
        p = Path(m.group(1))
        p = p if p.is_absolute() else raiz / p
        if p.is_file():
            saida.append(p.read_text(encoding="utf-8"))
            lidos.append(str(p))
        else:
            perguntas.append(f"CONTEXT aponta para {m.group(1)}, que não existe (raiz: {raiz}).")
    return "\n".join(saida).strip(), lidos


def _referencia(origem: str, i: int, pasta: Path, bases: list[Path]) -> Referencia:
    """Baixa (URL) ou localiza (arquivo) e valida que é imagem. Levanta ValueError."""
    if re.match(r"https?://", origem, re.I):
        try:
            with urllib.request.urlopen(origem, timeout=30) as r:
                dados = r.read(LIMITE_REF + 1)
        except OSError as e:
            raise ValueError(f"não consegui baixar {origem}: {e}") from e
        if len(dados) > LIMITE_REF:
            raise ValueError(f"{origem} passa de 25 MB")
        destino = None
    else:
        p = Path(origem).expanduser()
        achado = [p] if p.is_absolute() else [b / p for b in bases]
        arq = next((a for a in achado if a.is_file()), None)
        if arq is None:
            raise ValueError(f"arquivo de referência não encontrado: {origem}")
        dados, destino = arq.read_bytes(), arq
    try:
        with Image.open(BytesIO(dados)) as im:
            im.verify()
        with Image.open(BytesIO(dados)) as im:
            largura, altura, fmt = im.width, im.height, im.format or "?"
    except Exception as e:
        raise ValueError(f"{origem} não é uma imagem válida") from e
    if destino is None:
        pasta.mkdir(parents=True, exist_ok=True)
        destino = pasta / f"ref_{i:02d}.{'jpg' if fmt == 'JPEG' else fmt.lower()}"
        destino.write_bytes(dados)
    return Referencia(
        origem=origem, caminho=str(destino), largura=largura, altura=altura, formato=fmt
    )


def carregar(
    pedido: Path,
    saida: Path | None = None,
    raiz: Path = RAIZ,
    hoje: date | None = None,
) -> Brief:
    """Lê o pedido, normaliza, valida e devolve o Brief (avisos e perguntas dentro dele)."""
    pedido = Path(pedido)
    campos, avisos, perguntas = _campos(pedido.read_text(encoding="utf-8"))
    b = Brief(pedido=str(pedido), avisos=avisos, perguntas=perguntas)
    for k in list(campos):
        if _vazio(campos[k]):
            del campos[k]

    for k in OBRIGATORIOS:
        if k not in campos:
            b.perguntas.append(f"Campo obrigatório ausente ou vazio: {k.upper()}.")
    b.titulo = campos.get("titulo", "")
    b.uso = campos.get("uso", "")
    b.descricao = campos.get("descricao", "")
    b.slug = _slug(b.titulo or pedido.stem)
    saida = saida or PIPELINE / "output" / f"{(hoje or date.today()).isoformat()}_{b.slug}"
    b.saida = str(saida)

    # --- estilo
    if "estilo" in campos:
        alvo = next((n for n, rx in ESTILOS.items() if re.search(rx, campos["estilo"], re.I)), None)
        if alvo:
            b.estilo, b.estilo_padrao = alvo, False
        else:
            b.perguntas.append(
                f"STYLE '{campos['estilo']}' não tem linguagem definida em brand/ILUSTRACOES/ "
                f"(hoje só existe collage / paper cut). Usar o padrão ou definir o estilo?"
            )

    # --- proporção, resolução, tamanho (o que o autor escreveu vence o preset do USO)
    ratio = tam = None
    if "aspect_ratio" in campos:
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*[:/xX×]\s*(\d+(?:[.,]\d+)?)", campos["aspect_ratio"])
        if m:
            ratio = f"{m.group(1)}:{m.group(2)}".replace(",", ".")
            if ratio != campos["aspect_ratio"].strip():
                b.avisos.append(f"ASPECT RATIO '{campos['aspect_ratio']}' lido como {ratio}.")
        else:
            b.perguntas.append(f"ASPECT RATIO '{campos['aspect_ratio']}' não é uma proporção (ex.: 16:9).")
    if "tamanho" in campos:
        m = re.search(r"(\d+)\s*[xX×*]\s*(\d+)", campos["tamanho"])
        if m:
            tam = (int(m.group(1)), int(m.group(2)))
            if campos["tamanho"] != f"{tam[0]}x{tam[1]}":
                b.avisos.append(f"SIZE '{campos['tamanho']}' normalizado para {tam[0]}x{tam[1]}.")
        else:
            b.perguntas.append(f"SIZE '{campos['tamanho']}' não é LARGURAxALTURA (ex.: 2560x1440).")
    res = None
    if "resolucao" in campos:
        m = re.fullmatch(r"\s*([124])\s*k\s*", campos["resolucao"], re.I)
        if m:
            res = f"{m.group(1)}k"
        else:
            b.perguntas.append(f"RESOLUTION '{campos['resolucao']}' inválida (use 1k, 2k ou 4k).")

    # --- preset do USO preenche o que faltou
    uso_n = _norm(b.uso).lower()
    preset = next((p for p in PRESETS if re.search(p[1], uso_n)), None)
    if b.uso and preset is None and tam is None:
        b.perguntas.append(f"USO '{b.uso}' não tem preset conhecido: informe SIZE (e, se quiser, proporção).")
    elif preset:
        b.preset = preset[0]
        if preset[2] is None and tam is None:
            b.perguntas.append(
                f"USO '{b.uso}' é conhecido, mas nem brand/ nem o pedido definem o tamanho: informe SIZE."
            )
        elif tam is None and preset[2]:
            if ratio and abs(_num(ratio) - preset[2][0] / preset[2][1]) > 0.01 * _num(ratio):
                b.perguntas.append(
                    f"ASPECT RATIO {ratio} difere do preset de '{b.uso}' ({_razao_str(*preset[2])}) "
                    "e não há SIZE: informe o tamanho exato."
                )
            else:
                tam = preset[2]
                b.avisos.append(f"SIZE ausente: usado o preset de '{b.uso}' ({tam[0]}x{tam[1]}).")
                if res and res != _faixa(*tam):
                    b.perguntas.append(f"RESOLUTION {res} diverge do preset de '{b.uso}' ({tam[0]}x{tam[1]}).")
    if tam and ratio is None:
        ratio = _razao_str(*tam)
    if tam and ratio and abs(tam[0] / tam[1] - _num(ratio)) > 0.01 * _num(ratio):
        b.perguntas.append(f"SIZE {tam[0]}x{tam[1]} não bate com ASPECT RATIO {ratio}. Qual vale?")
    if tam and res and res != _faixa(*tam):
        b.perguntas.append(f"SIZE {tam[0]}x{tam[1]} é {_faixa(*tam)}, mas RESOLUTION diz {res}. Qual vale?")
    b.aspect_ratio, b.tamanho = ratio, tam
    b.resolucao = res or (_faixa(*tam) if tam else None)

    # --- contexto e referências
    b.contexto, b.contexto_arquivos = _resolver_arquivos(campos.get("contexto", ""), raiz, b.perguntas)
    itens = [
        re.sub(r"^[-*]\s+", "", x).strip().strip("\"'")
        for x in re.split(r"[\n,]", campos.get("referencias", ""))
    ]
    pasta = saida / "referencias"
    for i, item in enumerate(filter(None, itens), 1):
        try:
            b.referencias.append(_referencia(item, i, pasta, [pedido.parent, raiz, PIPELINE]))
        except ValueError as e:
            b.perguntas.append(f"REFERENCE IMAGES: {e}.")
    return b


def _num(razao: str) -> float:
    w, h = razao.split(":")
    return float(w) / float(h)


def gravar(b: Brief) -> Path:
    destino = Path(b.saida) / "brief.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(b.model_dump_json(indent=2), encoding="utf-8")
    return destino
