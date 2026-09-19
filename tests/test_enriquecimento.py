import json
import shutil
from pathlib import Path

import pytest

from portinari import brand, enriquecimento as enr
from portinari.cli import main

AQUI = Path(__file__).parent
FIXT = AQUI / "fixtures"
BOM = json.loads((FIXT / "enriquecimento/cafe-lca-v01.json").read_text())
SNAP = brand.resolver(FIXT / "brand", verificar_git=False)


def modelo(**mut):
    d = json.loads(json.dumps(BOM))
    d.update(mut)
    return enr.Enriquecimento.model_validate(d)


def com_elemento(i, **campos):
    d = json.loads(json.dumps(BOM))
    d["elementos"][i].update(campos)
    return enr.Enriquecimento.model_validate(d)


def erros(e, modo="dark", **kw):
    return enr.validar(e, SNAP, modo, **kw).erros


def test_exemplo_bom_valida_sem_erros():
    r = enr.validar(modelo(), SNAP)
    assert r.erros == [] and len(BOM["elementos"]) == 11
    assert len(r.verificar) == 1 and "e5" in r.verificar[0] and "peneira" in r.verificar[0]
    assert any("pilha-4" in a for a in r.avisos)  # existe no dark, não no light


def test_papeis_de_cor_vem_do_snapshot():
    assert enr.papeis_de_cor(SNAP, "dark")["pilha-4"] == "#1B6A45"
    assert "pilha-4" not in enr.papeis_de_cor(SNAP, "light") and enr.papeis_de_cor(SNAP, "light")["acento"] == "#5F7D1C"


def test_v1_ids_repetidos():
    d = json.loads(json.dumps(BOM))
    d["elementos"][1]["id"] = "e1"
    assert any("V1" in m for m in erros(enr.Enriquecimento.model_validate(d)))


@pytest.mark.parametrize("papel_do_foco,esperado", [("apoio", "há 0"), ("foco", "há 2")])
def test_v2_um_unico_foco(papel_do_foco, esperado):
    e = com_elemento(0, papel=papel_do_foco) if papel_do_foco == "apoio" else com_elemento(2, papel="foco")
    assert any("V2" in m and esperado in m for m in erros(e))


def test_v3_excesso_de_elementos():
    assert any("V3" in m for m in erros(modelo(), max_elementos=10))


def test_v4_poucos_acrescimos():
    d = json.loads(json.dumps(BOM))
    for x in d["elementos"][3:]:
        x["origem"] = "pedido"
    assert any("V4" in m for m in erros(enr.Enriquecimento.model_validate(d)))
    assert not any("V4" in m for m in erros(modelo(), min_acrescimos=8))  # 8 acréscimos no exemplo
    assert any("V4" in m for m in erros(modelo(), min_acrescimos=9))


def test_v5_pedido_preservado():
    assert any("V5" in m for m in erros(modelo(pedido_preservado=[])))


def test_v6_papel_de_cor_invalido_e_pilha_4_no_light():
    assert any("V6" in m and "vermelho" in m for m in erros(com_elemento(3, cor="vermelho")))
    r = enr.validar(modelo(), SNAP, "light")
    assert any("V6" in m and "pilha-4" in m for m in r.erros)  # e6, e7, e11 usam pilha-4


@pytest.mark.parametrize("texto", ["cerejas vermelhas", "red cherries", "madeira marrom", "moedas douradas", "selo azul"])
def test_v7_cor_fora_da_paleta(texto):
    assert any("V7" in m for m in erros(com_elemento(3, elemento=texto)))
    assert any("V7" in m for m in erros(com_elemento(3, termo_en=texto)))


def test_v7_na_cena():
    assert any("V7" in m and "cena" in m for m in erros(modelo(cena="Um selo dourado à direita.")))


@pytest.mark.parametrize("texto", ["um selo com a legenda LCA", "a page of numbers", "preço em R$ 10", "barcode strip"])
def test_v8_texto_na_imagem(texto):
    assert any("V8" in m for m in erros(com_elemento(8, elemento=texto)))


def test_v8_negacao_nao_dispara_e_texto_exigido_desliga():
    assert erros(com_elemento(8, elemento="borda picotada, sem texto legível")) == []
    assert erros(com_elemento(8, elemento="folha de papel com textura e nada de letras")) == []  # 'textura' não é 'texto'
    assert not any("V8" in m for m in erros(com_elemento(8, elemento="selo com a legenda LCA"), texto=True))


def test_avisos_acento_e_descritor():
    d = json.loads(json.dumps(BOM))
    for i in (3, 4, 5):
        d["elementos"][i]["cor"] = "acento"
    r = enr.validar(enr.Enriquecimento.model_validate(d), SNAP)
    assert any("acento" in a for a in r.avisos)
    r = enr.validar(modelo(cena=BOM["cena"] + " Com drop shadow."), SNAP)
    assert r.erros == [] and any("drop shadow" in a for a in r.avisos)


# --- cobertura do prompt -----------------------------------------------------------------------
def test_prompt_enriquecido_cobre_todos_os_termos():
    p = (FIXT / "enriquecimento/cafe-lca-prompt_criativo.md").read_text()
    assert enr.termos_ausentes(modelo(), p) == []
    assert enr.termos_ausentes(modelo(), p.upper().replace(" ", "  ")) == []  # sem caixa, espaços normalizados


def test_prompt_do_s1_perdeu_o_enriquecimento():
    """O prompt do S1 (sem trabalhadores, ferramentas nem detalhes de papel) é o caso que motivou o épico."""
    faltam = enr.termos_ausentes(modelo(), (FIXT / "enriquecimento/s1-prompt_criativo.md").read_text())
    assert {"two faceless harvesters", "wicker basket", "jute sacks", "perforated edge", "round seal", "guilloche band"} <= set(faltam)


# --- carregar / renderizar / CLI ---------------------------------------------------------------
def montar_execucao(tmp_path, versoes=("v01.json",)):
    run = tmp_path / "run"
    (run / "enriquecimento").mkdir(parents=True)
    for v in versoes:
        shutil.copy(FIXT / "enriquecimento/cafe-lca-v01.json", run / "enriquecimento" / v)
    shutil.copy(FIXT.parent.parent / "tests/fixtures/pedidos/cafe-lca.md", tmp_path / "pedido.md")
    assert main(["ingest", str(tmp_path / "pedido.md"), "--saida", str(run)]) == 0
    assert main(["marca", str(run), "--brand", str(FIXT / "brand"), "--sem-fetch"]) == 0
    return run


def test_carregar_versao_mais_recente_e_por_numero(tmp_path):
    run = montar_execucao(tmp_path, ("v01.json", "v02.json"))
    assert enr.carregar(run)[1].name == "v02.json" and enr.carregar(run, 1)[1].name == "v01.json"
    with pytest.raises(FileNotFoundError):
        enr.carregar(tmp_path / "nada")
    (run / "enriquecimento" / "v03.json").write_text("{ não é json")
    with pytest.raises(ValueError, match="v03.json inválido"):
        enr.carregar(run)


def test_cli_enriquecer_ok_grava_md_com_hex(tmp_path, capsys):
    run = montar_execucao(tmp_path)
    assert main(["enriquecer", str(run)]) == 0
    out = capsys.readouterr().out
    assert "11 elementos" in out and "VERIFICAR: e5" in out and "aviso:" in out
    md = (run / "enriquecimento/v01.md").read_text()
    assert "figura-principal (#2D9E67)" in md and "acento (#CDF163)" in md and "⚠ verificar" in md
    assert "## Descartados" in md and "colheitadeira" in md


def test_cli_enriquecer_erro_da_exit_2(tmp_path, capsys):
    run = montar_execucao(tmp_path)
    d = json.loads((run / "enriquecimento/v01.json").read_text())
    d["elementos"][3]["elemento"] = "colhedores com cerejas vermelhas"
    (run / "enriquecimento/v02.json").write_text(json.dumps(d))
    assert main(["enriquecer", str(run)]) == 2
    assert "ERRO: V7: e4" in capsys.readouterr().out
    assert main(["enriquecer", str(run), "--versao", "1"]) == 0  # a v01 continua válida


def test_cli_prompt_recusa_prompt_que_perdeu_termos(tmp_path, capsys):
    run = montar_execucao(tmp_path)
    it = run / "iteracoes" / "01"
    it.mkdir(parents=True)
    shutil.copy(FIXT / "enriquecimento/s1-prompt_criativo.md", it / "prompt_criativo.md")
    assert main(["prompt", str(run), "--iteracao", "1"]) == 2
    out = capsys.readouterr().out
    assert "perdeu" in out and "- two faceless harvesters" in out and not (it / "prompt_final.md").exists()
    shutil.copy(FIXT / "enriquecimento/cafe-lca-prompt_criativo.md", it / "prompt_criativo.md")
    assert main(["prompt", str(run), "--iteracao", "1"]) == 0
    final = (it / "prompt_final.md").read_text()
    assert "guilloche band" in final and "#0F3D27" in final and "#E2E8F0" not in final
