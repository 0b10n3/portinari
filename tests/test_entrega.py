"""E12 — o entregável é o prompt. Aqui se testa o que impede entregar um prompt quebrado."""

import json
import shutil
from datetime import date
from pathlib import Path

import pytest
from PIL import Image

from portinari import agy, brand, brief, entrega
from portinari.cli import main

AQUI = Path(__file__).parent
FIXT = AQUI / "fixtures" / "brand"
HOJE = date(2026, 9, 20)
PEDIDO = (
    "# TITLE: Café vira LCA\n**USO**: capa de post para substack\n"
    "**DESCRIPTION**: lavoura de café à esquerda, título à direita\n"
)
CRIATIVO = "Cut-paper collage: a coffee slope on the left becomes a certificate on the right."


@pytest.fixture
def execucao(tmp_path):
    """Uma execução até a imagem de validação: brief, marca, prompt final e uma geração."""
    saida = tmp_path / "out"
    p = tmp_path / "pedido.md"
    p.write_text(PEDIDO, encoding="utf-8")
    b = brief.carregar(p, saida=saida, raiz=tmp_path, hoje=HOJE, marca=brand.marca_leve(FIXT))
    brief.gravar(b)
    snap = brand.resolver(FIXT, verificar_git=False)
    brand.gravar(snap, saida)
    prompt = agy.montar_prompt(CRIATIVO, snap["bloco"]["dark"], b.tamanho, b.master,
                               [snap["estilos"]["flat"]["fragmento"]])
    img = tmp_path / "val.jpg"
    Image.new("RGB", (1376, 768), "#0F3D27").save(img)
    agy.importar([img], prompt, saida, 1, modelo="gemini-3.1-flash-image")
    return saida


def entregar(saida, **kw):
    return entrega.entregar(saida, kw.pop("modo", "dark"), aprovado=kw.pop("aprovado", True), hoje=HOJE, **kw)


def _regravar_prompt(saida, texto, it=1, gen="gen_01"):
    (saida / "iteracoes" / f"{it:02d}" / f"{gen}.prompt.md").write_text(texto, encoding="utf-8")


# --- caminho feliz ------------------------------------------------------------------------------
def test_entrega_grava_prompt_validacao_como_gerar_e_manifesto(execucao):
    e = entregar(execucao)
    arq = execucao / "final" / "prompt_dark.md"
    texto = arq.read_text(encoding="utf-8")
    assert e["prompt"] == "final/prompt_dark.md" and e["geracao"] == "gen_01"
    assert texto.startswith("# Café vira LCA — prompt dark (pilha escura)")
    assert "2026-09-20" in texto and CRIATIVO in texto and "#0F3D27" in texto
    assert (execucao / e["validacao"]).is_file() and e["validacao_px"] == [1376, 768]

    cg = (execucao / "final" / "COMO-GERAR.md").read_text(encoding="utf-8")
    assert "gemini-3-pro-image" in cg and "Gere em 2560×1440" in cg and "Entregue em 1456×816" in cg
    assert "JPEG ou PNG, até 2 MB" in cg and "78,75% × 93,06%" in cg
    assert "não** é a entrega" in cg  # a validação não é o produto

    m = json.loads((execucao / "manifest.json").read_text(encoding="utf-8"))
    assert m["entregavel"] == "prompt" and m["etapa_atual"] == "entregue"
    assert m["marca"]["versao_tokens"] == "2.7.0" and m["estilo"]["base"] == "flat"
    assert m["entregas"]["dark"]["gate2"] == "aprovado"


def test_prompt_entregue_nao_depende_do_repositorio(execucao):
    entregar(execucao)
    texto = (execucao / "final" / "prompt_dark.md").read_text(encoding="utf-8")
    corpo = texto.split("---\n", 1)[1]
    # nada da execução: nem a pasta de saída, nem caminho absoluto. (`brand/LOGO/` aparece porque
    # é prosa do próprio bloco de marca, injetado verbatim — conselho ao humano, não dependência.)
    assert "output/" not in corpo and str(execucao) not in corpo and "iteracoes/" not in corpo


def test_dois_modos_convivem(execucao):
    snap = json.loads((execucao / "brand_snapshot.json").read_text())
    img = execucao.parent / "val2.jpg"
    Image.new("RGB", (1376, 768), "#E2E8F0").save(img)
    agy.importar([img], agy.montar_prompt(CRIATIVO, snap["bloco"]["light"], (1456, 816), (2560, 1440)),
                 execucao, 2, modelo="gemini-3.1-flash-image")
    entregar(execucao, iteracao=1)  # sem --iteracao ele pegaria a 02, que é a pilha clara
    entregar(execucao, modo="light", iteracao=2)
    m = json.loads((execucao / "manifest.json").read_text(encoding="utf-8"))
    assert set(m["entregas"]) == {"dark", "light"} and m["entregas"]["light"]["iteracao"] == 2
    cg = (execucao / "final" / "COMO-GERAR.md").read_text(encoding="utf-8")
    assert "`dark`" in cg and "`light`" in cg


# --- recusas ------------------------------------------------------------------------------------
def test_sem_gate_nao_entrega(execucao):
    with pytest.raises(entrega.EntregaErro, match="Gate 2"):
        entrega.entregar(execucao, "dark")
    assert not (execucao / "final").exists()


def test_hex_da_paleta_ausente_recusa(execucao):
    snap = json.loads((execucao / "brand_snapshot.json").read_text())
    _regravar_prompt(execucao, snap["bloco"]["dark"].replace("#CDF163", "um verde-limão"))
    with pytest.raises(entrega.EntregaErro, match="#CDF163"):
        entregar(execucao)
    assert not (execucao / "final").exists()


def test_pilha_do_outro_modo_recusa(execucao):
    snap = json.loads((execucao / "brand_snapshot.json").read_text())
    _regravar_prompt(execucao, snap["bloco"]["dark"] + "\nalso use #E2E8F0 somewhere.\n")
    with pytest.raises(entrega.EntregaErro, match="mistura a pilha light"):
        entregar(execucao)


def test_prompt_sem_bloco_de_marca_recusa(execucao):
    _regravar_prompt(execucao, CRIATIVO + "\n#141414 #0F3D27 #125233 #1B6A45 #F7F7F5 #E2E8F0x #CDF163\n")
    with pytest.raises(entrega.EntregaErro, match="bloco de marca"):
        entregar(execucao)


def test_termo_do_enriquecimento_ausente_recusa(execucao):
    d = execucao / "enriquecimento"
    d.mkdir()
    shutil.copy(AQUI / "fixtures" / "enriquecimento" / "cafe-lca-v01.json", d / "v01.json")
    with pytest.raises(entrega.EntregaErro, match="termo\\(s\\) do enriquecimento"):
        entregar(execucao)


def test_uso_sem_formato_na_marca_recusa(execucao):
    b = json.loads((execucao / "brief.json").read_text())
    b["tamanho"], b["formato"] = None, []
    (execucao / "brief.json").write_text(json.dumps(b), encoding="utf-8")
    with pytest.raises(entrega.EntregaErro, match="FORMATOS.md"):
        entregar(execucao)


def test_geracao_sem_imagem_recusa(execucao):
    g = execucao / "iteracoes" / "01" / "gen_01.json"
    d = json.loads(g.read_text())
    Path(d["imagem"]).unlink()
    with pytest.raises(entrega.EntregaErro, match="nunca foi validado"):
        entregar(execucao)


def test_geracao_inexistente(execucao):
    with pytest.raises(entrega.EntregaErro, match="gen_99 não existe"):
        entregar(execucao, gen="gen_99")


def test_execucao_sem_iteracao(tmp_path, execucao):
    shutil.rmtree(execucao / "iteracoes")
    (execucao / "iteracoes").mkdir()
    with pytest.raises(entrega.EntregaErro, match="nenhuma iteração"):
        entregar(execucao)


# --- CLI ----------------------------------------------------------------------------------------
def test_cli_entregar(execucao, capsys):
    assert main(["entregar", str(execucao), "--modo", "dark", "--aprovado"]) == 0
    out = capsys.readouterr().out
    assert "final/prompt_dark.md" in out and "1376x768" in out and "COMO-GERAR.md" in out
    assert main(["entregar", str(execucao), "--modo", "dark"]) == 2
    assert "Gate 2" in capsys.readouterr().out
