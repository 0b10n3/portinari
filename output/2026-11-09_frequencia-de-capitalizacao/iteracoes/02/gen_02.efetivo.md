A flat papercut elevation, seen straight on, of a paper staircase that squashes flat as it climbs and ends as a thin ledge just beneath a ceiling it never touches.

The collage fills the whole image edge to edge. The night sky sheet, the darkest sheet, reaches all four edges of the picture. Across the top runs a flat ceiling band, from the left edge to the right edge, its lower edge cut perfectly straight; it is the stack sheet immediately above the sky, one step lighter.

The left half holds five shrinking steps of equal width, cut square with right-angled corners. They are not steps of equal height: the staircase looks like it is being squashed flat as it climbs. The first riser is huge, a tall block that takes up more than half the height of the whole staircase. The second riser is half as tall as the first. The third is half as tall as the second. The fourth is low, a short ledge. The fifth is only a sliver, barely thicker than a strip of paper. Each step is clearly flatter than the one below it, so the outline of the stairs bends from steep to almost level. The first step and the figure stand on one straight base line in the lower part of the picture, comfortably above the bottom edge.

The fifth sliver flows straight into a single flat plateau sheet at exactly the same level, with no jump and no step up: one thin continuous strip, about as thick as the fourth riser, that runs level from the top of the stairs to the right edge. Sliver and plateau sit almost against the ceiling, held off only by a thin constant gap under the ceiling, a straight line of sky that stays the same from the knee to the right edge. Staircase and plateau are one continuous shape cut from the primary figure tone, the lightest and most saturated figure tone, standing out strongly against the sky. Every strip sits directly on the sky, which shows right up to its lower edge.

The focal point is the knee, slightly right of centre, where the stairs turn into the plateau. Directly above it, one short rectangular accent tab is glued onto the face of the ceiling band, its bottom edge flush with the ceiling's lower edge, so the line of sky beneath it stays open. It is the only accent in the piece.

Two or three thin horizontal slits run through the plateau, each a straight-sided rectangle with square ends, spaced closer together near the knee, showing the sky. Well inside the left margin, more than a tenth of the width from the left edge, one small faceless figure with a faceted hexagonal head and a flat trapezoid body stands with both feet whole on the base line, just in front of the first riser, head tilted up toward the accent. Four small diamond-cut stars, each a straight-sided diamond, sit in the sky above the first steps, away from the knee. Figure and stars share the secondary figure tone. The lower right area under the plateau stays empty. Only the sky sheet carries a faint paper fibre grain; every other shape is clean flat paper. Every surface is blank, with no writing, digits or marks.

# Bloco de marca Syntaxis — modo dark (pilha escura)

## Paleta — pilha escura (a única desta peça)

Pinte só com estes hex, um por folha de papel (âncora absoluta: nunca compare uma folha com outra,
nunca aproxime uma cor). Nunca misture a pilha escura com a clara. Não desenhe amostras de cor,
legendas, códigos hex nem nenhum texto na imagem: os hex abaixo são instrução, não conteúdo.

- Folhas da pilha escura: nível 1 #141414 (a mais escura), nível 2 #0F3D27, nível 3 #125233, nível 4 #1B6A45 (a mais clara).
- Figura, sobre a pilha (nunca empilha): #2D9E67 e #78C9A4.
- Acento único, só na virada/conquista/ação: #CDF163.

## Tetos numéricos

- Matizes de pilha por peça: 1, mais um neutro estrutural.
- Cores ≥1% do quadro: no máximo 7.
- Fundo mínimo do quadro: 40%.
- Acento do quadro: até 1%.
- Granulação (só no fundo), amplitude de luminância: abaixo de 0.028.

## A escada — como escrever profundidade sem sombra
Duas camadas adjacentes da pilha diferem por **um degrau de luminância pequeno e regular**,
nunca por sombra projetada. Medido nos tokens (`revisao-2026-r5/lab/src/dados/medidas-fase2.json`):
pilha escura 0,029 · 0,028 · 0,046; pilha clara 0,075 · 0,052. O menor degrau, 0,028, é também
o teto da granulação.

**Âncora absoluta, nunca comparação relativa.** "Cada folha claramente mais clara que a
anterior" faz o gerador inflar o intervalo e sair da paleta. Cite o hex de cada folha, mais um
adjetivo de família ("verdes escuros e profundos, não médios nem claros").

**Luz de scanner de mesa, idêntica em todo o quadro** — a alavanca mais forte contra sombra
projetada. Cada folha é "uma cor perfeitamente uniforme de borda a borda, o mesmo tom no meio e
na margem".

**A parede do recorte é uma segunda fonte de rampa**, distinta da sombra entre camadas. Ataque
com frase própria: "inside an opening you see nothing but the flat surface of the layer below —
no visible paper thickness, no wall, no bevel, no darkening at the rim."

Frase obrigatória no prompt (inglês, para o gerador):

> Lit like a flatbed scan: identical, shadowless light over the whole frame. Every sheet is one
> perfectly uniform opaque color from edge to edge. Depth comes only from the next sheet being a
> different flat tone — never from a shadow, a glow, a gradient, a darker rim or a visible paper
> edge.

## Frame
- **Ilustração dentro de página** (Substack, e-mail, livro): frame retangular, radius 0,
  hairline 1 px; nada sangra para fora.
- **Ilustração em quadro social inteiro** (capa de carrossel, capa de Reels): a borda da peça é
  o frame. Texto nunca entra sobre a colagem — vai numa faixa sólida de token (Deep Forest ou
  Ink na pilha escura, Chalk na clara). Componha deixando livre a área da faixa, que o pedido
  informa (ex.: "o terço inferior é fundo vazio").
- Medidas, área segura e recorte do grid por formato: `brand/ILUSTRACOES/FORMATOS.md` (e
  `brand/SOCIAL.md` para peça social, a partir da v4.0).

## Borda e retícula
- Corte a faca: **reto ou a 45°**, nunca curva livre.
- Objeto de forma naturalmente curva (roda, cabeça, mão, moeda, sol) se recorta como polígono, e
  a parte criativa **nomeia o polígono** ("octagonal wheels", "a faceted hexagonal head"). Um
  "no curves" genérico não basta: o gerador o ignorou nas três gerações de teste (rodas redondas
  em G1 e G2, cabeça redonda em G3). A única curva da marca é o quarto de arco do símbolo.
- Vista frontal, chapada, como elevação de arquitetura: nenhuma perspectiva, nenhuma porta ou
  folha entreaberta. Folha girada em profundidade mostra a espessura do papel, que é a parede
  de recorte por outra porta (G2).
- Rasgo: vocabulário base em capa editorial; nas demais taxonomias, um por peça, na ruptura.
- Retícula de meio-tom: até duas escalas de ponto na mesma peça, só quando codificam ordem de
  camada (ponto maior = camada mais próxima, por exemplo) — nunca como textura decorativa sem
  função.
- Offset de registro tipo risograph: 2–4 px, cor chapada, sem gradiente.

## Escala pequena
Abaixo de 96 px não existe ilustração — existe símbolo. Não gere ilustração para favicon,
avatar ou ícone pequeno; use `brand/LOGO/`. Thumbnail de YouTube e capa de Reels vista no grid:
no máximo três camadas visíveis.

## Sem texto renderizado
Nenhuma imagem gerada carrega texto. Geradores erram tipografia; a marca tem tipografia
própria (`DESIGN.md` §4.2). Quem carrega a informação verbal é o alt-text e, na peça social, a
faixa sólida composta por cima no template.

Flat cut-paper sheets, each sheet one perfectly uniform solid color from edge to edge, the same
tone in the middle and at the margin. Straight edges and 45-degree cuts only. No texture on any
sheet. Lit like a flatbed-scanner image, identical light across the whole frame.

## Technical
Render at 2560x1440, or the largest size the generator supports; keep every edge crisp.