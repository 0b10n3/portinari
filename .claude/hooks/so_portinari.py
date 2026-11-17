"""PreToolUse: bloqueia Write/Edit fora de pipelines/portinari (e do temporário do sistema).

`brand/`, o hemingway e o resto do monorepo são só leitura para este pipeline (CLAUDE.md regra 3).
A regra estava só em texto; aqui ela não depende de o agente lembrar. Exit 2 = recusa, e o stderr
volta para o agente como motivo. Bash não passa por aqui: escrita por shell continua sendo instrução.
"""

import json
import sys
import tempfile
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[2]
PERMITIDOS = (PIPELINE, Path(tempfile.gettempdir()).resolve())


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except ValueError:
        return 0  # sem evento legível não há o que julgar
    entrada = evento.get("tool_input") or {}
    alvo = entrada.get("file_path") or entrada.get("notebook_path")
    if not alvo:
        return 0
    p = Path(alvo)
    p = (p if p.is_absolute() else Path(evento.get("cwd") or PIPELINE) / p).resolve()
    if any(p == r or r in p.parents for r in PERMITIDOS):
        return 0
    print(
        f"portinari: escrita fora de pipelines/portinari bloqueada ({p}). brand/ e os outros pipelines "
        "são só leitura: escreva a proposta no relatório e deixe a edição para o autor.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
