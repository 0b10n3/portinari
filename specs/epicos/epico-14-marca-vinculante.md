# Épico 14 — Marca vinculante (brand v4.0/v4.1)

**Status:** concluído em 01/11/2026 · origem: rodada 5 da marca (`brand/revisao-2026-r5/04-propagacao.md`, PR 1).

## 1. Objetivo

Aplicar no pipeline a decisão da rodada 5 da marca (Q4 do CHECKPOINT 1, 30/10/2026): tudo o que
`brand/ILUSTRACOES/_bloco-marca.md` declara é **vinculante**. Revoga A2 ("o pedido vence a marca,
exceto a paleta"). Motivo registrado na marca: o bloco injetado não carregava a regra anti-sombra
("A escada" era descartada) e um prompt entregue chegou a pedir sombra de contato.

## 2. Escopo

| Arquivo | Mudança |
| --- | --- |
| `src/portinari/brand.py` | `INJETAR` ganha `a escada` e `frame`; `DESCARTADAS = ()`; seção "Tetos numéricos" sem "(diretrizes; o pedido do autor pode sobrepor)"; snapshot com tudo em `vinculante` e `sobreponivel = []` |
| `src/portinari/cli.py` | descritor proibido na parte criativa **bloqueia** o `prompt` (código 2), inclusive negado |
| `src/portinari/enriquecimento.py` | descritor proibido na cena vira erro V9 |
| `rubrica/rubrica.md` | bloqueantes B8 (sombra/rampa), B9 (curva livre/perspectiva), B10 (tetos) |
| `CLAUDE.md` regra 2, `docs/PLANO.md` A2 | texto novo; A2 fica como registro, com a revogação ao lado |
| `tests/fixtures/brand/ILUSTRACOES/_bloco-marca.md` | atualizado para o bloco vigente da marca |

Fora do escopo: execuções antigas em `output/` (não retroativo — decisão Q15 do CHECKPOINT 2 da marca).

## 3. Critérios de aceite e testes

- O bloco montado contém "A escada" (frase de luz de scanner) e "Frame" nos dois modos.
- `portinari prompt` com descritor proibido na parte criativa sai com 2; sem ele, sai com 0.
- `enriquecimento.validar` devolve erro V9 para descritor proibido na cena.
- `uv run pytest`: verde (156 testes).
- `brand.resolver()` contra o `brand/` real (v4.1, tokens 3.1.0) sem deriva nem aviso.
