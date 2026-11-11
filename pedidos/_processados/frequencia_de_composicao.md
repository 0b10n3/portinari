
# TITLE: Frequência de Capitalização
**USO**: capa de post para substack
**ASPECT RATIO**: 16:9
**RESOLUTION**: 2k 
**SIZE**: 2560 x 1440 

**DESCRIPTION**: ### **A Escada de Bernoulli e o Limite "e" (Foco Histórico e Conceitual)**

Esta ideia foca na metáfora visual mais forte do texto: a escada de juros que sobe, mas encontra um teto natural representado pelo número $e$ de Euler.

- **Composição:** Uma longa escada em espiral ou diagonal, feita de dezenas de pequenas camadas de papel sobrepostas. Os degraus inferiores são largos e espaçados (marcados discretamente com "1", "2", "2,25"), mas conforme sobem, tornam-se extremamente finos, numerosos e próximos (representando a capitalização diária, por segundo, contínua), achatando-se no topo.
    
- **O Topo:** No topo da escada, que parece flutuar em um céu de fim de tarde ou noturno, brilha o número matemático "**e**" e discretamente "**2,71828...**" recortado em papel dourado ou marfim, cercado de pequenas estrelas, constelações e pequenas engrenagens que remetem ao tempo.
    
- **Elementos ao redor:** A escada pode ser ladeada por "árvores de dinheiro" ou folhagens estilizadas que também crescem em padrões geométricos. Na base, pequenas figuras humanas de papel olham ou sobem os degraus, simbolizando os matemáticos e investidores.
    


**STYLE**: papercut 

**CONTEXT**:   
File Settings

Done

Title

Description

Thumbnail

Will be cropped to a 3:2 aspect ratio

Upload

No fim do último texto, deixei uma conta para você. Por que 12% ao ano capitalizados mensalmente viram 12,68% efetivos? E qual dos dois números você de fato paga?

A resposta cabe em poucas linhas. ‘Capitalizados mensalmente’ quer dizer que o contrato divide os 12% por doze, dá 1% ao mês, e compõe esse 1% doze vezes. Cada real vira 1,01 elevado a 12, ou 1,1268.

Você paga os 12,68%. Os 12% são só a forma de cotar.

Agora altere a pergunta. E se o contrato capitalizasse todo dia? E a cada segundo?

Cada corte a mais no ano faz o juro render mais cedo, então o rendimento sobe. O texto anterior adiantou que, a 14%, o rendimento nunca passa de 15,03%. Mas por que existe um teto, se dá para cortar o ano em pedaços cada vez menores? E de onde vem esse número?

Em 1683, o matemático suíço Jacob Bernoulli fez essa mesma pergunta, com a taxa mais simples que existe: 100% ao ano.

A resposta dele explica duas coisas que parecem não ter relação. Por que o composto que você usa todo dia, o du/252 (dias úteis sobre 252) desta série, é só um caso particular. E por que o manual de opções da B3, a bolsa brasileira, faz as contas em outra taxa, que nenhum CDB (Certificado de Depósito Bancário) jamais cotou.

## Dois motores rivais

A versão que circula é mais ou menos esta.

O juro composto é o regime do mundo real: CDB, Tesouro, financiamento. A capitalização contínua é outro bicho, coisa de modelo e de quem precifica opções.

E, como capitaliza a cada instante, o contínuo seria o mais agressivo dos dois. Ou o mais preciso, conforme quem conta.

No texto anterior, apresentei três motores lado a lado, e uma linha avisava que o contínuo, com a taxa certa, dá o mesmo montante que o composto. Aquela linha merece um texto inteiro, porque diz mais do que parece: dois dos três motores são o mesmo.

O contínuo não compete com o composto. É o limite dele.

## Nominal, frequência, efetiva

Esses são os três nomes que resolvem a conta da abertura.

A taxa nominal, j, é o número escrito no contrato.

A frequência de capitalização, m, diz quantas vezes por ano o juro é incorporado ao saldo. A taxa de cada subperíodo é a taxa proporcional, j/m, que se compõe m vezes no ano.

A taxa efetiva, i, é o que de fato rendeu no fim do ano:

1+i=(1+jm)m

Com j = 12% e m = 12, sai a conta da abertura: 1,01 elevado a 12, ou 12,68%.

É a mesma embalagem da _over_ ao mês do texto anterior, em que a taxa das operações de um dia é multiplicada por 30. Linear por fora, composta por dentro: uma taxa nominal com capitalização diária.

Volte à imagem do último texto. Dentro de cada subperíodo, o juro corre em linha reta: é uma corda. Na passagem para o subperíodo seguinte, o juro vira saldo e passa a render. As cordas se emendam numa linha quebrada e, quanto maior o m, mais curtas elas ficam.

### A escada de Bernoulli

Bernoulli tomou um capital de 1, aplicado a 100% ao ano.

Com uma capitalização no ano, o capital vira 2. Com duas, de 50% cada, vira 1,5 × 1,5 = 2,25. Com quatro, 2,44. Com 12, 2,61. Com 52, uma por semana, 2,69. Com 365, uma por dia, 2,7146.

Cada degrau sobe menos que o anterior. Do anual para o semestral, o capital ganha 0,25. Do diário para o capitalizado a cada hora, ganha menos de quatro milésimos.

  

[

![](https://substackcdn.com/image/fetch/$s_!PcRK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff98ce4ee-0e24-43f5-800b-a5072ee85044_1800x1280.png)



](https://substackcdn.com/image/fetch/$s_!PcRK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff98ce4ee-0e24-43f5-800b-a5072ee85044_1800x1280.png)

Bernoulli mostrou, utilizando o binômio de Newton, que a escada nunca passa de 3.

A conta cabe em uma linha. Expandido, o fator do ano fica assim:

(1+1n)n=1+1+12!(1−1n)+13!(1−1n)(1−2n)+⋯

Os parênteses são todos menores que 1, e cada fatorial cresce mais rápido que as potências de 2. A partir do terceiro termo, a soma fica abaixo de 1/2 + 1/4 + 1/8 + …, que dá 1. O total, portanto, nunca passa de 1 + 1 + 1 = 3.

E, quanto maior o n, mais perto de 1 chega cada parêntese: a escada sobe sempre, sem passar de 3. Uma escada assim tem um topo. O topo é 2,71828…, o número que Leonhard Euler, numa carta de 1731, chamaria de e.

Até aqui, é o capítulo de taxas equivalentes (taxas diferentes que entregam o mesmo rendimento) de qualquer livro, com uma nota histórica. O interessante começa quando se trocam os 100% de Bernoulli por uma taxa qualquer.

## De onde vem o “_e_”

Troque os 100% por uma taxa nominal qualquer, j, e chame de n o quociente m/j. Então j/m = 1/n e m = n × j. O fator do ano vira a escada de Bernoulli elevada a j:

(1+jm)m=[(1+1n)n]j⟶ej(m→∞)

Para 14% nominais, o teto é e elevado a 0,14, ou 1,1503: 15,03% ao ano, o número que apareceu duas vezes no texto anterior. Para um capital C e um prazo t quaisquer, o montante no limite é C vezes e elevado a (j × t). É a capitalização contínua.

Há outro caminho até a mesma fórmula, e ele mostra a hipótese escondida.

Se o juro é incorporado a cada instante, o saldo, M, cresce a uma velocidade proporcional a ele mesmo: a taxa vezes o saldo.

dMdt=jM⟹M(t)=Cejt

O _e_ é a base em que a curva sobe, em cada ponto, a uma velocidade igual ao próprio valor. Por isso ele aparece sempre que alguma coisa cresce em proporção a si mesma.

> A hipótese embutida é que nenhum centavo fica parado, nem por um instante, e que tudo é reinvestido à mesma taxa.

É a hipótese que o texto anterior já atribuía ao composto: o juro reinvestido à mesma taxa. Muda só o tamanho do intervalo em que ele volta a render. Mesma hipótese, mesmo motor.

### Mesma curva, outra etiqueta

Agora, aquela linha do texto anterior por extenso. Pegue a convenção brasileira, 14% ao ano efetivos, e reescreva o fator de um prazo qualquer:

(1+i)t=etln⁡(1+i)=ert,r=ln⁡(1,14)=13,10%

Não é uma aproximação. É uma identidade, e por isso nenhuma das duas etiquetas, os dois jeitos de cotar a mesma taxa, é mais precisa que a outra. A curva de um CDB prefixado a 14% ao ano, com o prazo medido em du/252, é, ponto a ponto, uma curva de capitalização contínua, com taxa de 13,10%.

É isso que faz do du/252 desta série um caso particular. O composto brasileiro é o limite de Bernoulli com outra etiqueta: taxa efetiva no lugar de r = ln(1 + i), prazo medido em dias úteis sobre 252.

O mesmo vale para as frequências do meio do caminho. As cinco taxas abaixo entregam o mesmo rendimento, 14% em um ano:

- capitalização anual: 14,000%;
    
- semestral: 13,542% nominais;
    
- mensal: 13,175% nominais;
    
- diária, 252 vezes no ano: 13,106% nominais;
    
- contínua: 13,103%.
    

Quanto mais vezes se capitaliza, menor precisa ser o número cotado para entregar o mesmo rendimento. Os números descem e encostam nos 13,10% da taxa contínua.

Entre o composto e o contínuo, o que existe é uma escada de etiquetas para o mesmo rendimento, e o contínuo é o topo dela.

Para a série, isso muda o mapa. Ficam dois motores, o linear e o composto. O composto tem três etiquetas: a efetiva, a nominal com a sua frequência e a contínua.

A fama de ‘mais agressivo’ vem de comparar o mesmo número nas duas etiquetas: 14% compostos uma vez por ano contra 14% contínuos. É a conta dos 15,03% do texto anterior. Para o mesmo rendimento, o que muda é o número cotado, não o motor.

### Um aviso de vocabulário

No mercado brasileiro, ‘exponencial’ quase sempre quer dizer composto. A B3 chama a convenção de 252 dias úteis de “conversão exponencial 252”, e foi nesse sentido que o texto anterior falou em regime exponencial. O manual de opções da mesma B3 chama a taxa contínua de “taxa de juro exponencial, em regime contínuo e base anual”.

As duas taxas são exponenciais. É justamente o ponto deste texto.

## Render todo dia não é render mais

Volte aos 14% nominais e suba com eles a escada de Bernoulli.

[

![](https://substackcdn.com/image/fetch/$s_!k6Fq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89e255a6-58d0-494e-81eb-6900d713ad9d_1800x1280.png)



](https://substackcdn.com/image/fetch/$s_!k6Fq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89e255a6-58d0-494e-81eb-6900d713ad9d_1800x1280.png)

Em R$ 1 milhão aplicado por um ano, passar da capitalização anual para a mensal vale R$ 9.342,03. Da mensal para a diária (252 dias úteis), mais R$ 887,05. Da diária para a contínua, mais R$ 44,72.

Cada vez que se dobra a frequência, a distância até o teto cai quase exatamente pela metade. O ganho existe, mas some rápido.

Isso desmonta uma frase comum de propaganda: o dinheiro que ‘rende todo dia’. Rende mesmo. O CDI (no mercado, o nome da taxa DI, a dos empréstimos de um dia entre bancos) é apurado e incorporado a cada dia útil. Mas a taxa DI é divulgada como taxa efetiva ao ano, base 252, e a própria B3 registra que a capitalização acontece só em dias úteis. A capitalização diária já está dentro dos 14%.

A 14% ao ano, a taxa de cada dia útil é 1,14 elevado a 1/252, menos 1: 0,05201% ao dia. Composto 252 vezes, dá exatamente 14%. Não sobra nada para a frequência acrescentar.

Ela só acrescenta quando o número cotado é nominal. Quem lê os 14% como nominal e divide por 252 chega a 0,05556% ao dia, e a 15,02% no ano. É o erro da etiqueta, em versão de varejo.

Numa taxa efetiva, a frequência já foi paga.

Os degraus da escada encolhem assim a 14%. A distância até o teto cresce mais rápido que o quadrado da taxa, e há taxas no Brasil em que ela não some. Segundo o Banco Central, o rotativo do cartão de crédito custou 451,7% ao ano em setembro de 2026, o equivalente a cerca de 15,3% ao mês. Se a mesma taxa nominal, 12 × 15,29%, ou 183,5% ao ano, fosse capitalizada todo dia, nos 365 dias do ano, em vez de todo mês, o ano sairia por 523,9%. No contínuo, por 526,7%. A taxas assim, até o último degrau da escada vale quase três pontos percentuais.

## No munda das opções, falamos contínuo

Se composto e contínuo são a mesma curva, por que alguém se daria ao trabalho de trocar a etiqueta?

O Manual de Apreçamento de Contratos de Opções da B3, o documento com a metodologia dos prêmios de referência (os preços que a B3 calcula para cada opção) das opções negociadas em bolsa, responde na prática. Para opções sobre ações, ETFs (fundos negociados em bolsa) e índices, o manual usa a fórmula de Black-Scholes-Merton, a de preço de opções. A taxa que entra nela é a do DI futuro, o contrato futuro da B3 sobre a taxa DI, traduzida:

rn=ln⁡(1+TPren),Tn=DUn252

TPreₙ é a taxa prefixada para o vencimento n, tirada da curva do DI1 (o código do DI futuro na B3), cotado em taxa efetiva anual, base 252. DUₙ é o número de dias úteis até o vencimento.

A régua continua brasileira: o prazo é du/252. A curva também continua a mesma: e elevado a (rₙ × Tₙ) dá exatamente o fator do DI. A B3 não trocou de motor. Trocou de etiqueta.

Troca porque o modelo é escrito em tempo contínuo, e nele a etiqueta contínua facilita três coisas. As duas primeiras, o texto anterior já adiantou:

1. O retorno vira soma. Em taxa contínua, a taxa de dois anos é a soma das taxas de cada ano: 13,103% + 13,103% = 26,21%; e elevado a 0,26206 dá 1,2996, que é 1,14 ao quadrado. Na taxa efetiva, dois anos de 14% dão 29,96%, e não 28%. Para tirar de uma curva a taxa a termo (a taxa combinada hoje para um período que começa no futuro), basta subtrair os expoentes (r × T) de um prazo e do outro.
    
2. O cálculo diferencial trabalha. O modelo descreve o preço do ativo mudando instante a instante, e o preço da opção sai de uma equação diferencial. O desconto que se encaixa nela é e elevado a (−r × T): a equação dM/dt = r × M, lida de trás para a frente.
    
3. A volatilidade (a medida de quanto o preço oscila) já fala essa língua. No modelo, ela é o desvio-padrão dos retornos logarítmicos (cada um, o logaritmo da razão entre dois preços seguidos, que é o retorno em taxa contínua). Quando o manual estima a volatilidade de ativos pouco negociados a partir do histórico, é com esses retornos que trabalha.
    

No livro de opções do John Hull, que escreveu um dos textos de derivativos mais usados no mercado, o capítulo de taxas de juros trabalha em taxa contínua e mostra a conversão entre as etiquetas.

A escolha é de conveniência, não de precisão.

### Onde mora o erro

Dentro da mesma instituição, a tesouraria cota o DI em taxa efetiva, base 252, e a mesa de opções precisa de uma taxa contínua. O risco mora na passagem de uma para a outra. Quem paga fica do outro lado do balcão.

É o erro dos 15,03% que o texto anterior apontou, agora com endereço: o DI futuro a 14% colocado direto no modelo, como se fosse r.

Um exemplo simples, em cálculo próprio. Ação a R$ 100,00, sem dividendos. Opção com preço de exercício (o preço fixado no contrato) de R$ 100,00, volatilidade de 25% ao ano e vencimento em um ano (252 dias úteis).

O preço a termo da ação, o preço justo, combinado hoje, para entregá-la daqui a um ano, é R$ 114,00 com a taxa traduzida e R$ 115,03 sem a tradução. A opção de compra (o direito de comprar a ação pelo preço de exercício) sai a R$ 16,72 com r = 13,10% e a R$ 17,24 com r = 14%: 3,1% mais cara. A opção de venda (o direito de vender a ação pelo preço de exercício) sai a R$ 4,44 com r = 13,10% e a R$ 4,18 com r = 14%: 6,0% mais barata.

Do outro lado do balcão, quem compra a opção de compra cotada assim paga R$ 0,52 a mais por ação, e quem vende a opção de venda recebe cerca de R$ 0,27 a menos. A taxa estava certa. A etiqueta, errada.

Na escada dos 14%, capitalizar a cada instante em vez de todo dia vale menos de meio ponto-base (um centésimo de ponto percentual). Errar a etiqueta vale 103.

O perigo nunca foi a frequência. É a etiqueta.

## Uma pergunta antes das outras três

As três perguntas do texto anterior (motor, base, dias que contam) ganham uma que vem antes delas:

Qual é a etiqueta da taxa? Efetiva, nominal ou contínua? E, se é nominal, capitaliza quantas vezes por ano?

Com a resposta, a decisão fica simples.

Se uma das taxas é nominal e a outra, efetiva, converta antes de comparar. Os 12% nominais com capitalização mensal custam 68 pontos-base a mais do que parecem.

Se as duas têm frequências altas, diária contra contínua, e a taxa é da ordem do DI, a diferença cabe no arredondamento. Pode ignorar. Se a taxa é de cartão, não pode.

Se a taxa vai entrar num modelo, traduza sempre. A taxas da ordem do DI, o erro da etiqueta é da ordem de um ponto percentual.

Na planilha, as contas são estas:

```
Nominal (m vezes ao ano) → efetiva:   =EFETIVA(j;m)     ou  =(1+j/m)^m-1
Efetiva → nominal (m vezes ao ano):   =NOMINAL(i;m)     ou  =m*((1+i)^(1/m)-1)
Efetiva → contínua:                   =LN(1+i)
Contínua → efetiva:                   =EXP(r)-1
DI futuro → Black-Scholes:            r: =LN(1+taxa)    T: =du/252
```

E uma regra de bolso: dobrar a frequência corta quase exatamente pela metade a distância até o teto contínuo, enquanto a taxa de cada subperíodo for pequena. Para saber se a frequência importa no seu caso, compare essa distância com a precisão que o seu caso exige.

Para comparar dois CDBs, meio ponto-base some. Para replicar um preço, não: a 14%, meio ponto-base muda em quase R$ 0,04 o preço de uma LTN (Letra do Tesouro Nacional, o título público prefixado) de um ano, que paga R$ 1.000 no vencimento. No mercado, até a precisão é cláusula. Na metodologia do Tesouro Nacional para a LTN, o expoente du/252 é truncado na 14ª casa decimal e o PU (preço unitário), na 6ª. Para replicar o preço na planilha:

```
PU da LTN:   =TRUNCAR(1000/(1+i)^TRUNCAR(du/252;14);6)
```

Matemática financeira é uma das dimensões do [Syntaxis Skill Check](https://skill.syntaxis.com.br/). É um diagnóstico gratuito, que compara o seu perfil com o que o mercado espera para o próximo degrau da carreira.

## O topo da escada

Capitalizar com mais frequência rende mais, mas cada corte rende menos que o anterior. Bernoulli provou que a escada tem topo, e Euler deu a esse topo um nome. Uma taxa efetiva de 14% e uma contínua de 13,10% descrevem o mesmo dinheiro. A frequência só muda a etiqueta.

O contínuo não compete com o composto. É o limite dele.

Se o texto funcionou, você consegue ler sozinho uma taxa de que todo brasileiro já ouviu falar. Quando a meta da Selic (a taxa básica de juros) está acima de 8,5% ao ano, a poupança paga 0,5% ao mês, mais a TR (Taxa Referencial). Deixe a TR de lado. Por que os 6% ao ano que se costuma atribuir à poupança são uma taxa nominal? Quanto ela vale como taxa efetiva? E quanto vale na etiqueta que um modelo usaria?

Com a régua, o motor e agora a etiqueta, o expoente du/252 desta série está explicado de ponta a ponta.

Se este texto ajudou você a ler uma taxa pela etiqueta, encaminhe para quem ainda acha que o contínuo é o juro mais agressivo.

## Para continuar aprendendo

- Eli Maor, _e: A História de um Número_ (Record) [VERIFICAR: ano da edição] — a biografia do número, dos juros compostos de Bernoulli à notação de Euler; o apêndice sobre a existência do limite de (1 + 1/n)ⁿ é a versão completa da conta deste texto.
    
- John C. Hull, _Options, Futures, and Other Derivatives_, 11ª ed. (Pearson, 2021), cap. 4, “Interest Rates” — frequência de capitalização, taxa contínua e as fórmulas de conversão entre uma e outra (seção 4.4).
    
- Alexandre Assaf Neto, _Matemática Financeira e suas Aplicações_, 15ª ed. (GEN Atlas, 2022) — taxas nominais, efetivas e equivalentes, com a nomenclatura e os exemplos do mercado brasileiro.
    
- J. J. O’Connor e E. F. Robertson, [“The number e”](https://mathshistory.st-andrews.ac.uk/HistTopics/e/) (MacTutor History of Mathematics, Universidade de St Andrews) — o registro histórico curto: Bernoulli em 1683, o binômio, a carta de Euler de 1731.
    

---

_Os textos publicados na Syntaxis expressam exclusivamente minhas opiniões pessoais, formadas a partir da minha experiência profissional, e não representam a posição de meu empregador atual ou de empregadores anteriores. O conteúdo tem finalidade educacional e informativa: não constitui recomendação de investimento, análise de valores mobiliários ou consultoria financeira._

2026/09/11
**REFERENCE IMAGES**: <caminhos locais ou URLs, um por linha ou separados por vírgula>
