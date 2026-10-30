# Crítica — gen_01 (modo dark)

**Veredito: REVISAR** — 4ª volta, extra e autorizada pelo autor, com o mesmo bloqueante B5 das três anteriores. **Recomendação: parar e levar ao autor.** Mais uma volta que só reescreva coordenadas ou o gesto não resolve; ver "Para levar ao autor" no fim.

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | Estão na imagem as cinco figuras, a arma que vira rolo, a névoa em três degraus de fundo, o velho no tom secundário e o acento só nos rolos. Mas o gesto que o autor pediu depois da 3ª volta não aparece: o velho segura o feixe numa palma estendida, à frente do corpo, em vez de junto ao peito com os cotovelos dobrados. Além disso, o menino está em passada. |
| Uma ideia | 4 | Lê-se de uma vez, da esquerda para a direita: o feixe Lime em 1º plano, o velho claro em 2º e a fileira em 3º. Ressalva: um homem curvado sobre um retângulo luminoso, no fim de uma fileira de humanos, lembra o meme da "evolução que termina curvada diante da tela". |
| Fidelidade ao enriquecimento | 2 | Todos os elementos aparecem, ao menos em parte, mas o foco está fora do lugar pela 4ª vez. O feixe tem centro em x≈0.88 e termina em x≈0.94; o pedido era centro em x≈0.78, nunca além de 0.82. A fileira inteira também se espalhou: centros em x≈0.12 · 0.27 · 0.43 · 0.63 · 0.78, contra 0.17 · 0.31 · 0.45 · 0.59 · 0.73. |
| Paleta e acento | 4 | Seis massas de cor, todas a ΔE ≤ 3 da pilha escura, sem nenhum tom da pilha clara, e Lime só no feixe. A única licença é a faixa de chão no verde de figura (#2D9E67): os pés se fundem no piso e a cor de figura vira folha da pilha. |
| Matéria de papel | 4 | Dá para contar as camadas: quatro tons de fundo com cortes verticais retos e figuras chapadas por cima, com um leve deslocamento de sombra. As frestas de corte (e11) quase não aparecem, e por isso as silhuetas parecem mais vetor do que papel. |
| Leitura em miniatura | 3 | A 200px a ideia sobrevive: cinco perfis, um fundo que escurece e um ponto Lime. Mas o ponto Lime fica colado na borda direita, e o preview 14:10 corta quase metade dele. |

Média 3,3, com uma nota abaixo de 3. Mesmo sem o bloqueante, a imagem não passaria.

**Bloqueantes:**
- **B5 — o foco está fora da área segura.** A área segura do `brief.json` vai de x 0.106 a x 0.894. O feixe vai de x≈0.83 a x≈0.94, então ≈40% dele fica de fora: o preview 14:10 do Substack mostra só ≈58% do feixe. A miniatura 3:2 que o próprio pedido cita (x 0.081 a 0.919) também corta as pontas dos eixos. É a 4ª volta seguida com este bloqueante.

**Elementos do enriquecimento ausentes:** nenhum elemento sumiu por inteiro, então não há B7. Vários aparecem só em parte:
- **e1, feixe (foco).** Presente: cinco rolos contáveis, cordão no meio e pontas do eixo. Mas está fora da coordenada e da área segura, e não fica junto ao peito.
- **e2, velho.** Presente, no tom secundário e com o maior contraste do quadro. Mas o centro está em x≈0.78 em vez de 0.73, e a cabeça em y≈0.33–0.40 em vez de y ≤ 0.30.
- **e3, homem perto dos 50.** Presente: ereto, mãos vazias, cabos à frente. Mas as bainhas são enormes, mais longas que a espada do homem de 29. Atravessam o vão para trás até x≈0.52, e os cabos quase tocam o velho.
- **e4, homem de 29.** Presente: é o mais alto e segura a espada em diagonal a 45°. Mas a espada é mais curta que as bainhas do vizinho e quase do tamanho da do menino. A ponta para em x≈0.59, quase encostando na nuca do homem seguinte, em vez de parar no meio do vão (x≈0.54).
- **e5, jovem de armadura.** Presente e bom: elmo com a proteção de nuca em degraus e ombreira quadrada.
- **e6, menino.** Presente, mas segura a espada com uma mão só, está em passada (o pé de trás na ponta) e tem a cabeça em y≈0.39.
- **e7, três folhas de fundo.** Presente e o melhor elemento da imagem: três folhas opacas, atrás das figuras, com cortes em x≈0.20 · 0.37 · 0.56, todos no meio dos vãos.
- **e8, pontas do eixo e cordão.** Presente.
- **e9, hakama.** Parcial: o homem perto dos 50 e o velho usam hakama; o de 29 está de túnica curta e pernas à mostra.
- **e10, pés assentados e passo regular.** Parcial: o menino está em passada, e o vão entre a 3ª e a 4ª figura é ≈35% mais largo que os outros (≈0.21 contra ≈0.15).
- **e11, frestas de corte.** Fracas.
- **e12, entrega com as duas mãos.** Parcial: só uma palma aparece sob o feixe.

**Checagens objetivas:**
- **Erros:** nenhum. Seis massas de cor, ΔE máximo de 3,0.
- **Aviso "fundo 29% < 40%":** não incomoda. É efeito da decisão do autor pelas três folhas de fundo: a pilha inteira ocupa ≈67% do quadro, e só a folha base fica com 29%.
- **`acento_fracao` 0,0:** a checagem não isolou o Lime, porque o feixe é menor que o limiar do agrupamento de cores. Na imagem o acento está lá, pequeno e só nos rolos, sem excesso.

**Em miniatura (200px):** a imagem fica com ≈200×112px. Sobram cinco perfis verdes sobre faixas que escurecem até o preto, com o velho, mais claro, em destaque. O feixe vira um retângulo Lime de ≈21×8px colado na borda direita. Espadas e bainhas viram linhas de 1 a 2px, ainda legíveis como diagonais. A névoa que se dissipa se lê bem. Dois riscos:
- No preview 14:10, o ponto Lime aparece cortado e as costas do menino também.
- Um retângulo luminoso diante de uma figura curvada pode ser lido como tela.

**O que mudar no prompt** (em ordem de impacto; cada item é uma mudança de prompt):
1. Estreite a fileira inteira em vez de mexer só no gesto. Diga que o conjunto, do pé de trás do menino à ponta do feixe, ocupa só a faixa central do quadro, com fundo vazio nos dois lados. À direita do feixe deve sobrar uma faixa de fundo base pelo menos tão larga quanto o próprio velho. Encurte o passo entre as figuras para caber.
2. Prenda o feixe ao corpo por uma relação anatômica, não por coordenada. Por exemplo: "o feixe encostado no peito, os dois antebraços dobrados por baixo, os cotovelos colados ao tronco, e nenhuma parte dele passa à frente da ponta do nariz do velho".
3. Encurte as bainhas do homem perto dos 50: as pontas não devem passar mais de um palmo atrás das costas. A espada do homem de 29 deve ser a linha mais longa do quadro, com a ponta parando no meio do vão. Isso devolve o passo regular entre a 3ª e a 4ª figura.
4. Ponha o menino com os dois pés assentados, lado a lado, e as duas mãos na espada. A passada atual reforça a "marcha do progresso".
5. Vista o homem de 29 com hakama em trapézio até os pés, como os dois homens seguintes.
6. Detalhe menor: faça o chão terminar no fundo base ou numa folha da pilha, e não no verde de figura.

**Para levar ao autor:**
- **O diagnóstico.** O B5 reprovou as quatro voltas, e esta mostra a causa. Não é só o gesto: a fileira ocupa ≈88% da largura, do pé do menino (x≈0.06) ao fim do feixe (x≈0.94), e a área segura tem 79%. Mesmo que o gerador tivesse obedecido o "junto ao peito", com o velho em x≈0.78 o feixe ficaria entre x≈0.80 e 0.90 e continuaria fora. E o gerador não obedeceu o gesto novo.
- **As decisões que só o autor toma:**
  - **(a)** Aceitar uma fileira menor ou mais apertada (figuras ≈15% menores, ou passo de ≈0.12), com margem vazia nos dois lados. Mantém o conceito e perde um pouco de escala em miniatura.
  - **(b)** Mudar a forma do feixe: menor e em pé, com os rolos na vertical, abraçado ao peito. Encolhe a largura do foco, mas troca o "deitados lado a lado".
  - **(c)** Redefinir a área segura desta peça como 16:9 + 3:2 (a miniatura do Substack que o pedido cita), aceitando o corte do preview 14:10. Mesmo assim o feixe precisa recuar ≈2% da largura.
  - **(d)** Parar aqui e registrar este como o melhor estado, com o diagnóstico.
- **Recomendação.** Não autorizar uma 5ª volta que só reescreva coordenadas ou o gesto, porque isso falhou quatro vezes. Se houver 5ª volta, que ela parta de (a) ou (b), escolhidas pelo autor. Os itens 3 a 6 acima podem ir na mesma volta.
