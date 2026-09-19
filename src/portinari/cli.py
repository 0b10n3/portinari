"""CLI do Portinari — chamado pelo orquestrador (skill /portinari). Um subcomando por etapa."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import brief


def _ingest(a: argparse.Namespace) -> int:
    b = brief.carregar(Path(a.pedido), Path(a.saida) if a.saida else None)
    destino = brief.gravar(b)
    print(f"brief: {destino}")
    for av in b.avisos:
        print(f"aviso: {av}")
    for p in b.perguntas:
        print(f"PERGUNTA AO AUTOR: {p}")
    return 2 if b.perguntas else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="portinari", description="Pipeline de ilustração da Syntaxis")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="lê o pedido e grava brief.json (exit 2 = há perguntas)")
    i.add_argument("pedido")
    i.add_argument("--saida", help="pasta da execução (padrão: output/AAAA-MM-DD_slug)")
    i.set_defaults(fn=_ingest)
    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
