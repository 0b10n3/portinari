"""E5 — checagens objetivas na imagem de validação e derivação master → entrega."""

import json
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

from portinari import agy, brand, brief, imaging
from portinari.cli import main

FIXT = Path(__file__).parent / "fixtures" / "brand"
SNAP = brand.resolver(FIXT, verificar_git=False)
DARK = [c["hex"] for c in SNAP["paletas"]["dark"]["camadas"]]  # #141414 #0F3D27 #125233 #1B6A45
FIGURA = [c["hex"] for c in SNAP["paletas"]["dark"]["figura"]]
ACENTO = SNAP["paletas"]["dark"]["acento"]["hex"]


def peca(tmp_path, nome="peca.png", acento_px=0, intruso=None, gradiente=False):
    """Uma peça sintética no espírito da marca: fundo dominante + três folhas + acento."""
    im = Image.new("RGB", (800, 450), DARK[0])
    d = ImageDraw.Draw(im)
    d.rectangle([40, 60, 260, 390], fill=DARK[1])
    d.rectangle([300, 140, 460, 390], fill=DARK[2])
    d.rectangle([500, 220, 680, 390], fill=FIGURA[0])
    if acento_px:
        d.rectangle([0, 0, acento_px, acento_px], fill=ACENTO)
    if intruso:
        d.rectangle([600, 20, 780, 160], fill=intruso)
    if gradiente:  # rampa de luminância dentro de uma folha só
        for i, x in enumerate(range(40, 260)):
            v = 20 + i // 5
            d.line([(x, 60), (x, 390)], fill=(v, v + 40, v + 20))
    p = tmp_path / nome
    im.save(p)
    return p


# --- ΔE e cores ---------------------------------------------------------------------------------
def test_delta_e_zero_e_simetrico():
    assert imaging.delta_e((15, 82, 69), (15, 82, 69)) == 0
    a, b = (20, 20, 20), (200, 200, 200)
    assert imaging.delta_e(a, b) == pytest.approx(imaging.delta_e(b, a))
    assert imaging.delta_e(a, b) > imaging.delta_e(a, (30, 30, 30))


def test_cores_dominantes_funde_o_ruido_do_jpeg(tmp_path):
    p = peca(tmp_path, "p.jpg")  # JPEG: cada folha vira uma nuvem de tons
    with Image.open(p) as im:
        cores = imaging.cores_dominantes(im)
    assert len(cores) == 4  # quatro folhas, sem estourar em dezenas de variações do JPEG
    assert cores[0][0] > 0.5  # o fundo domina


# --- checagens ----------------------------------------------------------------------------------
def test_peca_correta_passa(tmp_path):
    r = imaging.checar(peca(tmp_path), SNAP, "dark")
    assert r["erros"] == []
    assert r["fundo"]["hex"] == DARK[0] and r["fundo"]["fracao"] > 0.4
    assert all(m["delta_e"] < imaging.DELTA_AVISO for m in r["cores"])


def test_cor_fora_da_paleta_reprova(tmp_path):
    r = imaging.checar(peca(tmp_path, intruso="#C81E1E"), SNAP, "dark")  # a cereja vermelha do S1
    assert any("não é nenhuma cor da paleta dark" in e for e in r["erros"])


def test_a_mesma_peca_no_modo_errado_reprova(tmp_path):
    """Pilha escura medida contra a paleta clara: é o que pega uma derivação que não derivou."""
    assert imaging.checar(peca(tmp_path), SNAP, "light")["erros"]


def test_gradiente_dentro_da_folha_avisa(tmp_path):
    r = imaging.checar(peca(tmp_path, gradiente=True), SNAP, "dark")
    assert any("varia de tom dentro da própria folha" in a for a in r["avisos"])


def test_acento_acima_do_teto_avisa(tmp_path):
    r = imaging.checar(peca(tmp_path, acento_px=260), SNAP, "dark")
    assert r["acento_fracao"] > SNAP["tetos"]["acento_max"]
    assert any("o acento" in a and "teto da marca" in a for a in r["avisos"])
    assert r["erros"] == []  # teto numérico é padrão sobreponível (A2), não reprovação


def test_fundo_pequeno_avisa(tmp_path):
    im = Image.new("RGB", (800, 450), DARK[2])  # a folha toma o quadro
    ImageDraw.Draw(im).rectangle([0, 0, 799, 449], outline=DARK[0], width=12)  # fundo vira moldura
    p = tmp_path / "sem-fundo.png"
    im.save(p)
    r = imaging.checar(p, SNAP, "dark")
    assert any("o fundo ocupa" in a for a in r["avisos"])


# --- recorte e derivação ------------------------------------------------------------------------
@pytest.mark.parametrize(
    "proporcao,recorte,deslocamento",
    [   # a tabela "Áreas seguras" de brand/ILUSTRACOES/FORMATOS.md, para o master 2560×1440
        ((16, 9), (2560, 1440), (0, 0)),
        ((14, 10), (2016, 1440), (272, 0)),
        ((191, 100), (2560, 1340), (0, 50)),
        ((1, 1), (1440, 1440), (560, 0)),
        ((4, 5), (1152, 1440), (704, 0)),
        ((3, 4), (1080, 1440), (740, 0)),
    ],
)
def test_recorte_central_reproduz_a_tabela_da_marca(proporcao, recorte, deslocamento):
    x0, y0, x1, y1 = imaging.recorte_central((2560, 1440), proporcao)
    assert (x1 - x0, y1 - y0) == recorte and (x0, y0) == deslocamento


def test_derivar_sai_no_tamanho_exato(tmp_path):
    master = tmp_path / "master.png"
    peca(tmp_path).replace(master)
    for alvo, ext in [((1456, 816), "jpg"), ((1080, 1350), "png"), ((1100, 220), "jpg")]:
        d = imaging.derivar(master, alvo, tmp_path / f"e_{alvo[0]}x{alvo[1]}.{ext}")
        with Image.open(d) as im:
            assert im.size == alvo


def test_derivar_nao_distorce(tmp_path):
    """Uma faixa vertical continua vertical: recorte + redução, nunca esticão."""
    im = Image.new("RGB", (2560, 1440), DARK[0])
    ImageDraw.Draw(im).rectangle([1260, 0, 1300, 1440], fill=ACENTO)
    master = tmp_path / "m.png"
    im.save(master)
    d = imaging.derivar(master, (1080, 1920), tmp_path / "story.png")
    with Image.open(d) as saida:
        px = saida.convert("RGB")
        largura = sum(imaging.delta_e(px.getpixel((x, 960)), imaging._hex_rgb(ACENTO)) < 10 for x in range(1080))
    assert 45 <= largura <= 62  # 41px dentro de um recorte de 810 -> ~55px em 1080


# --- CLI ----------------------------------------------------------------------------------------
@pytest.fixture
def execucao(tmp_path):
    saida = tmp_path / "out"
    p = tmp_path / "pedido.md"
    p.write_text("# TITLE: Peça\n**USO**: capa de post para substack\n**DESCRIPTION**: x\n", encoding="utf-8")
    b = brief.carregar(p, saida=saida, raiz=tmp_path, marca=brand.marca_leve(FIXT))
    brief.gravar(b)
    brand.gravar(SNAP, saida)
    agy.importar([peca(tmp_path)], "prompt", saida, 1)
    return saida


def test_cli_checar(execucao, capsys, tmp_path):
    assert main(["checar", str(execucao), "--iteracao", "1"]) == 0
    assert "checagens:" in capsys.readouterr().out
    r = json.loads((execucao / "iteracoes" / "01" / "gen_01.checagens.json").read_text())
    assert r["modo"] == "dark" and r["erros"] == []
    agy.importar([peca(tmp_path, "ruim.png", intruso="#C81E1E")], "prompt", execucao, 1)
    assert main(["checar", str(execucao), "--iteracao", "1", "--gen", "gen_02"]) == 2
    assert "ERRO" in capsys.readouterr().out


def test_cli_derivar(execucao, capsys, tmp_path):
    master = peca(tmp_path, "master.png")
    assert main(["derivar", str(execucao), str(master), "--modo", "dark"]) == 0
    saidas = list((execucao / "final").glob("*.jpg"))
    assert len(saidas) == 1 and saidas[0].name.endswith("_dark_1456x816.jpg")
    assert "1456x816" in capsys.readouterr().out
    with Image.open(saidas[0]) as im:
        assert im.size == (1456, 816)
