# Crítica — gen_01 (modo dark, C4, volta 2 de 3)

**Veredito: REVISAR**: não há bloqueante nem erro de checagem, mas a média das notas é 3,7, abaixo dos 4 que a aprovação exige. A fita (o foco) saiu cortada junto com as peças e deixou de segurar a réplica.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | As gêmeas estão lá: mesmo octógono, mesmo tamanho, mesma linha de centro, uma inteira e uma em três peças. Mas "montada e cintada" não se lê: a faixa lime é interrompida nos dois vãos, e a réplica lê como "moeda fatiada com uma listra", não como "moeda montada e presa". |
| Uma ideia | 4 | Há uma leitura só, com hierarquia clara: fita lime, depois réplica, depois moeda inteira. O vão de ~0,08 do quadro entre as moedas mantém o par sem virar díptico, embora a simetria exata sobre o centro fique perto disso. |
| Fidelidade ao enriquecimento | 3 | Os nove elementos aparecem, mas o foco perdeu o traço que o define (atravessar os dois vãos sem se interromper). A réplica repete a divisão da volta 1: peça média, tira, peça larga, em vez de tira, tira, peça larga. |
| Paleta e acento | 5 | Só a pilha escura e as duas cores de figura (ΔE ≤ 6,8). O lime está num ponto só, a fita, com 0,87% do quadro. |
| Matéria de papel | 4 | Fundo, anel e face contam como três folhas chapadas, sem sombra e sem parede dentro dos vãos. A fita, cortada junto com as peças, parece pintada no anel em vez de ser a quarta folha colada por cima. |
| Leitura em miniatura | 3 | A 200 px sobram duas moedas e uma barra lime. Os vãos ficam com ~2 px e as três peças mal se contam. |

**Bloqueantes:** nenhum. A B7 não dispara: a fita, que é o foco, está na imagem. O defeito é ela ter perdido a função, e isso entra nas notas.

**Elementos do enriquecimento ausentes:** nenhum está ausente, mas três saíram fora da medida.
- **e1 (foco, a fita):**
  - Defeitos:
    - A faixa sai cortada pelos dois vãos, em três segmentos (x ~0,145–0,247, ~0,259–0,305 e ~0,316–0,471). Na volta 1 ela passava inteira por cima dos vãos; agora é interrompida, e por isso dentro de cada vão não aparece lime sobre o fundo, que é justamente onde a fita deveria se ler melhor.
    - A espessura é ~22 px, cerca de 1,4 vez a largura de um vão. O conceito pede cerca de metade.
  - O que está certo: é única, fica só na réplica, as pontas passam ~meio corte das bordas e a ponta da direita fica longe da moeda inteira.
- **e3 (a réplica):** os cortes caíram na mesma posição relativa da volta 1. O primeiro passa no vértice superior esquerdo do octógono, onde começa o lado de cima; o segundo passa na linha de centro vertical da moeda. A meia altura, as peças medem ~0,30, ~0,15 e ~0,47 da largura da moeda. O item 3 da crítica anterior pedia essa mudança e ela não aconteceu.
- **e4 (os vãos):** são exatamente dois, retos, paralelos, de cima a baixo, só na réplica, com fundo liso dentro. Mas cada um tem ~0,011 do quadro, contra ~0,025 pedidos: cerca de um quarto da largura do anel.
- **e2 e e7 (tamanho do par e vão entre as moedas):**
  - Cada moeda ocupa ~0,30 da largura do quadro: o pedido era ~0,24, e na volta 1 eram 0,36.
  - O vão entre elas é ~0,084, contra ~0,05 pedidos.
  - O par se lê como par e fica dentro da área segura universal do brief. O recorte 1:1 (x 0,22–0,78) cortaria as bordas externas das duas moedas, mas esse recorte não está no brief.
- **Vistos como pedidos:**
  - e5: o octógono concêntrico, com ~0,69 da largura e igual nas duas moedas.
  - e6: as peças em registro, com topo e base alinhados aos da moeda inteira e a face contínua, interrompida só pelos vãos.
  - e8: uma folha única de fundo, sem chão nem margem, com 74% do quadro.
  - e9: fibra tênue só no fundo; moedas e fita limpas.

**Checagens objetivas:** erros: nenhum · avisos: nenhum.
- Três cores de token passam de 1% do quadro: #141414 com 74,1%, #78C9A4 com 13,0% e #2D9E67 com 11,3%. O fundo ocupa 74%.
- O acento está em 0,87%, o que resolve o erro da volta 1 (1,5%).
- A margem até o teto de 1% é estreita: a mesma fita, inteira sobre os vãos e na espessura de hoje, iria a ~0,93%.

**Em miniatura:**
- O que se vê a 200 px:
  - duas moedas de ~60 px, com o octógono da face visível;
  - uma barra lime de ~3 px atravessando a da esquerda e passando das duas bordas.
- Os vãos (~2 px) quase somem. O que sobra deles é a tira do meio (~9 px).
- A barra, que ultrapassa as bordas e não mostra vão visível, lembra uma moeda riscada, ao lado da gêmea limpa.
- Lê-se "duas moedas iguais, uma marcada"; "uma delas feita de três peças e cintada" não se lê.

**Alt-text** (o `alt` de `v03.json`): "duas moedas octogonais iguais" e "feita de três peças" conferem. "Presa por uma cinta" ainda não é verdade nesta imagem, porque a faixa está cortada junto com as peças. O alt descreve a peça que o conceito pede, então fica como está. Se esta imagem fosse aceita do jeito que saiu, a troca seria para "atravessada por uma faixa".

**O que mudar no prompt** (para a volta 3 de 3, a última):
1. Dizer que a fita é colada depois do corte, por cima de tudo: os vãos param nela, nenhum vão a corta, e dentro de cada vão se vê a fita lime passando sobre o fundo escuro, como uma ponte.
2. Terminar as pontas da fita rentes às bordas esquerda e direita da réplica. É a saída prevista no próprio e1 para o caso de a validação ler "riscado": passando das duas bordas, a fita lê como risco sobre a moeda; rente, lê como cinta. De quebra, encurta a fita e devolve margem ao teto do acento.
3. Medir os vãos e a fita pelo anel da moeda, que o gerador vem desenhando estável: cada vão com cerca de metade da largura do anel (hoje cerca de um quarto), e a fita com cerca de metade da largura de um vão (hoje 1,4 vez).
4. Tirar os cortes dos dois pontos onde o gerador os colocou nas duas voltas. O segundo corte fica um pouco à esquerda da linha de centro vertical da moeda. O primeiro fica no meio do caminho entre a borda esquerda e o segundo, longe do vértice superior esquerdo. Assim as duas peças da esquerda saem da mesma largura e a da direita fica com mais da metade da moeda.

Esta foi a volta 2 de 3. Se na volta 3 a fita sair cortada de novo, ou os cortes voltarem para o vértice e para o centro, recomendo parar e levar ao autor com a melhor imagem até aqui e este diagnóstico, sem aprovar por cansaço.
