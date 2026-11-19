# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

Não há bloqueante e nenhuma nota ficou abaixo de 3, mas a média é 3,5, abaixo do mínimo de 4.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | Tudo o que o pedido lista está na imagem: moeda octogonal chapada, face lisa com o octógono concêntrico, mão de polegar erguido no canto inferior esquerdo, chão vazado e acento numa faceta. Mas a moeda está no centro exato (x 0,50), não "um pouco à direita". O vazado que fica embaixo dela é o pequeno do meio, não o grande. E os "dois bem pequenos" saíram médios e de tamanhos diferentes. |
| Uma ideia | 4 | A hierarquia é limpa: a moeda clara no alto vem em 1º, a fileira de vazados em 2º e a mão em 3º, sem díptico. A ressalva é que o joinha e os vazados em tamanho crescente puxam leituras paralelas ("curtir", "crescimento"). |
| Fidelidade ao enriquecimento | 3 | Os onze elementos estão lá e o foco está dentro da área segura. Quatro deles saíram fora da posição, da medida ou do gesto pedidos: e1 em x 0,50 em vez de 0,60, e6 em x 0,69, e7 com ~0,50 e ~0,60 da largura do grande, e e9 num joinha em pé. |
| Paleta e acento | 4 | Só a pilha escura e nenhuma cor inventada. O acento lime cai num único trapézio, o de cima à direita, e ocupa 0,35% do quadro. Houve deriva: a mão e o miolo da moeda saíram mais escuros que #2D9E67, o anel mais amarelado que #78C9A4, e o chão caiu no nível 2 da pilha. |
| Matéria de papel | 4 | Dá para contar as folhas: céu, chão, vazados que mostram o céu, anel de oito trapézios com as juntas, miolo colado por cima, faceta lime e mão. A fibra tênue fica só no fundo. A mão em facetas de dois tons puxa mais para low-poly que para papel recortado. |
| Leitura em miniatura | 3 | A moeda e o ponto lime sobrevivem a 200 px. Os vazados, porém, leem como degraus crescentes, a mão lê como joinha, e a relação "moeda → vazado grande" não se forma, porque o grande fica na diagonal da moeda. |

**Bloqueantes:** nenhum. B1/B2: só a pilha escura, sem erro de ΔE. B3: nenhum texto, número ou símbolo. B5: moeda, mão e vazados dentro da área segura universal (x 0,106–0,894). B6: uma cena só, sem díptico. B7: o foco e todos os apoios presentes. B9: a moeda e os vazados são octógonos de topo reto, a mão é poligonal, tudo em elevação frontal sem perspectiva. B10: tetos dentro. B8: nenhuma sombra projetada, parede escurecida ou rampa visível nesta escala (ver checagens).

**Elementos do enriquecimento ausentes:** nenhum.
- **Vejo como pedido:**
  - e2: miolo com ~0,63 da largura da moeda.
  - e3: oito trapézios no mesmo tom, com juntas retas.
  - e4: um só trapézio lime, o de cima à direita.
  - e8: as pontes deixam os três vazados separados, mas saíram mais largas (~0,047 e ~0,059 do quadro) e diferentes entre si.
  - e10: céu liso e vazio entre a mão e a moeda.
  - e11: fibra tênue no céu e no chão.
- **Presentes, mas fora do descrito:**
  - e1: moeda centrada em x 0,50 e com ~0,18 de largura, contra 0,60 e 0,15.
  - e5: chão a partir de y ~0,57, no nível 2 (#0F3D27) e não no nível 4.
  - e6: vazado grande com ~0,91 da largura da moeda (certo), mas centrado em x 0,69, fora do eixo dela.
  - e7: os pequenos têm ~0,50 e ~0,60 da largura do grande, diferentes entre si, em x ~0,36 e ~0,50. O do meio é o que fica exatamente sob a moeda.
  - e9: punho em pé, quatro dedos dobrados em gomos separados, polegar quase vertical, em dois verdes. É o joinha que o "punho deitado" deveria evitar.

**Checagens objetivas:** sem erros. São 7 cores com ≥1% do quadro, no teto; o fundo ocupa 57,9%, o acento 0,35% e o grão do céu mede 0,010. Avisos que importam:
- **#328059 (ΔE 8,5) e #297551:** são a mão e o miolo da moeda, mais escuros que a figura. O #2D9E67 não aparece na imagem.
- **#90C494 (ΔE 10,4):** é o anel da moeda, mais claro e amarelado que #78C9A4.
- **Variação de 0,034 dentro de #297551:** olhei a folha. A variação está nas facetas e nas juntas da mão, sem sombra projetada nem gradiente visível, então não fecho B8. Mesmo assim, a mão não é de um tom só (item 4).
- **Chão:** caiu inteiro perto de #0F3D27 (#1A4430 + #143E2A). Com isso, o contraste dos vazados (céu sobre chão) fica em ~1,7:1, contra ~2,8:1 se o chão fosse #1B6A45.

**Em miniatura:** a 200 px (200×112), o céu preto e a faixa verde se separam bem. A moeda vira um octógono verde-claro de ~37 px, e o ponto lime ainda aparece no canto de cima à direita. Os três vazados viram manchas escuras de ~17, ~20 e ~33 px, que leem como uma escada crescente. A mão vira uma cunha verde de polegar para cima, um joinha. Sobra "moeda no ar sobre três buracos", mas não "o buraco grande é o molde dela".

**Alt-text:** confere no essencial (mão, moeda octogonal, molde em três peças no chão). Ajuste do alt, não do prompt: trocar "em três peças que a somam" por "em três peças, duas pequenas e uma grande, logo abaixo dela". A soma não se vê na imagem; a composição em tamanhos, sim.

**O que mudar no prompt** (em ordem de impacto):
1. Pôr a moeda e o vazado grande no mesmo eixo vertical, em x 0,60, com o grande exatamente sob a moeda. Hoje o que fica embaixo dela é o vazado pequeno do meio, e a leitura "é ali que ela cai" se perde.
2. Fazer os dois vazados pequenos idênticos entre si e com um terço da largura do grande. Hoje eles têm ~0,50 e ~0,60 dela, e a fileira lê como degraus de crescimento, não como dois cupons iguais e um principal.
3. Trocar a mão pelo plano B pré-autorizado no Gate 1: mão aberta, palma para cima, dedos juntos num só polígono. O gerador entregou exatamente o joinha vertical que o punho deitado deveria evitar, e em miniatura ele lê como "curtir".
4. Seja qual for o gesto, descrever a mão como uma única folha lisa de #2D9E67, com as facetas só no recorte do contorno e nenhuma faceta em outro tom. Hoje ela sai em dois verdes mais escuros que a figura.
5. Ancorar o chão pelo hex #1B6A45 (nível 4). Ele saiu no nível 2 (#0F3D27), colado no tom do céu, e os vazados perdem contraste.
6. Ancorar o anel da moeda pelo hex #78C9A4. Ele saiu #90C494, mais amarelado, o que o aproxima do lime e dilui a faceta que ganha.
