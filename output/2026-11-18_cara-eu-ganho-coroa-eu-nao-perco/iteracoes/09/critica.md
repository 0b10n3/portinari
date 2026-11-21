# Crítica — gen_01 (modo light, derivação da primária aprovada em iteracoes/08, C7)

**Veredito: APROVADO**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | A peça diz o mesmo C7 da primária em uma leitura. São duas faces gêmeas de topo reto na mesma linha de centro: a cara à esquerda, com quatro folhas de acento atrás da cabeça, e a coroa à direita, inteira e sem acento. A ressalva vem da primária e tem de continuar igual na derivação: o leque abre desde o vertical até "para trás e para baixo", com a folha de baixo na altura da nuca. |
| Uma ideia | 4 | O bloco é o mesmo da primária: compacto no centro, com vão de ~0,055 e fundo dos quatro lados. Há uma ressalva própria do claro. O acento #5F7D1C é mais escuro que o campo e fica perto da escuridão da orla (1,4:1 entre os dois), então ele lidera pela cor, não pela luz. A primeira olhada se divide entre as duas orlas verde-escuras e o tufo oliva. Isso vem do token lime.700, não do prompt. |
| Fidelidade ao enriquecimento | 4 | Os dez elementos estão lá e o foco está no lugar. As cores seguem a inversão que e4, e5 e e6 preveem para o claro: orla em figura-principal, campo em figura-secundária, vazados mostrando a pilha-3. Os desvios de escala do e4 (moedas a ~0,31 da largura) e do e8 (vazio lateral de ~0,17) são os mesmos da primária, como deviam ser. |
| Paleta e acento | 5 | Só aparecem #F7F7F5 (fundo, ΔE 0,0), #78C9A4 (campo, ΔE 3,6), #2D9E67 (orla, ΔE 6,1) e o oliva das folhas. Nenhum tom da pilha escura sobrou. O acento fica num ponto só, com 0,33% do quadro (0,31% na primária), e a coroa ficou no tom do fundo. |
| Matéria de papel | 4 | Dá para contar as mesmas quatro camadas: fundo, orla, campo vazado mostrando o fundo e folhas por cima. Os cortes são retos, sem sombra e sem parede. Continua perto de um ícone vetorial, um pouco mais que no escuro, porque o grão do fundo claro é ainda mais tênue (amplitude 0,0056). |
| Leitura em miniatura | 4 | A 200 px, a cara e a coroa ainda são silhuetas reconhecíveis, mas com menos contraste que na primária: silhueta #F7F7F5 sobre campo #78C9A4 dá ~1,8:1, contra 5,4:1 no escuro. O tufo oliva fica preso à nuca, mas não se contam as quatro folhas. |

Média 4,2 (25/6). Nenhuma nota abaixo de 3 e nenhum bloqueante.

**Bloqueantes:** nenhum.
- **B1, B2 e B10:** `checagens.json` não tem erro. A pilha é só a clara, com quatro cores ≥ 1% (o teto é 7), fundo de 74,6% (o mínimo é 40%) e acento de 0,33% (o teto é 1%).
- **B3:** não há letra, número nem marca. A orla é lisa nos oito lados, e o campo é liso abaixo do pescoço e em volta da coroa.
- **B5:** o foco vai de x ≈ 295 a 385 e de y ≈ 248 a 385 (num quadro de 1376 × 768). A área segura universal do `brief.json` vai de x 146 a 1230 e de y 27 a 741, então o foco cabe inteiro. As duas moedas (x 228–1148) também cabem no corte 14:10.
- **B8:** a amplitude de luminância é 0,0056 no fundo, 0,0052 no campo e 0,0091 na orla. Olhando, não vejo sombra sob as moedas, nem degrau escurecido entre orla e campo, nem parede ou borda escura nos vazados, nem halo em volta do par.
- **B9:** cabeça, coroa, moedas e folhas são todos poligonais, e nada está entreaberto ou em perspectiva.
- **Derivação (D1–D4):** o IoU do par é 0,97, acima de 0,75, então não exigia exame minucioso. Abri as duas imagens assim mesmo.
  - **D1 (composição):** confere. As moedas estão nos mesmos x (228–650 e 725–1148) e no mesmo y (~170–598), com o mesmo enquadramento e o mesmo ponto focal. Nas duas, o perfil tem o topo reto em y ≈ 282, a ponta do nariz em x ≈ 555 e o pescoço cortado em y ≈ 498, e a faixa da coroa vai de x 848 a 1025. A troca de tom entre orla e campo é o mapeamento de cor que o v04 prevê para o claro: as massas não mudaram.
  - **D2 (elementos):** confere. As quatro folhas têm as mesmas posições e os mesmos ângulos (incluindo a de baixo, voltada para a nuca). A coroa mantém os três losangos no topo e a faixa solta das pontas por um filete de campo, e a orla continua lisa. Nada sumiu e nada apareceu. Nesta resolução, não vejo diferença de forma introduzida pela edição.
  - **D3 (pilha):** confere. Fundo em pilha-3, figuras em #2D9E67 e #78C9A4, acento em #5F7D1C. O #E6F4EE (1,2%) também é da pilha clara (ver checagens).
  - **D4 (acento):** confere. Ocupa o mesmo ponto, com o mesmo leque e o mesmo tamanho relativo (0,33% contra 0,31%).

**Elementos do enriquecimento ausentes:** nenhum.
- **e1 (foco):** quatro losangos oliva, iguais e inteiros, sem haste e sem fita, colados sobre o campo. As bases ficam no canto de trás do crânio, sem entrar no vazado, e o leque para antes da orla. No claro, o contraste das folhas contra o campo é de ~2,4:1, como o e1 previa.
- **e2:** perfil virado para a direita, com crânio facetado de topo reto, nariz em cunha, recuo reto sob a ponta e pescoço retangular cortado reto. Sem olho, orelha, cabelo ou boca.
- **e3:** coroa aberta de três pontas, cada uma com um losango, e faixa embaixo. Sem escudo nem cruz, no tom do fundo.
- **e4:** gêmeas regulares de topo reto, no mesmo y e simétricas em torno do centro, com a orla em #2D9E67, como prevê a inversão do claro. A escala é a mesma da primária.
- **e5:** campo concêntrico em #78C9A4, com ~0,81 da largura da moeda.
- **e6:** orla lisa de ~40 px, igual nos oito lados e sem serrilha.
- **e7:** os vazados mostram só o fundo #F7F7F5, sem parede, e nenhuma folha de acento foi cortada.
- **e8:** vão de ~0,055. O vazio lateral de ~0,17 é o mesmo da primária.
- **e9:** uma folha de fundo só, de borda a borda, sem chão e sem margem.
- **e10:** grão quase imperceptível (amplitude 0,0056).

**Checagens objetivas:** erros: nenhum · avisos: nenhum. O que importa:
- **Fundo:** 74,6% (75,9% na primária).
- **Acento:** 0,33%, com as quatro folhas.
- **Tokens ≥ 1%:** #F7F7F5 (74,4%), #78C9A4 (14,0%), #2D9E67 (9,8%) e #E6F4EE (1,2%).
  - O #E6F4EE não aparece como folha visível. Ele corresponde à faixa de transição de ~3 px nas bordas entre o verde e o branco (o contorno das moedas e dos vazados) e ao croma do JPEG. É também mais ou menos o 1,3 ponto que falta ao fundo em relação à primária. Olhando a imagem, não há folha menta, halo em volta das moedas nem vazado tingido. E, sendo da pilha clara, não toca a B2.
- **Par:** IoU 0,97 com a primária.

**Em miniatura:** a 200 × 112 px, ficam duas placas octogonais de ~61 px, com um anel verde-escuro de ~6 px em volta do campo menta. Elas ficam separadas por ~11 px de branco quente e têm fundo dos quatro lados.
- A cabeça (~32 px de altura) e a coroa (~35 px de largura) aparecem em branco sobre menta e leem pela silhueta, mais suaves que o preto sobre verde da primária. A leitura cara/coroa sobrevive.
- Os louros viram um tufo oliva de ~13 × 20 px preso à nuca. Ficam separados da orla por ~3–5 px de menta e se distinguem dela pelo matiz mais que pela luz.
- No recorte 14:10 do preview, o par fica inteiro. Numa página branca do Substack, o fundo #F7F7F5 quase some na página e o par fica solto. Isso é esperado no claro, e quem dá o frame é o hairline da página.

**Alt-text** (o `alt` de `v04.json`): confere com o que se vê.

**O que mudar no prompt:** nada, a variante clara está aprovada. Ficam duas ressalvas para o autor no Gate 2, e nenhuma delas pede nova volta:
1. **Ressalvas herdadas da primária** (a escala do par a ~0,31 e a folha de baixo do leque voltada para a nuca): se o autor quiser corrigir, a correção vai na primária e a clara é derivada de novo. Corrigir só a clara quebra D1 e D2.
2. **Hierarquia no claro:** o acento lidera pelo matiz, não pela luz, e as silhuetas ficam a ~1,8:1 contra o campo. As duas coisas vêm do token #5F7D1C e da inversão orla/campo que o v04 escolheu para dar 2,4:1 às folhas, não de uma frase do prompt. Aceitar como está.
