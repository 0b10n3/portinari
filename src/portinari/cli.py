"""CLI do Portinari — chamado pelo orquestrador (skill /portinari). Um subcomando por etapa."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import agy, brand, brief


def _ingest(a: argparse.Namespace) -> int:
    b = brief.carregar(Path(a.pedido), Path(a.saida) if a.saida else None)
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
    atras = (s["git"] or {}).get("atras")
    if atras:  # nunca faz pull por conta própria
        print(f"PERGUNTA AO AUTOR: brand/ está {atras} commit(s) atrás do remoto. Atualizar (git pull) antes de seguir?")
        return 2
    return 0


def _iter_dir(a: argparse.Namespace) -> Path:
    return Path(a.saida) / "iteracoes" / f"{a.iteracao:02d}"


def _prompt(a: argparse.Namespace) -> int:
    """prompt_criativo.md + bloco de marca do modo (injetado por código) -> prompt_final.md."""
    saida, d = Path(a.saida), _iter_dir(a)
    b = json.loads((saida / "brief.json").read_text())
    s = json.loads((saida / "brand_snapshot.json").read_text())
    criativo = (d / "prompt_criativo.md").read_text(encoding="utf-8")
    for termo in brand.lint_descritores(criativo, s["descritores_proibidos"]):
        print(f"aviso: descritor da marca no prompt criativo: '{termo}' (o pedido pode sobrepor)")
    if not b.get("tamanho"):
        print("PERGUNTA AO AUTOR: brief.json sem tamanho; resolva as perguntas do ingest.")
        return 2
    final = agy.montar_prompt(criativo, s["bloco"][a.modo], *b["tamanho"])
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


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="portinari", description="Pipeline de ilustração da Syntaxis")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="lê o pedido e grava brief.json (exit 2 = há perguntas)")
    i.add_argument("pedido")
    i.add_argument("--saida", help="pasta da execução (padrão: output/AAAA-MM-DD_slug)")
    i.set_defaults(fn=_ingest)
    m = sub.add_parser("marca", help="resolve a marca e grava brand_snapshot.json (exit 2 = brand/ atrás do remoto)")
    m.add_argument("saida", help="pasta da execução")
    m.add_argument("--brand", default=str(brand.BRAND))
    m.add_argument("--sem-fetch", action="store_true", help="não consulta o git de brand/")
    m.add_argument("--texto", action="store_true", help="o pedido exige texto na imagem (dropa a regra 'sem texto')")
    m.set_defaults(fn=_marca)
    pr = sub.add_parser("prompt", help="monta prompt_final.md = prompt_criativo.md + bloco de marca do modo")
    pr.add_argument("saida")
    pr.add_argument("--iteracao", type=int, required=True)
    pr.add_argument("--modo", choices=brand.MODOS, default="dark")
    pr.set_defaults(fn=_prompt)
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
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
