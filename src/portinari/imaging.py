"""Checagens objetivas na imagem e derivação das entregas a partir de um master.

Mede duas coisas com a mesma régua: a imagem de validação do `agy` (prova de que o prompt funciona,
A16) e a peça final gerada à mão e trazida por `importar` (o que vai ao ar — `concluir` a exige).

Hierarquia de gravidade (épico 14 — a marca é vinculante, A2 revogada): cor fora da paleta, teto
estourado (nº de cores, fundo, acento, grão no fundo), proporção errada, peça pequena demais e par
light/dark que não é a mesma peça são ERRO. A variação de tom dentro de uma folha que não é o fundo
continua AVISO: no JPEG ~1K ela mistura compressão com sombra, e o crítico visual decide pela B8.

O que este módulo NÃO mede (fica com o crítico visual, e a rubrica diz isso): texto desenhado na
imagem (não há OCR instalado), sombra, ângulo de corte, perspectiva, ponto focal, fidelidade ao
enriquecimento.
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
PROPORCAO_TOL = 0.01  # 1376×768 é "16:9" para o gerador (0,8% de diferença)
# Par light/dark: IoU das máscaras figura+acento (o que fica sobre a pilha). Calibrado na auditoria
# de 16/11/2026 (auditoria/2026-11-16.md §7), nas imagens de validação entregues:
#   par idêntico (frequência) ..................... 0,90
#   mesma cena, papéis de cor trocados (CRA) ....... 0,53
#   composição mudou (juro, D1 sem conferência) .... 0,22
#   peças diferentes (controle) .................... 0,07 – 0,13
# ponytail: 3 pares. Recalibrar com os pares da Fase 3 antes de apertar.
PAR_AVISO = 0.75
PAR_ERRO = 0.40


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


def _alvos(snapshot: dict, modo: str) -> dict[str, tuple[int, int, int]]:
    p = snapshot["paletas"][modo]
    return {c["hex"]: _hex_rgb(c["hex"]) for c in p["camadas"] + p["figura"] + [p["acento"]]}


def _reduzir(im: Image.Image, lado: int = 400) -> Image.Image:
    """Cópia menor por vizinho mais próximo: mantém as cores que existem, não cria mistura nova."""
    im = im.convert("RGB")
    k = max(1, max(im.size) // lado)
    return im if k == 1 else im.resize((im.width // k, im.height // k), Image.Resampling.NEAREST)


def fracao_por_token(im: Image.Image, alvos: dict[str, tuple[int, int, int]]) -> dict[str, float]:
    """Fração do quadro de cada token, com cada pixel atribuído ao token mais próximo — é como a
    marca conta "cores ≥1%" (DESIGN.md §5.1: "por token mais próximo"). Pixel a mais de DELTA_ERRO
    de todos os tokens não conta para nenhum (é cor fora da paleta, pega pelos clusters)."""
    p = _reduzir(im)
    total = p.width * p.height
    out: dict[str, float] = {}
    for n, cor in p.getcolors(total) or []:
        h = min(alvos, key=lambda t: delta_e(cor, alvos[t]))
        if delta_e(cor, alvos[h]) <= DELTA_ERRO:
            out[h] = out.get(h, 0.0) + n / total
    return out


def _mascara_figura(im: Image.Image, snapshot: dict, modo: str, tamanho: tuple[int, int]) -> list[bool]:
    """True onde o pixel está mais perto da figura ou do acento do que da pilha: a silhueta do que
    está sobre o papel de fundo. É o que sobrevive à troca de pilha numa derivação."""
    p = snapshot["paletas"][modo]
    pilha = [_hex_rgb(c["hex"]) for c in p["camadas"]]
    sobre = [_hex_rgb(c["hex"]) for c in p["figura"]] + [_hex_rgb(p["acento"]["hex"])]
    px = im.convert("RGB").resize(tamanho, Image.Resampling.NEAREST)
    return [min(delta_e(c, s) for s in sobre) < min(delta_e(c, s) for s in pilha)
            for c in (px.getpixel((x, y)) for y in range(tamanho[1]) for x in range(tamanho[0]))]


def par(a: Path, modo_a: str, b: Path, modo_b: str, snapshot: dict) -> float:
    """IoU das silhuetas figura+acento de duas imagens: 1 = mesma composição, ~0,1 = peças diferentes."""
    with Image.open(a) as ia, Image.open(b) as ib:
        tamanho = (192, max(1, round(192 * ia.height / ia.width)))
        ma = _mascara_figura(ia, snapshot, modo_a, tamanho)
        mb = _mascara_figura(ib, snapshot, modo_b, tamanho)
    uniao = sum(x or y for x, y in zip(ma, mb))
    return round(sum(x and y for x, y in zip(ma, mb)) / uniao, 2) if uniao else 1.0


def _razao(proporcao: str) -> float:
    w, h = proporcao.replace(",", ".").split(":")
    return float(w) / float(h)


def checar(
    caminho: Path,
    snapshot: dict,
    modo: str,
    *,
    proporcao: str | None = None,
    entrega: tuple[int, int] | None = None,
    par_com: tuple[Path, str] | None = None,
) -> dict:
    """Mede a imagem contra a paleta e os tetos do modo (erro, épico 14).

    `proporcao` = a pedida ao gerador ("16:9"); `entrega` = o tamanho que o corte central da imagem
    precisa cobrir (só para a peça final); `par_com` = (imagem, modo) da outra variante do par.
    """
    with Image.open(caminho) as im:
        im.load()
        largura, altura = im.size
        dominantes = cores_dominantes(im)
        fundo = _fundo(im, dominantes)
        amostras = _amostrar(im)
        alvos = _alvos(snapshot, modo)
        acento_hex = snapshot["paletas"][modo]["acento"]["hex"]
        por_token = fracao_por_token(im, alvos)

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
        if m["delta_e"] > DELTA_ERRO:
            erros.append(
                f"{m['hex_imagem']} ocupa {m['fracao']:.1%} do quadro e não é nenhuma cor da paleta "
                f"{modo} (mais perto: {m['token_mais_perto']}, ΔE {m['delta_e']})"
            )
        elif m["delta_e"] > DELTA_AVISO:
            avisos.append(f"{m['hex_imagem']} ({m['fracao']:.1%}) está longe de {m['token_mais_perto']} (ΔE {m['delta_e']})")
        if m["amplitude_luminancia"] > t["granulacao_max"]:
            no_fundo = fundo is not None and tuple(m["rgb"]) == tuple(fundo[1])
            msg = (f"{m['hex_imagem']} varia de tom dentro da própria folha "
                   f"(amplitude {m['amplitude_luminancia']:.3f} > {t['granulacao_max']})")
            if no_fundo:  # o teto de granulação vale para o fundo (DESIGN.md §7.3)
                erros.append(msg + ": grão acima do teto no fundo")
            else:
                avisos.append(msg + ": sombra, gradiente ou grão fora do fundo — o crítico decide pela B8")
    tokens = sorted((h for h, f in por_token.items() if f >= FRACAO_MINIMA), key=lambda h: -por_token[h])
    if not 3 <= len(tokens) <= t["max_cores"]:
        erros.append(f"{len(tokens)} cores de token ≥1% do quadro; a marca pede entre 3 e {t['max_cores']}")
    # O fundo é a cor que ocupa a borda. Dois jeitos de contar, e cada um só erra para menos:
    # o cluster parte um fundo com vinheta (borboletas dark: 22% medidos, ~80% à vista); o token
    # parte um fundo claro que oscila entre mint e chalk, a ΔE 5,8 um do outro (borboletas light: 35%).
    # ponytail: máximo dos dois. Se um fundo for superestimado, trocar por região conexa à borda.
    fundo_token = min(alvos, key=lambda h: delta_e(fundo[1], alvos[h])) if fundo else None
    fundo_fracao = max(fundo[0], por_token.get(fundo_token, 0.0)) if fundo else None
    if fundo and fundo_fracao < t["fundo_minimo"]:
        erros.append(f"o fundo ocupa {fundo_fracao:.0%} do quadro; a marca pede ao menos {t['fundo_minimo']:.0%}")
    acento = por_token.get(acento_hex, 0.0)
    if acento > t["acento_max"]:
        erros.append(f"o acento {acento_hex} ocupa {acento:.1%} do quadro; o teto da marca é {t['acento_max']:.0%}")
    if min(largura, altura) < t["tamanho_minimo_px"]:
        erros.append(f"lado menor de {min(largura, altura)} px; abaixo de {t['tamanho_minimo_px']} px é símbolo, não ilustração")
    if proporcao and abs(largura / altura / _razao(proporcao) - 1) > PROPORCAO_TOL:
        erros.append(f"a imagem tem {largura}×{altura}, que não é {proporcao} (o gerador não respeitou a proporção pedida)")
    if entrega:
        x0, y0, x1, y1 = recorte_central((largura, altura), entrega)
        if x1 - x0 < entrega[0] or y1 - y0 < entrega[1]:
            erros.append(f"o corte central de {largura}×{altura} para {entrega[0]}×{entrega[1]} sai menor que a entrega: gere maior")
    iou = None
    if par_com:
        iou = par(Path(caminho), modo, Path(par_com[0]), par_com[1], snapshot)
        msg = f"o par com {Path(par_com[0]).name} ({par_com[1]}) tem IoU de silhueta {iou:.2f}"
        if iou < PAR_ERRO:
            erros.append(msg + f" (< {PAR_ERRO}): não é a mesma composição")
        elif iou < PAR_AVISO:
            avisos.append(msg + f" (< {PAR_AVISO}): algo mudou de lugar ou de papel de cor — D1–D4 da rubrica")

    return {
        "imagem": str(caminho),
        "modo": modo,
        "dimensoes": [largura, altura],
        "proporcao_pedida": proporcao,
        "cores": medidas,
        "tokens": {h: round(por_token[h], 4) for h in tokens},
        "fundo": {"hex": "#%02X%02X%02X" % fundo[1], "token": fundo_token, "fracao": round(fundo_fracao, 4)} if fundo else None,
        "acento_fracao": round(acento, 4),
        "par": {"com": str(par_com[0]), "modo": par_com[1], "iou": iou} if par_com else None,
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
