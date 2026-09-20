"""Entrega do Portinari: o produto é o PROMPT, não a imagem (decisão A16, 20/09/2026).

A imagem que o `agy` gerou existe para provar que o prompt funciona — é evidência, não produto.
Quem gera a peça final é o autor, colando `final/prompt_<modo>.md` no Nano Banana Pro. Por isso a
única coisa que este módulo protege é a autossuficiência do texto entregue: quem abrir o arquivo
num computador sem o monorepo tem de conseguir usá-lo.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import date
from pathlib import Path

from . import enriquecimento

NOMES_MODO = {"dark": "escura", "light": "clara"}


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
    if faltam:  # T2 — a paleta é a única parte vinculante da marca (A2)
        erros.append(f"o prompt não cita {len(faltam)} hex da paleta {modo}: {', '.join(faltam)}")

    outro = "light" if modo == "dark" else "dark"
    invasores = sorted((_hex_da_paleta(snap, outro) - _hex_da_paleta(snap, modo)) & no_prompt)
    if invasores:  # T1 — um modo por arquivo; pilha misturada é reprovação da marca
        erros.append(f"o prompt mistura a pilha {outro} na peça {modo}: {', '.join(invasores)}")

    if _norm(snap["bloco"][modo]) not in _norm(prompt):  # T4
        erros.append(f"o bloco de marca do modo {modo} não está íntegro no prompt")

    try:  # T3 — o mesmo teste que `portinari prompt` faz, agora sobre o que vai ser entregue
        enr, versao = enriquecimento.carregar(Path(saida))
    except (FileNotFoundError, ValueError):
        pass
    else:
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
    tam, master = brief.get("tamanho"), brief.get("master")
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
        "",
        "## Tamanho e formato",
        "",
    ]
    if master:
        linhas.append(f"- **Gere em {master[0]}×{master[1]}** (ou o maior que o gerador permitir).")
    if tam:
        linhas.append(
            f"- **Entregue em {tam[0]}×{tam[1]}** ({brief.get('aspect_ratio')}), por corte central "
            "e redução do que foi gerado — nunca gerando de novo num tamanho diferente."
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
        "- Nenhuma sombra projetada nova que o prompt não tenha pedido.",
        "",
        "Se algo estiver errado: `uv run portinari importar <execução> --iteracao N <imagem>` traz a "
        "peça de volta para as checagens do pipeline.",
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
        "modelo_validacao": g.get("modelo_imagem") or "gemini-3.1-flash-image (agy)",
        "validacao": str(val.relative_to(saida)),
        "validacao_px": [g.get("largura"), g.get("altura")],
        "sha256_prompt": hashlib.sha256(arq.read_bytes()).hexdigest(),
        "gate2": "aprovado",
    }
    (final / "COMO-GERAR.md").write_text(como_gerar(brief, snap, m["entregas"]), encoding="utf-8")
    m["etapa_atual"] = "entregue"
    (saida / "manifest.json").write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    return m["entregas"][modo]


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
