# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

Nenhum bloqueante e nenhuma nota abaixo de 3, mas a média é 3,5. A rubrica pede pelo menos 4. **Esta é a 3ª volta da etapa, o limite.** Recomendo parar e levar ao autor o melhor estado, com o diagnóstico abaixo. A decisão de aceitar este prompt como está, ou de autorizar uma volta a mais, é do autor. Não aprovo para fechar a etapa.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | A cabine é grande, alta e está no centro. O dinheiro, em cédulas e moedas, forma um oito deitado ao fundo, e a peça se lê de uma vez. O problema é a cabine: o topo reto, em degrau, com um bloco em cima, aproxima a silhueta da cabine de série em vez de afastar dela. |
| Uma ideia | 4 | A hierarquia aparece: a cabine em 1º plano, os dois anéis octogonais em 2º, as cédulas e moedas em 3º. Não é díptico, porque a cabine costura as duas alças. O foco do enriquecimento, porém, não se destaca das cédulas vizinhas. |
| Fidelidade ao enriquecimento | 3 | O foco está lá: uma cédula sai da borda direita da cabine com o medalhão lima. Só que ela é do mesmo tamanho das vizinhas, e não a maior da fita. Faltam o telhado de duas águas a 45° (e3), e as dobras de canto saíram em lima em vez de no tom da figura principal (e11). |
| Paleta e acento | 3 | Não há cor fora da paleta. O acento lima aparece em três pontos, e não em um: o medalhão focal e as dobras de canto em x≈0,72 y≈0,27 e x≈0,95 y≈0,67. A cabine saiu num menta claro (#9AD1B1), e não na figura principal #2D9E67 do enriquecimento, então tem o mesmo tom das cédulas. |
| Matéria de papel | 4 | As camadas se contam: fundo, trilha, cédula, moldura interna e medalhão. As moedas têm aro sobreposto e as tábuas da cabine estão recortadas uma a uma. Tudo chapado, sem pintura digital. |
| Leitura em miniatura | 3 | A troca de escala entre a esquerda e a direita sobrevive. Mas o oito vira "O ▮ O", o medalhão lima vira um pingo que não se distingue das dobras lima, e a cabine se lê como um armário com tampa. |

**Bloqueantes:** nenhum.
- B1 e B2 não se aplicam: sem erro nas checagens e sem tom da pilha clara.
- B3 não se aplica: não há texto, número nem cifrão, e os medalhões estão vazios.
- B5 não se aplica: o foco fica em x≈0,65 y≈0,31, dentro da área segura universal (x 0,106–0,894 · y 0,035–0,965), e não está cortado.
- B6 e B7 não se aplicam: a peça tem uma ideia só e o foco está presente.

**Elementos do enriquecimento ausentes:**
- **Vistos:**
  - e1, o foco, porém fraco (detalhe abaixo).
  - e2, o medalhão octogonal lima cheio.
  - e4, a trilha em oito com o miolo vazio. Os octógonos estão quase regulares, não alongados.
  - e5, as cédulas pequenas e espaçadas à esquerda.
  - e6, as cédulas grandes e sobrepostas à direita, com razão de cerca de 1,7–1,9:1, um pouco abaixo dos 2:1 pedidos.
  - e7, as moedas octogonais com aro, pequenas à esquerda e grandes à direita.
  - e8, a cédula genérica com moldura interna e medalhão, sem nada legível.
  - e9, as fitas passando atrás da cabine e trocando de escala ali, sem peça intermediária.
  - e10, as vigias e a lanterna chapadas, sem brilho. A lanterna saiu larga, retangular, não pequena e quadrada.
  - e12, as duas faixas horizontais, com a base da cabine sobre a faixa de baixo.
- **Parciais:**
  - e3: as tábuas, a porta dupla e as vigias estão lá, mas o **telhado de duas águas a 45° sumiu**. No lugar há uma cornija reta com um bloco por cima.
  - e11: as dobras de canto existem, mas na cor do acento, não na figura principal.
- **Ausentes:** nenhum por inteiro. Os apoios estão bem acima de dois terços.
- **e1:** a cédula focal não é "a maior e mais nítida da fita", tem o tamanho das outras da alça direita. A posição y 0,50 do enriquecimento não se cumpriu, mas o gerador acertou. Com fitas a 45° que se cruzam no centro atrás de uma cabine de cerca de 0,21 da largura, as fitas só aparecem na borda da cabine perto de y 0,31 e y 0,69. A coordenada y 0,50 é geometricamente incompatível com a cena e deve ser corrigida no enriquecimento, não cobrada da imagem.

**Checagens objetivas:** sem erros.
- **11 cores ≥1% (teto 7):** a maioria é variação de antisserrilhado e de JPEG dos tons de figura. Não incomoda.
- **#9AD1B1 a 8,9%, ΔE 9,9 de #78C9A4:** importa. É o corpo da cabine, mais claro que a paleta e do mesmo tom das cédulas. Por isso o foco não se separa da cabine.
- **#2A8660 a 6,2%, ΔE 11,0; #3F956E e #479D74, ΔE 10–11,5:** um meio-tom entre a pilha 4 e a figura principal, nas molduras das cédulas. É deriva tolerável.
- **Amplitude de tom 0,029–0,037 em três tons:** são áreas pequenas e não se vê sombra nem gradiente. Não incomoda.
- **acento_fracao 0,0:** o lima existe, mas cada ponto é pequeno demais para a medição. Isso confirma que o medalhão está pequeno demais para a miniatura.
- **Fundo #171717 a 40,1%:** no limite, ok.

**Em miniatura:** a 200px sobra um campo escuro com dois anéis octogonais e um retângulo claro e alto no meio. O anel da direita é mais claro e mais cheio que o da esquerda, então a ideia de crescer ao atravessar a cabine sobrevive. O cruzamento do oito fica escondido pela cabine, e o ∞ só se adivinha pelos tocos diagonais. O medalhão lima vira um pingo de uns 5px, igual às dobras lima. Sem o telhado, a cabine lê como armário ou elevador, não como máquina do tempo.

**O que mudar no prompt** (em ordem de impacto):
1. Limitar o lima ao medalhão da cédula focal e pintar as dobras de canto das cédulas grandes em #2D9E67, com uma frase explícita: "nenhum outro lima em toda a imagem".
2. Trocar o topo da cabine por um telhado de duas águas a 45°, como uma guarita, com uma lanterna pequena e quadrada na cumeeira, e proibir a cornija reta em degrau com bloco em cima. É o que afasta a silhueta da cabine de série.
3. Pintar o corpo e as tábuas da cabine em #2D9E67 e reservar #78C9A4 às cédulas e moedas, para que a cédula focal clara se recorte contra a cabine.
4. Fazer da cédula focal a maior da fita, cerca de 1,3 vez as vizinhas, com o medalhão lima ocupando cerca de 40% da altura da cédula. Assim o acento sobrevive a 200px.
5. Situar o foco onde a fita de cima sai da borda direita da cabine (cerca de x 0,64, y 0,33), no lugar de y 0,50, e registrar essa correção no enriquecimento.
6. Firmar a razão de 2:1 no comprimento das cédulas entre a direita e a esquerda (hoje está em cerca de 1,8:1).
