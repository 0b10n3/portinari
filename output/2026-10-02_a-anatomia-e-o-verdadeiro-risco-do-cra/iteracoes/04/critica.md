# Crítica: gen_01 (modo light), iteração 04, volta 1 de 3, derivação de 03/gen_02 (dark aprovado)

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | Diz o que o pedido pede em uma leitura: lavoura, galpões, prédios e títulos se desfiam em tiras, as tiras viram caixas, e o médico com lanterna de testa e bisturi vai até a última caixa. Mas nenhuma caixa tem mais a "etiqueta lisa", que é um dos três sinais de pacote que o autor citou. |
| Uma ideia | 4 | A leitura vai da esquerda para a direita, numa faixa só. As caixas e o médico ficam em primeiro plano. A coluna de estratos, clara sobre fundo claro, perdeu peso e virou um segundo plano mais fraco do que no dark. |
| Fidelidade ao enriquecimento | 4 | O foco está no lugar: o lacre de acento da última caixa, na altura da mão. Os apoios aparecem quase todos (ver lista abaixo). Só a etiqueta lisa de e2 sumiu. |
| Paleta e acento | 4 | A pilha é a clara do começo ao fim (mist, mint, chalk), com a figura em grove e o acento oliva só na última caixa. As tiras verdes das caixas saem mais escuras que #2D9E67 (ΔE 9.1), e a linha de base é cinza (#C0C6CA). Nenhuma das duas coisas reprova. |
| Matéria de papel | 4 | Dá para contar as folhas: painéis dos estratos, folhas de cana recortadas, tiras com ponta a 45°, cinta sobre a caixa e jaleco em camada. A leve sombra de borda nos painéis é aceitável. |
| Leitura em miniatura | 3 | A 200px, caixas, médico e lacre se leem bem. Já a coluna da esquerda vira um retângulo pálido com franja branca, e o estrato de baixo quase some no fundo. |

Média 3.83. Uma nota abaixo de 4 na média já impede aprovar, e há ainda o D2.

**Bloqueantes:** nenhum de B1 a B7. Na régua de derivação:
- **D2 (sumiu um elemento):** a etiqueta lisa retangular da caixa 1, que no dark aparece no canto inferior direito da face frontal, não aparece em nenhuma caixa do light. A rubrica diz que elemento que some é REVISAR.
- D1 está ok: mesmo enquadramento, mesmas massas e mesmo ponto focal, sobreponível quase pixel a pixel.
- D3 está ok: pilha clara inteira, sem tom escuro.
- D4 está ok: o acento continua na cinta e no lacre da terceira caixa, do mesmo tamanho que no dark.

**Elementos do enriquecimento ausentes:**
- Ausente: só a etiqueta lisa de e2 (veja D2).
- Presentes: e1, e2 (3 caixas, cinta, lacre, tampa a 45°), e3, e4, e5, e6, e7, e8, e9, e10, e11, e12.

Ressalva herdada do dark, que não muda o veredito: a cinta da última caixa também ficou na cor de acento, e o enriquecimento queria só o lacre. Isso já estava assim no dark aprovado e, pelo D4, deve continuar igual.

**Checagens objetivas:**
- Erros: nenhum.
- #C0C6CA (1,6%, ΔE 12.4, amplitude 0.032) e #CED9DD (amplitude 0.036): linha de base cinza e sombra/faixa do estrato de baixo. Incomodam pouco, mas são o motivo de o pé da coluna se misturar ao fundo.
- 8 cores ≥1%: vem desse mesmo cinza e do verde escuro das faces laterais das caixas. Não incomoda.
- #349369 e #43906E longe de #2D9E67: faces das caixas e calças do médico, um pouco mais escuras. Igual ao dark.
- acento_fracao 0.0: o lacre oliva é visível; ocupa menos de 1% do quadro.

**Em miniatura:** três caixas verdes em fila, a terceira com a faixa oliva, e o médico entrando pela direita. "Alguém vai abrir aquela caixa" continua de pé. A coluna da esquerda vira um bloco pálido sem estratos distintos; o estrato de baixo se confunde com o fundo.

**O que mudar no prompt** (em ordem de impacto):
1. Recoloque a etiqueta lisa: na face frontal da primeira caixa, no canto inferior direito, um retângulo pequeno chapado e vazio no tom da cinta, igual à imagem dark aprovada, sem nenhuma marca dentro.
2. Faça cada painel de estrato usar um tom da pilha diferente do fundo #E2E8F0, alternando #E6F4EE e #F7F7F5 de cima para baixo, com o estrato dos títulos em #E6F4EE e nunca em #E2E8F0, para a coluna se destacar do fundo como um bloco.
3. Desenhe a linha de base como uma tira chapada em #E6F4EE, sem sombra nem cinza, e diga que as folhas dos painéis não têm sombra projetada na borda.
4. Não mude mais nada: composição, posições, tamanhos e o acento na cinta e no lacre da terceira caixa ficam exatamente como na imagem dark aprovada.
