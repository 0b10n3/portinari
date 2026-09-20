# Grain-Textured — base

**Origem (Kasra):** meio-tom, grão ou pontilhado aplicados para dar sensação tátil, de feito à
mão; vetores "suavizados". Editorial, aparência vintage, profundidade.

## O que a marca mantém e o que muda

- **Grão só no fundo**, com amplitude de luminância abaixo de 0,028 — um degrau da escada
  (`illustration.grainMaxLuminanceAmplitude`). Nunca sobre a figura nem sobre o acento.
- **Compressão come o grão:** medido, ele sobrevive 47–59% da amplitude em
  LinkedIn/YouTube/Instagram (`DESIGN.md` §11, item 4). Mire a metade superior da faixa aceitável
  — e exporte conforme `../FORMATOS.md` (JPEG 90–92, croma 4:4:4).
- **Meio-tom:** até duas escalas de ponto na mesma peça, e só quando codificam ordem de camada
  (ponto maior = camada mais próxima). Nunca como textura decorativa sem função
  (`DESIGN.md` §7.3).
- **Muda:** "vetores suavizados" não vale — arestas continuam secas. Grão é textura do papel, não
  do contorno.

## Onde usar

Capa editorial de Substack e LinkedIn, fundo de retrato de dado. **Não** em thumbnail pequena: o
grão vira ruído e some na redução.

## Fragmento de prompt

```text
Fine paper-fiber grain on the background sheet only, very low contrast, barely visible.
Where a halftone dot screen appears, use at most two dot sizes, the larger dots on the layer
nearest the viewer. Figure and accent sheets are perfectly clean and uniform.
```

## Checagem

- Grão presente só no fundo; figura e acento limpos.
- No máximo duas escalas de ponto, cada uma ligada a uma camada.
- Amplitude do grão abaixo do teto; conferir depois da exportação, não só no master.
