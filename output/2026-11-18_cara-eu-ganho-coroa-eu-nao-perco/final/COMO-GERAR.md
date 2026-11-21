# Como gerar — Cara, eu ganho. Coroa, eu não perco.

O Portinari entrega o **prompt**; a peça final é gerada por você. A imagem em `validacao/` é a prova de que o prompt funciona (gerada pelo modelo flash, ~1K): ela **não** é a entrega.

## Onde colar

- **Modelo:** Nano Banana Pro (`gemini-3-pro-image`) — é o único que gera 2K/4K nativos.
- **Prompt:** `dark`, `light` (um arquivo por modo; use um de cada vez).
- **light:** gere o dark primeiro. Depois anexe a peça dark final como imagem de referência e cole `prompt_light.md`: ele foi validado como edição dela, e é assim que o par sai com a mesma composição.

## Tamanho e formato

- **No gerador: proporção 16:9, resolução 2K** (sai 2752×1536). O Pro recebe proporção e 1K/2K/4K, não pixels.
- **Entregue em 1456×816** (16:9), por corte central e redução do que foi gerado (`portinari derivar`) — nunca gerando de novo num tamanho diferente.
- **Formato:** JPEG ou PNG, até 2 MB. JPEG a 90–92 com croma 4:4:4 (com 4:2:0 a borda reta e o acento ganham franja). sRGB.

## Área segura

- O ponto focal e tudo que precisa sobreviver ficam dentro de **78,75% × 93,06%** do quadro, centralizados (Universal (16:9 ∩ 14:10 ∩ 1,91:1)).
- O fundo é o que sangra para as bordas.

## O que conferir na imagem que voltar

- Nenhum texto, número, legenda, logo ou código desenhado na imagem.
- Só os hex listados no prompt; nenhuma cor fora deles.
- O acento aparece em **um** ponto só (a virada), não espalhado.
- O fundo ocupa a maior parte do quadro.
- Nenhuma sombra, brilho, gradiente, parede de recorte escurecida ou curva livre.

## Depois de gerar — o pedido só fecha com isto

1. `uv run portinari importar <execução> --iteracao N <peça> --modelo nano-banana-pro` (N = uma iteração nova, uma por modo).
2. `uv run portinari checar <execução> --iteracao N --modo <modo>`; no segundo modo, `--par <peça do primeiro>`. Tem de sair sem `ERRO`.
3. `uv run portinari derivar <execução> <peça> --modo <modo>` → o arquivo do tamanho exato.
4. `uv run portinari entregar <execução> --modo <modo> --aprovado --concluir`.

## Alt-text (o mesmo para as duas variantes)

> Colagem de papel: as duas faces da mesma moeda octogonal; a cara, um perfil facetado, leva louros, e a coroa fica intacta.

Cole no campo de texto alternativo da plataforma. A imagem não carrega texto: quem carrega a informação verbal é o alt.

## Marca desta entrega

- tokens v3.1.0 · DESIGN v4.1 · fingerprint `c13b4ab7b310`.
