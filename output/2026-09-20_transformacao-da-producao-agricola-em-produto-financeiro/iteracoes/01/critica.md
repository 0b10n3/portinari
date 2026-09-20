# Crítica — iteração 01 (modo dark), gen_01 e gen_02

## gen_01 — **Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | Café à esquerda e documento à direita, mas a transformação não acontece: três objetos lado a lado (saca, folha lisa atrás, pilha), não um material que muda de estado. |
| Uma ideia | 3 | O retângulo grande atrás da saca é massa própria e disputa a leitura; o olho conta objetos em vez de seguir uma passagem. |
| Fidelidade ao enriquecimento | 3 | e1 (foco) meio cumprido: a costura abre e o fio sai, mas o pano não segue liso — a folha é outro plano, atrás. e12 com dois grãos, não três. Os outros 10 presentes. |
| Paleta e acento | 4 | Nada fora da paleta, acento num ponto só; mas 10 cores ≥1% e #2C8558 a ΔE 11,2 de #1B6A45 mostram a pilha se esparramando em degraus intermediários. |
| Matéria de papel | 4 | Estrado, remendo, canto puído, furos e canto dobrado: dá para contar as camadas. Sobra sombreamento macio em algumas dobras. |
| Leitura em miniatura | 3 | Sobra "saco + cartão em branco + pilha". O cartão do meio é ruído e a transformação não sobrevive. |

**Bloqueantes:** B7, no limite e contado como não cumprido — e1 existe como costura com fio, não como o mesmo plano seguindo liso.
**Checagens:** sem erro. Os dois avisos são o mesmo fato visível — a saca ganhou verdes de sombreado entre as folhas chapadas e o fundo subiu para #242424. Sobreponível (A2), mas aqui nenhum pedido do autor justifica ceder.

## gen_02 — **Veredito: APROVADO**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 5 | Café à esquerda, produto financeiro à direita, e no meio o pano deixa de ser trama e vira folha lisa — o pedido inteiro numa leitura. |
| Uma ideia | 4 | Três planos claros; o drapeado claro disputa por um instante com a saca, mas a diagonal empurra o olho na direção certa. |
| Fidelidade ao enriquecimento | 4 | Os 12 elementos visíveis, foco literal e central. Descontos: e11 termina em ~x 0,91 (o enriquecimento pediu antes de 0,78) e e8 virou uma barra em vez de três tábuas. |
| Paleta e acento | 5 | Zero avisos, maior ΔE 6,6, sete cores, fundo 57%, fio de acento num traço único exatamente na virada. |
| Matéria de papel | 4 | Camadas contáveis, dobra a 45° com verso mais escuro, remendo e canto puído recortados dente a dente. |
| Leitura em miniatura | 4 | Saca escura à esquerda, faixa clara em diagonal, pilha à direita: a passagem continua legível. |

Média 4,33 · nenhuma nota abaixo de 3 · nenhum bloqueante.

**Elementos ausentes:** nenhum. e8 em forma reduzida; e11 estourando x 0,78.
**Checagens:** sem erro e sem aviso. Nada a ceder.

## Qual vai ao Gate 2

**gen_02** — é a única das duas em que a transformação acontece dentro do material (a trama termina e vira folha lisa, com o fio de acento na emenda), e vem com checagens limpas.

## O que as checagens não resolvem

**(a) O acento existe.** `acento_fracao: 0.0` é artefato de medição. Nas duas imagens o fio em tom lima está desenhado, num único ponto, saindo de onde a costura abre; tem 2–3px, área muito abaixo do bin de 1% com que o contador agrupa cores. Nada a corrigir.

**(b) Texto alucinado: nada encontrado, nas duas.** Saca só com faixas chapadas cruzadas e pontinhos de costura no remendo — nenhum carimbo, peso, safra, sigla ou moldura. Pilha com folhas completamente vazias, furos de picote e canto dobrado — nenhum selo, fita, algarismo ou linha de assinatura. Os descartes do enriquecimento pegaram.

**A vigiar (não bloqueante):** a grade quadriculada de gen_02 na passagem trama→liso é uniforme e lê como malha de tecido, mas é o tipo de padrão que, em resolução maior, pode escorregar para cara de código.

## O que mudar no prompt (opcional, para reduzir a variância entre amostras)

gen_02 aprova o prompt como está. Para a próxima geração acertar com mais frequência, em ordem de impacto:

1. Dizer que a folha lisa **é a continuação do mesmo pano saindo da boca da saca**, na mesma profundidade, nunca uma folha separada atrás dela (é o que gen_01 errou).
2. Pedir que a pilha **termine antes de 78% da largura**, com espaço vazio à direita (as duas foram a ~91% e perdem o canto dobrado no preview 14:10).
3. Trocar a grade fina de quadrados da trama por **poucas faixas largas chapadas**, o vocabulário já usado no flanco da saca.
4. Reforçar **três** grãos e o estrado como **três tábuas retas** visíveis.
