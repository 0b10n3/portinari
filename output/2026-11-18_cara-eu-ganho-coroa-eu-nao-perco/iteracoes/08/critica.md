# Crítica — gen_01 (modo dark, C7, volta 2 de 3)

**Veredito: APROVADO**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | A peça diz o C7 em uma leitura. São duas faces gêmeas de topo reto na mesma linha de centro: a cara à esquerda, com quatro folhas de lime atrás da cabeça, e a coroa à direita, inteira e sem acento. Agora há fundo vazio em volta (75,9% do quadro). Ressalva: o leque abre desde o vertical até "para trás e para baixo", e a folha de baixo fica na altura da nuca, não "no alto". Ainda assim, as folhas saem do crânio e leem como coisa posta na cabeça, não como a faísca no canto da moeda da volta 1. |
| Uma ideia | 4 | A ordem de leitura é limpa: o lime, depois o perfil, depois a coroa. O par é um bloco compacto no centro, com vão de 0,055 e fundo dos quatro lados. Ressalva: o vazio de cada lado (0,17 da largura) é metade do que o e8 pede, então o par ainda ocupa dois terços da largura. |
| Fidelidade ao enriquecimento | 4 | Os dez elementos estão lá e o foco está no lugar: quatro folhas sobre o campo, com a base no crânio, fora do vazado e antes da orla. Os desvios são de escala: cada moeda tem 0,31 da largura em vez de ~0,20, e o vazio lateral é menor que uma moeda. |
| Paleta e acento | 5 | Só aparecem #141414, #2D9E67, #78C9A4 e o lime das folhas. O acento fica num ponto só, na virada (os louros), com 0,31% do quadro, e a coroa ficou no tom do fundo. |
| Matéria de papel | 4 | Dá para contar as camadas: fundo com grão, orla, campo vazado mostrando o fundo, folhas por cima. Os cortes são retos, sem sombra e sem parede. Continua perto de um ícone vetorial, porque a leitura de papel depende do degrau entre orla e campo e de um grão quase invisível. |
| Leitura em miniatura | 4 | A 200 px, a cabeça e a coroa ainda são silhuetas reconhecíveis e o lime fica preso à cabeça, mas não se contam as quatro folhas. |

Média 4,2 (25/6). Nenhuma nota abaixo de 3 e nenhum bloqueante.

**Bloqueantes:** nenhum. Os dois da volta 1 caíram:
- **B5:** o foco vai de x ≈ 295 a 385 e de y ≈ 248 a 385 (num quadro de 1376 × 768). A área segura universal do `brief.json` vai de x 146 a 1230 e de y 27 a 741, então o foco cabe inteiro. As duas moedas também cabem (x 228–1148), com ~80 px de folga de cada lado no corte 14:10.
- **B6:** o par deixou de encher as metades. Cada moeda tem 0,31 da largura (era 0,43), com 0,17 de fundo de cada lado e 0,22 acima e abaixo. O par lê como um objeto no meio do quadro, não como díptico.

**Elementos do enriquecimento ausentes:** nenhum.
- **Vistos e corretos:**
  - **e1 (foco):** quatro losangos de lime, iguais e inteiros, sem haste e sem fita, colados sobre o campo. As bases encostam no canto de trás do crânio sem entrar no vazado, e o leque para antes da orla. Cada folha tem ~55–65 px, perto de um quarto da altura do perfil (~217 px). Desvio leve: o leque cobre ~130°, do vertical até para trás e para baixo, e o pedido é "para trás e um pouco para cima".
  - **e2:** perfil virado para a direita, com o nariz em cunha apontando para a direita, crânio facetado de topo reto e pescoço retangular cortado reto, sem olho, orelha ou cabelo. Ocupa ~0,63 da altura do campo. Os dois entalhes de lábio da volta 1 sumiram: do nariz ao queixo resta só o recuo sob a ponta da cunha.
  - **e3:** coroa aberta de três pontas, cada uma com um losango no topo, e faixa retangular embaixo. A faixa está solta das pontas por um filete de campo, como na volta 1. Sem escudo nem cruz, no tom do fundo, com ~0,69 da largura do campo.
  - **e5:** campo concêntrico, com ~0,81 da largura da moeda.
  - **e6:** orla lisa de ~40 px, igual nos oito lados e sem serrilha. O campo fica liso abaixo do pescoço e em volta da coroa.
  - **e7:** os vazados mostram só o fundo chapado, sem parede, e nenhuma folha de acento foi cortada.
  - **e9:** uma folha de fundo só, de borda a borda, sem chão e sem margem.
  - **e10:** grão quase imperceptível (amplitude 0,0072).
- **Com desvio:**
  - **e4:** as moedas são gêmeas, regulares, de topo reto, no mesmo y (centro em 0,50) e simétricas em torno de x 0,50. Mas cada uma tem 0,31 da largura e 0,56 da altura do quadro. O pedido é ~0,20 da largura, e a volta 1 pediu ~1/3 da altura. As bordas ficam em x 0,17–0,47 e 0,53–0,83.
  - **e8:** o vão tem 0,055, dentro dos ~0,06 previstos. O vazio de cada lado tem 0,17, e o pedido é "pelo menos uma moeda" (0,31).

**Checagens objetivas:** erros: nenhum · avisos: nenhum. O que importa:
- **Fundo:** 75,9% (era 54,5%), dentro dos 74–88% que o e9 previa.
- **Acento:** 0,31% com as quatro folhas (era 0,92% com três), com folga até o teto de 1%.
- **Tokens:** três cores ≥ 1% (#141414, #2D9E67, #78C9A4), com ΔE de 0,5, 6,7 e 7,2. O quarto grupo escuro da volta 1 (#09100B, 1,3%) não reapareceu.
- **Rampa:** a amplitude de luminância é 0,010 nas duas folhas de figura e 0,0072 no fundo, nada que sugira rampa. Olhando a imagem, não vejo sombra entre orla e campo nem borda escurecida nos vazados.

**Em miniatura:** a 200 × 112 px, ficam duas placas octogonais verdes de ~61 px, separadas por ~11 px de preto e com fundo dos quatro lados. A cabeça (~32 px de altura) e a coroa (~35 px de largura) continuam legíveis, e a leitura cara/coroa sobrevive. Os louros viram um tufo lime de ~13 × 20 px preso à nuca. Lê como algo posto na cabeça (na volta 1 era um ponto solto no canto da moeda), mas não se contam as folhas. No recorte 14:10 do preview, o par fica inteiro.

**Alt-text** (o `alt` de `v04.json`): confere com o que se vê.

**O que mudar no prompt:** nada, a peça está aprovada. Ficam duas ressalvas para o autor no Gate 2, e nenhuma delas pede nova volta:
1. **Escala:** o gerador encolheu o par de 0,43 para 0,31 da largura, mas não chegou a ~0,20. Parou no teto da inflação que o próprio e4 previa (0,26–0,30). Se o Pro inflar mais na peça final, o vazio lateral é o primeiro a sumir.
2. **Leque:** a folha de baixo aponta para trás e para baixo. Se o autor quiser um louro mais de vencedor e menos tufo, basta uma frase no e1: as quatro pontas entre o vertical e o horizontal para trás, nenhuma abaixo. O custo é uma volta, e ela arrisca o que já acertou.
