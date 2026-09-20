import json
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

from portinari import agy
from portinari.cli import main

AQUI = Path(__file__).parent
PROMPT = "A paper-cut coffee plant on the left, a bond certificate on the right.\n" * 4 + "Palette: #0F3D27 #125233 #CDF163\n"


@pytest.fixture
def fake(tmp_path, monkeypatch):
    home = tmp_path / "agyhome"
    home.mkdir()
    monkeypatch.setenv("PORTINARI_AGY", f"{sys.executable} {AQUI / 'fake_agy.py'}")
    monkeypatch.setenv("PORTINARI_AGY_HOME", str(home))
    monkeypatch.setattr(agy, "HOME", home)

    def cenario(*modos):
        c = tmp_path / "cenario.json"
        c.write_text(json.dumps(modos))
        c.with_suffix(".n").unlink(missing_ok=True)
        monkeypatch.setenv("FAKE_SCENARIO", str(c))
        return c

    return cenario


def gerar(tmp_path, **kw):
    dormidos = []
    kw.setdefault("dormir", dormidos.append)
    g = agy.gerar(PROMPT, "16:9", tmp_path / "run", 1, **kw)
    return g, dormidos


def linhas(tmp_path):
    return [json.loads(l) for l in (tmp_path / "run" / "geracoes.jsonl").read_text().splitlines()]


def test_sucesso_salva_tudo(tmp_path, fake):
    fake("ok")
    g, _ = gerar(tmp_path)
    d = tmp_path / "run" / "iteracoes" / "01"
    assert g.fiel and g.hex_ausentes == [] and (g.largura, g.altura) == (1376, 768)
    assert {p.name for p in d.iterdir()} == {"gen_01.jpg", "gen_01.prompt.md", "gen_01.efetivo.md", "gen_01.json"}
    assert (d / "gen_01.prompt.md").read_text() == PROMPT  # prompt completo, sem cortes
    assert agy._norm((d / "gen_01.efetivo.md").read_text()) == agy._norm(PROMPT)
    meta = json.loads((d / "gen_01.json").read_text())
    assert meta["modelo_orquestrador"] == "gemini-3.8-flash-low" and meta["conversation_id"]
    assert "--output-format" in meta["comando"] and PROMPT.strip() in meta["comando"][meta["comando"].index("-p") + 1]
    assert len(linhas(tmp_path)) == 1
    with Image.open(d / "gen_01.jpg") as im:
        assert im.size == (1376, 768)


def test_prompt_reescrito_sobe_o_modelo_e_recupera(tmp_path, fake):
    fake("rewrite", "ok")
    g, _ = gerar(tmp_path)
    assert g.fiel and g.tentativa == 2 and g.modelo_orquestrador == "gemini-3.8-flash-medium"
    primeira = json.loads((tmp_path / "run/iteracoes/01/gen_01.json").read_text())
    assert not primeira["fiel"] and primeira["hex_ausentes"]  # os hex da 2ª metade sumiram
    assert len(linhas(tmp_path)) == 2
    cmd = json.loads((tmp_path / "run/iteracoes/01/gen_02.json").read_text())["comando"]
    assert "WARNING" in cmd[cmd.index("-p") + 1]  # a retentativa exige literalidade


def test_sempre_reescrito_devolve_a_ultima_infiel(tmp_path, fake):
    fake("rewrite")
    g, _ = gerar(tmp_path)
    assert not g.fiel and g.tentativa == 3 and g.modelo_orquestrador == "gemini-3.8-flash-high"
    assert len(linhas(tmp_path)) == 3


def test_falha_transitoria_retenta_com_backoff(tmp_path, fake):
    fake("transient", "ok")
    g, dormidos = gerar(tmp_path)
    assert g.fiel and g.tentativa == 2 and dormidos == [5]
    assert len(linhas(tmp_path)) == 2


def test_falha_permanente_nao_retenta(tmp_path, fake):
    fake("fatal", "ok")
    with pytest.raises(agy.AgyErro, match="não transitório"):
        gerar(tmp_path)
    assert len(linhas(tmp_path)) == 1


def test_sem_imagem_apesar_do_exit_0(tmp_path, fake):
    fake("noimage")
    with pytest.raises(agy.AgyErro, match="sem imagem"):
        gerar(tmp_path)
    assert len(linhas(tmp_path)) == 3 and not list((tmp_path / "run").rglob("*.jpg"))


def test_timeout_e_transitorio(tmp_path, fake):
    fake("hang", "ok")
    g, dormidos = gerar(tmp_path, timeout=1, folga=0)
    assert g.fiel and g.tentativa == 2 and dormidos == [5]


def test_teto_de_geracoes(tmp_path, fake):
    fake("ok")
    (tmp_path / "run").mkdir()
    (tmp_path / "run" / "geracoes.jsonl").write_text('{"x":1}\n' * 2)
    with pytest.raises(agy.TetoDeGeracoes):
        gerar(tmp_path, max_geracoes=2)


def test_teto_no_meio_devolve_a_imagem_ja_paga(tmp_path, fake):
    fake("rewrite", "ok")
    g, _ = gerar(tmp_path, max_geracoes=1)
    assert not g.fiel and len(linhas(tmp_path)) == 1


def test_referencias_vao_como_imagepaths(tmp_path, fake):
    ref = tmp_path / "ref.png"
    Image.new("RGB", (8, 8)).save(ref)
    c = fake("ok")
    gerar(tmp_path, referencias=[str(ref)])
    args = json.loads(Path(str(c) + ".args").read_text())
    assert f'ImagePaths: ["{ref}"]' in args[args.index("-p") + 1] and str(tmp_path) in args


def test_passos_imagem_formato_real(tmp_path):
    conv = "abc"
    logs = tmp_path / "brain" / conv / ".system_generated" / "logs"
    logs.mkdir(parents=True)
    conteudo = ("Created At: 2026-08-14T13:05:04-03:00\nCompleted At: 2026-08-14T13:05:15-03:00\n"
                "Using prompt: linha 1\n\nlinha 3 com #0F3D27\n\nGenerated image is saved at "
                "/home/x/brain/abc/cdb_1786723515382.jpg.\n\n Do not output the path of this image to show.")
    (logs / "transcript_full.jsonl").write_text(json.dumps({"type": "GENERATE_IMAGE", "status": "DONE", "content": conteudo}))
    assert agy.passos_imagem(conv, tmp_path) == [
        {"prompt": "linha 1\n\nlinha 3 com #0F3D27", "caminho": "/home/x/brain/abc/cdb_1786723515382.jpg"}
    ]
    assert agy.passos_imagem("nao-existe", tmp_path) == []


@pytest.mark.parametrize(
    "tam,esperado",
    [((2560, 1440), "16:9"), ((1200, 627), "16:9"), ((1080, 1080), "1:1"), ((1080, 1920), "9:16"),
     ((900, 1200), "3:4"), ((3000, 1000), "16:9"), ((1000, 1500), "2:3")],
)
def test_melhor_proporcao(tam, esperado):
    assert agy.melhor_proporcao(*tam) == esperado


def test_montar_prompt_injeta_o_bloco_verbatim():
    bloco = "# Bloco\n\n| x | `#0F3D27` |\n"
    p = agy.montar_prompt("Criativo aqui.  ", bloco, (1456, 816), (2560, 1440))
    assert bloco.strip() in p and p.startswith("Criativo aqui.") and "2560x1440" in p


def test_cli_prompt_e_gerar_ponta_a_ponta(tmp_path, fake, capsys):
    fake("ok", "ok")
    run = tmp_path / "exec"
    assert main(["ingest", str(AQUI / "fixtures/pedidos/cafe-lca.md"), "--saida", str(run)]) == 0
    assert main(["marca", str(run), "--brand", str(AQUI / "fixtures/brand"), "--sem-fetch"]) == 0
    it = run / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_criativo.md").write_text("Coffee on the left, a drop shadow, LCA certificate on the right.")
    assert main(["prompt", str(run), "--iteracao", "1", "--modo", "dark"]) == 0
    out = capsys.readouterr().out
    assert "drop shadow" in out  # lint avisa (não bloqueia)
    final = (it / "prompt_final.md").read_text()
    assert "#0F3D27" in final and "#E2E8F0" not in final and "2560x1440" in final
    assert main(["gerar", str(run), "--iteracao", "1", "--variacoes", "2"]) == 0
    assert {p.name for p in it.glob("gen_*.jpg")} == {"gen_01.jpg", "gen_02.jpg"}
    assert (it / "gen_01.prompt.md").read_text() == final
    assert len((run / "geracoes.jsonl").read_text().splitlines()) == 2


def test_cli_gerar_falha_quando_paleta_nao_chega(tmp_path, fake, monkeypatch):
    fake("rewrite")
    run = tmp_path / "exec"
    main(["ingest", str(AQUI / "fixtures/pedidos/cafe-lca.md"), "--saida", str(run)])
    it = run / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_final.md").write_text(PROMPT)
    assert main(["gerar", str(run), "--iteracao", "1", "--variacoes", "1"]) == 4


# --- E5b: importação de imagens geradas à mão -----------------------------------------------------
def test_importar_imagens_manuais(tmp_path):
    a, b = tmp_path / "pro_4k.png", tmp_path / "pro2.JPG"
    Image.new("RGB", (2752, 1536), "#0F3D27").save(a)
    Image.new("RGB", (1024, 1024), "#141414").save(b)
    gs = agy.importar([a, b], PROMPT, tmp_path / "run", 1, modelo="nano-banana-pro")
    d = tmp_path / "run" / "iteracoes" / "01"
    assert [g.nome for g in gs] == ["gen_01", "gen_02"] and (gs[0].largura, gs[0].altura) == (2752, 1536)
    assert gs[0].proporcao == "16:9" and gs[1].proporcao == "1:1" and gs[1].imagem.endswith("gen_02.jpg")
    assert (d / "gen_01.prompt.md").read_text() == PROMPT  # prompt completo, colável
    meta = json.loads((d / "gen_01.json").read_text())
    assert meta["origem"] == "manual" and meta["modelo_imagem"] == "nano-banana-pro" and meta["comando"] == []
    assert [l["origem"] for l in linhas(tmp_path)] == ["manual", "manual"]  # contam como gerações


def test_importar_recusa_nao_imagem_e_respeita_teto(tmp_path):
    ruim = tmp_path / "x.png"
    ruim.write_text("não sou imagem")
    ok = tmp_path / "ok.png"
    Image.new("RGB", (8, 8)).save(ok)
    with pytest.raises(agy.AgyErro, match="não é uma imagem"):
        agy.importar([ok, ruim], PROMPT, tmp_path / "run", 1)
    assert not (tmp_path / "run").exists()  # nada foi gravado
    with pytest.raises(agy.TetoDeGeracoes):
        agy.importar([ok, ok], PROMPT, tmp_path / "run", 1, max_geracoes=1)


def test_cli_importar_usa_o_prompt_final(tmp_path, capsys):
    run = tmp_path / "exec"
    it = run / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_final.md").write_text("prompt colado no Pro")
    img = tmp_path / "pro.png"
    Image.new("RGB", (16, 9)).save(img)
    assert main(["importar", str(run), str(img), "--iteracao", "1", "--modelo", "nano-banana-pro"]) == 0
    assert "manual · nano-banana-pro" in capsys.readouterr().out
    assert (it / "gen_01.prompt.md").read_text() == "prompt colado no Pro"
    assert main(["importar", str(run), str(tmp_path / "nao.png"), "--iteracao", "1"]) == 3
