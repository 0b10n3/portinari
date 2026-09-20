# Estilos de ilustração — os 14 de referência, traduzidos para a marca

Referência: [14 illustration styles](https://www.kasradesign.com/14-illustration-styles-every-illustrator-should-learn/)
(Kasra Design). Escopo: o mesmo de `../README.md` — **nunca app, nunca site**.

## A regra que organiza tudo

A marca tem **um** estilo de ilustração: collage / paper cut (`DESIGN.md` §7). Os 14 estilos
abaixo não competem com ele — cada um é **traduzido para dentro do paper cut** ou **recusado**.
Traduzir = manter só o que sobrevive à paleta, à ausência de sombra/gradiente, ao corte reto ou
a 45° e à matéria "papel empilhado".

| Peso da regra           | O que é                                                                              | Como se comporta                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Vinculante**          | A paleta: tokens do modo, uma pilha por peça (`../meta-prompt-collage-paper-cut.md`) | Reprova                                                                           |
| **Padrão sobreponível** | O resto de `../_bloco-marca.md` (sombra, grão, frame, corte, tetos de cor)           | Aviso; cede se o pedido pedir o contrário (decisão A2 do `portinari`, 18/09/2026) |

Os arquivos abaixo dizem, para cada estilo, qual regra ele dobra e qual nunca dobra.

## Matriz

| Estilo (Kasra)    | Veredito                                      | Arquivo / motivo                                                                                                                                                                                                                                                                |
| ----------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flat Illustration | **Base**                                      | [`flat.md`](flat.md)                                                                                                                                                                                                                                                            |
| Grain-Textured    | **Base**                                      | [`grain-textured.md`](grain-textured.md)                                                                                                                                                                                                                                        |
| Risograph         | **Base**                                      | [`risograph.md`](risograph.md)                                                                                                                                                                                                                                                  |
| Geometric         | **Base**                                      | [`geometric.md`](geometric.md)                                                                                                                                                                                                                                                  |
| Nostalgic         | **Modo**                                      | [`nostalgic.md`](nostalgic.md)                                                                                                                                                                                                                                                  |
| Surreal           | **Modo**                                      | [`surreal.md`](surreal.md)                                                                                                                                                                                                                                                      |
| Minimal Vibrant   | **Modo**                                      | [`minimal-vibrant.md`](minimal-vibrant.md)                                                                                                                                                                                                                                      |
| Abstract          | **Modo**                                      | [`abstract.md`](abstract.md)                                                                                                                                                                                                                                                    |
| Isometric         | **Modo, restrito** — exige peça-piloto medida | [`isometric.md`](isometric.md)                                                                                                                                                                                                                                                  |
| Psychedelic Retro | **Fora**                                      | Paleta multimatiz e formas distorcidas: viola a paleta (vinculante) e a curva orgânica livre (`DESIGN.md` §4.4). Use _Surreal_ para o lado conceitual                                                                                                                           |
| Pop Art           | **Fora**                                      | Contorno grosso e cores primárias: a paleta é fechada e paper cut não tem traço. O que se aproveita, o meio-tom, já está em [`grain-textured.md`](grain-textured.md) com a regra da marca                                                                                       |
| Doodle & Line Art | **Fora**                                      | `handwritten` e `sketchy` são descritores proibidos (§7.5); paper cut é preenchimento, não traço. Traço fino existe na camada de **sistema** (hairline, `growthLine`, diagramas), nunca na ilustração                                                                           |
| Holographic       | **Fora**                                      | Iridescência é gradiente + glow, proibidos. A exceção de gradiente (§4.5) é só ambiente de sistema, baixa opacidade — nunca ilustração                                                                                                                                          |
| Pixel Art         | **Fora**                                      | O mais próximo dos recusados (geometria reta, paleta curta), mas quebra a matéria: papel não tem pixel, e retícula só é permitida quando codifica ordem de camada (§7.3). Adotar seria decidir um **segundo estilo** — pergunta ao founder (`APLICACAO.md` §11), não inferência |

## Como escolher e combinar

- **Uma base + no máximo um modo** por peça. A base é a técnica (como as folhas são feitas); o
  modo é o tema/composição (o que a peça mostra). Sem base declarada, o padrão é `flat`.
- Comece pelo modo, que vem do briefing: _o que a peça precisa dizer?_

| A peça precisa…                      | Modo                               | Base que costuma acompanhar |
| ------------------------------------ | ---------------------------------- | --------------------------- |
| traduzir um número em matéria        | `abstract`                         | `geometric`                 |
| carregar uma metáfora inesperada     | `surreal`                          | `flat` ou `grain-textured`  |
| parar o scroll em tamanho pequeno    | `minimal-vibrant`                  | `flat`                      |
| contar a história de algo do passado | `nostalgic`                        | `grain-textured`            |
| mostrar estrutura/arquitetura        | `isometric` (piloto) ou `abstract` | `geometric`                 |

- Destino manda: thumbnail e capa de Reels/Story sofrem compressão e redução — prefira `flat` +
  `minimal-vibrant`. Capa editorial de Substack/LinkedIn aguenta `grain-textured` e `risograph`.
  Tamanhos e áreas seguras: `../FORMATOS.md`.
- O fragmento de prompt de cada arquivo **entra depois** do bloco de marca
  (`../_bloco-marca.md`), nunca no lugar dele.

## Formato de cada arquivo

Origem · o que a marca mantém e o que muda · onde usar · fragmento de prompt (inglês, só termos
positivos — os descritores proibidos de `../_bloco-marca.md` continuam sendo lint) · checagem.
