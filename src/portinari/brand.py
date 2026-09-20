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
# Formatos e estilos (brand 97cfadd, 19/09/2026). Ficam fora de ARQUIVOS porque o lint de deriva
# (`_drift`) só faz sentido nos arquivos que citam hex; estes citam token, não cor.
FORMATOS = "ILUSTRACOES/FORMATOS.md"
ESTILOS_DIR = "ILUSTRACOES/estilos"
ESTILOS_README = f"{ESTILOS_DIR}/README.md"
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


# --- Formatos e estilos (ILUSTRACOES/FORMATOS.md e ILUSTRACOES/estilos/) ----------------------

_DIM = re.compile(r"(\d{3,5})\s*[×x]\s*(\d{3,5})")
_PROP = re.compile(r"(\d+(?:[.,]\d+)?)\s*:\s*(\d+(?:[.,]\d+)?)")


def _tabela(md: str, *cabecalhos: str) -> list[dict[str, str]]:
    """Primeira tabela markdown cujo cabeçalho começa por `cabecalhos`. Falha alto se sumir."""
    for bloco in re.findall(r"(?:^[ \t]*\|.*\n)+", md, flags=re.M):
        linhas = [l.strip().strip("|") for l in bloco.splitlines() if l.strip()]
        cab = [c.strip() for c in linhas[0].split("|")]
        if [_plano(c) for c in cab[: len(cabecalhos)]] == [_plano(c) for c in cabecalhos]:
            return [dict(zip(cab, [c.strip() for c in l.split("|")])) for l in linhas[2:]]
    raise BrandError(f"tabela com cabeçalho {cabecalhos!r} não existe mais (o arquivo da marca mudou de estrutura?)")


def _limpo(celula: str) -> str:
    return re.sub(r"\s+", " ", celula.replace("**", "").replace("`", "")).strip(" *")


def _sobra(celula: str, m: re.Match | None) -> str:
    """O que a célula diz além da medida — nota que o autor precisa ler ao gerar à mão."""
    if m is None:
        return _limpo(celula)
    return _limpo(celula[: m.start()] + " " + celula[m.end() :]).strip(" (),;")


def _tipos_arquivo(celula: str) -> list[str]:
    """Extensões aceitas, na ordem em que a marca as cita (a primeira é a preferida)."""
    vistos: list[str] = []
    for m in re.finditer(r"\b(JPE?G|PNG)\b", celula, re.I):
        ext = "jpeg" if m.group(1).lower().startswith("jp") else "png"
        if ext not in vistos:
            vistos.append(ext)
    return vistos


def _peso_mb(celula: str) -> float | None:
    m = re.search(r"[≤<]=?\s*(\d+(?:[.,]\d+)?)\s*MB", celula, re.I)
    return float(m.group(1).replace(",", ".")) if m else None


def formatos(md: str) -> dict[str, dict]:
    """Tabela por uso de FORMATOS.md → {chave: {...}}. Linhas sem chave são referência, não uso."""
    out: dict[str, dict] = {}
    for linha in _tabela(md, "Chave", "Uso", "Proporção", "Entrega", "Master"):
        chave = _limpo(linha["Chave"])
        if not chave or chave == "—":
            continue
        entrega, master = _DIM.search(linha["Entrega"]), _DIM.search(linha["Master"])
        prop = _PROP.search(linha["Proporção"])
        if not (entrega and prop):
            raise BrandError(f"FORMATOS.md: o uso '{chave}' não traz entrega e proporção legíveis")
        tipos = _tipos_arquivo(linha["Formato / peso"])
        if not tipos:
            raise BrandError(f"FORMATOS.md: o uso '{chave}' não diz o formato do arquivo")
        out[chave] = {
            "uso": _limpo(linha["Uso"]),
            "proporcao": f"{prop.group(1)}:{prop.group(2)}".replace(",", "."),
            "entrega": [int(entrega.group(1)), int(entrega.group(2))],
            "master": [int(master.group(1)), int(master.group(2))] if master else None,
            "formato": tipos,
            "peso_max_mb": _peso_mb(linha["Formato / peso"]),
            "observacoes": [o for o in (_sobra(linha["Entrega"], entrega), _sobra(linha["Master"], master)) if o],
            "fonte": _limpo(linha.get("Fonte", "")),
        }
    if not out:
        raise BrandError("FORMATOS.md: nenhuma linha com chave de uso")
    return out


def areas_seguras(md: str) -> dict:
    """Recortes centrais de FORMATOS.md, guardados como fração do master de referência — assim
    valem para qualquer master, inclusive o ~1K que o gerador de validação entrega."""
    zonas: dict[str, dict] = {}
    ref: list[int] | None = None
    for linha in _tabela(md, "Destino", "Recorte central", "Deslocamento"):
        m = _DIM.search(linha["Recorte central"])
        if not m:
            continue
        w, h = int(m.group(1)), int(m.group(2))
        ref = ref or [w, h]  # a primeira linha da tabela é o master inteiro (16:9)
        destino = _limpo(linha["Destino"])
        nome = "universal" if "universal" in _plano(destino) else _plano(destino).split(" (")[0]
        zonas[nome] = {
            "destino": destino,
            "recorte": [w, h],
            "fracao": [round(w / ref[0], 6), round(h / ref[1], 6)],
            "deslocamento": _limpo(linha["Deslocamento"]),
        }
    if "universal" not in zonas:
        raise BrandError("FORMATOS.md: a tabela de áreas seguras perdeu a linha 'Universal'")
    return {"master_referencia": ref, "zonas": zonas}


def estilos(pasta: Path) -> dict[str, dict]:
    """Um arquivo por estilo usável de ILUSTRACOES/estilos/ → base/modo, restrição e fragmento."""
    out: dict[str, dict] = {}
    for arq in sorted(Path(pasta).glob("*.md")):
        if arq.name == "README.md":
            continue
        md = arq.read_text(encoding="utf-8")
        titulo = re.search(r"^#\s+(.+?)\s+—\s+(.+)$", md, flags=re.M)
        if not titulo:
            raise BrandError(f"estilos/{arq.name}: título fora do padrão '# Nome — base|modo'")
        frag = re.search(r"```text\n(.*?)```", md, flags=re.S)
        if not frag:
            raise BrandError(f"estilos/{arq.name}: sem fragmento de prompt (bloco ```text)")
        out[arq.stem] = {
            "nome": titulo.group(1),
            "papel": "base" if _plano(titulo.group(2)).startswith("base") else "modo",
            "restrito": "status: nao usar" in _plano(md),
            "fragmento": frag.group(1).strip(),
        }
    if not out:
        raise BrandError("ILUSTRACOES/estilos/ não tem nenhum arquivo de estilo")
    return out


def estilos_recusados(readme_md: str) -> dict[str, dict]:
    """Os estilos que a marca recusa, com o motivo — vira pergunta ao autor, nunca escolha nossa."""
    out = {}
    for linha in _tabela(readme_md, "Estilo (Kasra)", "Veredito"):
        if "fora" not in _plano(_limpo(linha["Veredito"])):
            continue
        nome = _limpo(linha["Estilo (Kasra)"])
        chave = re.sub(r"[^a-z0-9]+", "-", _plano(nome)).strip("-")
        out[chave] = {"nome": nome, "motivo": _limpo(linha["Arquivo / motivo"])}
    return out


def marca_leve(brand: Path = BRAND) -> dict:
    """Só o que o parser do pedido precisa (formatos e estilos): sem tokens, sem git, sem bloco."""
    brand = Path(brand)
    fmt = (brand / FORMATOS).read_text(encoding="utf-8")
    return {
        "formatos": formatos(fmt),
        "areas_seguras": areas_seguras(fmt),
        "estilos": estilos(brand / ESTILOS_DIR),
        "estilos_recusados": estilos_recusados((brand / ESTILOS_README).read_text(encoding="utf-8")),
    }


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
    estilos_rel = sorted(f"{ESTILOS_DIR}/{a.name}" for a in (brand / ESTILOS_DIR).glob("*.md"))
    lidos: dict[str, bytes] = {}
    for rel in (*ARQUIVOS, FORMATOS, *estilos_rel):
        p = brand / rel
        if not p.is_file():
            raise BrandError(f"arquivo de marca ausente: {p}")
        lidos[rel] = p.read_bytes()
    if ESTILOS_README not in lidos:
        raise BrandError(f"arquivo de marca ausente: {brand / ESTILOS_README}")
    tokens = json.loads(lidos[ARQUIVOS[0]])
    fmt_md = lidos[FORMATOS].decode()
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
        "formatos": formatos(fmt_md),
        "areas_seguras": areas_seguras(fmt_md),
        "estilos": estilos(brand / ESTILOS_DIR),
        "estilos_recusados": estilos_recusados(lidos[ESTILOS_README].decode()),
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
