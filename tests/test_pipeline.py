"""E7 — ensaio a seco do pipeline inteiro (sem agy real) e conferência dos agentes e da skill."""

import json
import re
import sys
from pathlib import Path

import pytest

from portinari.cli import main

AQUI = Path(__file__).parent
RAIZ = AQUI.parent
FIXT = AQUI / "fixtures" / "brand"
AGENTES = RAIZ / ".claude" / "agents"
SKILL = RAIZ / ".claude" / "skills" / "portinari" / "SKILL.md"
RUBRICA = RAIZ / "rubrica" / "rubrica.md"
PEDIDO = (
    "# TITLE: Transformação do café em LCA\n"
    "**USO**: capa de post para substack\n"
    "**DESCRIPTION**: a lavoura de café à esquerda vira um título financeiro à direita\n"
    "**STYLE**: grain-textured + nostalgic\n"
)
CRIATIVO = (
    "Cut-paper collage: a terraced coffee slope on the left folds into a certificate on the right.\n"
    "Two faceless harvesters work the rows. The focal point sits at the fold, slightly right of centre.\n"
)


def _frontmatter(p: Path) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), re.S)
    assert m, f"{p.name} não tem frontmatter"
    return dict(
        (k.strip(), v.strip())
        for k, _, v in (l.partition(":") for l in m.group(1).splitlines() if ":" in l and not l.startswith(" "))
    )


# --- agentes, rubrica e skill --------------------------------------------------------------------
@pytest.mark.parametrize(
    "nome", ["diretor-de-arte", "critico-conceito", "enriquecedor-de-cena", "prompter-tecnico", "critico-visual"]
)
def test_agente_existe_e_se_declara(nome):
    f = _frontmatter(AGENTES / f"{nome}.md")
    assert f["name"] == nome and len(f["description"]) > 60 and "tools" in f


def test_critico_visual_nao_pode_escrever_nem_rodar_nada():
    """D7: o crítico só lê. É o único olho independente do pipeline."""
    corpo = (AGENTES / "critico-visual.md").read_text(encoding="utf-8")
    assert _frontmatter(AGENTES / "critico-visual.md")["tools"] == "Read"
    assert "não lê nenhum arquivo de prompt" in corpo and "prompt_final.md" in corpo


def test_rubrica_tem_bloqueantes_e_regua():
    r = RUBRICA.read_text(encoding="utf-8")
    assert all(b in r for b in ("B1", "B2", "B3", "B4", "B5", "B6", "B7"))
    assert "nunca aprova sozinho" in r and "APROVADO** exige" in r


def test_skill_nao_e_invocavel_pelo_modelo_e_cobre_os_dois_gates():
    s = SKILL.read_text(encoding="utf-8")
    assert _frontmatter(SKILL)["disable-model-invocation"] == "true"
    assert "GATE 1" in s and "GATE 2" in s and "AskUserQuestion" in s
    assert "Três voltas por etapa" in s and "--aprovado" in s


def test_skill_so_cita_subcomando_que_existe():
    subcomandos = set(re.findall(r"uv run portinari (\w+)", SKILL.read_text(encoding="utf-8")))
    with pytest.raises(SystemExit):
        main(["--help"])
    assert subcomandos <= {"ingest", "marca", "enriquecer", "prompt", "gerar", "checar",
                           "derivar", "importar", "entregar"}


# --- ensaio a seco --------------------------------------------------------------------------------
@pytest.fixture
def agy_falso(tmp_path, monkeypatch):
    monkeypatch.setenv("PORTINARI_AGY", f"{sys.executable} {AQUI / 'fake_agy.py'}")
    monkeypatch.setenv("PORTINARI_AGY_HOME", str(tmp_path / "agyhome"))
    cenario = tmp_path / "cenario.json"
    cenario.write_text('["ok"]')
    monkeypatch.setenv("FAKE_SCENARIO", str(cenario))
    return cenario


def test_pipeline_de_ponta_a_ponta_sem_agy_real(tmp_path, agy_falso, capsys):
    saida = tmp_path / "out"
    pedido = tmp_path / "pedido.md"
    pedido.write_text(PEDIDO, encoding="utf-8")

    assert main(["ingest", str(pedido), "--saida", str(saida), "--brand", str(FIXT)]) == 0
    assert main(["marca", str(saida), "--brand", str(FIXT), "--sem-fetch"]) == 0
    b = json.loads((saida / "brief.json").read_text())
    assert (b["tamanho"], b["master"], b["estilo_base"], b["estilo_modo"]) == ([1456, 816], [2560, 1440],
                                                                              "grain-textured", "nostalgic")

    it = saida / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_criativo.md").write_text(CRIATIVO, encoding="utf-8")  # o prompter-tecnico faria isto
    assert main(["prompt", str(saida), "--iteracao", "1", "--modo", "dark"]) == 0
    final = (it / "prompt_final.md").read_text(encoding="utf-8")
    assert CRIATIVO.strip() in final and "#0F3D27" in final
    assert "Flat cut-paper" not in final and "halftone" in final  # a base é grain-textured
    assert "Render at 2560x1440" in final and "Final delivery is 1456x816" in final

    assert main(["gerar", str(saida), "--iteracao", "1", "--variacoes", "1"]) == 0
    assert main(["checar", str(saida), "--iteracao", "1", "--modo", "dark"]) == 0
    assert main(["entregar", str(saida), "--modo", "dark", "--iteracao", "1", "--aprovado"]) == 0

    entregue = (saida / "final" / "prompt_dark.md").read_text(encoding="utf-8")
    assert CRIATIVO.strip() in entregue and "Transformação do café em LCA" in entregue
    assert (saida / "final" / "COMO-GERAR.md").is_file()
    m = json.loads((saida / "manifest.json").read_text())
    assert m["entregas"]["dark"]["gate2"] == "aprovado" and m["estilo"]["modo"] == "nostalgic"
    assert len((saida / "geracoes.jsonl").read_text().splitlines()) == 1


def test_teto_de_geracoes_para_o_pipeline(tmp_path, agy_falso, capsys):
    saida = tmp_path / "out"
    pedido = tmp_path / "pedido.md"
    pedido.write_text(PEDIDO, encoding="utf-8")
    main(["ingest", str(pedido), "--saida", str(saida), "--brand", str(FIXT)])
    main(["marca", str(saida), "--brand", str(FIXT), "--sem-fetch"])
    it = saida / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_criativo.md").write_text(CRIATIVO, encoding="utf-8")
    main(["prompt", str(saida), "--iteracao", "1", "--modo", "dark"])
    assert main(["gerar", str(saida), "--iteracao", "1", "--variacoes", "1", "--max-geracoes", "1"]) == 0
    assert main(["gerar", str(saida), "--iteracao", "1", "--variacoes", "1", "--max-geracoes", "1"]) == 3
    assert "teto de 1 gerações" in capsys.readouterr().out


def test_prompt_que_perdeu_termo_do_enriquecimento_nao_passa(tmp_path, agy_falso, capsys):
    saida = tmp_path / "out"
    pedido = tmp_path / "pedido.md"
    pedido.write_text(PEDIDO, encoding="utf-8")
    main(["ingest", str(pedido), "--saida", str(saida), "--brand", str(FIXT)])
    main(["marca", str(saida), "--brand", str(FIXT), "--sem-fetch"])
    (saida / "enriquecimento").mkdir()
    (saida / "enriquecimento" / "v01.json").write_bytes(
        (AQUI / "fixtures" / "enriquecimento" / "cafe-lca-v01.json").read_bytes()
    )
    it = saida / "iteracoes" / "01"
    it.mkdir(parents=True)
    (it / "prompt_criativo.md").write_text(CRIATIVO, encoding="utf-8")
    assert main(["prompt", str(saida), "--iteracao", "1", "--modo", "dark"]) == 2
    assert "perdeu" in capsys.readouterr().out
