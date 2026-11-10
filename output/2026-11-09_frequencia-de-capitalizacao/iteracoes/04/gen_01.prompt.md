This is the light version of the same picture: same layout, same elements, same positions, same single accent point; only the tones change to the light stack, which has just three sheets. If a reference image of this scene is supplied, keep its composition, silhouettes and placement exactly and change only the tones as described here.

A flat papercut elevation, seen straight on, of a zigzag stair narrowing like a funnel: wide at the bottom, narrow at the top, each flight clearly shorter than the one below it, the last one a tiny stub that stops just beneath a ceiling it never touches.

The collage fills the whole image edge to edge. The sky sheet is the lightest sheet of the stack and reaches all four edges of the picture as one even sheet, a single flat tone from top to bottom. Across the top runs a flat ceiling band from the left edge to the right edge, its lower edge cut perfectly straight; it is the darkest sheet of the light stack, two steps darker than the sky, so the limit reads clearly.

The staircase stands in the middle of the picture, in a central column, with wide empty sky on both sides. It has only four flights. Each flight is a separate strip of paper with a straight lower edge and a sawtooth step profile along its upper edge, all corners square. The first flight is long and climbs to the right across almost the whole central column. The second starts where the first ends and climbs back to the left, about half as long. The third climbs to the right again, about half as long as the second. The fourth is a stub of one or two steps, sitting on the vertical centre line of the picture. The steps may all be the same size; it is the flights that get shorter, so the outline tapers like a funnel. Between one flight and the next run thin sky gaps between flights, each a straight hairline of sky, the same thickness at every turn. The whole stair is cut from the primary figure tone, the deeper and more saturated figure tone, standing out strongly against the sky.

The focal point is the top of the stub, on the centre line, just under the ceiling. It rises almost against the ceiling, held off only by a paper-thin gap beneath the ceiling: the same hairline of sky as between the flights, no wider. Directly above the stub lies a single flat accent bar inside the ceiling, a short rectangle much wider than it is tall, wholly within the ceiling band. Its bottom edge sits exactly on the ceiling's lower edge, the two cut along one straight line, so the bar touches the bottom of the ceiling and the hairline of sky beneath it stays open. It is the only accent in the piece.

There is no floor and no ground strip. The first flight and the figure rest directly on the sky sheet, in the lower part of the picture, comfortably above the bottom edge. At the foot of the first flight, on its left side, stands one small faceless figure with a faceted hexagonal head and a flat trapezoid body. The head is visibly tilted back and up, its top leaning toward the stair, as if gazing up at the stub; well inside the left margin and closer to the stair than to the left edge. Four diamond-cut stars, each a small straight-sided diamond, sit in the empty sky, two to the left of the stair and two to the right, far from the stub. Figure and stars share the secondary figure tone, the paler one. Only the sky sheet carries a faint paper fibre grain; every other shape is clean flat paper. Every surface is blank, with no digits, no letters, no letter e, no symbols and no marks.

# Bloco de marca Syntaxis — modo light (pilha clara)

## Paleta — pilha clara (a única desta peça)

Pinte só com estes hex, um por folha de papel (âncora absoluta: nunca compare uma folha com outra,
nunca aproxime uma cor). Nunca misture a pilha escura com a clara. Não desenhe amostras de cor,
legendas, códigos hex nem nenhum texto na imagem: os hex abaixo são instrução, não conteúdo.

- Folhas da pilha clara: nível 1 #E2E8F0 (a mais escura), nível 2 #E6F4EE, nível 3 #F7F7F5 (a mais clara).
- Figura, sobre a pilha (nunca empilha): #2D9E67 e #78C9A4.
- Acento único, só na virada/conquista/ação: #5F7D1C.

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
