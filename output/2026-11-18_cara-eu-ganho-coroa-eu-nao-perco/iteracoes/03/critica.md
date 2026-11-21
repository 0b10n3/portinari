# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

Esta é a volta 3 de 3, a última, e há um bloqueante de pé (B6). **Recomendo parar aqui e levar ao autor, sem gerar de novo.**

A volta 3 corrigiu dois itens da crítica 02: o chão agora vai de borda a borda e a mão encolheu. Mas perdeu o que a volta 2 tinha acertado:
- A moeda saiu do eixo do vazado grande. Voltou ao centro (x 0,50) e ficou sobre o vazado pequeno do meio, como na gen_01.
- Apareceu atrás da moeda um segundo disco, que o pedido não tem. É ele, e não a moeda, que fica sobre o vazado grande.
- Cada ponte ganhou uma fenda, e o chão passou a ter cinco aberturas em vez de três.

As duas medidas que já falhavam ficaram iguais ou pioraram: os pequenos têm 0,63 da largura do grande (eram 0,58) e o grande tem 0,63 da largura da moeda (era 0,62). A média é 2,67, com quatro notas abaixo de 3.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | Estão lá a moeda octogonal chapada, a face lisa com o octógono menor, a mão aberta no canto, o chão vazado e o acento numa faceta. Mas a moeda está no centro exato, não "um pouco à direita", e o vazado embaixo dela é um pequeno. Os pequenos não são "bem pequenos" (0,63 do grande). O grande não é "quase do tamanho da moeda" (0,63 dela). E à direita da moeda, onde o pedido quer espaço vazio, há um segundo disco. |
| Uma ideia | 2 | No alto, dois discos sobrepostos dividem o ponto focal. Não dá para saber se o verde-escuro é outra moeda, o verso da moeda ou um eco dela. Embaixo, a fileira tem cinco aberturas. E o vazado grande fica sob o disco extra, então "é ali que ela cai" passa a valer para a peça errada. |
| Fidelidade ao enriquecimento | 2 | O foco está lá, mas fora do lugar e do tamanho: centro em x 0,50 e largura 0,21, contra 0,60 e 0,15, e fora do eixo do vazado grande. e6, e7, e8, e9 e e10 saem diferentes do descrito. Entraram três peças que a v02 não tem, e uma delas, o punho de manga, foi descartada por nome. |
| Paleta e acento | 4 | Só a pilha escura (níveis 1 e 4) e as duas cores de figura, sem cor inventada. O lime fica num único trapézio, o de cima à direita, com 0,49% do quadro. Ressalvas: a figura principal se afastou mais do tom certo (ΔE 8,9, contra 7,6 na gen_02), e a borda de fora do trapézio lime agora encosta em parte no disco extra, não no céu. |
| Matéria de papel | 4 | Dá para contar as folhas: céu, chão, vazados mostrando o céu, anel de oito trapézios com juntas retas, miolo colado por cima, faceta lime e mão. Não há sombra nem parede de recorte. Mas a mão voltou a mostrar arestas internas em tons muito próximos, e puxa um pouco para low-poly. |
| Leitura em miniatura | 2 | A 200 px, a moeda e o ponto lime ainda aparecem, mas colados a um segundo disco. A fileira vira "O ▮ O ▮ O", cinco marcas em vez de três. A mão fica toda dentro do chão e quase some. O encaixe de três peças sob a moeda, que o brief pede para o preview, não aparece. |

**Bloqueantes:**
- **B6: a peça não se resolve em uma leitura.**
  - O segundo disco cria outro ponto focal no alto. Ele é verde-escuro, tem ~0,16 do quadro de largura visível, vértice para cima e orientação diferente da moeda, e fica parcialmente atrás dela, de x ~0,57 a ~0,73.
  - É ele que está no eixo do vazado grande (x ~0,65–0,66). A moeda fica sobre o pequeno do meio (x 0,50).
  - Quem olha não sabe qual das duas peças tem o molde. A ideia da peça é que a moeda já tem preço, porque o chão mostra a réplica dela, e essa ideia fica sem dono.
- **Volta 3 com bloqueante de pé:** pela regra das três voltas, o pipeline para e leva ao autor.

Os demais bloqueantes não se aplicam:
- **B1/B2:** só a pilha escura, sem erro de ΔE.
- **B3:** nenhum texto, número, símbolo ou marca. Em miniatura, a fileira "O ▮ O ▮ O" lembra uma sequência de caracteres, mas são recortes, não letras.
- **B4:** a palma para cima logo depois do lance é um gesto plausível.
- **B5:** a moeda ocupa x 0,39–0,61 e y 0,12–0,50, dentro da área segura universal (x 0,106–0,894, y 0,035–0,965), sem corte.
- **B7:** o foco e todos os apoios estão presentes, embora deformados (ver abaixo).
- **B8:**
  - Não há sombra projetada nem de contato.
  - Dentro dos vazados e das fendas aparece só o preto liso do céu, sem parede nem borda escurecida.
  - O disco extra é mais claro que o céu e não repete a silhueta da moeda. Por isso não o leio como sombra chapada, e sim como uma folha a mais.
  - A variação de tom dentro de cada folha fica em no máximo 0,0112.
- **B9:** moeda e vazados são octógonos regulares de topo reto, o disco extra e a mão são recortados em retas, e tudo está em vista frontal.
- **B10:** os tetos numéricos estão dentro.

**Elementos do enriquecimento ausentes:** nenhum sumiu por inteiro.
- **Como pedido:**
  - e2: miolo com ~0,63 da largura da moeda, na mesma orientação, chapado.
  - e3: oito trapézios no mesmo tom, com juntas retas de quina a quina.
  - e4: só o trapézio de cima à direita, no lado a 45°, em lime.
  - e5: chão no nível 4 (#266947 ≈ #1B6A45), com a borda de cima reta em y ~0,65. Agora vai de borda a borda, sem a moldura preta da gen_02 (corrigido).
  - e11: fibra quase imperceptível, só no fundo (amplitude 0,005).
- **Presentes, mas diferentes do descrito:**
  - e1: centro em x ~0,50 e y ~0,31, largura ~0,21, contra 0,60, 0,24 e 0,15. Vai de y 0,12 a 0,50, além do terço superior. Perdeu o eixo comum com o vazado grande, que a gen_02 tinha acertado, e está sobre o pequeno do meio.
  - e6: a largura (~0,134 do quadro) é a pedida, mas equivale a ~0,63 da moeda. O centro está em x ~0,66, sob o disco extra.
  - e7: os pequenos são idênticos entre si e estão na ordem certa. Mas cada um tem ~0,084 do quadro, ~0,63 do grande, contra 1/3 (~0,045). Centros em x ~0,36 e ~0,50.
  - e8: no lugar de cada ponte inteira há uma fenda retangular escura (~0,014 × 0,083 do quadro), entre duas tiras de chão de ~0,02. Os octógonos continuam separados, mas o chão passa a ter cinco aberturas.
  - e9: palma para cima, dedos estendidos para o lado da moeda, sem polegar erguido, ponta dos dedos em x ~0,26 (tamanho corrigido). Mas a mão inteira fica dentro do chão, com os dedos em y ~0,78–0,80 contra ~0,60, e contrasta só ~1,7:1 com ele. Os dedos vêm separados em tiras, não num só polígono.
  - e10: o céu entre a mão e a moeda está vazio, mas à direita da moeda está o disco extra.
- **Na imagem, mas fora do enriquecimento:**
  - o segundo disco atrás da moeda, que responde por perto de metade da área de #2D9E67 no quadro;
  - as duas fendas nas pontes;
  - uma cunha preta no pulso, entre a mão e a borda esquerda, que lê como punho de manga (descartado na v02).

**Checagens objetivas:** sem erros.
- São 4 cores com ≥1% do quadro, dentro da faixa de 3 a 7: #141414 com 60,1%, #266947 com 26,8%, #339064 com 6,9% e #89C4A5 com 3,4%.
- O fundo ocupa 60,45%, o acento 0,49%, e a granulação do céu mede 0,005.

Avisos que importam:
- **#339064 (ΔE 8,9 de #2D9E67):** é o miolo da moeda, a mão e o disco extra, mais escuros que a cor de figura. O desvio é maior que na gen_02 (ΔE 7,6), mas não chega a fechar B1.
- **Desvio menor, sem aviso:** o anel, em #89C4A5, fica a ΔE 7,7 de #78C9A4 (5,3 na gen_02).
- **Contraste:** os vazados (céu sobre chão) ficam em ~2,8:1, como na gen_02. A mão sobre o chão fica em ~1,7:1. Como nenhum dedo sai para o céu preto, ela não tem onde se destacar.

**Em miniatura:** a 200 px (200×112), o céu preto e a faixa verde se separam bem.
- A moeda vira um octógono verde-claro de ~42 px no centro, com o ponto lime (~12×15 px) no canto de cima à direita. Colado nela, à direita, fica um disco verde-escuro de ~32 px.
- Os vazados viram manchas escuras de ~17, ~17 e ~27 px, com duas fendas de ~3×9 px entre elas: "O ▮ O ▮ O". O grande fica sob o disco escuro, não sob a moeda.
- A mão vira uma cunha verde de ~50 px, quase da cor do chão.

Sobra "duas moedas no ar e uma fileira de buracos". Não sobra "o encaixe de três peças da moeda".

**Alt-text:** descreve a peça pretendida e está certo para ela. Quem não confere é esta imagem: tem um segundo disco, cinco aberturas e o vazado grande fora do eixo da moeda. Manter o alt.

**O que mudar no prompt** (se o autor decidir continuar; em ordem de impacto):
1. Partir do prompt da volta 2, não do da volta 3. A volta 2 acertou o eixo comum e não tinha peça extra; a volta 3 perdeu as duas coisas.
2. Dizer que há uma única moeda e nenhuma outra forma no céu: nada atrás dela, ao lado ou deslocado. Se o prompt descreve a moeda caindo no vazado ou preenchendo-o (o item 1 da crítica 02 pedia essa relação), cortar essa imagem. O gerador parece tê-la desenhado como uma segunda moeda, sobre o vazado grande.
3. Dizer que o chão tem exatamente três aberturas e que as pontes são papel do chão, inteiras, sem fenda nem furo. Hoje cada ponte tem uma fenda, e a fileira vira cinco marcas.
4. Fazer a ponta dos dedos passar da borda de cima do chão e se destacar contra o céu, como na gen_02. Cortar o pulso pela borda esquerda no próprio verde da mão, sem nenhuma peça preta. Hoje a mão inteira fica dentro do chão, a ~1,7:1, com uma cunha preta de manga.
5. As proporções (pequenos com 1/3 do grande; moeda só um pouco maior que o grande) falharam nas três voltas. Mais uma frase dificilmente resolve: ver a seção abaixo.

## Melhor estado das três voltas

**A gen_02 (volta 2) é a que está mais perto de aprovar.**
- É a única sem bloqueante e tem a média mais alta: 3,83, contra 3,50 da gen_01 e 2,67 desta.
- É a única em que a moeda e o vazado grande ficam no mesmo eixo, que é o que faz a leitura "é ali que ela cai".
- Os dois pequenos saem iguais, a mão sai de palma para cima numa folha só, o chão fica no nível 4 e não sobra nenhuma peça. Paleta e matéria de papel tiveram nota 5.

O que ainda falta nela:
- a moeda grande (0,22 do quadro) e deslocada para a direita (x 0,735);
- os pequenos com 0,58 do grande, e o grande com 0,62 da moeda;
- a moldura preta em volta do chão;
- a mão grande demais.

A moldura e a mão se resolvem no prompt, e a volta 3 provou isso: as duas foram corrigidas.

**O defeito que persiste nas três voltas é a relação de tamanho do encaixe.**
- Os pequenos nunca ficaram abaixo da metade da largura do grande: 0,50/0,60, depois 0,58, depois 0,63.
- Depois da gen_01, a moeda nunca mais coube no vazado grande: o grande tinha 0,91 da largura dela, depois 0,62, depois 0,63.
- O eixo entre a moeda e o vazado grande só se manteve em uma das três voltas.
- Cada correção acertou uma medida e soltou outra. Nesta volta, ao tentar amarrar a moeda ao vazado, apareceu um segundo disco.

**É defeito de conceito, não de prompt**, no sentido prático: a leitura da peça depende de uma razão de tamanho precisa entre peças separadas e distantes (a moeda no alto do céu, os vazados no chão), e o gerador de validação não a manteve com nenhuma das formulações tentadas. Não é regra de marca, então a decisão é do autor:
- **(a)** Aceitar a gen_02 com o encaixe aproximado, sabendo que ela fica abaixo da régua da rubrica: os pequenos leem como médios e a moeda é maior que o molde. Nesse caso, corrigir no prompt da volta 2 só a moldura e a mão.
- **(b)** Voltar ao Gate 1 com uma versão do conceito que não dependa da proporção. Por exemplo: a moeda mais baixa, logo acima do vazado grande, para que os tamanhos se comparem de perto e não à distância. Isso muda o "ponto mais alto do lance, no terço superior" do pedido, por isso exige o Gate 1.
