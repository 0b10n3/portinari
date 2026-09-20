"""Checagens objetivas na imagem e derivação das entregas a partir de um master.

Com A16 a imagem não é mais o produto: ela é a **prova de que o prompt funciona**. Por isso as
checagens daqui servem ao crítico visual e ao Gate 2, não à entrega.

Hierarquia de gravidade (decisão A2): a **paleta** é a única parte vinculante da marca — cor fora
dela é ERRO. Os tetos numéricos (nº de cores, fundo, acento, granulação) são padrão sobreponível:
viram AVISO, e o pedido do autor pode contrariá-los.

O que este módulo NÃO mede (fica com o crítico visual, e a rubrica diz isso): texto desenhado na
imagem, ângulo de corte, ponto focal, fidelidade ao enriquecimento.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from PIL import Image

# Limiares de ΔE (CIE76) entre uma cor dominante da imagem e o hex mais próximo da paleta.
# Calibrados nas duas gerações reais do S1/S2 (JPEG 1376×768, docs/agy.md §6), medindo tudo o que
# passa de 1% do quadro:
#   folha pintada certa .................. 1,0 – 4,3
#   mistura de borda entre duas folhas ... 6,5 – 17,3   (antialias + JPEG; não é cor nova)
#   cor genuinamente fora da paleta ...... 36,7          (o cinza de sombra do S2)
# Daí aviso em 8 e erro em 25: a mistura de borda avisa, a cor inventada reprova.
# ponytail: 2 imagens de amostra. Se um falso positivo aparecer, meça antes de mexer no número —
# e considere detectar mistura pela reta entre dois hex da paleta, em vez de subir o limiar.
DELTA_AVISO = 8.0
DELTA_ERRO = 25.0
# Duas cores mais próximas que isto são a mesma folha vista através do ruído do JPEG.
DELTA_MESMA_COR = 3.0
FRACAO_MINIMA = 0.01  # "cor ≥1% do quadro", como a marca conta


@lru_cache(maxsize=1 << 16)  # a mesma cor reaparece milhares de vezes numa peça de paper cut
def _lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    """sRGB (0–255) → CIE Lab (D65). Fórmula direta: não vale uma dependência nova."""
    def _lin(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (_lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def _f(t: float) -> float:
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116

    fx, fy, fz = _f(x), _f(y), _f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """ΔE CIE76. Suficiente aqui: a pergunta é "é esta folha ou outra?", não colorimetria fina."""
    la, aa, ba = _lab(a)
    lb, ab, bb = _lab(b)
    return ((la - lb) ** 2 + (aa - ab) ** 2 + (ba - bb) ** 2) ** 0.5


def _hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _luminancia(rgb: tuple[int, int, int]) -> float:
    return (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255


def cores_dominantes(im: Image.Image, minimo: float = FRACAO_MINIMA) -> list[tuple[float, tuple[int, int, int]]]:
    """Cores que ocupam pelo menos `minimo` do quadro, já fundindo o que o JPEG separou.

    Quantiza em 64 buckets (uma peça de paper cut tem 3–7 folhas; o resto é ruído de compressão)
    e funde buckets com ΔE < DELTA_MESMA_COR, ponderando a cor pela área de cada um.
    """
    q = im.convert("RGB").quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    paleta = q.getpalette() or []
    total = im.width * im.height
    grupos: list[list[float | tuple[int, int, int]]] = []
    for n, i in sorted(q.getcolors(64) or [], reverse=True):
        cor = tuple(paleta[i * 3 : i * 3 + 3])
        for g in grupos:
            if delta_e(cor, g[1]) < DELTA_MESMA_COR:  # type: ignore[arg-type]
                peso, atual = g[0], g[1]
                g[0] = peso + n
                g[1] = tuple(round((a * peso + c * n) / (peso + n)) for a, c in zip(atual, cor))  # type: ignore
                break
        else:
            grupos.append([float(n), cor])
    return sorted(((g[0] / total, g[1]) for g in grupos if g[0] / total >= minimo), reverse=True)  # type: ignore


def _fundo(im: Image.Image, dominantes: list[tuple[float, tuple[int, int, int]]]) -> tuple[float, tuple[int, int, int]] | None:
    """A cor que ocupa a borda do quadro é o fundo; devolve a fatia dela no quadro inteiro."""
    amostras = []
    px = im.convert("RGB")
    for x in range(0, im.width, max(1, im.width // 200)):
        amostras += [px.getpixel((x, 0)), px.getpixel((x, im.height - 1))]
    for y in range(0, im.height, max(1, im.height // 200)):
        amostras += [px.getpixel((0, y)), px.getpixel((im.width - 1, y))]
    if not (amostras and dominantes):
        return None
    contagem: dict[int, int] = {}
    for a in amostras:
        i = min(range(len(dominantes)), key=lambda k: delta_e(a, dominantes[k][1]))
        contagem[i] = contagem.get(i, 0) + 1
    return dominantes[max(contagem, key=contagem.get)]  # type: ignore[arg-type]


def _amostrar(im: Image.Image) -> list[tuple[int, int, int]]:
    """Uma grade de pixels, amostrada uma vez e reaproveitada por todas as cores."""
    px = im.convert("RGB")
    passo = max(1, min(im.width, im.height) // 300)
    return [px.getpixel((x, y)) for x in range(0, im.width, passo) for y in range(0, im.height, passo)]


def _amplitude_luminancia(amostras: list[tuple[int, int, int]], cor: tuple[int, int, int]) -> float:
    """Dispersão de luminância dentro de uma folha — proxy de sombra/gradiente/granulação."""
    ls = [_luminancia(p) for p in amostras if delta_e(p, cor) < DELTA_MESMA_COR * 2]
    if len(ls) < 20:
        return 0.0
    media = sum(ls) / len(ls)
    return (sum((l - media) ** 2 for l in ls) / len(ls)) ** 0.5


def checar(caminho: Path, snapshot: dict, modo: str) -> dict:
    """Mede a imagem contra a paleta e os tetos do modo. Erros só de paleta (A2)."""
    with Image.open(caminho) as im:
        im.load()
        largura, altura = im.size
        dominantes = cores_dominantes(im)
        fundo = _fundo(im, dominantes)
        amostras = _amostrar(im)
        p = snapshot["paletas"][modo]
        alvos = {c["hex"]: _hex_rgb(c["hex"]) for c in p["camadas"] + p["figura"]}
        alvos[p["acento"]["hex"]] = _hex_rgb(p["acento"]["hex"])
        acento_hex = p["acento"]["hex"]

        medidas = []
        for fracao, cor in dominantes:
            mais_perto = min(alvos, key=lambda h: delta_e(cor, alvos[h]))
            medidas.append(
                {
                    "rgb": list(cor),
                    "hex_imagem": "#%02X%02X%02X" % cor,
                    "fracao": round(fracao, 4),
                    "token_mais_perto": mais_perto,
                    "delta_e": round(delta_e(cor, alvos[mais_perto]), 1),
                    "amplitude_luminancia": round(_amplitude_luminancia(amostras, cor), 4),
                }
            )

    t = snapshot["tetos"]
    erros, avisos = [], []
    for m in medidas:
        if m["delta_e"] > DELTA_ERRO:  # a paleta é a única parte vinculante da marca
            erros.append(
                f"{m['hex_imagem']} ocupa {m['fracao']:.1%} do quadro e não é nenhuma cor da paleta "
                f"{modo} (mais perto: {m['token_mais_perto']}, ΔE {m['delta_e']})"
            )
        elif m["delta_e"] > DELTA_AVISO:
            avisos.append(f"{m['hex_imagem']} ({m['fracao']:.1%}) está longe de {m['token_mais_perto']} (ΔE {m['delta_e']})")
        if m["amplitude_luminancia"] > t["granulacao_max"]:
            avisos.append(
                f"{m['hex_imagem']} varia de tom dentro da própria folha "
                f"(amplitude {m['amplitude_luminancia']:.3f} > {t['granulacao_max']}): sombra, gradiente ou grão demais"
            )
    if not 3 <= len(medidas) <= t["max_cores"]:
        avisos.append(f"{len(medidas)} cores ≥1% do quadro; a marca pede entre 3 e {t['max_cores']}")
    if fundo and fundo[0] < t["fundo_minimo"]:
        avisos.append(f"o fundo ocupa {fundo[0]:.0%} do quadro; a marca pede ao menos {t['fundo_minimo']:.0%}")
    acento = next((m["fracao"] for m in medidas if m["token_mais_perto"] == acento_hex), 0.0)
    if acento > t["acento_max"]:
        avisos.append(f"o acento {acento_hex} ocupa {acento:.1%} do quadro; o teto da marca é {t['acento_max']:.0%}")

    return {
        "imagem": str(caminho),
        "modo": modo,
        "dimensoes": [largura, altura],
        "cores": medidas,
        "fundo": {"hex": "#%02X%02X%02X" % fundo[1], "fracao": round(fundo[0], 4)} if fundo else None,
        "acento_fracao": round(acento, 4),
        "erros": erros,
        "avisos": avisos,
    }


def gravar(r: dict, saida: Path, iteracao: int, nome: str) -> Path:
    destino = Path(saida) / "iteracoes" / f"{iteracao:02d}" / f"{nome}.checagens.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    return destino


def recorte_central(origem: tuple[int, int], alvo: tuple[int, int]) -> tuple[int, int, int, int]:
    """Caixa do recorte central do master para a proporção do alvo (fórmula de FORMATOS.md)."""
    w, h = origem
    razao = alvo[0] / alvo[1]
    if razao > w / h:  # alvo mais largo: mantém a largura
        cw, ch = w, round(w / razao)
    else:
        cw, ch = round(h * razao), h
    return (w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch


def derivar(master: Path, alvo: tuple[int, int], destino: Path, qualidade: int = 91) -> Path:
    """Master → entrega: corte central + redução Lanczos, no tamanho exato. Nunca distorce.

    JPEG sai com croma 4:4:4 (`subsampling=0`): com 4:2:0 a borda reta do recorte e o acento
    (≤1% do quadro) ganham franja — FORMATOS.md, "Regras de resolução e exportação".
    """
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(master) as im:
        im = im.convert("RGB").crop(recorte_central(im.size, alvo)).resize(alvo, Image.Resampling.LANCZOS)
        if destino.suffix.lower() in (".jpg", ".jpeg"):
            im.save(destino, quality=qualidade, subsampling=0)
        else:
            im.save(destino)
    with Image.open(destino) as saida:
        assert saida.size == tuple(alvo), f"{destino} saiu {saida.size}, esperado {tuple(alvo)}"
    return destino
