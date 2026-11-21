# Crítica — gen_02 (modo dark, C4, volta 3 de 3)

**Veredito: REVISAR.** Não há bloqueante nem erro de checagem, mas a média das notas é 3,7, e a aprovação exige 4. A fita, que é o foco, voltou a sair cortada pelos vãos, como na volta 2. Esta é a última volta: **recomendo parar e levar ao autor**, sem aprovar por cansaço.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | As gêmeas estão lá: o mesmo octógono, do mesmo tamanho e na mesma linha de centro, uma inteira e outra em três peças. Mas "montada e cintada" não se lê. A faixa lime se interrompe nos dois vãos, e a réplica lê como "moeda fatiada com uma listra". |
| Uma ideia | 4 | A leitura é uma só, nesta ordem: a fita lime, depois a moeda cortada, depois a gêmea. O par ficou mais compacto (vão de ~0,064 do quadro, contra ~0,084 na volta 2). É simétrico sobre o centro, mas não chega a virar díptico. |
| Fidelidade ao enriquecimento | 3 | Os nove elementos aparecem. Mas o foco perdeu, de novo, o traço que o define: atravessar os vãos sem se interromper. A divisão da réplica repete as voltas 1 e 2: peça média, tira estreita, peça larga. |
| Paleta e acento | 5 | Só a pilha escura e as duas cores de figura, com ΔE ≤ 6,7. O lime está num ponto só, a fita, com 0,89% do quadro. |
| Matéria de papel | 4 | Fundo, anel, face e fita contam como folhas chapadas, sem sombra visível e sem parede dentro dos vãos. A fita, cortada junto com as peças, parece impressa nelas, e não uma folha colada por cima. |
| Leitura em miniatura | 3 | A 200 px sobram duas moedas e uma barra lime. Os vãos ficam com ~2 px e as três peças mal se contam. |

**Bloqueantes:** nenhum.
- B5: a fita vai de x ~0,16 a ~0,47 e de y ~0,48 a ~0,52, dentro da área segura universal (x 0,106–0,894).
- B7: o foco está presente. O defeito dele é de função, e por isso entra nas notas, como na volta 2.
- B8: as amplitudes de luminância das folhas de figura ficam em ≤ 0,0096, e os vãos mostram só o fundo liso.

**Elementos do enriquecimento ausentes:** nenhum. Três saíram fora da medida, e são os mesmos da volta 2. As medidas abaixo são feitas a olho na imagem de 1376×768.
- **e1 (foco, a fita):**
  - Defeitos:
    - Sai em três segmentos, cortada pelos dois vãos (x ~220–362, ~378–467 e ~484–650 px). Dentro dos vãos não aparece lime sobre o fundo.
    - A espessura é ~24 px, cerca de 1,5 vez a largura de um vão e ~0,45 da largura do anel. O pedido era menos da metade de um vão.
  - O que melhorou:
    - As pontas ficaram quase rentes às bordas da réplica: passam ~6 px, contra ~18 px na volta 2. O item 2 da crítica anterior foi cumprido.
    - A fita é única, fica só na réplica, e a ponta da direita fica longe da moeda inteira.
- **e3 (a réplica):**
  - A meia altura, as peças medem ~0,33, ~0,22 e ~0,38 da largura da moeda.
  - O primeiro corte (a ~0,34 da largura) continua colado ao vértice superior esquerdo, que fica a 0,29.
  - O segundo corte foi para a direita do centro (a ~0,60), o oposto do que o item 4 pedia.
  - A peça da direita ficou com menos da metade da moeda. Na volta 2 tinha ~0,47.
- **e4 (os vãos):** são exatamente dois, retos, paralelos, de cima a baixo, só na réplica e com fundo liso dentro. Mas cada um tem ~0,011 do quadro (~15 px, ~0,3 do anel), contra 0,025 pedidos. É a mesma largura das voltas 1 e 2.
- **e2, e5 e e7:**
  - Cada moeda tem ~0,30 da largura do quadro, contra ~0,24 pedidos.
  - O octógono da face tem ~0,75 da largura da moeda, contra ~0,6 pedidos, e é igual nas duas.
  - O vão entre as moedas é ~0,064, contra ~0,05 pedidos. O par cabe na área segura do brief.
- **Vistos como pedidos:**
  - e6: as peças em registro. Topo (y 175) e base (y 592) iguais aos da moeda inteira, e a face contínua, interrompida só pelos vãos.
  - e8: uma folha única de fundo, sem chão nem margem, com 73,6% do quadro.
  - e9: grão tênue só no fundo, com amplitude de 0,0062.

**Checagens objetivas:** erros: nenhum · avisos: nenhum.
- Três cores de token passam de 1% do quadro: #141414 com 73,6%, #2D9E67 com 13,5% e #78C9A4 com 11,3%. O fundo ocupa 73,6%.
- O acento está em 0,89%. Mas está em 0,89% justamente porque a fita saiu cortada e curta. Inteira sobre os vãos, nesta espessura e neste comprimento, iria a ~0,98%, sem margem até o teto de 1%.

**Em miniatura** (200 px, escala ~0,145):
- As moedas ficam com ~61 px e o vão entre elas com ~13 px.
- A tira do meio fica com ~13 px e os vãos com ~2 px.
- A fita vira uma barra lime de ~3,5 × 62 px, quase rente às bordas, com duas quebras de ~2 px.
- Rente, a fita deixou de lembrar um risco passando por cima da moeda. Mas não chega a ler como cinta.
- Lê-se "duas moedas iguais, uma listrada". "Uma delas feita de três peças e cintada" não se lê.

**Alt-text** (o `alt` de `v03.json`):
- "Duas moedas octogonais iguais" e "feita de três peças" conferem.
- "Presa por uma cinta" não é verdade nesta imagem: a faixa foi cortada junto com as peças e não prende nada.
- Se o autor aceitar esta imagem como está, a troca é para "atravessada por uma faixa".

**O que mudar no prompt** (o limite de três voltas foi atingido; estes itens não são para uma volta 4 automática, são insumo para a decisão do autor):
1. Descrever cada vão como indo da borda de cima até a fita e da fita até a borda de baixo, e não "de cima a baixo". O próprio `v03` diz que os vãos atravessam "de cima a baixo" e que a fita passa sobre eles "sem se interromper", e nas voltas 2 e 3 o gerador resolveu essa ambiguidade a favor dos vãos.
2. Medir a fita pelo anel, que o gerador desenha estável: cerca de um terço da largura dele (~18 px). Assim ela cabe inteira com folga no teto, a ~0,7%. A relação "metade de um vão" foi ignorada nas três voltas.
3. Descrever os cortes pelos vértices, que o gerador segura:
   - o primeiro no vértice onde começa o lado de cima, que é onde ele já cai nas três voltas;
   - o segundo a cerca de um terço desse lado, para a peça da direita ficar com mais da metade;
   - e parar de pedir duas tiras iguais junto à borda esquerda (ver o diagnóstico abaixo).

## Melhor estado do C4

**A mais perto de aprovar é a 06 (esta).**
- Ela e a 05 não têm bloqueante e ficam na mesma média (~3,7).
- A 06 resolve as pontas da fita (quase rentes) e aproxima o par (vão de 0,064).
- A 05 tem a divisão melhor: a peça da direita fica com ~metade da moeda.
- A 04 é a única em que a fita passa inteira sobre os vãos e lê como cinta. Mas tem dois bloqueantes:
  - B10: acento em 1,5%, que é erro de checagem;
  - B5: a ponta esquerda da fita fica em x ~0,08, fora da área segura.

**O que não se resolveu nas três voltas:**
1. A fita sai cortada pelos vãos na 05 e na 06. Só ficou inteira na 04, quando era larga, comprida e passava muito das bordas, como um objeto à parte. À medida que foi trazida para dentro do teto e das bordas, o gerador a incorporou à moeda e passou a cortá-la.
2. O primeiro corte cai no vértice superior esquerdo nas três voltas, e a divisão sai média, estreita, larga nas três.
3. Os vãos ficam em ~0,011 do quadro nas três voltas.

**Prompt ou conceito: principalmente conceito.**
- **A divisão é conceito, por geometria.** No octógono de topo reto, a faixa das facetas de 45° ocupa 29% da largura em cada lado. Duas tiras de mesma largura junto à borda têm alturas e formas diferentes (a de fora é um toco), então não podem ler como "iguais". O gerador contorna isso levando o corte para o vértice. A ordem cupom, cupom, principal não cabe nessa forma.
- **A fita é conceito com uma parte de prompt.**
  - O que aponta para conceito: o mesmo defeito do foco em duas voltas seguidas, depois de um pedido explícito de correção. Formalmente não é bloqueante, então a regra "o mesmo bloqueante em duas voltas volta ao Gate 1" não dispara à letra, mas o padrão é o mesmo.
  - O que fica sem testar: a frase do item 1 acima, que tira a ambiguidade do próprio enriquecimento.
  - Ressalva: sem ler o prompt, não sei se a correção da crítica da volta 2 (fita colada depois do corte, como ponte) chegou ao gerador. O orquestrador confere isso antes de classificar.

**Opções para o autor:**
1. **Autorizar uma volta extra, fora do limite.** O enriquecimento seria reescrito com os itens 1 a 3, e a divisão passaria a ser "uma tira estreita entre duas peças maiores". A 04 prova que o gerador sabe desenhar a fita inteira. O risco é sair o mesmo resultado; confira o teto de 12 gerações no `manifest.json`.
2. **Voltar ao Gate 1.** Trocar no C4 o sinal de "montada" por um que não dependa de o gerador pintar por cima de um corte, ou escolher outro conceito.
3. **Aceitar a 06 como está.** O alt passa a dizer "atravessada por uma faixa". A peça diz "a moeda e a mesma moeda em três peças", e a fita vira só um marcador, não a cinta. É a capa mais fraca das três opções e fica abaixo da régua de aprovação. Se o autor quiser seguir assim, decide no Gate 2.

---

**Nota do orquestrador (conferência da ressalva):** a correção chegou ao gerador. O prompt efetivo da
gen_02 (`gen_02.efetivo.md`) traz, íntegro: "Where it meets each cut, it carries straight on across the
opening: inside each cut a short length of the band spans the gap like a little bridge, the accent tone
lying over the darkest sheet, joining one piece to the next." O gerador recebeu a instrução e a
ignorou, o que puxa a fita também para defeito de conceito. O "de cima a baixo" dos vãos aparece uma
vez no mesmo prompt (item 1 da lista acima). Gerações gastas: 7 de 12 (uma tentativa falhou no `agy` e
conta no teto).
