A flat papercut elevation, seen straight on: a flat octagonal paper token floats motionless in an empty sky at the very top of its toss, and in the floor directly beneath it, three octagonal holes cut side by side, two small and one large, mark the exact place where it is about to land.

The flat sky sheet is the darkest sheet of the stack and reaches all four edges of the picture, behind everything. Over its lower part lies the flat floor band, a second sheet running from the left edge to the right edge and covering a little more than the lower third of the picture's height, its top edge cut perfectly straight and horizontal. The floor is seen straight on, exactly like the sky, as an upright stripe cut from the lightest sheet of the stack. The sky fills the upper part of the picture, calm and open.

In the upper third, a little right of the vertical centre line, about three fifths of the way across, floats the token, about one seventh of the picture's width. It is a regular octagon with a flat top: horizontal top and bottom sides, vertical left and right sides, and four diagonal sides at 45 degrees. It faces the viewer squarely, upright and untilted, flat as an architectural elevation, so only its front face shows, and it touches nothing. Its rim is a ring of eight trapezoid pieces, cut one by one and butted together along thin straight seams that run from each inner corner to the matching outer corner, all eight in the paler figure tone, the same flat tone in every piece. Inside the ring sits a smaller concentric octagon, about three fifths of the token's width, with the same flat-top orientation, cut from the deeper figure tone and laid on top like a second flat sheet. Both octagons are plain, unprinted paper.

One trapezoid of the ring, the one on the upper-right diagonal side, between the top side and the right side, is cut from the accent tone: a single accent trapezoid, its outer edge meeting the empty sky. It is the only accent in the whole picture; the other seven trapezoids, the inner octagon and every other shape keep their own tones. This trapezoid, at the top of the toss, is the focal point.

Directly below the token, on the same vertical axis, a large octagonal cut-out goes straight through the floor band, about nine tenths of the token's width, with the same flat-top orientation, sitting in the middle of the floor band's height with plain floor above and below it. To its left, on the same horizontal centre line, lie two small octagonal cut-outs, each one third the width of the large one, with the same orientation. Read from left to right, the order is small, small, large. Between them run two narrow bridges of floor paper, equal and straight, each about half as wide as a small opening, so the three octagons stay separate and whole. Each opening is a clean hole through the floor sheet: inside it lies only the flat sky sheet behind, the same tone as the sky above, meeting the floor at a crisp cut line. Together the three empty openings add up to the token.

In the lower left corner, a faceted paper hand enters from the left edge of the picture, its wrist cut off by that edge. It is a single flat silhouette in the deeper figure tone, its outline built entirely from short straight cuts, and it lies over the floor band. The fist is turned on its side and lies horizontally, knuckles pointing right toward the token, the four fingers closed into one solid block. The thumb sticks out of the top of the fist as a straight, narrow wedge on a 45-degree diagonal, up and to the right, toward the token, its tip rising a little above the top edge of the floor band and staying far to the left of the small openings. It is the pose of a hand that has just flicked the token into the air.

Between the thumb and the token there is only open sky, and to the right of the token and of the large opening, sky and floor are empty and calm. The sky holds only the token and the tip of the thumb. Everything important sits well inside the picture: the token stays comfortably below the top edge, and the openings stay comfortably above the bottom edge. Only the sky sheet and the floor band carry a faint paper fibre grain; the token, its accent trapezoid and the hand are clean, smooth paper.

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

Fine paper-fiber grain on the background sheet only, very low contrast, barely visible.
Where a halftone dot screen appears, use at most two dot sizes, the larger dots on the layer
nearest the viewer. Figure and accent sheets are perfectly clean and uniform.

One impossible juxtaposition of two ordinary objects at mismatched scale, built from cut-paper
sheets, with a single clear focal point and a large calm background. Symbolic and quiet, not
comic.

## Technical
Render at 2560x1440, or the largest size the generator supports; keep every edge crisp.
Final delivery is 1456x816, taken from this image by centre crop and downscale: keep the focal point and everything that must survive well inside the frame.