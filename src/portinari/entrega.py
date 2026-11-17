"""Entrega do Portinari: o produto é o PROMPT, não a imagem (decisão A16, 20/09/2026).

A imagem que o `agy` gerou existe para provar que o prompt funciona — é evidência, não produto.
Quem gera a peça final é o autor, colando `final/prompt_<modo>.md` no Nano Banana Pro. Por isso a
única coisa que este módulo protege é a autossuficiência do texto entregue: quem abrir o arquivo
num computador sem o monorepo tem de conseguir usá-lo.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import shutil
from datetime import date
from pathlib import Path

from . import agy, enriquecimento, imaging

NOMES_MODO = {"dark": "escura", "light": "clara"}
# Nano Banana Pro (`gemini-3-pro-image`): proporções e tamanho 1K; 2K e 4K são ×2 e ×4.
# Fonte: https://ai.google.dev/gemini-api/docs/image-generation, lida em 16/11/2026. Isto é
# capacidade do gerador, não regra de marca — confira na doc antes de mexer.
PRO_1K = {"1:1": (1024, 1024), "2:3": (848, 1264), "3:2": (1264, 848), "3:4": (896, 1200), "4:3": (1200, 896),
          "4:5": (928, 1152), "5:4": (1152, 928), "9:16": (768, 1376), "16:9": (1376, 768), "21:9": (1584, 672)}


def gerador_final(brief: dict) -> dict:
    """Como pedir a peça final ao Nano Banana Pro: a proporção dele mais próxima da entrega e a menor
    resolução cujo corte central ainda cobre o master (nunca ampliar)."""
    alvo = tuple(brief["tamanho"])
    master = tuple(brief.get("master") or alvo)
    ln = lambda w, h: math.log(w / h)  # noqa: E731
    prop = min(PRO_1K, key=lambda p: abs(ln(*PRO_1K[p]) - ln(*alvo)))
    for k in (1, 2, 4):
        tam = (PRO_1K[prop][0] * k, PRO_1K[prop][1] * k)
        x0, y0, x1, y1 = imaging.recorte_central(tam, alvo)
        if x1 - x0 >= master[0] and y1 - y0 >= master[1]:
            break
    w, h = PRO_1K[prop]
    corta = abs(w / h / (alvo[0] / alvo[1]) - 1) > imaging.PROPORCAO_TOL
    return {"proporcao": prop, "resolucao": f"{k}K", "tamanho": list(tam), "corta": corta}


class EntregaErro(Exception):
    pass


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _hex(s: str) -> set[str]:
    return {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", s)}


def _hex_da_paleta(snap: dict, modo: str) -> set[str]:
    p = snap["paletas"][modo]
    return {c["hex"] for c in p["camadas"] + p["figura"]} | {p["acento"]["hex"]}


def iteracoes(saida: Path) -> list[int]:
    return sorted(int(d.name) for d in (Path(saida) / "iteracoes").glob("[0-9]*") if d.is_dir())


def geracao(saida: Path, iteracao: int, nome: str | None = None) -> dict:
    """gen_KK.json da geração aprovada (padrão: a última da iteração, que é a mais recente)."""
    pasta = Path(saida) / "iteracoes" / f"{iteracao:02d}"
    arqs = sorted(pasta.glob("gen_*.json"))
    if not arqs:
        raise EntregaErro(f"a iteração {iteracao:02d} não tem nenhuma geração")
    if nome:
        alvo = pasta / f"{nome}.json"
        if not alvo.is_file():
            raise EntregaErro(f"{nome} não existe em {pasta} (há: {', '.join(a.stem for a in arqs)})")
        arqs = [alvo]
    return json.loads(arqs[-1].read_text(encoding="utf-8"))


def verificar(prompt: str, snap: dict, modo: str, brief: dict, saida: Path) -> list[str]:
    """As recusas T1–T4 e T6 do épico 12. Só o que o código sabe conferir sem opinar."""
    erros: list[str] = []
    no_prompt = _hex(prompt)

    faltam = sorted(_hex_da_paleta(snap, modo) - no_prompt)
    if faltam:  # T2 — a paleta é vinculante (épico 14)
        erros.append(f"o prompt não cita {len(faltam)} hex da paleta {modo}: {', '.join(faltam)}")

    outro = "light" if modo == "dark" else "dark"
    invasores = sorted((_hex_da_paleta(snap, outro) - _hex_da_paleta(snap, modo)) & no_prompt)
    if invasores:  # T1 — um modo por arquivo; pilha misturada é reprovação da marca
        erros.append(f"o prompt mistura a pilha {outro} na peça {modo}: {', '.join(invasores)}")

    if _norm(snap["bloco"][modo]) not in _norm(prompt):  # T4
        erros.append(f"o bloco de marca do modo {modo} não está íntegro no prompt")

    try:  # T3 — o mesmo teste que `portinari prompt` faz, agora sobre o que vai ser entregue
        enr, versao = enriquecimento.carregar(Path(saida))
    except (FileNotFoundError, ValueError) as e:  # T7 — sem enriquecimento não há alt-text
        erros.append(f"sem enriquecimento válido não há alt-text para entregar ({e})")
    else:
        if not enr.alt.strip():  # T7 — a informação verbal vai no alt (DESIGN.md §4.4; SOCIAL.md §7)
            erros.append(f"{versao.name} não tem `alt`: peça uma versão nova ao enriquecedor com o alt-text")
        ausentes = enriquecimento.termos_ausentes(enr, prompt)
        if ausentes:
            erros.append(
                f"o prompt perdeu {len(ausentes)} termo(s) do enriquecimento ({versao.name}): "
                + ", ".join(ausentes)
            )

    if not (brief.get("tamanho") and brief.get("aspect_ratio") and brief.get("formato")):  # T6
        erros.append(
            f"o USO '{brief.get('uso', '')}' não resolveu em brand/ILUSTRACOES/FORMATOS.md "
            "(sem tamanho, proporção ou formato): sem isso não dá para dizer ao autor como gerar"
        )
    return erros


def cabecalho(brief: dict, modo: str, hoje: date | None = None) -> str:
    return "\n".join(
        [
            f"# {brief.get('titulo') or brief.get('slug', '')} — prompt {modo} (pilha {NOMES_MODO[modo]})",
            "",
            f"Uso: {brief.get('uso', '')} · gerado pelo Portinari em {(hoje or date.today()).isoformat()}.",
            "Cole daqui para baixo, inteiro, no gerador. Não resuma, não traduza, não reordene.",
            "Como gerar (modelo, tamanho, formato, o que conferir): `COMO-GERAR.md`, ao lado.",
            "",
            "---",
            "",
        ]
    )


def como_gerar(brief: dict, snap: dict, entregas: dict) -> str:
    """Tudo o que o autor precisa saber ao colar o prompt — vindo de FORMATOS.md, nunca do código."""
    fmt = (snap.get("formatos") or {}).get(brief.get("preset") or "", {})
    tam = brief.get("tamanho")
    area = brief.get("area_segura")
    universal = ((snap.get("areas_seguras") or {}).get("zonas", {}).get("universal") or {})
    linhas = [
        f"# Como gerar — {brief.get('titulo') or brief.get('slug', '')}",
        "",
        "O Portinari entrega o **prompt**; a peça final é gerada por você. A imagem em "
        "`validacao/` é a prova de que o prompt funciona (gerada pelo modelo flash, ~1K): "
        "ela **não** é a entrega.",
        "",
        "## Onde colar",
        "",
        "- **Modelo:** Nano Banana Pro (`gemini-3-pro-image`) — é o único que gera 2K/4K nativos.",
        f"- **Prompt:** {', '.join(f'`{a}`' for a in sorted(entregas))} (um arquivo por modo; use um de cada vez).",
    ]
    for modo, e in sorted(entregas.items()):
        if e.get("derivado_por_edicao"):
            outro = "light" if modo == "dark" else "dark"
            linhas.append(
                f"- **{modo}:** gere o {outro} primeiro. Depois anexe a peça {outro} final como imagem de "
                f"referência e cole `prompt_{modo}.md`: ele foi validado como edição dela, e é assim que o par "
                "sai com a mesma composição."
            )
    linhas += [
        "",
        "## Tamanho e formato",
        "",
    ]
    if tam:
        gf = gerador_final(brief)
        linhas.append(
            f"- **No gerador: proporção {gf['proporcao']}, resolução {gf['resolucao']}** "
            f"(sai {gf['tamanho'][0]}×{gf['tamanho'][1]}). O Pro recebe proporção e 1K/2K/4K, não pixels."
        )
        if gf["corta"]:
            linhas.append(f"- A proporção do uso ({brief.get('aspect_ratio')}) não existe no Pro: gere em "
                          f"{gf['proporcao']} e o corte central faz o resto.")
        linhas.append(
            f"- **Entregue em {tam[0]}×{tam[1]}** ({brief.get('aspect_ratio')}), por corte central "
            "e redução do que foi gerado (`portinari derivar`) — nunca gerando de novo num tamanho diferente."
        )
    if brief.get("formato"):
        peso = f", até {brief['peso_max_mb']:g} MB" if brief.get("peso_max_mb") else ""
        linhas.append(
            f"- **Formato:** {' ou '.join(f.upper() for f in brief['formato'])}{peso}. "
            "JPEG a 90–92 com croma 4:4:4 (com 4:2:0 a borda reta e o acento ganham franja). sRGB."
        )
    for obs in brief.get("observacoes_formato") or []:
        linhas.append(f"- **Atenção ({fmt.get('uso', brief.get('uso', ''))}):** {obs}.")
    if area and universal:
        linhas += [
            "",
            "## Área segura",
            "",
            f"- O ponto focal e tudo que precisa sobreviver ficam dentro de "
            f"**{area[0]:.2%} × {area[1]:.2%}**".replace(".", ",") + " do quadro, centralizados "
            f"({universal.get('destino', 'universal')}).",
            "- O fundo é o que sangra para as bordas.",
        ]
    linhas += [
        "",
        "## O que conferir na imagem que voltar",
        "",
        "- Nenhum texto, número, legenda, logo ou código desenhado na imagem.",
        "- Só os hex listados no prompt; nenhuma cor fora deles.",
        "- O acento aparece em **um** ponto só (a virada), não espalhado.",
        "- O fundo ocupa a maior parte do quadro.",
        "- Nenhuma sombra, brilho, gradiente, parede de recorte escurecida ou curva livre.",
        "",
        "## Depois de gerar — o pedido só fecha com isto",
        "",
        "1. `uv run portinari importar <execução> --iteracao N <peça> --modelo nano-banana-pro` "
        "(N = uma iteração nova, uma por modo).",
        "2. `uv run portinari checar <execução> --iteracao N --modo <modo>`; no segundo modo, "
        "`--par <peça do primeiro>`. Tem de sair sem `ERRO`.",
        "3. `uv run portinari derivar <execução> <peça> --modo <modo>` → o arquivo do tamanho exato.",
        "4. `uv run portinari entregar <execução> --modo <modo> --aprovado --concluir`.",
        "",
        "## Alt-text (o mesmo para as duas variantes)",
        "",
        f"> {next((e['alt'] for e in entregas.values() if e.get('alt')), '(falta)')}",
        "",
        "Cole no campo de texto alternativo da plataforma. A imagem não carrega texto: quem carrega a "
        "informação verbal é o alt.",
        "",
        "## Marca desta entrega",
        "",
        f"- tokens v{snap.get('versao_tokens')} · DESIGN v{snap.get('versao_design')} · "
        f"fingerprint `{str(snap.get('fingerprint', ''))[:12]}`.",
    ]
    return "\n".join(linhas) + "\n"


def entregar(
    saida: Path,
    modo: str,
    *,
    iteracao: int | None = None,
    gen: str | None = None,
    aprovado: bool = False,
    hoje: date | None = None,
) -> dict:
    """Grava final/prompt_<modo>.md, a imagem de validação, COMO-GERAR.md e manifest.json.

    Levanta EntregaErro sem gravar nada se alguma recusa do épico 12 falhar.
    """
    saida = Path(saida)
    if not aprovado:  # T5 — o Gate 2 é humano; ninguém entrega sozinho
        raise EntregaErro("o Gate 2 não foi declarado: só entrego com --aprovado")
    brief = json.loads((saida / "brief.json").read_text(encoding="utf-8"))
    snap = json.loads((saida / "brand_snapshot.json").read_text(encoding="utf-8"))
    its = iteracoes(saida)
    if not its:
        raise EntregaErro(f"{saida} não tem nenhuma iteração: não há prompt validado para entregar")
    it = iteracao if iteracao is not None else its[-1]
    g = geracao(saida, it, gen)
    if not g.get("imagem") or not Path(g["imagem"]).is_file():
        raise EntregaErro(f"{g['nome']} não tem imagem: esse prompt nunca foi validado")
    prompt = (saida / "iteracoes" / f"{it:02d}" / f"{g['nome']}.prompt.md").read_text(encoding="utf-8")

    erros = verificar(prompt, snap, modo, brief, saida)
    if erros:
        raise EntregaErro("o prompt não pode ser entregue:\n  - " + "\n  - ".join(erros))

    final = saida / "final"
    (final / "validacao").mkdir(parents=True, exist_ok=True)
    arq = final / f"prompt_{modo}.md"
    arq.write_text(cabecalho(brief, modo, hoje) + prompt.strip() + "\n", encoding="utf-8")
    val = final / "validacao" / f"{modo}_{g['nome']}{Path(g['imagem']).suffix}"
    shutil.copy2(g["imagem"], val)

    m = manifesto(saida)
    m["entregas"][modo] = {
        "prompt": str(arq.relative_to(saida)),
        "iteracao": it,
        "geracao": g["nome"],
        "origem": g.get("origem"),
        "modelo_validacao": g.get("modelo_imagem") or "não registrado",
        "validacao": str(val.relative_to(saida)),
        "validacao_px": [g.get("largura"), g.get("altura")],
        "sha256_prompt": hashlib.sha256(arq.read_bytes()).hexdigest(),
        "derivado_por_edicao": bool(g.get("referencias")),
        "alt": enriquecimento.carregar(saida)[0].alt.strip(),  # verificar() já garantiu que existe
        "gate2": "aprovado",
    }
    (final / "COMO-GERAR.md").write_text(como_gerar(brief, snap, m["entregas"]), encoding="utf-8")
    m["etapa_atual"] = "entregue"
    (saida / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return m["entregas"][modo]


def finais(saida: Path) -> dict[str, str]:
    """Modo -> peça final conferida: geração importada à mão cuja checagem saiu sem erro."""
    out: dict[str, str] = {}
    for chk in sorted(Path(saida).glob("iteracoes/*/gen_*.checagens.json")):
        meta = chk.with_name(chk.name.replace(".checagens.json", ".json"))
        if not meta.is_file() or json.loads(meta.read_text(encoding="utf-8")).get("origem") != "manual":
            continue
        r = json.loads(chk.read_text(encoding="utf-8"))
        if not r.get("erros"):
            out[r["modo"]] = f"iteracoes/{chk.parent.name}/{meta.stem}"
    return out


def concluir(saida: Path, processados: Path, *, sem_final: bool = False) -> Path:
    """Arquiva o pedido: copia para a execução e MOVE o original para pedidos/_processados/.

    Só depois de `final/` ter pelo menos um prompt — o pedido é a única cópia do que o autor
    escreveu, e um pedido arquivado sem entregável é trabalho perdido. E só com a peça final de cada
    modo entregue conferida por `checar` (auditoria M1: o gate de ilustração mede o que vai ao ar,
    não só a validação do flash); `sem_final` pula isso e deixa registrado.
    """
    saida = Path(saida)
    prompts = sorted((saida / "final").glob("prompt_*.md"))
    if not prompts:
        raise EntregaErro("final/ não tem nenhum prompt: não arquivo o pedido antes de entregar")
    m = manifesto(saida)
    conferidas = finais(saida)
    faltam = sorted(set(m["entregas"]) - set(conferidas))
    if faltam and not sem_final:
        raise EntregaErro(
            f"falta a peça final conferida do(s) modo(s) {', '.join(faltam)}: gere no Nano Banana Pro "
            "(final/COMO-GERAR.md), traga com `importar` e passe `checar` sem erro — ou use --sem-final, "
            "que fica registrado no manifest"
        )
    m["final_conferido"] = {modo: conferidas.get(modo) for modo in sorted(m["entregas"])}
    origem = Path(m.get("pedido") or "")
    if not origem.is_file():
        raise EntregaErro(f"o pedido original não está mais em {origem}")
    shutil.copy2(origem, saida / "pedido.md")  # a execução guarda o que o autor escreveu
    destino = Path(processados) / origem.name
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        raise EntregaErro(f"{destino} já existe: resolva à mão antes de arquivar de novo")
    shutil.move(str(origem), destino)
    m["etapa_atual"] = "concluido"
    m["pedido_arquivado"] = str(destino)
    (saida / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return destino


def estado(saida: Path) -> dict:
    """Onde a execução parou e qual é a próxima ação — é o que permite retomar numa sessão nova."""
    saida = Path(saida)
    m = json.loads((saida / "manifest.json").read_text(encoding="utf-8")) if (saida / "manifest.json").is_file() else {}
    feito = {
        "brief": (saida / "brief.json").is_file(),
        "marca": (saida / "brand_snapshot.json").is_file(),
        "conceitos": (saida / "conceitos.md").is_file(),
        "enriquecimento": sorted(p.name for p in (saida / "enriquecimento").glob("v*.json")),
        "iteracoes": iteracoes(saida) if (saida / "iteracoes").is_dir() else [],
        "geracoes": agy.contar(saida),
        "entregas": sorted(m.get("entregas", {})),
        "finais": sorted(finais(saida)) if (saida / "iteracoes").is_dir() else [],
    }
    # de trás para a frente: o que já foi feito mais adiante manda, mesmo que uma etapa
    # intermediária não tenha deixado arquivo (o autor pode ter pulado o gate de conceito).
    if m.get("etapa_atual") == "concluido":
        proxima = "nada: execução concluída"
    elif feito["entregas"] and set(feito["entregas"]) - set(feito["finais"]):
        proxima = ("gerar a peça final de cada modo no Nano Banana Pro (final/COMO-GERAR.md), `importar` e "
                   f"`checar` sem erro; depois `uv run portinari entregar {saida} ... --concluir`")
    elif feito["entregas"]:
        proxima = f"entregar o outro modo, ou `uv run portinari entregar {saida} ... --concluir`"
    elif any(Path(saida).glob("iteracoes/*/gen_*.json")):  # há imagem, do agy ou importada
        proxima = f"checar, crítica visual, Gate 2 e `uv run portinari entregar {saida} --modo dark --aprovado`"
    elif feito["iteracoes"]:
        proxima = f"uv run portinari gerar {saida} --iteracao {feito['iteracoes'][-1]}"
    elif feito["enriquecimento"]:
        proxima = "subagente prompter-tecnico (iteracoes/01/prompt_criativo.md)"
    elif feito["conceitos"]:
        proxima = "Gate 1 e depois o subagente enriquecedor-de-cena"
    elif feito["marca"]:
        proxima = "subagente diretor-de-arte (conceitos.md)"
    elif feito["brief"]:
        proxima = f"uv run portinari marca {saida}"
    else:
        proxima = "uv run portinari ingest <pedido.md>"
    return {"saida": str(saida), "etapa_atual": m.get("etapa_atual", "em andamento"), **feito, "proxima": proxima}


def manifesto(saida: Path) -> dict:
    """O manifesto da execução (criado aqui; o E6 o amplia). Nunca perde o que já está nele."""
    p = Path(saida) / "manifest.json"
    if p.is_file():
        m = json.loads(p.read_text(encoding="utf-8"))
        m.setdefault("entregas", {})
        return m
    brief = json.loads((Path(saida) / "brief.json").read_text(encoding="utf-8"))
    snap = json.loads((Path(saida) / "brand_snapshot.json").read_text(encoding="utf-8"))
    return {
        "pedido": brief.get("pedido"),
        "slug": brief.get("slug"),
        "titulo": brief.get("titulo"),
        "uso": brief.get("uso"),
        "preset": brief.get("preset"),
        "entregavel": "prompt",  # A16: o produto é o texto, não a imagem
        "tamanho_entrega": brief.get("tamanho"),
        "master": brief.get("master"),
        "estilo": {"tecnica": brief.get("estilo"), "base": brief.get("estilo_base"), "modo": brief.get("estilo_modo")},
        "marca": {
            "versao_tokens": snap.get("versao_tokens"),
            "versao_design": snap.get("versao_design"),
            "fingerprint": snap.get("fingerprint"),
        },
        "entregas": {},
    }
