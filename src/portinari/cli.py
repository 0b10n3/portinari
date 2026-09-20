"""CLI do Portinari — chamado pelo orquestrador (skill /portinari). Um subcomando por etapa."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import agy, brand, brief, enriquecimento, entrega


def _ingest(a: argparse.Namespace) -> int:
    try:
        marca = brand.marca_leve(Path(a.brand))
    except (brand.BrandError, OSError) as e:
        print(f"ERRO: não consegui ler os formatos/estilos da marca: {e}")
        return 1
    b = brief.carregar(Path(a.pedido), Path(a.saida) if a.saida else None, marca=marca, piloto=a.piloto)
    destino = brief.gravar(b)
    print(f"brief: {destino}")
    for av in b.avisos:
        print(f"aviso: {av}")
    for p in b.perguntas:
        print(f"PERGUNTA AO AUTOR: {p}")
    return 2 if b.perguntas else 0


def _marca(a: argparse.Namespace) -> int:
    s = brand.resolver(Path(a.brand), verificar_git=not a.sem_fetch, texto=a.texto)
    print(f"marca: {brand.gravar(s, Path(a.saida))}")
    print(f"tokens v{s['versao_tokens']} · DESIGN v{s['versao_design']} · fingerprint {s['fingerprint'][:12]}")
    for av in s["avisos"] + (s["git"] or {}).get("avisos", []):
        print(f"aviso: {av}")
    print(f"formatos: {len(s['formatos'])} usos · estilos: {len(s['estilos'])} "
          f"({sum(e['papel'] == 'base' for e in s['estilos'].values())} base)")
    atras = (s["git"] or {}).get("atras")
    if atras:  # nunca faz pull por conta própria (A13: desatualizada bloqueia)
        msg = f"brand/ está {atras} commit(s) atrás do remoto — atualize com `git -C {a.brand} pull` antes de gerar."
        if not a.permitir_desatualizada:
            print(f"ERRO: {msg}")
            return 1
        print(f"aviso: {msg} Seguindo por --permitir-desatualizada.")
        s["avisos"].append(f"executado com brand/ {atras} commit(s) atrás do remoto (--permitir-desatualizada)")
        brand.gravar(s, Path(a.saida))
    return 0


def _enriquecer(a: argparse.Namespace) -> int:
    """Valida enriquecimento/vNN.json (o mais recente, ou --versao) e grava vNN.md para o autor."""
    saida = Path(a.saida)
    snap = json.loads((saida / "brand_snapshot.json").read_text())
    try:
        enr, arq = enriquecimento.carregar(saida, a.versao)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERRO: {e}")
        return 2
    r = enriquecimento.validar(enr, snap, a.modo, max_elementos=a.max_elementos,
                               min_acrescimos=a.min_acrescimos, texto=a.texto)
    arq.with_suffix(".md").write_text(enriquecimento.renderizar(enr, snap, a.modo, r), encoding="utf-8")
    print(f"enriquecimento: {arq.name} · {len(enr.elementos)} elementos · visão: {arq.with_suffix('.md')}")
    for m in r.erros:
        print(f"ERRO: {m}")
    for m in r.avisos:
        print(f"aviso: {m}")
    for m in r.verificar:
        print(f"VERIFICAR: {m}")
    return 2 if r.erros else 0


def _importar(a: argparse.Namespace) -> int:
    """Importa imagens geradas à mão (ex.: Nano Banana Pro) para iteracoes/NN/."""
    saida, d = Path(a.saida), _iter_dir(a)
    arq = d / a.prompt if not Path(a.prompt).is_absolute() else Path(a.prompt)
    try:
        gs = agy.importar([Path(x) for x in a.imagens], arq.read_text(encoding="utf-8"), saida, a.iteracao,
                          modelo=a.modelo, max_geracoes=a.max_geracoes)
    except (agy.AgyErro, OSError) as e:
        print(f"ERRO: {e}")
        return 3
    for g in gs:
        print(f"{g.nome}: {g.imagem} {g.largura}x{g.altura} · manual" + (f" · {g.modelo_imagem}" if g.modelo_imagem else ""))
    return 0


def _iter_dir(a: argparse.Namespace) -> Path:
    return Path(a.saida) / "iteracoes" / f"{a.iteracao:02d}"


def _prompt(a: argparse.Namespace) -> int:
    """prompt_criativo.md + bloco de marca do modo (injetado por código) -> prompt_final.md."""
    saida, d = Path(a.saida), _iter_dir(a)
    b = json.loads((saida / "brief.json").read_text())
    s = json.loads((saida / "brand_snapshot.json").read_text())
    criativo = (d / "prompt_criativo.md").read_text(encoding="utf-8")
    try:
        enr, venr = enriquecimento.carregar(saida)
    except FileNotFoundError:
        enr = None
    except ValueError as e:
        print(f"ERRO: {e}")
        return 2
    if enr:
        faltam = enriquecimento.termos_ausentes(enr, criativo)
        if faltam:
            print(f"ERRO: o prompt criativo perdeu {len(faltam)} termo(s) do enriquecimento ({venr.name}):")
            for t in faltam:
                print(f"  - {t}")
            return 2
    for termo in brand.lint_descritores(criativo, s["descritores_proibidos"]):
        print(f"aviso: descritor da marca no prompt criativo: '{termo}' (o pedido pode sobrepor)")
    if not b.get("tamanho"):
        print("PERGUNTA AO AUTOR: brief.json sem tamanho; resolva as perguntas do ingest.")
        return 2
    fragmentos = [
        s.get("estilos", {})[k]["fragmento"]
        for k in (b.get("estilo_base"), b.get("estilo_modo"))
        if k and k in s.get("estilos", {})
    ]
    final = agy.montar_prompt(
        criativo, s["bloco"][a.modo], tuple(b["tamanho"]),
        tuple(b["master"]) if b.get("master") else None, fragmentos,
    )
    (d / "prompt_final.md").write_text(final, encoding="utf-8")
    print(f"prompt: {d / 'prompt_final.md'} ({len(final)} caracteres)")
    return 0


def _gerar(a: argparse.Namespace) -> int:
    saida, d = Path(a.saida), _iter_dir(a)
    b = json.loads((saida / "brief.json").read_text())
    proporcao = a.proporcao or agy.melhor_proporcao(*b["tamanho"])
    prompt = (d / a.prompt).read_text(encoding="utf-8")
    codigo = 0
    for _ in range(a.variacoes):
        try:
            g = agy.gerar(prompt, proporcao, saida, a.iteracao, referencias=a.ref, max_geracoes=a.max_geracoes,
                          modelo=a.modelo, timeout=a.timeout)
        except agy.AgyErro as e:
            print(f"ERRO: {e}")
            return 3
        print(f"{g.nome}: {g.imagem} {g.largura}x{g.altura} · orquestrador {g.modelo_orquestrador} · "
              f"prompt {'íntegro' if g.fiel else 'ALTERADO'}")
        if g.hex_ausentes:  # a paleta é a única parte vinculante (A2)
            print(f"ERRO: a ferramenta não recebeu os hex da paleta: {', '.join(g.hex_ausentes)}")
            codigo = 4
        elif not g.fiel:
            print("aviso: o agy reescreveu o prompt (paleta preservada); ver gen_KK.efetivo.md")
    return codigo


def _entregar(a: argparse.Namespace) -> int:
    """O entregável é o prompt (A16): final/prompt_<modo>.md + COMO-GERAR.md + manifest.json."""
    try:
        e = entrega.entregar(Path(a.saida), a.modo, iteracao=a.iteracao, gen=a.gen, aprovado=a.aprovado)
    except (entrega.EntregaErro, FileNotFoundError, KeyError) as erro:
        print(f"ERRO: {erro}")
        return 2
    print(f"entregue: {e['prompt']} (validado por {e['geracao']} da iteração {e['iteracao']:02d}, "
          f"{e['validacao_px'][0]}x{e['validacao_px'][1]})")
    print(f"como gerar: {Path(a.saida) / 'final' / 'COMO-GERAR.md'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="portinari", description="Pipeline de ilustração da Syntaxis")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="lê o pedido e grava brief.json (exit 2 = há perguntas)")
    i.add_argument("pedido")
    i.add_argument("--saida", help="pasta da execução (padrão: output/AAAA-MM-DD_slug)")
    i.add_argument("--brand", default=str(brand.BRAND))
    i.add_argument("--piloto", action="store_true", help="libera estilo que a marca marca como restrito")
    i.set_defaults(fn=_ingest)
    m = sub.add_parser("marca", help="resolve a marca e grava brand_snapshot.json (exit 1 = brand/ atrás do remoto)")
    m.add_argument("saida", help="pasta da execução")
    m.add_argument("--brand", default=str(brand.BRAND))
    m.add_argument("--sem-fetch", action="store_true", help="não consulta o git de brand/")
    m.add_argument("--texto", action="store_true", help="o pedido exige texto na imagem (dropa a regra 'sem texto')")
    m.add_argument("--permitir-desatualizada", action="store_true", help="segue mesmo com brand/ atrás do remoto")
    m.set_defaults(fn=_marca)
    en = sub.add_parser("enriquecer", help="valida enriquecimento/vNN.json e grava vNN.md (exit 2 = erros)")
    en.add_argument("saida")
    en.add_argument("--versao", type=int, help="padrão: a mais recente")
    en.add_argument("--modo", choices=brand.MODOS, default="dark")
    en.add_argument("--max-elementos", type=int, default=12)
    en.add_argument("--min-acrescimos", type=int, default=3)
    en.add_argument("--texto", action="store_true", help="o pedido exige texto na imagem (desliga V8)")
    en.set_defaults(fn=_enriquecer)
    pr = sub.add_parser("prompt", help="monta prompt_final.md = prompt_criativo.md + bloco de marca do modo")
    pr.add_argument("saida")
    pr.add_argument("--iteracao", type=int, required=True)
    pr.add_argument("--modo", choices=brand.MODOS, default="dark")
    pr.set_defaults(fn=_prompt)
    im = sub.add_parser("importar", help="importa imagens geradas à mão (ex.: Nano Banana Pro) para iteracoes/NN/")
    im.add_argument("saida")
    im.add_argument("imagens", nargs="+")
    im.add_argument("--iteracao", type=int, required=True)
    im.add_argument("--prompt", default="prompt_final.md", help="o prompt colado no gerador (dentro de iteracoes/NN/ ou caminho absoluto)")
    im.add_argument("--modelo", help="modelo de imagem usado, só para registro (ex.: nano-banana-pro)")
    im.add_argument("--max-geracoes", type=int, default=agy.MAX_GERACOES)
    im.set_defaults(fn=_importar)
    g = sub.add_parser("gerar", help="gera imagens via agy (exit 3 = falha, 4 = paleta não chegou ao gerador)")
    g.add_argument("saida")
    g.add_argument("--iteracao", type=int, required=True)
    g.add_argument("--prompt", default="prompt_final.md", help="arquivo dentro de iteracoes/NN/")
    g.add_argument("--variacoes", type=int, default=2)
    g.add_argument("--proporcao", choices=list(agy.PROPORCOES), help="padrão: a mais próxima do tamanho do brief")
    g.add_argument("--ref", action="append", default=[], help="imagem de referência/edição (até 3)")
    g.add_argument("--max-geracoes", type=int, default=agy.MAX_GERACOES)
    g.add_argument("--modelo", help="orquestrador do agy (padrão: escada low→medium→high)")
    g.add_argument("--timeout", type=int, default=300)
    g.set_defaults(fn=_gerar)
    e = sub.add_parser("entregar", help="grava o prompt entregável do modo (exit 2 = recusado)")
    e.add_argument("saida")
    e.add_argument("--modo", choices=brand.MODOS, default="dark")
    e.add_argument("--iteracao", type=int, help="padrão: a última")
    e.add_argument("--gen", help="geração que validou o prompt (padrão: a última da iteração)")
    e.add_argument("--aprovado", action="store_true", help="confirma que o Gate 2 aprovou este prompt")
    e.set_defaults(fn=_entregar)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
