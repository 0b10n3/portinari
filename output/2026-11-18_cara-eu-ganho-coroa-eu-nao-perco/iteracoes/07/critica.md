# Crítica — gen_01 (modo dark, C7, volta 1 de 3)

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | A leitura do C7 aparece de uma vez: duas faces gêmeas, um perfil à esquerda e uma coroa à direita. Mas o "fundo liso e muito espaço vazio" do pedido preservado sumiu: o par ocupa o quadro de borda a borda. E os louros ficam no canto da moeda, longe do contorno da cabeça, e leem mais como faísca do que como louro posto na cabeça. |
| Uma ideia | 3 | A ordem de leitura é clara (lime, depois perfil, depois coroa), mas o quadro se parte em duas metades iguais no x 0,50, cada uma cheia até a borda: díptico. |
| Fidelidade ao enriquecimento | 3 | Nenhum elemento sumiu, mas há desvios. O foco tem três folhas em vez de quatro, com ~0,36 da altura da cabeça em vez de ~0,25, e metade dele fica sobre a orla. Cada moeda tem 0,43 da largura do quadro em vez de ~0,20. O vazio dos lados não existe. O perfil ganhou entalhe de boca. |
| Paleta e acento | 4 | Só aparecem #141414, #2D9E67, #78C9A4 e o lime. O acento está num ponto só, nos louros, que são a virada, e a coroa ficou fora do lime, como pedido. Ressalva: o acento está em 0,92%, colado no teto (ver item 2 abaixo). |
| Matéria de papel | 4 | Dá para contar as camadas: fundo, orla, campo vazado com o fundo aparecendo, folhas por cima. As folhas são chapadas, os cortes retos e não há sombra. Fica perto de um ícone vetorial, porque a leitura de papel depende só do grão quase invisível do fundo. |
| Leitura em miniatura | 4 | Cabeça e coroa continuam legíveis a 200 px, graças à escala exagerada. Os louros viram um ponto lime em que não se contam as folhas. |

Média 3,5: o APROVADO exige ≥ 4 e nenhum bloqueante.

**Bloqueantes:**
- **B5**: o leque de louros (o foco) começa em x ≈ 120 de 1376 px. A área segura universal do `brief.json` (0,7875 × 0,9306, centrada) começa em x ≈ 146. A ponta da folha de trás, cerca de um quinto dela, cai fora do corte 14:10 do preview. O mesmo corte come a lateral externa das duas moedas (x 68–146 e 1230–1306), que deixam de ler como octógono.
- **B6**: a ideia é uma só (cara e coroa), mas a forma virou díptico. Cada moeda enche a sua metade até 0,05 da borda, sem o vazio lateral que o e8 previa justamente contra o R13.

**Elementos do enriquecimento ausentes:** nenhum sumiu por inteiro, então a B7 não se aplica.
- **Vistos e corretos:**
  - **e3:** coroa aberta de três pontas com losango no topo, faixa embaixo, sem escudo nem cruz, no tom do fundo, sem lime.
  - **e5:** campo concêntrico, com ~0,82 da largura da moeda contra ~0,75 pedido; desvio aceitável.
  - **e6:** orla lisa e igual nos oito lados, sem serrilha. Campo liso abaixo do pescoço e em volta da coroa.
  - **e7:** vazados limpos, sem parede, com as folhas por cima e não cortadas.
  - **e9:** uma folha só de fundo, sem chão e sem margem.
  - **e10:** grão quase imperceptível, amplitude 0,0076.
- **Com desvio:**
  - **e1 (foco):** são três losangos, e o pedido é "quatro, nem mais". Cada um tem ~0,36 da altura da cabeça, contra ~0,25. As bases ficam perto do canto de trás do crânio, mas as pontas cobrem a orla, a do meio encosta na borda externa da moeda, e o pedido é "sem chegar à orla".
  - **e2:** perfil virado para a direita, com o nariz certo, crânio facetado, pescoço cortado reto e ~0,67 da altura do campo. Mas tem dois entalhes de lábio entre o nariz e o queixo, e o pedido é "sem boca".
  - **e4:** duas moedas gêmeas, de topo reto, na mesma linha de centro (y 0,50). As bordas internas saíram exatas (0,48 e 0,52), mas as moedas cresceram para fora até 0,05 e 0,95. Cada uma tem 0,43 da largura e 0,77 da altura do quadro.
  - **e8:** o vão está certo (0,042), mas o vazio de cada lado do par, que deveria ter pelo menos a largura de uma moeda, ficou em 0,05.

**Checagens objetivas:** erros: nenhum · avisos: nenhum. O que importa:
- **Acento:** 0,92% com três folhas. A quarta folha, no tamanho atual, levaria a ~1,2% e estouraria a B10.
- **Fundo:** 54,5%. Está acima do mínimo, mas longe dos 74–88% que o e9 previa; é efeito direto da escala.
- **Quarto grupo de cor:** #09100B, 1,3%, ΔE 4 do #141414. É mais escuro que o fundo e fino demais para se ver; é compatível com artefato de JPEG nas bordas entre verde e preto. Não vejo sombra, parede nem espessura de papel, então não é B8.
- **Tokens:** só três cores de token ≥ 1%, dentro da faixa de 3 a 7.

**Em miniatura:** a 200 × 112 px, sobram duas placas verdes octogonais de ~86 px. A silhueta da cabeça (~48 px de altura) e a da coroa (~49 px de largura) continuam legíveis, e a leitura cara/coroa sobrevive. Os louros viram um ponto lime de ~25 px no canto da moeda: lê como brilho, não como louro, e não se contam as folhas. No preview 14:10, as duas moedas perdem a lateral externa. Com o par reduzido a 0,26–0,30, cada moeda fica com ~55 px: cabeça e coroa ainda passam, mas as folhas precisam estar coladas ao crânio para lerem como coisa da cabeça.

**Alt-text** (o `alt` de `v04.json`): confere com o que se vê.

**O que mudar no prompt** (em ordem de impacto):
1. **Escala do par (resolve B5, B6 e o "muito espaço vazio").** O gerador acertou as bordas internas e o vão e cresceu as moedas para fora, de 0,20 para 0,43 da largura. É inflação maior que a do C4, que foi de 0,24 para 0,30–0,36. Amarre o tamanho também pela altura e pelo vazio:
   - cada moeda com cerca de um terço da altura do quadro;
   - vazio acima e abaixo maior que meia moeda;
   - à esquerda e à direita do par, vazio mais largo que uma moeda inteira;
   - o par inteiro dentro da metade central da largura.
2. **Louros.** Peça exatamente quatro folhas, cada uma com um quarto da altura da cabeça, cerca de dois terços do comprimento de hoje. O leque inteiro fica dentro do campo verde, com as bases tocando o canto de trás do alto do crânio e as pontas parando antes da orla. Reduzir as folhas é obrigatório junto com a quarta: no tamanho atual, quatro folhas estouram o teto do acento.
3. **Perfil.** Do nariz ao queixo, uma só aresta reta, sem os entalhes de lábio que apareceram.
