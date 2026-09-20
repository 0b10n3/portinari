# Rubrica do crítico visual

A pergunta é sempre a mesma: **o prompt que gerou esta imagem está pronto para o autor gerar a peça
final com ele?** A imagem é de validação (modelo flash, ~1K, JPEG) — ela prova o prompt, não é o
produto (decisão A16).

Este arquivo mora fora do código de propósito: mudar a régua não é mudar programa.

## Bloqueantes — qualquer um = REVISAR

| # | Bloqueante | Por quê |
| --- | --- | --- |
| B1 | **Cor fora da paleta** do modo (erro em `checagens.json`, ΔE > 25) | A paleta é a única regra vinculante da marca (A2). Vale inclusive para objeto que "tem cor própria": a cereja vermelha do S1 é o caso de origem |
| B2 | **Pilhas misturadas** — tons da pilha clara numa peça escura, ou o contrário | Uma pilha por peça; peça que mistura não deriva |
| B3 | **Texto renderizado**: qualquer palavra, letra, número, sigla, legenda, código de barras, marca d'água ou logo desenhado na imagem | O gerador alucina texto com frequência e a marca proíbe. Inclui `$` onde deveria ser `R$`: numa peça sobre finanças brasileiras, o símbolo errado é erro factual |
| B4 | **Elemento factualmente errado** no ofício retratado (ferramenta que não existe naquela cultura, gesto impossível, planta trocada) | Uma peça editorial que erra o mundo real desmente o texto que ela ilustra |
| B5 | **Ponto focal fora da área segura** do `brief.json`, ou cortado pela borda | As derivações de plataforma cortam do centro; foco na borda some |
| B6 | **Duas ideias** — a peça não se resolve em uma leitura, ou virou díptico de duas metades | Uma ideia por peça (risco R13) |
| B7 | **Elemento `foco` do enriquecimento ausente** da imagem, ou mais de um terço dos apoios sumidos | O enriquecimento é o que separa uma imagem rala de uma profissional |

**Não são bloqueantes** (padrão sobreponível — A2; citar, nunca reprovar sozinho): sombra projetada,
gradiente, granulação acima do teto, número de cores fora de 3–7, fundo abaixo de 40%, acento acima
de 1%, descritor proibido, ângulo de corte fora de 0°/45°. Quando o pedido do autor pede o
contrário, a marca cede — e o crítico registra que cedeu.

## Notas — 1 a 5

| Critério | O que se mede | 5 | 1 |
| --- | --- | --- | --- |
| **Fidelidade ao pedido** | a peça diz o que o autor pediu que ela dissesse | diz, e em uma leitura | ilustra outra coisa |
| **Uma ideia** | leitura única, hierarquia clara | 1º, 2º e 3º plano evidentes | sopa de elementos |
| **Fidelidade ao enriquecimento** | os elementos de `vNN.json` estão lá | todos, com o foco no lugar | foco ausente |
| **Paleta e acento** | pilha do modo, acento em um ponto | só a paleta, acento na virada | cor inventada |
| **Matéria de papel** | folhas legíveis, bordas cortadas, camadas | dá para contar as camadas | pintura digital genérica |
| **Leitura em miniatura** | o que sobra a 200px | conceito ainda legível | mancha |

Régua da nota: 5 = pronto como está · 4 = pronto, com ressalva que não muda o prompt · 3 = uma volta
resolve · 2 = duas voltas ou mudança de conceito · 1 = o prompt não está no caminho.

**APROVADO** exige: nenhum bloqueante, nenhuma nota abaixo de 3, e média ≥ 4.

## Limite de voltas

Três por etapa. Chegando à terceira com bloqueante de pé, o veredito é `REVISAR` com a recomendação
explícita de parar e levar ao autor. O pipeline nunca aprova sozinho para "fechar" (regra herdada do
`revisor-final` do gary_halbert).

## Quando a peça é uma derivação (light a partir de dark, ou o contrário)

A derivação existe para mudar **só a pilha de cor**. Além de tudo acima, medido contra a imagem
aprovada do modo primário:

| # | O que conferir | Veredito |
| --- | --- | --- |
| D1 | Mesma composição: cada massa no mesmo lugar, mesmo enquadramento, mesmo ponto focal | mudou = REVISAR |
| D2 | Mesmos elementos: nada some, nada aparece | sumiu ou apareceu = REVISAR |
| D3 | A pilha é a do modo novo, inteira (B1 e B2 valem) | misturou = REVISAR |
| D4 | O acento continua no mesmo ponto e no mesmo tamanho relativo | espalhou = REVISAR |

Em derivação, "ficou mais bonito" é defeito: o par light/dark tem de ser reconhecível como a mesma
peça. Diferença de forma que apareceu na edição vai na lista de revisão, mesmo que melhore a peça.

## O que esta rubrica não mede

Nitidez, resolução e acabamento: a imagem de validação é ~1K por construção, e a peça final vai ser
gerada pelo autor no Nano Banana Pro a partir do prompt aprovado. Pedir "mais nítido" ao prompter é
pedir o que o prompt não controla.
