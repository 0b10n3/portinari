"""CLI do Portinari — chamado pelo orquestrador (skill /portinari). Um subcomando por etapa."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import brand, brief


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
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
