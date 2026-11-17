"""E12 — o entregável é o prompt. Aqui se testa o que impede entregar um prompt quebrado."""

import json
import shutil
from datetime import date
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

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
ALT = "Colagem de papel: uma encosta de café à esquerda vira um certificado à direita."
ENR = {
    "conceito": "C1", "pedido_preservado": ["café à esquerda, título à direita"], "cena": "…", "alt": ALT,
    "elementos": [
        {"id": "e1", "zona": "esquerda", "papel": "apoio", "origem": "pedido", "elemento": "encosta",
         "termo_en": "coffee slope", "cor": "pilha-3"},
        {"id": "e2", "zona": "direita", "papel": "foco", "origem": "pedido", "elemento": "certificado",
         "termo_en": "certificate", "cor": "figura-principal"},
    ],
}


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
    (saida / "enriquecimento").mkdir()
    (saida / "enriquecimento" / "v01.json").write_text(json.dumps(ENR, ensure_ascii=False), encoding="utf-8")
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
    assert "gemini-3-pro-image" in cg and "proporção 16:9, resolução 2K" in cg and "Entregue em 1456×816" in cg
    assert ALT in cg and e["alt"] == ALT and e["derivado_por_edicao"] is False
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
    shutil.copy(AQUI / "fixtures" / "enriquecimento" / "cafe-lca-v01.json", d / "v02.json")
    with pytest.raises(entrega.EntregaErro, match="termo\\(s\\) do enriquecimento"):
        entregar(execucao)


def test_sem_alt_text_recusa(execucao):
    """Auditoria M4: a imagem não carrega texto; sem alt, a informação verbal some."""
    (execucao / "enriquecimento" / "v01.json").write_text(json.dumps({**ENR, "alt": ""}), encoding="utf-8")
    with pytest.raises(entrega.EntregaErro, match="não tem `alt`"):
        entregar(execucao)
    shutil.rmtree(execucao / "enriquecimento")
    with pytest.raises(entrega.EntregaErro, match="não há alt-text"):
        entregar(execucao)


def test_light_derivado_manda_anexar_a_peca_dark(execucao):
    entregar(execucao)
    g = execucao / "iteracoes" / "01" / "gen_01.json"
    d = json.loads(g.read_text())
    g.write_text(json.dumps({**d, "referencias": ["/x/dark.jpg"]}))
    snap = json.loads((execucao / "brand_snapshot.json").read_text())
    _regravar_prompt(execucao, agy.montar_prompt(CRIATIVO, snap["bloco"]["light"], (1456, 816), (2560, 1440)))
    entregar(execucao, modo="light")
    cg = (execucao / "final" / "COMO-GERAR.md").read_text(encoding="utf-8")
    assert "**light:** gere o dark primeiro" in cg and "anexe a peça dark final" in cg


@pytest.mark.parametrize("tamanho,master,esperado", [
    ((1456, 816), (2560, 1440), ("16:9", "2K", False)),   # capa do Substack
    ((1100, 220), (2200, 440), ("21:9", "2K", True)),     # e-mail 5:1: o Pro não tem
    ((1080, 1350), (2160, 2880), ("4:5", "4K", False)),   # post do Instagram
    ((1200, 627), (2560, 1340), ("16:9", "2K", True)),    # LinkedIn 1,91:1
])
def test_gerador_final(tamanho, master, esperado):
    gf = entrega.gerador_final({"tamanho": tamanho, "master": master})
    assert (gf["proporcao"], gf["resolucao"], gf["corta"]) == esperado


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


# --- E6: estado e arquivamento do pedido ---------------------------------------------------------
def test_estado_diz_a_proxima_acao(tmp_path, execucao):
    vazio = entrega.estado(tmp_path / "nada")
    assert vazio["brief"] is False and vazio["proxima"].startswith("uv run portinari ingest")

    e = entrega.estado(execucao)
    assert e["iteracoes"] == [1] and e["geracoes"] == 0 and e["entregas"] == []  # importada: fora do teto
    assert "Gate 2" in e["proxima"]  # já há geração: a próxima é checar e aprovar

    entregar(execucao)
    depois = entrega.estado(execucao)
    assert depois["entregas"] == ["dark"] and "concluir" in depois["proxima"]


def test_concluir_arquiva_o_pedido(tmp_path, execucao):
    entregar(execucao)
    processados = tmp_path / "_processados"
    origem = Path(json.loads((execucao / "brief.json").read_text())["pedido"])
    destino = entrega.concluir(execucao, processados, sem_final=True)

    assert destino == processados / origem.name and destino.is_file()
    assert not origem.exists()  # movido, não copiado
    assert (execucao / "pedido.md").read_text(encoding="utf-8") == PEDIDO  # a execução guarda a cópia
    m = json.loads((execucao / "manifest.json").read_text())
    assert m["etapa_atual"] == "concluido" and m["pedido_arquivado"] == str(destino)
    assert m["final_conferido"] == {"dark": None}  # pulado, e registrado
    assert entrega.estado(execucao)["proxima"] == "nada: execução concluída"


def _peca_final(tmp_path, nome="pro.png", tamanho=(2752, 1536)):
    """Uma peça no espírito da marca, no tamanho que o Pro devolve em 16:9 2K."""
    snap = brand.resolver(FIXT, verificar_git=False)["paletas"]["dark"]
    im = Image.new("RGB", tamanho, snap["camadas"][0]["hex"])
    d = ImageDraw.Draw(im)
    w, h = tamanho
    d.rectangle([w // 10, h // 4, w // 3, h * 3 // 4], fill=snap["camadas"][1]["hex"])
    d.rectangle([w // 2, h // 3, w * 2 // 3, h * 3 // 4], fill=snap["figura"][0]["hex"])
    p = tmp_path / nome
    im.save(p)
    return p


def test_concluir_exige_a_peca_final_conferida(tmp_path, execucao, capsys):
    """Auditoria M1: o pedido só fecha quando a peça que vai ao ar passou pela mesma régua."""
    entregar(execucao)
    proc = tmp_path / "_processados"
    with pytest.raises(entrega.EntregaErro, match="falta a peça final conferida do\\(s\\) modo\\(s\\) dark"):
        entrega.concluir(execucao, proc)
    assert "Nano Banana Pro" in entrega.estado(execucao)["proxima"]

    agy.importar([_peca_final(tmp_path)], "prompt", execucao, 2, modelo="nano-banana-pro")
    assert main(["checar", str(execucao), "--iteracao", "2", "--modo", "dark"]) == 0
    assert entrega.estado(execucao)["finais"] == ["dark"]
    entrega.concluir(execucao, proc)
    m = json.loads((execucao / "manifest.json").read_text())
    assert m["final_conferido"] == {"dark": "iteracoes/02/gen_01"}


def test_peca_final_pequena_nao_conta(tmp_path, execucao, capsys):
    entregar(execucao)
    agy.importar([_peca_final(tmp_path, tamanho=(1024, 576))], "prompt", execucao, 2)  # menor que 1456×816
    assert main(["checar", str(execucao), "--iteracao", "2", "--modo", "dark"]) == 2
    assert "sai menor que a entrega" in capsys.readouterr().out
    assert entrega.estado(execucao)["finais"] == []


def test_nao_arquiva_pedido_sem_entregavel(tmp_path, execucao):
    with pytest.raises(entrega.EntregaErro, match="não tem nenhum prompt"):
        entrega.concluir(execucao, tmp_path / "_processados")
    assert Path(json.loads((execucao / "brief.json").read_text())["pedido"]).is_file()


def test_cli_entregar_com_concluir_e_estado(tmp_path, execucao, capsys):
    proc = tmp_path / "_processados"
    assert main(["entregar", str(execucao), "--modo", "dark", "--aprovado",
                 "--concluir", "--sem-final", "--processados", str(proc)]) == 0
    assert "pedido arquivado" in capsys.readouterr().out
    assert main(["estado", str(execucao), "--brand", str(FIXT)]) == 0
    out = capsys.readouterr().out
    assert "etapa: concluido" in out and "aviso:" not in out


def test_estado_avisa_marca_que_mudou(execucao, capsys):
    """Auditoria M5: 4 de 5 execuções entregues rodaram na marca anterior à v4.0."""
    snap = json.loads((execucao / "brand_snapshot.json").read_text())
    (execucao / "brand_snapshot.json").write_text(json.dumps({**snap, "fingerprint": "antigo"}))
    assert main(["estado", str(execucao), "--brand", str(FIXT)]) == 0
    assert "Não reuse os prompts de final/" in capsys.readouterr().out
