# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | A cabine sai como capela de madeira (tábuas de celeiro, lanterna com coruchéu pontudo, vigias na altura da maçaneta), não como máquina do tempo. O "oito deitado" sai como dois anéis octogonais quase regulares, um de cada lado da cabine, e não como um laço contínuo. |
| Uma ideia | 3 | A ideia está lá: pouco e espaçado à esquerda, muito e junto à direita, a cabine no meio. Mas a composição simétrica anel–torre–anel lê como três blocos, e a cédula focal entra horizontalmente no miolo vazio da alça direita, formando com o anel um glifo de "G"/"e". |
| Fidelidade ao enriquecimento | 3 | O foco (e1) e o medalhão (e2) estão no lugar. Faltam a troca de escala legível nas duas fitas (e9) e os cantos dobrados das cédulas grandes (e11). A razão de escala fica em ~1,7:1, não 2:1. O corte do fundo cai em y≈0,50, não em 0,72. |
| Paleta e acento | 4 | Só a pilha escura e a figura. O acento é um único octógono lima no medalhão focal, exatamente na virada. Ressalva sem efeito no prompt: um tom de figura derivou ΔE 12,9 em 1% do quadro. |
| Matéria de papel | 4 | Dá para contar as camadas nas cédulas (folha, moldura colada, medalhão) e no canto dobrado da focal. A cabine e a trilha estão chapadas demais e quase sem borda de corte: aparecem como vetor plano, não como folha sobre folha. |
| Leitura em miniatura | 3 | A 200px sobra o glifo "O \| G" com um ponto lima. A diferença esquerda/direita aparece só como textura rala contra corrente densa. ∞ e máquina do tempo não chegam. |

**Bloqueantes:** nenhum. B1/B2: nada fora da paleta nem pilha misturada. B3: nenhum texto, número ou cifrão. B5: o foco está em x≈0,67, y≈0,50, dentro da área segura universal (x 0,106–0,894). B6: a peça não chega a díptico. B7: o foco está presente e só 1 de 8 apoios sumiu.

**Elementos do enriquecimento ausentes:**
- Vistos: e1 (cédula grande saindo da borda direita da cabine, ponta esquerda escondida, medalhão inteiro) · e2 (medalhão octogonal cheio em lima) · e3 (cabine alta e estreita, de frente, telhado a 45°, tábuas verticais, porta dupla com vigias, sem letreiro) · e4 (trilha em dois octógonos, miolos vazios) · e5 (cédulas pequenas e espaçadas à esquerda) · e6 (cédulas grandes, juntas, em telha à direita) · e7 (moedas octogonais intercaladas, menores à esquerda) · e8 (cédulas com chanfro, moldura interna e medalhão, nada legível) · e10 (lanterna e vigias chapadas, sem brilho) · e12 (fundo em duas faixas retas).
- Ausente: e9. O cruzamento em X fica inteiro escondido atrás da cabine. Não se vê fita sumindo pequena e reaparecendo grande, nem a volta do desconto. Só um fragmento pequeno espia à esquerda, embaixo.
- Fracos: e11 (só a cédula focal tem canto dobrado; as grandes da alça direita, não) · e6 (razão ~1,7:1, abaixo dos 2:1 pedidos) · e12 (o corte das faixas está em y≈0,50, não em 0,72) · e4 (os octógonos não são alongados e o X não aparece, então não lê como ∞).

**Checagens objetivas:** erros nenhum.
- Fundo 27%: o checador conta só a faixa #151515. A faixa #0F3D27 (26%) também é fundo, então o fundo livre real fica perto de 53%. Não incomoda.
- Amplitude 0,030 em #1F6C49 e #3F8F68: frações de 1,8% e 1,0%, nas bordas recortadas das cédulas e moedas. É serrilhado do JPEG, não sombra. Não incomoda.
- #3F8F68 a ΔE 12,9 de #2D9E67: 1% do quadro, invisível na imagem. Não incomoda.
- Acento medido em 0,0: a imagem mostra um octógono lima de ~0,5% do quadro. É falha de medição, não de imagem.
- O que importa (lido na imagem, não nos avisos): a trilha saiu perto de #1B6A45/#267C55, mais clara que a pilha-3 pedida (#125233). Ficou no mesmo valor da cabine e as duas massas se fundem.

**Em miniatura:** a 200px, metade de cima preta e metade de baixo verde-escura. Dois anéis octogonais verdes grandes ladeiam uma torre verde com ponta. Um ponto lima fica logo à direita do centro. As cédulas viram pontinhos: à esquerda espaçados, à direita uma corrente contínua, então algum crescimento ainda se lê. O conjunto vira o glifo "O | G" e não um ∞. A torre lê como campanário, não como máquina do tempo.

**O que mudar no prompt** (em ordem de impacto):
1. Desenhe a lemniscata como uma única faixa contínua em oito deitado, com dois octógonos bem alongados na horizontal (cerca de 2:1). Os lados internos dos octógonos são as duas diagonais a 45° do X, e essas diagonais aparecem acima e abaixo da cabine, que cobre só o terço central do cruzamento.
2. Faça a cédula focal sair da borda direita da cabine inclinada a 45°, ao longo da diagonal ascendente do X e encaixada sobre a faixa da trilha (medalhão perto de x 0,64, y 0,45). Ela não pode avançar na horizontal para dentro do miolo vazio da alça direita.
3. Tire o ar de capela da cabine: lanterna quadrada de topo reto, sem coruchéu nem ponta; as duas vigias octogonais sobem para a metade superior das folhas da porta, como janelas, e não ficam na altura da maçaneta; a cabine fica sobre uma base em dois degraus chanfrados a 45°. Mantém o telhado de duas águas e a proibição de letreiro e de grade de painéis.
4. Separe a cabine da trilha pelo valor: a trilha toda em #125233 (pilha-3), claramente mais escura e recuada, e a cabine em #2D9E67 com as tábuas alternando #2D9E67 e #78C9A4, para que fique à frente.
5. Mostre a passagem pela cabine dos dois lados: uma cédula pequena entra pela borda esquerda da cabine na diagonal ascendente e a focal sai grande do outro lado. Na diagonal descendente, uma cédula grande entra pela direita e uma pequena reaparece à esquerda. Nada de tamanho intermediário.
6. Cada cédula da alça direita tem pelo menos o dobro do comprimento das da esquerda. Duas ou três delas mostram um canto dobrado a 45°, além da focal.
7. A faixa escura do fundo ocupa a parte de cima até y 0,72 e a faixa #0F3D27 fica só no terço de baixo, sob a base da cabine.
