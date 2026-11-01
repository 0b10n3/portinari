# Bloco de marca — injetável em prompt de geração

Cole este bloco inteiro em qualquer prompt de ilustração da Syntaxis. Quem gera hoje é o
pipeline `pipelines/portinari`, que regera a paleta e os tetos a partir de
`brand/tokens/syntaxis.tokens.json` e injeta o resto daqui.

## Onde a ilustração existe

Capa editorial e retrato de dado do Substack; peça social de Instagram, Facebook e LinkedIn
(capa de carrossel, slide de metáfora, capa de Reels); thumbnail de YouTube; e a capa de
`brand/templates/livro` (exceção nomeada, `DESIGN.md` §7.7); hero, banner e estados de
`apps/skill_test` e de `syntaxis.com.br` (`DESIGN.md` §5.1 — sempre com variante clara e escura).
**Nunca** em slide de dado (gráfico, tabela, bento: são camada de sistema) nem no miolo de
material de curso.

## Governança — tudo neste bloco é regra

Não existe "padrão sobreponível". Paleta, escada, tetos, borda, escala, descritores e
ausência de texto valem para toda peça, e o pedido do autor não os desliga. Um pedido que
precise de uma exceção vira pergunta ao founder e, se aprovado, exceção nomeada no
`DESIGN.md` — nunca uma decisão do pipeline.

| Violação | Efeito |
| --- | --- |
| Cor fora da pilha do modo, figura ou acento | reprova |
| Sombra projetada, sombra de contato, parede de recorte sombreada, desfoque, brilho | reprova |
| Gradiente | reprova |
| Curva livre (fora do quarto de arco) | reprova |
| Texto, número, sigla, logo ou símbolo monetário na imagem | reprova |
| Teto numérico estourado (tabela abaixo) | reprova |

## Paleta (alias de token — nunca hex solto)

Uma pilha por peça: escura **ou** clara, nunca as duas.

| Papel | Token | Hex |
| --- | --- | --- |
| Pilha escura, nível 1 (mais escuro) | `illustration.stack.dark.layer1` | `#141414` (Ink) |
| Pilha escura, nível 2 | `illustration.stack.dark.layer2` | `#0F3D27` (Deep Forest) |
| Pilha escura, nível 3 | `illustration.stack.dark.layer3` | `#125233` (forest.700) |
| Pilha escura, nível 4 (mais claro) | `illustration.stack.dark.layer4` | `#1B6A45` (forest.500) |
| Pilha clara, nível 1 (mais escuro) | `illustration.stack.light.layer1` | `#E2E8F0` (Mist) |
| Pilha clara, nível 2 | `illustration.stack.light.layer2` | `#E6F4EE` (Mint) |
| Pilha clara, nível 3 (mais claro) | `illustration.stack.light.layer3` | `#F7F7F5` (Chalk) |
| Figura, sobre a pilha (nunca empilha) | `illustration.figure.primary` / `.secondary` | `#2D9E67` / `#78C9A4` |
| Acento — virada, conquista, ação | `illustration.accent` | `#CDF163` (Lime 500) na pilha escura; `#5F7D1C` (Lime 700) na pilha clara |

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

## Tetos numéricos

| Regra | Valor | Token |
| --- | --- | --- |
| Matizes de pilha por peça | 1, mais um neutro estrutural | `illustration.maxHues` |
| Cores ≥1% do quadro | entre 3 e 7 | `illustration.maxColors` |
| Fundo mínimo do quadro | 40% | `illustration.minBackground` |
| Acento (Lime) do quadro | até 1% (medido 0,35% na referência aprovada) | `illustration.accentMaxCoverage` |
| Granulação, amplitude de luminância, só no fundo | abaixo de 0,028 | `illustration.grainMaxLuminanceAmplitude` |

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

## Descritores proibidos

`drop shadow`, `soft shadow`, `cast shadow`, `contact shadow`, `blur`, `glow`, `rounded corners`,
`organic curve`, `gradient`, `3D`, `bevel`, `emboss`, `depth of field`, `handwritten`, `sketchy`,
`text`, `lettering`, `typography`, `caricature`, `satirical`.

Lint da parte criativa do prompt: qualquer um destes reprova o prompt antes de gerar — **inclusive negado** ("no glow"), porque o lint procura palavra inteira (em brand.py do Portinari, linhas 179-181; sem crase aqui de propósito: o Portinari lê como descritor todo termo entre crases desta seção). As negações moram neste bloco, que não passa pelo lint; a parte criativa descreve só o que existe na cena.

## Sem texto renderizado

Nenhuma imagem gerada carrega texto. Geradores erram tipografia; a marca tem tipografia
própria (`DESIGN.md` §4.2). Quem carrega a informação verbal é o alt-text e, na peça social, a
faixa sólida composta por cima no template.
