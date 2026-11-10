A flat papercut elevation, seen straight on, of a paper staircase whose steps shrink as they climb until they flatten just beneath a ceiling they never touch.

The picture is built in halves. Across the very top runs a flat ceiling band, edge to edge, its lower edge cut perfectly straight; it is the next stack sheet up from the night sky sheet behind everything. The left half holds the staircase: five shrinking steps of equal width, cut square with right-angled corners. The first step rises half the distance from the base line to the ceiling, and each next step rises half of what remains, so the fifth is only a sliver. The staircase stays compact, contained inside the left half; it never stretches across the frame, and wide empty margins stay clear on both sides of the picture. The right half is a single flat plateau sheet: one narrow horizontal strip that leaves the top of the stairs and runs to the right edge, just under the ceiling. Steps and plateau are one continuous shape in the primary figure tone.

The focal point sits slightly right of centre, at the knee where the stairs turn into the plateau. There the last sliver almost meets the ceiling but is held off by a thin constant gap under the ceiling, a straight line of sky that continues unchanged along the whole plateau. Directly above the knee, attached to the underside of the ceiling, sits one short rectangular accent tab in the accent tone, small but clearly visible, the only accent in the piece.

Two or three thin horizontal slits are cut through the plateau, showing the sky behind, spaced closer together near the knee. At the foot of the first step, well inside the left margin, stands one small faceless figure with a faceted hexagonal head tilted upward and a flat trapezoid body, in the secondary figure tone, looking up at the ceiling. Four small diamond-cut stars in the secondary figure tone dot the sky between the staircase and the ceiling, on the left side, away from the knee. The lower right area under the plateau stays empty as breathing room. Only the sky sheet carries a faint paper fibre grain; every other shape is clean flat paper.

Every surface is blank paper, with no writing anywhere: no digits, no numbers, no letters, no letter e, no mathematical symbols, no percent sign, no marks or labels on the steps or the ceiling.

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