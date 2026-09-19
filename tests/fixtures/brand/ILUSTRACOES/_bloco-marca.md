# Bloco de marca — injetável em prompt de geração

Cole este bloco inteiro em qualquer prompt de ilustração da Syntaxis. Escopo:
**`pipelines/hemingway` apenas — nunca app, nunca site.**

## Paleta (alias de token — nunca hex solto)

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
| Acento — virada, conquista, ação | `illustration.accent` | `#CDF163` (Lime 500), ou `#5F7D1C` (Lime 700) se o fundo for a pilha clara |

## A escada — como escrever profundidade sem sombra

Duas camadas adjacentes da pilha diferem por **um degrau de luminância pequeno e regular**
(0,017–0,046 nos tokens acima), nunca por sombra projetada. Isto é o que faz a peça ler como
papel empilhado.

**Lição cara de rodada anterior, vale para todo prompt:** linguagem **comparativa** ("cada
folha claramente mais clara que a anterior") faz o gerador inflar o intervalo e sair da paleta.
Use **âncora absoluta**: hex repetido por folha, mais adjetivo de família ("verdes escuros e
profundos, não médios nem claros"), nunca comparação relativa entre folhas.

**Descreva a cena como imagem de scanner de mesa, luz idêntica em todo o quadro** — é a
alavanca mais forte contra sombra projetada. Cada folha é "uma cor perfeitamente uniforme de
borda a borda, o mesmo tom no meio e na margem".

**A parede do recorte é uma segunda fonte de rampa, distinta da sombra entre camadas** — a
espessura do papel na borda de uma abertura, sombreada. Ataque com frase própria: "inside an
opening you see nothing but the flat surface of the layer below — no visible paper thickness,
no wall, no bevel, no darkening at the rim."

## Tetos numéricos (verificáveis, não de gosto)

| Regra | Valor | Token |
| --- | --- | --- |
| Matizes de pilha por peça | 1, mais um neutro estrutural | `illustration.maxHues` |
| Cores ≥1% do quadro | entre 3 e 7 | `illustration.maxColors` |
| Fundo mínimo do quadro | 40% | `illustration.minBackground` |
| Acento (Lime) do quadro | até 1% | medido em referência aprovada: 0,35% |
| Granulação, amplitude de luminância | abaixo de 0,028 (um degrau da escada) | — |

## Borda e retícula

- Corte a faca: **reto ou a 45°**, nunca curva livre.
- Rasgo: vocabulário base em capa editorial; nas demais taxonomias, um por peça, na ruptura.
- Retícula de meio-tom: até duas escalas de ponto na mesma peça, só quando codificam ordem de
  camada (ponto maior = camada mais próxima, por exemplo) — nunca como textura decorativa sem
  função.
- Offset de registro tipo risograph: 2–4px, cor chapada, sem gradiente.

## Escala pequena

Abaixo de 96px não existe ilustração — existe símbolo. Não gere ilustração para favicon,
avatar ou ícone pequeno; use `brand/LOGO/`. Thumbnail de YouTube: no máximo três camadas
visíveis.

## Descritores proibidos

`drop shadow`, `soft shadow`, `blur`, `glow`, `rounded corners`, `organic curve`, `gradient`,
`3D`, `bevel`, `emboss`, `handwritten`, `sketchy`, `text`, `lettering`, `typography`,
`caricature`, `satirical`.

## Sem texto renderizado

Nenhuma imagem gerada carrega texto. Geradores erram tipografia; a marca tem tipografia
própria (§4.2 do `DESIGN.md`). Quem carrega a informação verbal é o alt-text.
