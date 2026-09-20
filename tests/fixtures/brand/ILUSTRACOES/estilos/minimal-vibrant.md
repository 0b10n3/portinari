# Minimal Vibrant — modo

**Origem (Kasra):** reduz os elementos às formas núcleo e combina com cor forte e ousada. Marca,
editorial, gráfico moderno.

## O que a marca mantém e o que muda

- **Mantém:** redução radical. Poucas folhas, um elemento, muito fundo.
- **Muda:** "vibrante" **não** é saturação nova — a paleta é fechada. Aqui a vibração é
  **contraste**: pilha escura (Ink → Deep Forest) + figura em `illustration.figure.primary`
  (salto de +0,150 de luminância sobre a pilha) + o acento como único ponto quente.
- **O acento continua ≤1% do quadro** (`illustration.accentMaxCoverage`). A tentação deste modo é
  crescer o Lime; não cresce.
- **Números:** no máximo três camadas visíveis; o fundo passa dos 40% mínimos (`DESIGN.md` §7.2) e
  costuma ficar em 60–70%.

## Onde usar

O melhor modo para **thumbnail de YouTube** (teto de três camadas, `DESIGN.md` §7.4), **capa de
Reels/Story** e capa de post do Instagram — lugares vistos pequenos e por menos de um segundo.

## Fragmento de prompt

```text
At most three cut-paper sheets and one figure, on a large empty background that fills more than
half the frame. One small accent shape as the only warm point. Strong contrast between the dark
sheets and the figure. Nothing else.
```

## Checagem

- Contagem de camadas ≤3; fundo ≥40% (esperado 60–70%).
- Lime ≤1%.
- Continua legível reduzida a ~160px de largura (teste de miniatura proposto aqui, não medida de
  plataforma) — acima do limiar de 96px do `DESIGN.md` §7.4.
