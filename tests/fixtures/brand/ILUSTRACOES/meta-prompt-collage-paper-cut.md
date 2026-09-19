# Meta-prompt de cor — collage / paper cut

Bloco só de **cor, identidade de marca e como usá-las** para o estilo de ilustração
`collage / paper cut` (`DESIGN.md` §7). Cole isto na parte de paleta de qualquer prompt de
geração desse estilo. Fonte: `DESIGN.md` §7.1–§7.2 e `brand/tokens/syntaxis.tokens.json`
(`illustration.*`) — em caso de conflito, os dois vencem sobre este arquivo.

Este arquivo **não** cobre corte/borda, retícula, escala mínima ou os descritores proibidos de
forma/texto — isso é regra de construção, não de cor, e mora em
`brand/ILUSTRACOES/_bloco-marca.md` (o bloco operacional completo, usado pelo pipeline
`pipelines/hemingway`).

## Os três papéis da cor numa peça

Toda cor na peça entra em um destes três papéis — nunca solta, nunca "porque ficou bonita":

| Papel | O que é | Tokens |
| --- | --- | --- |
| **Pilha** | As camadas de papel empilhado que dão profundidade à peça | `illustration.stack.dark.*` ou `illustration.stack.light.*` |
| **Figura** | O que fica *sobre* a pilha — nunca mais um degrau dela | `illustration.figure.primary`, `illustration.figure.secondary` |
| **Acento** | O único ponto de ação, virada ou conquista da peça | `illustration.accent` |

Escolha **uma** das duas pilhas por peça (escura ou clara) — nunca misture as duas na mesma
peça.

## Paleta (token → hex)

| Token | Papel | Hex |
| --- | --- | --- |
| `illustration.stack.dark.layer1` (Ink) | Pilha escura, nível 1 (mais escuro) | `#141414` |
| `illustration.stack.dark.layer2` (Deep Forest) | Pilha escura, nível 2 | `#0F3D27` |
| `illustration.stack.dark.layer3` (forest.700) | Pilha escura, nível 3 | `#125233` |
| `illustration.stack.dark.layer4` (forest.500) | Pilha escura, nível 4 (mais claro) | `#1B6A45` |
| `illustration.stack.light.layer1` (mist) | Pilha clara, nível 1 (mais escuro) | `#E2E8F0` |
| `illustration.stack.light.layer2` (mint) | Pilha clara, nível 2 | `#E6F4EE` |
| `illustration.stack.light.layer3` (Chalk) | Pilha clara, nível 3 (mais claro) | `#F7F7F5` |
| `illustration.figure.primary` (grove.500) | Figura, sobre a pilha | `#2D9E67` |
| `illustration.figure.secondary` (grove.300) | Figura, traço sobre escuro | `#78C9A4` |
| `illustration.accent` (lime.500) | Acento único — ação/conquista/virada | `#CDF163` |
| — (lime.700) | Acento, só se o fundo for a pilha clara | `#5F7D1C` |

Nunca cite hex de memória nem "aproxime" uma cor da marca — sempre o valor exato da tabela
acima, e sempre pelo nome do token no prompt (ex.: "flat Deep Forest background `#0F3D27`"),
nunca só o hex solto.

## Como usar: profundidade é degrau de tom, nunca sombra

A identidade de marca aqui não é só "quais cores" — é **como as cores se relacionam** para
comunicar profundidade sem nunca desenhar uma sombra (`DESIGN.md` §4.5 proíbe sombra
projetada, qualquer forma, mesmo sólida e sem blur). O mecanismo é um **degrau de luminância
pequeno e regular** entre duas camadas adjacentes da pilha:

| Pilha | Sequência de tokens | Degrau de luminância medido |
| --- | --- | --- |
| Escura | Ink → Deep Forest → forest.700 → forest.500 | 0,029 · 0,028 · 0,046 |
| Clara | mist → mint → Chalk | 0,075 · 0,052 |
| Figura sobre a pilha | grove.500, grove.300 | +0,150 / +0,225 — salto, não degrau |
| Acento | lime.500 | +0,283 |

Duas lições de prompt, para não perder o degrau na geração:

- **Âncora absoluta, nunca comparação relativa.** "Cada folha claramente mais clara que a
  anterior" faz o gerador inflar o intervalo e sair da paleta. Cite o hex de cada folha, mais
  um adjetivo de família ("verdes escuros e profundos, não médios nem claros") — nunca compare
  uma folha à outra.
- **Luz de scanner de mesa, idêntica em todo o quadro.** É a frase que mais segura o gerador
  longe de sombra projetada: cada folha é "uma cor perfeitamente uniforme de borda a borda, o
  mesmo tom no meio e na margem".

## Tetos numéricos de cor (verificáveis, não de gosto)

| Regra | Valor | Token |
| --- | --- | --- |
| Matizes de pilha por peça | 1, mais um neutro estrutural | `illustration.maxHues` |
| Cores ≥1% do quadro | entre 3 e 7 | `illustration.maxColors` |
| Fundo mínimo do quadro | 40% | `illustration.minBackground` |
| Acento (lime) do quadro | até 1%, medido 0,35% na peça de referência | `illustration.accentMaxCoverage` |
| Granulação, amplitude de luminância (só no fundo) | abaixo de 0,028 | `illustration.grainMaxLuminanceAmplitude` |

## Descritores de cor proibidos no prompt

`drop shadow`, `soft shadow`, `blur`, `glow`, `gradient` — qualquer um destes na descrição de
cor/luz quebra o mecanismo de degrau de tom acima. (Descritores proibidos de forma/texto —
`rounded corners`, `3D`, `bevel`, `text`, etc. — não são regra de cor; ficam em
`_bloco-marca.md`.)

## Sem texto renderizado

Nenhuma cor existe para formar letra ou número dentro da imagem — geradores erram tipografia,
e a marca já tem tipografia própria (`DESIGN.md` §4.2). Informação verbal vai no alt-text, não
na cor.
