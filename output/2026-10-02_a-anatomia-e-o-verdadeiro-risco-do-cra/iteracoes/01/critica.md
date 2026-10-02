# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | Todos os elementos do pedido estão na imagem: lavoura, galpões, prédios e títulos que se desfiam em tiras, caixas sem texto e lidas pela forma, e o médico com lanterna de testa e bisturi indo até uma delas. |
| Uma ideia | 4 | A leitura da esquerda para a direita (origens, depois tiras, caixas e médico) se resolve de uma vez e não vira díptico. Só que os estratos formam um painel retangular fechado, e o leque de tiras começa depois da borda dele em vez de sair de dentro de cada estrato. |
| Fidelidade ao enriquecimento | 3 | Os 12 elementos estão lá, mas vários fora do lugar ou da forma pedida. O médico ocupa x 0,82–0,95 em vez de 0,62–0,80. O lacre focal está em x ~0,73, não em ~0,60. A cinta das caixas é uma faixa vertical só, não cruzada. Os prédios têm janelas e os galpões têm vão de porta. |
| Paleta e acento | 5 | Só a pilha escura, com fundo #161616 a ΔE 0,9 de #141414. O lima aparece em um ponto só, no lacre da última caixa, que é a virada. Não há cor inventada. |
| Matéria de papel | 4 | Dá para contar as camadas (bloco dos estratos, silhuetas recortadas, jaleco sobreposto ao corpo) e as bordas são cortadas. As folhas de cana são curvas, um padrão sobreponível que aqui não incomoda. |
| Leitura em miniatura | 3 | A 200px ficam bloco, leque, caixas e médico, mas o lacre de acento (o foco) vira um pixel e some. |

Média 3,83.

**Bloqueantes:** nenhum. O foco (e1) fica em x ~0,73, dentro da área segura de 0,106–0,894, então B5 não dispara. Mesmo assim, no recorte 14:10 do preview do Substack o médico perde a perna de trás, a aba do jaleco e o bisturi (x ~0,89–0,95), e o canavial perde a borda esquerda (o bloco começa em x 0,03). Esse corte é o principal motivo do REVISAR: a média fica abaixo de 4 e a capa sai cortada no preview.

**Elementos do enriquecimento ausentes:** nenhum.
- e1 (foco): presente. O lacre lima da terceira caixa está em x ~0,73 e y ~0,57.
- e2: presente, mas com cinta simples em vez de cruzada.
- e3: presente, deslocado para a direita, e o passo é mais largo que "curto".
- e4: presente, com faixa e lâmpada retangular, sem facho.
- e5: presente, baixo, na mão de trás.
- e6 e e7: presentes. A cana se lê pelos colmos com nós e pelo leque de folhas.
- e8: presente, mas com vão de porta.
- e9: presente, mas os prédios têm janelas.
- e10: presente. O picotado contorna a folha inteira, não só a borda superior, e o canto dobrado está lá.
- e11: presente como leque. As tiras saem da borda do bloco, não de dentro de cada estrato, e convergem num ponto em vez de formar um feixe horizontal que se dobra nas caixas. Nesse formato o leque corre o risco de ser lido como facho de luz.
- e12: presente. Há uma fresta nítida entre os dedos e a caixa.

**Checagens objetivas:** erros: nenhum. Os avisos foram estes:
- 10 cores ≥1% contra o teto de 7.
- #31875E e #3E946C a ΔE ~11 dos tokens mais próximos.
- #255F40 com amplitude 0,031, acima do teto de 0,028.

Na imagem nenhum deles incomoda. São tons intermediários das faces das caixas e das silhuetas, sem gradiente ou sombra visível, e não pedem mudança no prompt.

O `acento_fracao` deu 0,0 porque o lacre fica abaixo de 1% do quadro. Isso respeita o teto de acento, mas é pequeno demais para a miniatura (ver item 2).

**Em miniatura:** a 200px sobram a massa verde à esquerda com a crista do canavial, o leque claro, três cubos verdes e a silhueta clara do médico de jaleco. Galpões, prédios, grua e títulos viram textura. O lacre lima, que é o ponto focal, praticamente desaparece. O conceito "coisas viram pacote, alguém vem examinar" ainda se lê. O "qual pacote" não.

**O que mudar no prompt** (em ordem de impacto):
1. Recentralize a composição na faixa x 0,11–0,88: o bloco dos estratos começa em x ≥ 0,11, o médico fica inteiro entre x 0,62 e 0,82 (pé de trás, aba do jaleco e bisturi incluídos) e o lacre focal fica em x ~0,60, y ~0,52.
2. Aumente o lacre de acento da terceira caixa para cerca de um terço da largura da face frontal, ainda dentro do teto de 1% do quadro, para ele sobreviver a 200px de largura.
3. Diga que as tiras nascem de dentro da borda direita de cada um dos quatro estratos, como se o próprio papel do estrato se desfiasse, e que confluem num feixe horizontal de largura constante que se dobra a 45° e entra nas caixas. Não devem formar um leque que converge num ponto, que pode ser lido como facho de luz.
4. Peça cinta cruzada (vertical e horizontal) nas três caixas, prédios como blocos lisos sem janela e galpões como silhuetas lisas sem porta.

Esta é a volta 1 de 3.
