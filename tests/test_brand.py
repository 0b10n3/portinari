import json
import shutil
import subprocess
from pathlib import Path

import pytest

from portinari import brand
from portinari.cli import main

FIXT = Path(__file__).parent / "fixtures" / "brand"
TOKENS = "tokens/syntaxis.tokens.json"
BLOCO = "ILUSTRACOES/_bloco-marca.md"


@pytest.fixture
def copia(tmp_path):
    d = tmp_path / "brand"
    shutil.copytree(FIXT, d)
    return d


def _editar_tokens(d: Path, fn):
    p = d / TOKENS
    t = json.loads(p.read_text())
    fn(t)
    p.write_text(json.dumps(t))


def test_snapshot_da_fixture():
    s = brand.resolver(FIXT, verificar_git=False)
    assert (s["versao_tokens"], s["versao_design"]) == ("2.7.0", "3.1")
    assert [c["hex"] for c in s["paletas"]["dark"]["camadas"]] == ["#141414", "#0F3D27", "#125233", "#1B6A45"]
    assert [c["hex"] for c in s["paletas"]["light"]["camadas"]] == ["#E2E8F0", "#E6F4EE", "#F7F7F5"]
    assert s["paletas"]["dark"]["acento"]["hex"] == "#CDF163"
    assert s["paletas"]["light"]["acento"]["hex"] == "#5F7D1C"  # lime.700 sobre pilha clara
    assert s["tetos"]["max_cores"] == 7 and s["vinculante"] == ["paleta"]
    assert s["avisos"] == [] and s["git"] is None
    assert "drop shadow" in s["descritores_proibidos"]


def test_bloco_so_com_a_pilha_do_modo():
    s = brand.resolver(FIXT, verificar_git=False)
    dark, light = s["bloco"]["dark"], s["bloco"]["light"]
    assert "#0F3D27" in dark and "#E2E8F0" not in dark and "#5F7D1C" not in dark
    assert "#E2E8F0" in light and "#0F3D27" not in light and "#5F7D1C" in light
    assert "Borda e retícula" in dark and "Escala pequena" in dark and "Sem texto renderizado" in dark
    assert "scanner" not in dark and "A escada" not in dark  # parte anti-sombra: o pedido vence
    assert "Descritores proibidos" not in dark  # só lint
    # S2: a tabela com nomes de token virou legenda de amostras dentro da imagem
    for bloco in (dark, light):
        assert "illustration." not in bloco and "color." not in bloco and "|" not in bloco


def test_texto_exigido_dropa_regra_sem_texto():
    s = brand.resolver(FIXT, verificar_git=False, texto=True)
    assert "Sem texto renderizado" not in s["bloco"]["dark"]


def test_marca_lida_em_runtime_alterar_token_muda_o_bloco(copia):
    antes = brand.resolver(copia, verificar_git=False)
    _editar_tokens(copia, lambda t: t["color"]["neutral"]["deepForest"].update({"$value": "#0A5A30"}))
    depois = brand.resolver(copia, verificar_git=False)
    assert "#0F3D27" in antes["bloco"]["dark"]
    assert "#0A5A30" in depois["bloco"]["dark"] and "#0F3D27" not in depois["bloco"]["dark"]
    assert depois["paletas"]["dark"]["camadas"][1]["hex"] == "#0A5A30"
    assert depois["fingerprint"] != antes["fingerprint"]
    # o .md do bloco não foi atualizado: a deriva aparece como aviso, e os tokens vencem
    assert any("#0F3D27" in a and "tokens não têm" in a for a in depois["avisos"])


def test_teto_numerico_vem_dos_tokens(copia):
    _editar_tokens(copia, lambda t: t["illustration"]["accentMaxCoverage"].update({"$value": 0.02}))
    assert "até 2%" in brand.resolver(copia, verificar_git=False)["bloco"]["dark"]


def test_fingerprint_estavel_e_sensivel_ao_bloco(copia):
    a = brand.resolver(copia, verificar_git=False)["fingerprint"]
    assert a == brand.resolver(copia, verificar_git=False)["fingerprint"]
    (copia / BLOCO).write_text((copia / BLOCO).read_text() + "\nnota\n")
    assert brand.resolver(copia, verificar_git=False)["fingerprint"] != a


def test_falhas_altas(copia):
    (copia / BLOCO).write_text((copia / BLOCO).read_text().replace("## Borda e retícula", "## Outra coisa"))
    with pytest.raises(brand.BrandError, match="borda e reticula"):
        brand.resolver(copia, verificar_git=False)
    (copia / "DESIGN.md").unlink()
    with pytest.raises(brand.BrandError, match="ausente"):
        brand.resolver(copia, verificar_git=False)


def test_alias_inexistente(copia):
    _editar_tokens(copia, lambda t: t["illustration"]["accent"].update({"$value": "{color.lime.999}"}))
    with pytest.raises(brand.BrandError, match="lime.999"):
        brand.resolver(copia, verificar_git=False)


def test_lint_descritores_palavra_inteira():
    p = ["drop shadow", "text", "3D", "blur"]
    assert brand.lint_descritores("A soft Drop Shadow and 3D look, no context", p) == ["drop shadow", "3D"]
    assert brand.lint_descritores("contexto de texto e blurry", p) == []


# --- git de brand/ ----------------------------------------------------------------------------
def _git(cwd, *a):
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    import os

    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, env={**os.environ, **env})


def test_git_sem_repositorio(tmp_path):
    assert "não está num repositório" in brand.git_status(tmp_path)["avisos"][0]


def test_git_sem_remoto_e_alteracao_local(tmp_path):
    (tmp_path / "brand").mkdir()
    _git(tmp_path, "init", "-q")
    (tmp_path / "brand" / "a.md").write_text("1")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "x")
    (tmp_path / "brand" / "a.md").write_text("2")
    g = brand.git_status(tmp_path / "brand")
    assert g["remotos"] == [] and g["atras"] is None and len(g["alteracoes_locais"]) == 1
    assert any("sem remoto" in a for a in g["avisos"]) and any("não commitada" in a for a in g["avisos"])


def test_git_atras_do_remoto_nao_faz_pull(tmp_path):
    _git(tmp_path, "init", "-q", "--bare", "remoto.git")
    _git(tmp_path, "clone", "-q", "remoto.git", "a")
    (tmp_path / "a" / "brand").mkdir()
    (tmp_path / "a" / "brand" / "x.md").write_text("1")
    _git(tmp_path / "a", "add", "-A")
    _git(tmp_path / "a", "commit", "-qm", "1")
    _git(tmp_path / "a", "push", "-q", "origin", "HEAD")
    _git(tmp_path, "clone", "-q", "remoto.git", "b")  # clone já configura o upstream
    (tmp_path / "a" / "brand" / "x.md").write_text("2")
    _git(tmp_path / "a", "commit", "-qam", "2")
    _git(tmp_path / "a", "push", "-q", "origin", "HEAD")
    g = brand.git_status(tmp_path / "b" / "brand")
    assert g["atras"] == 1
    assert (tmp_path / "b" / "brand" / "x.md").read_text() == "1"  # não atualizou sozinho


# --- marca real e CLI ---------------------------------------------------------------------------
@pytest.mark.skipif(not (brand.BRAND / TOKENS).is_file(), reason="monorepo Syntaxis ausente")
def test_marca_real_sem_deriva():
    s = brand.resolver(verificar_git=False)
    assert s["avisos"] == [] and set(s["bloco"]) == {"dark", "light"}


def test_cli_marca(tmp_path, capsys):
    assert main(["marca", str(tmp_path), "--brand", str(FIXT), "--sem-fetch"]) == 0
    assert json.loads((tmp_path / "brand_snapshot.json").read_text())["versao_tokens"] == "2.7.0"
    assert "fingerprint" in capsys.readouterr().out
