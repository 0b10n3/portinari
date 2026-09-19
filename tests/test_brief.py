import functools
import hashlib
import http.server
import threading
from datetime import date
from pathlib import Path

import pytest
from PIL import Image

from portinari import brief
from portinari.cli import main

AQUI = Path(__file__).parent
FIXTURE = AQUI / "fixtures" / "pedidos" / "cafe-lca.md"
EXEMPLO = AQUI.parent / "pedidos" / "exemplo-cafe-lca.md"
HOJE = date(2026, 9, 18)


def carregar(tmp_path, texto, **kw):
    p = tmp_path / "pedido.md"
    p.write_text(texto, encoding="utf-8")
    return brief.carregar(p, saida=tmp_path / "out", raiz=kw.pop("raiz", tmp_path), hoje=HOJE, **kw)


BASE = "# TITLE: Um título\n**USO**: capa de post para substack\n**DESCRIPTION**: algo no centro\n"


# --- o exemplo com ruído, exatamente como o autor escreveu -------------------------------------
def test_exemplo_e_fixture_sao_o_mesmo_arquivo():
    assert hashlib.sha256(FIXTURE.read_bytes()).digest() == hashlib.sha256(EXEMPLO.read_bytes()).digest()
    txt = FIXTURE.read_text(encoding="utf-8")
    assert "16:9]" in txt and "**SIZE**:2560 × 1440 \n" in txt and txt.endswith("**REFERENCE IMAGES**:\n")


def test_exemplo_com_ruido(tmp_path):
    b = brief.carregar(FIXTURE, saida=tmp_path, hoje=HOJE)
    assert b.perguntas == []
    assert b.titulo == "Transformação da Produção Agricola em Produto Financeiro"
    assert b.slug == "transformacao-da-producao-agricola-em-produto-financeiro"
    assert (b.aspect_ratio, b.resolucao, b.tamanho) == ("16:9", "2k", (2560, 1440))
    assert (b.estilo, b.estilo_padrao) == ("papercut", False)
    assert b.contexto == "" and b.referencias == [] and b.preset == "substack-capa"
    assert b.descricao.endswith("(LCA) no lado direto da figura.")
    assert len(b.avisos) >= 2 and any("16:9" in a for a in b.avisos) and any("2560x1440" in a for a in b.avisos)


def test_saida_padrao_e_gravar(tmp_path):
    b = brief.carregar(FIXTURE, hoje=HOJE)
    assert b.saida.endswith("output/2026-09-18_transformacao-da-producao-agricola-em-produto-financeiro")
    b.saida = str(tmp_path / "x")
    assert brief.Brief.model_validate_json(brief.gravar(b).read_text()) == b


def test_template_nao_vira_pedido_valido(tmp_path):
    b = brief.carregar(AQUI.parent / "pedidos" / "_TEMPLATE.md", saida=tmp_path, hoje=HOJE)
    assert sum("obrigatório" in p for p in b.perguntas) == 3


# --- chaves -----------------------------------------------------------------------------------
def test_chaves_em_portugues_e_formatos(tmp_path):
    b = carregar(
        tmp_path,
        "# Título: Meu pedido\nuso: instagram\n**Descrição:** cena X\n**Estilo**: Collage\n"
        "**Contexto**: texto\n**Proporção**: 1:1\n**Resolução**: 1K\n",
    )
    assert (b.titulo, b.descricao, b.estilo, b.contexto) == ("Meu pedido", "cena X", "papercut", "texto")
    assert b.tamanho == (1080, 1080) and b.aspect_ratio == "1:1" and b.resolucao == "1k"


def test_contexto_longo_com_markdown_e_chave_falsa(tmp_path):
    ctx = (
        "# Um post inteiro\n\n## Seção com **negrito**\nO estilo: dele é X (meio de linha não é chave).\n"
        "Nota: linha começando com palavra que não é chave.\n```\nESTILO: dentro de cerca\n```\n- item\n"
    )
    b = carregar(tmp_path, BASE + "**CONTEXT**:\n" + ctx + "**STYLE**: papercut\n")
    assert b.perguntas == []
    assert "## Seção com **negrito**" in b.contexto and "ESTILO: dentro de cerca" in b.contexto
    assert b.contexto.endswith("- item") and b.estilo == "papercut"


def test_chave_repetida_vira_pergunta(tmp_path):
    b = carregar(tmp_path, BASE + "**CONTEXT**: a\nEstilo: b\n**STYLE**: c\n")
    assert any("mais de uma vez" in p for p in b.perguntas)


def test_contexto_arquivo(tmp_path):
    (tmp_path / "pipelines").mkdir()
    (tmp_path / "pipelines" / "post.md").write_text("# Post\n\nCorpo **forte**\n", encoding="utf-8")
    b = carregar(tmp_path, BASE + "**CONTEXT**: @pipelines/post.md\n")
    assert b.contexto == "# Post\n\nCorpo **forte**" and len(b.contexto_arquivos) == 1
    b = carregar(tmp_path, BASE + "**CONTEXT**: @pipelines/nao-existe.md\n")
    assert any("não existe" in p for p in b.perguntas)


# --- obrigatórios, presets e validação cruzada ---------------------------------------------------
@pytest.mark.parametrize("texto", ["", "   \n\n", "só texto solto\n"])
def test_pedido_vazio(tmp_path, texto):
    b = carregar(tmp_path, texto)
    assert sum("obrigatório" in p for p in b.perguntas) == 3


def test_obrigatorio_ausente(tmp_path):
    b = carregar(tmp_path, "# TITLE: x\n**USO**: substack\n**DESCRIPTION**:\n")
    assert b.perguntas == ["Campo obrigatório ausente ou vazio: DESCRICAO."]


def test_uso_sem_preset_pergunta(tmp_path):
    b = carregar(tmp_path, "# TITLE: x\n**USO**: cartaz de rua\n**DESCRIPTION**: y\n")
    assert any("não tem preset" in p for p in b.perguntas) and b.tamanho is None


def test_uso_sem_preset_mas_com_size_ok(tmp_path):
    b = carregar(tmp_path, "# TITLE: x\n**USO**: cartaz\n**DESCRIPTION**: y\n**SIZE**: 900x1200\n")
    assert b.tamanho == (900, 1200) and b.aspect_ratio == "3:4" and b.perguntas == []


def test_uso_conhecido_sem_tamanho_na_marca(tmp_path):
    b = carregar(tmp_path, "# TITLE: x\n**USO**: thumbnail de youtube\n**DESCRIPTION**: y\n")
    assert any("nem brand/ nem o pedido" in p for p in b.perguntas)


def test_size_incoerente_com_proporcao_vira_pergunta(tmp_path):
    b = carregar(tmp_path, BASE + "**ASPECT RATIO**: 4:3\n**SIZE**: 2560x1440\n")
    assert any("não bate" in p for p in b.perguntas) and b.tamanho == (2560, 1440)  # nada foi "corrigido"


def test_size_incoerente_com_resolucao(tmp_path):
    b = carregar(tmp_path, BASE + "**RESOLUTION**: 1k\n**SIZE**: 2560x1440\n")
    assert any("RESOLUTION" in p for p in b.perguntas)


def test_proporcao_diferente_do_preset_sem_size_pergunta(tmp_path):
    b = carregar(tmp_path, BASE + "**ASPECT RATIO**: 1:1\n")
    assert any("informe o tamanho exato" in p for p in b.perguntas) and b.tamanho is None


def test_preset_preenche_o_que_falta(tmp_path):
    b = carregar(tmp_path, BASE)
    assert (b.tamanho, b.aspect_ratio, b.resolucao) == ((2560, 1440), "16:9", "2k") and b.perguntas == []


def test_valores_invalidos(tmp_path):
    b = carregar(tmp_path, BASE + "**RESOLUTION**: alta\n**ASPECT RATIO**: largo\n**SIZE**: grande\n**STYLE**: aquarela\n")
    assert len(b.perguntas) == 4


# --- referências ------------------------------------------------------------------------------
@pytest.fixture
def servidor(tmp_path):
    raiz = tmp_path / "www"
    raiz.mkdir()
    Image.new("RGB", (30, 20), "#0F3D27").save(raiz / "ok.png")
    (raiz / "falso.png").write_text("isto não é imagem")
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(raiz))
    h.log_message = lambda *a: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}"
    srv.shutdown()


def test_referencias_local_url_e_invalidas(tmp_path, servidor):
    Image.new("RGB", (64, 32), "#F7F7F5").save(tmp_path / "local.jpg")
    (tmp_path / "texto.md").write_text("não sou imagem")
    refs = f"local.jpg, {servidor}/ok.png\n- {servidor}/falso.png\ntexto.md\nsumiu.png\n"
    b = carregar(tmp_path, BASE + "**REFERENCE IMAGES**: " + refs)
    assert [(r.largura, r.altura, r.formato) for r in b.referencias] == [(64, 32, "JPEG"), (30, 20, "PNG")]
    assert Path(b.referencias[1].caminho) == tmp_path / "out" / "referencias" / "ref_02.png"
    assert Path(b.referencias[1].caminho).is_file()
    assert len(b.perguntas) == 3  # url falsa, texto.md, sumiu.png


def test_referencia_url_fora_do_ar(tmp_path):
    b = carregar(tmp_path, BASE + "**REFERENCE IMAGES**: http://127.0.0.1:1/x.png\n")
    assert any("não consegui baixar" in p for p in b.perguntas)


# --- CLI --------------------------------------------------------------------------------------
def test_cli_ingest(tmp_path, capsys):
    assert main(["ingest", str(FIXTURE), "--saida", str(tmp_path)]) == 0
    assert (tmp_path / "brief.json").is_file() and "aviso:" in capsys.readouterr().out
    assert main(["ingest", str(AQUI.parent / "pedidos" / "_TEMPLATE.md"), "--saida", str(tmp_path / "t")]) == 2
