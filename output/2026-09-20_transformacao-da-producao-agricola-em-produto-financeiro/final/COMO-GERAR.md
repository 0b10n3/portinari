# Como gerar — Transformação da Produção Agricola em Produto Financeiro

O Portinari entrega o **prompt**; a peça final é gerada por você. A imagem em `validacao/` é a prova de que o prompt funciona (gerada pelo modelo flash, ~1K): ela **não** é a entrega.

## Onde colar

- **Modelo:** Nano Banana Pro (`gemini-3-pro-image`) — é o único que gera 2K/4K nativos.
- **Prompt:** `dark` (um arquivo por modo; use um de cada vez).

## Tamanho e formato

- **Gere em 2560×1440** (ou o maior que o gerador permitir).
- **Entregue em 1456×816** (16:9), por corte central e redução do que foi gerado — nunca gerando de novo num tamanho diferente.
- **Formato:** JPEG ou PNG, até 2 MB. JPEG a 90–92 com croma 4:4:4 (com 4:2:0 a borda reta e o acento ganham franja). sRGB.

## Área segura

- O ponto focal e tudo que precisa sobreviver ficam dentro de **78,75% × 93,06%** do quadro, centralizados (Universal (16:9 ∩ 14:10 ∩ 1,91:1)).
- O fundo é o que sangra para as bordas.

## O que conferir na imagem que voltar

- Nenhum texto, número, legenda, logo ou código desenhado na imagem.
- Só os hex listados no prompt; nenhuma cor fora deles.
- O acento aparece em **um** ponto só (a virada), não espalhado.
- O fundo ocupa a maior parte do quadro.
- Nenhuma sombra projetada nova que o prompt não tenha pedido.

Se algo estiver errado: `uv run portinari importar <execução> --iteracao N <imagem>` traz a peça de volta para as checagens do pipeline.

## Marca desta entrega

- tokens v2.7.0 · DESIGN v3.1 · fingerprint `723434af59c5`.
