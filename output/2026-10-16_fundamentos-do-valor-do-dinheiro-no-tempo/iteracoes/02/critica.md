# Crítica — gen_02 (modo dark)

**Veredito: REVISAR**

Não há bloqueante formal. O que reprova é a nota 2 em Fidelidade ao pedido e a média 3,2, abaixo do mínimo de 4. Esta é a 2ª volta da etapa, então resta uma.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | A cabine parece uma capela. Tem telhado de duas águas, lanterna que vira torre de sino com ponta e escadinha na base, e cercada de dinheiro a leitura imediata é "igreja e dinheiro", não máquina do tempo. A lemniscata aparece como dois octógonos fechados lado a lado ("O ⌂ O"), não como um oito deitado. |
| Uma ideia | 3 | A hierarquia está clara: cabine em 1º plano, cédula focal em 2º, alças em 3º. Mas a leitura "templo do dinheiro" é uma segunda ideia que compete com a de "máquina do valor no tempo". |
| Fidelidade ao enriquecimento | 3 | O foco está no lugar (e1 em x ≈ 0,67, y ≈ 0,49, medalhão lima). Quase todos os apoios aparecem, mas o cruzamento em X (e4) e a troca de escala atrás da cabine (e9) não existem: cada alça se fecha sozinha. |
| Paleta e acento | 4 | Só a pilha escura e um único acento, no medalhão da cédula focal. Os verdes da figura e da trilha estão desviados (ΔE 8–14). A trilha saiu num verde médio, perto do tom da cabine, quando devia ser o #125233, mais escuro. |
| Matéria de papel | 4 | Dá para contar as camadas: trilha, cédula, moldura interna, medalhão, tábuas da cabine sobre o fundo. O único deslize é o canto da cédula no alto da alça direita, enrolado em curva em vez de dobrado reto. |
| Leitura em miniatura | 3 | A silhueta sobrevive: dois anéis grandes, a casinha no centro e o ponto lima visível. A diferença de densidade entre as alças se lê. Mas a 200px a capela e o par de "O" ficam mais fortes do que "máquina do tempo" e "∞". |

**Bloqueantes:** nenhum. Checagens sem erro, nenhum texto, número ou cifrão, foco dentro da área segura e longe da borda.

**Elementos do enriquecimento ausentes:**
- **Vistos:**
  - e1 (cédula focal saindo da borda direita da cabine).
  - e2 (medalhão octogonal cheio em acento).
  - e3 (cabine alta, tábuas verticais, porta dupla com vigias octogonais, sem letreiro), mas com leitura de capela.
  - e5 (cédulas pequenas e espaçadas à esquerda).
  - e6 (cédulas grandes, juntas e sobrepostas à direita). A razão de tamanho está em torno de 1,7:1, abaixo do 2:1 pedido.
  - e7 (moedas octogonais, com aro visível só nas grandes).
  - e10 (lanterna e vigias chapadas, sem brilho).
  - e12 (duas faixas de fundo). A de cima vai até y ≈ 0,84, não até 0,72.
- **Parciais:**
  - e4: há trilha larga em dois octógonos com o miolo vazio, mas eles não se cruzam em X.
  - e8: moldura interna e medalhão aparecem, os cantos chanfrados a 45° não.
  - e11: um só canto dobrado, e enrolado em curva.
- **Ausente:** e9. Não há fita que atravesse a cabine trocando de escala; o laço capitalizar/descontar não se lê.
- Faltam 1 de 8 apoios inteiros e o foco está presente, então não chega a B7.

**Checagens objetivas:**
- **Erros:** nenhum.
- **Desvio de cor (ΔE 9,5–14,5):** não sai da paleta, mas na trilha incomoda. Ela ficou clara demais, mais perto de #1B6A45 ou #2D9E67 do que de #125233, e por isso não recua atrás da cabine. Nas cédulas (#95CAAC contra #78C9A4) não incomoda.
- **15 cores ≥1%:** efeito do JPEG e das variações entre folhas. A imagem tem cerca de 6 tons visíveis, não incomoda.
- **"Fundo 14%":** leitura equivocada da checagem, que tomou a faixa #0F3D27 como fundo. O preto #141414/#171717 sozinho passa de 40%, e o fundo livre real fica perto de 55%. Não incomoda.
- **acento_fracao 0,0:** o medalhão lima existe e é visível. Fica abaixo de 1% do quadro, por isso não foi contado, o que está dentro do teto.

**Em miniatura:** a 200px sobram dois anéis octogonais verdes grandes, uma casinha de torre pontuda no centro e um ponto lima pequeno mas legível à direita do eixo. A alça direita parece mais cheia e mais clara que a esquerda, e isso se lê como mais dinheiro. Não sobra nem "máquina do tempo" nem "infinito": a leitura é "capela entre dois anéis".

**O que mudar no prompt** (em ordem de impacto):
1. **Tirar a cabine do vocabulário de igreja.** Trocar o telhado de duas águas com lanterna em torre por um topo reto em degraus, com cantos chanfrados a 45°, e uma lanterna quadrada baixa assentada direto nesse topo. Nada de torre, ponta, cruz, sino ou escada na base: a cabine pousa direto na faixa de baixo.
2. **Dar à cabine leitura de gabinete, não de edifício.** A porta dupla com as duas vigias deve ocupar cerca de 3/4 da altura da fachada. As tábuas verticais vão do topo à base, sem frontão triangular.
3. **Fazer a trilha um oito deitado de verdade.** As duas alças se cruzam em X atrás da cabine. Dos dois lados dela devem aparecer duas faixas diagonais a 45°, uma subindo e uma descendo, que entram na borda da cabine. Nenhuma alça se fecha sozinha num octógono completo.
4. **Tornar visível a troca de escala no cruzamento (e9).** Cada faixa diagonal entra pela esquerda com peças pequenas e sai pela direita com peças grandes, e vice-versa, sem peça de tamanho intermediário fora da cabine.
5. **Escurecer a trilha.** Ela deve ser explicitamente a folha #125233, mais escura que a cabine (#2D9E67) e que as cédulas (#78C9A4), para recuar para o 3º plano.
6. **Corrigir escala e acabamento das cédulas.** As da alça direita com pelo menos duas vezes e meia o comprimento das da esquerda, para garantir o 2:1 na peça final. Os cantos dobrados viram dobras retas a 45°, chapadas, sem rolar nem curvar.

Fica uma volta. Se na 3ª a cabine ainda parecer uma capela ou a lemniscata ainda não se cruzar, o certo é parar e levar ao autor, não aprovar.
