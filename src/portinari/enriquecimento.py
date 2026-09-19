"""Etapa de enriquecimento do prompt (E4): schema, validação por código, renderização, cobertura.

O agente `enriquecedor-de-cena` escreve `enriquecimento/vNN.json`; este módulo garante o que dá para
garantir por código (um foco, paleta, sem texto, densidade) e deixa para o crítico só o que exige
olho. Spec: specs/epicos/epico-04-enriquecimento.md.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from . import brand

Zona = Literal["esquerda", "centro", "direita", "fundo", "primeiro-plano"]
Papel = Literal["foco", "apoio", "textura"]
Origem = Literal["pedido", "contexto", "dominio", "oficio"]

# Palavras de cor fora da paleta (a paleta é a única regra vinculante da marca — A2).
# Comparadas sem acento e em minúsculas.
_COR_FORA = (
    r"vermelh\w*|rubr\w*|azul|azuis|amarel\w*|laranj\w*|rox\w*|violet\w*|lilas|rosa|rosas|marrom|marrons|"
    r"castanh\w*|dourad\w*|ouro|prata|pratead\w*|bege|turquesa|magenta|ciano|"
    r"red|reds|blue|yellow|orange|purple|violet|pink|brown|golden|gold|silver|beige|cyan|crimson|scarlet|maroon"
)
# Referências a texto dentro da imagem (a marca e o pedido: nada de texto, salvo se o pedido exigir).
_TEXTO = (
    r"texto|textos|text|texts|letra|letras|palavra|palavras|numero|numeros|digito|digitos|escrita|escrito|"
    r"legenda|legendas|rotulo|rotulos|logo|logos|logotipo|codigo de barras|barcode|qr|inscricao|inscricoes|"
    r"tipografia|letter|letters|word|words|number|numbers|digit|digits|label|labels|caption|captions|"
    r"writing|written|inscription|inscriptions|typography"
)
_NEGACAO = re.compile(r"\b(sem|nenhum|nenhuma|nada de|nao|no|without|not|nor|zero|nunca)\b")
_SIMBOLOS = re.compile(r"R\$|\$")


class Elemento(BaseModel):
    id: str = Field(min_length=1)
    zona: Zona
    papel: Papel
    elemento: str = Field(min_length=1)
    termo_en: str = Field(min_length=1)
    cor: str = Field(min_length=1)
    origem: Origem
    justificativa: str = ""
    verificar: bool = False
    nota_verificacao: str = ""


class Descartado(BaseModel):
    elemento: str
    motivo: str


class Enriquecimento(BaseModel):
    conceito: str
    pedido_preservado: list[str]
    elementos: list[Elemento]
    descartados: list[Descartado] = Field(default_factory=list)
    cena: str


class Relatorio(BaseModel):
    erros: list[str] = Field(default_factory=list)
    avisos: list[str] = Field(default_factory=list)
    verificar: list[str] = Field(default_factory=list)


def _plano(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))


def papeis_de_cor(snapshot: dict, modo: str) -> dict[str, str]:
    """papel de cor -> hex, tudo vindo do snapshot (nada hardcoded)."""
    p = snapshot["paletas"][modo]
    papeis = {f"pilha-{i}": c["hex"] for i, c in enumerate(p["camadas"], 1)}
    papeis["figura-principal"] = p["figura"][0]["hex"]
    papeis["figura-secundaria"] = p["figura"][1]["hex"]
    papeis["acento"] = p["acento"]["hex"]
    papeis["neutro"] = p["camadas"][0]["hex"]  # neutro estrutural = base da pilha
    return papeis


def _achados(texto: str, padrao: str) -> list[str]:
    """Palavras do padrão presentes em `texto`, ignorando as precedidas de negação."""
    t = _plano(texto)
    out = []
    for m in re.finditer(rf"\b({padrao})\b", t):
        if not _NEGACAO.search(t[max(0, m.start() - 25) : m.start()]):
            out.append(m.group(1))
    return out


def validar(
    e: Enriquecimento,
    snapshot: dict,
    modo: str = "dark",
    *,
    max_elementos: int = 12,
    min_acrescimos: int = 3,
    texto: bool = False,
) -> Relatorio:
    r = Relatorio()
    papeis = papeis_de_cor(snapshot, modo)
    ids = [x.id for x in e.elementos]
    if len(set(ids)) != len(ids):
        r.erros.append(f"V1: ids repetidos: {sorted({i for i in ids if ids.count(i) > 1})}.")
    focos = [x.id for x in e.elementos if x.papel == "foco"]
    if len(focos) != 1:
        r.erros.append(f"V2: precisa de exatamente 1 elemento foco; há {len(focos)}" + (f" ({', '.join(focos)})." if focos else "."))
    if len(e.elementos) > max_elementos:
        r.erros.append(f"V3: {len(e.elementos)} elementos; o máximo é {max_elementos}. Corte ou mova para 'descartados'.")
    acrescimos = [x for x in e.elementos if x.origem != "pedido"]
    if len(acrescimos) < min_acrescimos:
        r.erros.append(f"V4: só {len(acrescimos)} acréscimo(s) além do pedido; o mínimo é {min_acrescimos}. Enriqueça de verdade.")
    if not e.pedido_preservado or not any(x.origem == "pedido" for x in e.elementos):
        r.erros.append("V5: liste o que o pedido já dizia em 'pedido_preservado' e mantenha ≥ 1 elemento de origem 'pedido'.")
    for x in e.elementos:
        if x.cor not in papeis:
            r.erros.append(f"V6: {x.id}: cor '{x.cor}' não é papel de cor do modo {modo} (válidos: {', '.join(papeis)}).")
        campos = f"{x.elemento} . {x.termo_en}"
        fora = _achados(campos, _COR_FORA)
        if fora:
            r.erros.append(f"V7: {x.id}: cor fora da paleta ({', '.join(fora)}). Descreva pelo papel de cor, não por cor real.")
        if not texto:
            t = _achados(campos, _TEXTO) + _SIMBOLOS.findall(campos)
            if t:
                r.erros.append(f"V8: {x.id}: referência a texto na imagem ({', '.join(t)}). Nada legível: use forma, trama, selo.")
        if x.verificar:
            r.verificar.append(f"{x.id} — {x.elemento}: {x.nota_verificacao or 'confirmar com o autor'}")
    fora = _achados(e.cena, _COR_FORA)
    if fora:
        r.erros.append(f"V7: cena: cor fora da paleta ({', '.join(fora)}).")
    if not texto:
        t = _achados(e.cena, _TEXTO) + _SIMBOLOS.findall(e.cena)
        if t:
            r.erros.append(f"V8: cena: referência a texto na imagem ({', '.join(t)}).")
    if sum(x.cor == "acento" for x in e.elementos) > 2:
        r.avisos.append("mais de 2 elementos com 'acento': a marca pede um ponto de acento por composição.")
    if modo == "dark" and any(x.cor == "pilha-4" for x in e.elementos):
        r.avisos.append("'pilha-4' não existe no modo light: a derivação terá de mapear esses elementos.")
    for d in brand.lint_descritores(e.cena, snapshot.get("descritores_proibidos", [])):
        r.avisos.append(f"descritor da marca na cena: '{d}' (o pedido pode sobrepor).")
    return r


def _versoes(saida: Path) -> list[Path]:
    return sorted((Path(saida) / "enriquecimento").glob("v[0-9][0-9].json"))


def carregar(saida: Path, versao: int | None = None) -> tuple[Enriquecimento, Path]:
    """Versão pedida ou a mais recente. FileNotFoundError se não houver; ValueError se inválida."""
    vs = _versoes(saida)
    if versao is not None:
        vs = [v for v in vs if v.stem == f"v{versao:02d}"]
    if not vs:
        raise FileNotFoundError(f"sem enriquecimento em {Path(saida) / 'enriquecimento'}")
    p = vs[-1]
    try:
        return Enriquecimento.model_validate_json(p.read_text(encoding="utf-8")), p
    except (ValidationError, json.JSONDecodeError) as x:
        raise ValueError(f"{p.name} inválido: {str(x).splitlines()[0]} ({len(str(x).splitlines())} linhas de detalhe)") from x


def termos_ausentes(e: Enriquecimento, prompt: str) -> list[str]:
    """termo_en que não aparece no prompt criativo (sem caixa, espaços normalizados)."""
    p = re.sub(r"\s+", " ", prompt.lower())
    return [x.termo_en for x in e.elementos if re.sub(r"\s+", " ", x.termo_en.lower().strip()) not in p]


def renderizar(e: Enriquecimento, snapshot: dict, modo: str, r: Relatorio) -> str:
    papeis = papeis_de_cor(snapshot, modo)
    L = [f"# Enriquecimento — conceito {e.conceito}", "", "## Pedido preservado", ""]
    L += [f"- {x}" for x in e.pedido_preservado]
    L += ["", "## Elementos", "", "| id | zona | papel | elemento | cor | origem | |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for x in e.elementos:
        hexa = papeis.get(x.cor)
        cor = f"{x.cor} ({hexa})" if hexa else f"{x.cor} (?)"
        L.append(f"| {x.id} | {x.zona} | {x.papel} | {x.elemento} | {cor} | {x.origem} | {'⚠ verificar' if x.verificar else ''} |")
    L += ["", "## Cena", "", e.cena.strip()]
    if e.descartados:
        L += ["", "## Descartados", ""] + [f"- **{d.elemento}** — {d.motivo}" for d in e.descartados]
    if r.verificar:
        L += ["", "## Para verificar com o autor", ""] + [f"- {v}" for v in r.verificar]
    return "\n".join(L) + "\n"
