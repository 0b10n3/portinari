"""E11 — tamanho e estilo saem do código e passam a vir de brand/ em runtime."""

import shutil
from pathlib import Path

import pytest

from portinari import agy, brand, brief
from portinari.cli import main

FIXT = Path(__file__).parent / "fixtures" / "brand"
FORMATOS = "ILUSTRACOES/FORMATOS.md"
BASE = "# TITLE: Um título\n**USO**: capa de post para substack\n**DESCRIPTION**: algo no centro\n"


@pytest.fixture
def copia(tmp_path):
    d = tmp_path / "brand"
    shutil.copytree(FIXT, d)
    return d


def carregar(tmp_path, texto, marca_dir=FIXT, **kw):
    p = tmp_path / "pedido.md"
    p.write_text(texto, encoding="utf-8")
    return brief.carregar(p, saida=tmp_path / "out", raiz=tmp_path, marca=brand.marca_leve(marca_dir), **kw)


# --- FORMATOS.md --------------------------------------------------------------------------------
def test_formatos_por_uso():
    f = brand.marca_leve(FIXT)["formatos"]
    assert set(f) == {"substack-capa", "substack-email", "linkedin-destaque",
                      "instagram-post", "instagram-story", "youtube-thumb"}
    assert f["substack-capa"]["entrega"] == [1456, 816] and f["substack-capa"]["master"] == [2560, 1440]
    assert f["substack-capa"]["formato"] == ["jpeg", "png"] and f["substack-capa"]["peso_max_mb"] == 2.0
    assert f["linkedin-destaque"]["proporcao"] == "1.91:1" and f["linkedin-destaque"]["peso_max_mb"] == 3.0
    # o e-mail é 5:1 e a marca proíbe derivá-lo de 16:9 — o autor precisa ler isso
    assert any("não cortar de 16:9" in o for o in f["substack-email"]["observacoes"])
    # linhas sem chave (retrato de dado, capa de artigo, Facebook) são referência, não uso
    assert "facebook" not in " ".join(f).lower()


def test_area_segura_e_fracao_do_master():
    a = brand.marca_leve(FIXT)["areas_seguras"]
    assert a["master_referencia"] == [2560, 1440]
    assert a["zonas"]["universal"]["recorte"] == [2016, 1340]
    assert a["zonas"]["universal"]["fracao"] == [0.7875, 0.930556]


def test_mudar_formatos_muda_a_entrega_sem_tocar_em_codigo(copia, tmp_path):
    p = copia / FORMATOS
    p.write_text(p.read_text(encoding="utf-8").replace("**1456×816**", "**1400×800**"), encoding="utf-8")
    b = carregar(tmp_path, BASE, marca_dir=copia)
    assert b.tamanho == (1400, 800)


def test_tabela_que_some_falha_alto(copia):
    p = copia / FORMATOS
    p.write_text(p.read_text(encoding="utf-8").replace("| Chave ", "| Outra "), encoding="utf-8")
    with pytest.raises(brand.BrandError, match="Chave"):
        brand.marca_leve(copia)


def test_uso_sem_formato_de_arquivo_falha_alto(copia):
    p = copia / FORMATOS
    p.write_text(p.read_text(encoding="utf-8").replace("| JPEG ou PNG, ≤2 MB (sem limite oficial achado)", "| ?"),
                 encoding="utf-8")
    with pytest.raises(brand.BrandError, match="formato do arquivo"):
        brand.marca_leve(copia)


# --- estilos ------------------------------------------------------------------------------------
def test_estilos_base_modo_e_restrito():
    e = brand.marca_leve(FIXT)["estilos"]
    assert {k for k, v in e.items() if v["papel"] == "base"} == {"flat", "geometric", "grain-textured", "risograph"}
    assert e["isometric"]["restrito"] and not e["flat"]["restrito"]
    assert "cut-paper" in e["flat"]["fragmento"] and "```" not in e["flat"]["fragmento"]


def test_estilos_recusados_trazem_o_motivo():
    r = brand.marca_leve(FIXT)["estilos_recusados"]
    assert set(r) == {"psychedelic-retro", "pop-art", "doodle-line-art", "holographic", "pixel-art"}
    assert "retícula" in r["pixel-art"]["motivo"]


def test_estilo_sem_fragmento_falha_alto(copia):
    p = copia / "ILUSTRACOES/estilos/flat.md"
    p.write_text(p.read_text(encoding="utf-8").replace("```text", "```"), encoding="utf-8")
    with pytest.raises(brand.BrandError, match="fragmento de prompt"):
        brand.marca_leve(copia)


# --- STYLE no pedido ----------------------------------------------------------------------------
def test_base_padrao_quando_o_pedido_nao_declara(tmp_path):
    b = carregar(tmp_path, BASE)
    assert (b.estilo, b.estilo_base, b.estilo_modo, b.estilo_padrao) == ("papercut", "flat", None, True)


def test_uma_base_e_um_modo(tmp_path):
    b = carregar(tmp_path, BASE + "**STYLE**: grain-textured + nostalgic\n")
    assert (b.estilo_base, b.estilo_modo) == ("grain-textured", "nostalgic")
    assert b.perguntas == [] and b.estilo_padrao is False


def test_duas_bases_viram_pergunta(tmp_path):
    b = carregar(tmp_path, BASE + "**STYLE**: flat e geometric\n")
    assert any("mais de uma base" in p for p in b.perguntas)


def test_estilo_recusado_pela_marca_vira_pergunta_com_motivo(tmp_path):
    b = carregar(tmp_path, BASE + "**STYLE**: pixel art\n")
    assert any("que a marca recusa" in p and "retícula" in p for p in b.perguntas)


def test_estilo_restrito_so_com_piloto(tmp_path):
    b = carregar(tmp_path, BASE + "**STYLE**: geometric + isometric\n")
    assert any("restrito" in p and "--piloto" in p for p in b.perguntas) and b.estilo_modo is None
    b = carregar(tmp_path, BASE + "**STYLE**: geometric + isometric\n", piloto=True)
    assert b.estilo_modo == "isometric" and b.perguntas == []


def test_estilo_desconhecido_continua_perguntando(tmp_path):
    b = carregar(tmp_path, BASE + "**STYLE**: aquarela\n")
    assert any("não tem linguagem definida" in p for p in b.perguntas)


# --- prompt -------------------------------------------------------------------------------------
def test_fragmentos_entram_depois_do_bloco_de_marca():
    s = brand.resolver(FIXT, verificar_git=False)
    frag = [s["estilos"]["grain-textured"]["fragmento"], s["estilos"]["surreal"]["fragmento"]]
    p = agy.montar_prompt("Criativo.", s["bloco"]["dark"], (1456, 816), (2560, 1440), frag)
    assert p.index("Criativo.") < p.index("Bloco de marca") < p.index(frag[0]) < p.index(frag[1]) < p.index("## Technical")
    assert "Render at 2560x1440" in p and "Final delivery is 1456x816" in p


def test_tecnico_sem_master_nao_fala_em_entrega():
    p = agy.montar_prompt("Criativo.", "# Bloco", (1080, 1080))
    assert "Render at 1080x1080" in p and "Final delivery" not in p


# --- snapshot e CLI -----------------------------------------------------------------------------
def test_snapshot_cobre_formatos_e_estilos_no_fingerprint(copia):
    antes = brand.resolver(copia, verificar_git=False)
    assert antes["formatos"]["substack-capa"]["entrega"] == [1456, 816]
    assert antes["estilos"]["flat"]["papel"] == "base" and antes["estilos_recusados"]
    p = copia / "ILUSTRACOES/estilos/surreal.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nnota\n", encoding="utf-8")
    assert brand.resolver(copia, verificar_git=False)["fingerprint"] != antes["fingerprint"]


def test_cli_marca_bloqueia_com_brand_atras_do_remoto(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(brand, "git_status", lambda *a, **k: {"atras": 2, "avisos": [], "remotos": ["origin"],
                                                              "alteracoes_locais": [], "repositorio": "x"})
    assert main(["marca", str(tmp_path), "--brand", str(FIXT)]) == 1
    assert "ERRO" in capsys.readouterr().out
    assert main(["marca", str(tmp_path), "--brand", str(FIXT), "--permitir-desatualizada"]) == 0
    assert "Seguindo por --permitir-desatualizada" in capsys.readouterr().out


def test_cli_ingest_usa_a_marca(tmp_path, capsys):
    p = tmp_path / "pedido.md"
    p.write_text(BASE, encoding="utf-8")
    assert main(["ingest", str(p), "--saida", str(tmp_path / "out"), "--brand", str(FIXT)]) == 0
    b = brief.Brief.model_validate_json((tmp_path / "out" / "brief.json").read_text())
    assert (b.tamanho, b.master, b.estilo_base) == ((1456, 816), (2560, 1440), "flat")
