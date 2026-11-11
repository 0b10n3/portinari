# Crítica — iteração 02 (modo dark) · volta 2 de 3

A gen_01 está mais perto: a fresta é menor, o contraste é melhor e lê melhor em miniatura. Nenhuma das duas entrega o foco.

Medidas na imagem de 1376×768 px:
- **Espelhos.** gen_01: 108, 110, 161, 60, 70 px (não monotônico). gen_02: 97, 98, 97, 83, 74 px (escada regular). Alvo (metades): ~38%, 19%, 9,5%, 4,8%, 2,4% da altura.
- **Fresta platô–teto.** gen_01: ≈59 px (7,7% da altura). gen_02: ≈144 px (18,8%). Alvo: 1–2%.
- **Acento.** O checador deu `acento_fracao 0.0` nas duas, mas o retângulo lima está visível: gen_01 ≈0,5% (61×84 px), gen_02 ≈0,87% (149×62 px).

---

## gen_01

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | Os espelhos medem 108/110/161/60/70 px: a escada não encolhe ao subir e se lê como uma escada comum que chega a uma prateleira. |
| Uma ideia | 3 | A leitura é única (figura → escada → platô → acento), mas o "quase toca" não acontece, então a virada não tem tensão. |
| Fidelidade ao enriquecimento | 2 | O foco (e1) existe como forma, mas a fresta tem ≈59 px (7,7% da altura) em vez de 1–2%. O e3 não segue a progressão de metades e o quinto degrau não vira lasca. |
| Paleta e acento | 4 | Só paleta, uma pilha, acento único sobre o joelho (≈0,5%). Os tons da escada (#78C9A4) e da figura (#2D9E67) estão invertidos em relação ao enriquecimento. |
| Matéria de papel | 3 | As folhas são chapadas e limpas, sem sombra nem rampa, mas as camadas são poucas: parece mais vetor flat que recorte. |
| Leitura em miniatura | 3 | A 200 px sobram a escada clara, a barra do platô e o quadradinho lima. A fresta cai para ≈9 px e ainda se vê, mas não se lê como "quase toca". |

**Bloqueantes:** B7. O foco e1 não foi entregue na propriedade que o define: o joelho deveria quase encostar no teto, com fresta fina, e fica a 7,7% da altura.
**Elementos do enriquecimento ausentes:**
- **Vejo:** e1 (fresta larga), e2 (o acento é vertical, 61×84 px, e não "curto e chapado"; desce 33 px para dentro da fresta), e4, e5 (duas frestas no platô, equidistantes, sem se apertar perto do joelho), e6, e7, e8 (quatro estrelas, uma de quatro pontas côncavas em vez de losango), e9 (fibra tênue).
- **Malformados:** e3 (progressão errada, sem lasca) e e7 (cabeça de frente, não inclinada para cima; borda a 117 px, 8,5% da largura).
- **Apareceu:** uma faixa de chão clara sob a figura e a escada, elemento que está nos descartados.
**Checagens objetivas:** erros nenhum. Aviso #4B9D74 (1,4%, ΔE 11,2) não importa. O fundo ocupa 67%. O acento não foi registrado pelo checador (`acento_fracao 0.0`), embora esteja visível (≈0,5%).
**Em miniatura:** uma escada verde-clara à esquerda, uma barra horizontal à direita e um ponto lima no teto. A ideia de degraus que encolhem não sobrevive porque já não existe em tamanho cheio.
**Área segura:** o foco (x≈665–747, y≈73–183) está dentro. A figura começa em x≈117, antes da margem de 10,6% (x≈146) do recorte 14:10 da prévia do Substack: fica parcialmente cortada.

---

## gen_02

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | Espelhos de 97/98/97/83/74 px: a escada é regular e o platô fica a 19% da altura abaixo do teto, ou seja, não persegue limite nenhum. |
| Uma ideia | 3 | A leitura é única, mas o acento flutua sozinho no teto, longe de tudo, e a virada não acontece. |
| Fidelidade ao enriquecimento | 2 | O foco e1 está ausente: o joelho fica a ≈144 px do teto. Também falta a progressão do e3. |
| Paleta e acento | 3 | Sem erro, mas três cores lavadas (ΔE 9,7–12) e o teto #2C4537 acinzentado. O acento ocupa ≈0,87% do quadro (149×62 px), perto do teto de 1%. |
| Matéria de papel | 3 | As folhas são chapadas, sem sombra, com fibra tênue no céu. As camadas são poucas. |
| Leitura em miniatura | 2 | A 200 px o teto escuro quase some contra o fundo, o platô vira uma prateleira no meio do quadro e o lima flutua solto. |

**Bloqueantes:** B7. O foco e1 está ausente: a fresta tem 18,8% da altura e nada "quase encosta" no teto.
**Elementos do enriquecimento ausentes:**
- **Ausente:** e1 (a fresta como foco).
- **Malformados:** e3 (degraus iguais), e2 (largo demais, ≈11% da largura em vez de 6%, e desce para dentro do céu) e e7 (cabeça de frente).
- **Vejo:** e4, e5 (três frestas escalonadas, sem se apertar perto do joelho), e6, e7 (borda a 145 px, 10,5%, no limite da área segura), e8 (quatro losangos) e e9.
- **Apareceu:** a faixa de chão descartada, como na gen_01.
**Checagens objetivas:** erros nenhum. Avisos: três cores de figura e camada com ΔE 9,7–12, isto é, paleta lavada. Não reprovam, mas pesam na nota. O fundo #1E1E1E ocupa 66%. O acento não foi registrado pelo checador, embora esteja visível (≈0,87%).
**Em miniatura:** uma escada média, uma barra mais ou menos no meio da altura e um retângulo lima solto no alto. Não se lê relação entre os três.

---

## O que mudar (em ordem de impacto, vale para as duas)

1. **Progressão com regra relacional, sem coordenadas:** "o primeiro degrau sozinho é mais alto que todos os outros somados; cada degrau tem metade da altura do anterior; o último é uma lasca tão fina quanto as frestas do platô".
2. **Platô rente ao teto, com a fresta ancorada num elemento visível:** "o topo do platô corre colado sob o teto, separado dele só por uma linha de fundo da mesma espessura das frestas do platô".
3. **Acento inteiro dentro do teto e achatado:** quatro vezes mais largo que alto, borda de baixo alinhada à do teto, sem descer para a fresta.
4. **Figura além de um oitavo da largura, cabeça inclinada para cima,** olhando o joelho.
5. **Proibir o chão pelo nome:** a figura e o primeiro degrau pousam direto sobre o fundo.
6. **(Menor) Tons de figura:** a inversão da gen_01 (escada #78C9A4, figura #2D9E67) lê melhor em miniatura; decidir de propósito.

**Limite:** a próxima é a volta 3 de 3. Se ela não mostrar espelhos visivelmente decrescentes e o platô a 1–2% do teto, o veredito é parar e levar ao autor — o mesmo padrão de geometria exata que não convergiu em A Corda e o Arco. Saída a oferecer: reduzir para quatro degraus.
