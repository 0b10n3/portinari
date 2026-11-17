"""Roda o validador (`imaging.checar`) em toda imagem de `output/` que já tem modo conhecido, com a
marca vigente, e resume. É a medição da avaliação de 16/11/2026 (auditoria/2026-11-16-avaliacao.md
§2 e §3): rode de novo depois de mexer no validador ou quando a marca mudar, e compare.

    uv run python scripts/avaliar.py [--json resultado.json]
"""

import argparse
import json
from pathlib import Path

from portinari import brand, brief, imaging

IMAGEM = (".jpg", ".jpeg", ".png", ".webp")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", help="grava o resultado completo neste arquivo")
    a = ap.parse_args()
    snap = brand.resolver(verificar_git=False)
    out = {}
    for chk in sorted((brief.PIPELINE / "output").glob("**/iteracoes/*/gen_*.checagens.json")):
        nome = chk.name.removesuffix(".checagens.json")
        img = next((p for p in chk.parent.glob(f"{nome}.*") if p.suffix.lower() in IMAGEM), None)
        if img is None:
            continue
        antigo = json.loads(chk.read_text(encoding="utf-8"))
        meta = json.loads((chk.parent / f"{nome}.json").read_text(encoding="utf-8"))
        par = antigo.get("par")
        r = imaging.checar(
            img, snap, antigo["modo"],
            proporcao=meta.get("proporcao") if meta.get("origem") == "agy" else None,
            par_com=(brief.PIPELINE / par["com"], par["modo"]) if par else None,
        )
        chave = str(img.relative_to(brief.PIPELINE))
        out[chave] = {"modo": antigo["modo"], "erros": r["erros"], "tokens": len(r["tokens"]),
                      "fundo": (r["fundo"] or {}).get("fracao"), "acento": r["acento_fracao"],
                      "par": (r["par"] or {}).get("iou")}
        print(f"{'ok  ' if not r['erros'] else 'ERRO'} {chave} · {antigo['modo']} · fundo {out[chave]['fundo']:.0%} · "
              f"acento {r['acento_fracao']:.1%}" + (f" · par {out[chave]['par']:.2f}" if par else ""))
        for e in r["erros"]:
            print(f"     {e}")
    print(f"\n{len(out)} imagens · {sum(not v['erros'] for v in out.values())} sem erro · "
          f"marca tokens v{snap['versao_tokens']} · DESIGN v{snap['versao_design']}")
    if a.json:
        Path(a.json).write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
