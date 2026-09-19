"""`agy` falso para os testes. Segue o contrato observado em docs/agy.md.

Cenário: FAKE_SCENARIO = arquivo JSON com a lista de modos, um por chamada:
ok | rewrite (prompt efetivo cortado) | noimage | transient | fatal | hang
"""

import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

from PIL import Image

TAMANHOS = {"16:9": (1376, 768), "1:1": (1024, 1024), "9:16": (768, 1376), "3:4": (896, 1200), "4:3": (1200, 896)}

args = sys.argv[1:]
instr = args[args.index("-p") + 1]
cenario = Path(os.environ["FAKE_SCENARIO"])
modos = json.loads(cenario.read_text())
contador = cenario.with_suffix(".n")
n = int(contador.read_text()) if contador.exists() else 0
contador.write_text(str(n + 1))
modo = modos[min(n, len(modos) - 1)]
Path(str(cenario) + ".args").write_text(json.dumps(args))

if modo == "hang":
    time.sleep(3)
if modo in ("transient", "fatal"):
    print('AGY_ERROR: {"code": 503, "retryable": %s}' % ("true" if modo == "transient" else "false"), file=sys.stderr)
    sys.exit(3)

home = Path(os.environ["PORTINARI_AGY_HOME"])
conv = str(uuid.uuid4())
logs = home / "brain" / conv / ".system_generated" / "logs"
logs.mkdir(parents=True)
prompt = re.search(r"<<<PROMPT\n(.*)\nPROMPT>>>", instr, re.S).group(1)
ratio = re.search(r'AspectRatio: "([^"]+)"', instr).group(1)
nome = re.search(r'ImageName: "([^"]+)"', instr).group(1)
linhas = [{"step_index": 0, "type": "USER_INPUT", "status": "DONE", "content": instr}]
if modo in ("ok", "rewrite"):
    efetivo = prompt if modo == "ok" else prompt[: len(prompt) // 2]
    img = home / "brain" / conv / f"{nome}_1789000000000.jpg"
    Image.new("RGB", TAMANHOS.get(ratio, (1024, 1024)), "#0F3D27").save(img)
    conteudo = (
        "Created At: 2026-09-18T13:04:35-03:00\nCompleted At: 2026-09-18T13:04:45-03:00\n"
        f"Using prompt: {efetivo}\n\nGenerated image is saved at {img}.\n\n Do not output the path of this image."
    )
    linhas.append({"step_index": 1, "type": "GENERIC", "status": "DONE", "content": conteudo})
(logs / "transcript_full.jsonl").write_text("\n".join(json.dumps(l) for l in linhas))
status = "ERROR" if modo == "noimage" else "SUCCESS"  # status não é confiável (docs/agy.md)
saida = {"conversation_id": conv, "status": status, "response": "DONE", "duration_seconds": 1.0}
if status == "ERROR":
    saida["error"] = "no image generated in response"
print(json.dumps(saida))
