# Crítica — gen_01 (modo dark)

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 5 | A fita/borboleta do atrator de Lorenz se desfia claramente numa mesa com executivo trabalhando feliz — exatamente o verbo do pedido. |
| Uma ideia | 4 | Leitura única e fluida (a fita conecta o emaranhado ao executivo), mas o vão entre as duas massas (canto superior-esquerdo vs. inferior-direito) deixa um respiro grande que, num primeiro olhar, sugere quase duas cenas antes de se perceber a fita ligando-as. |
| Fidelidade ao enriquecimento | 5 | Os 8 elementos de v01.json aparecem: emaranhado (e2), pilha de folhas soltas (e5), trecho de transição facetada (e3), dobra de acento no ponto de virada (e4), mesa + executivo sem rosto de mãos no teclado (e1, foco), fundo liso (e6), xícara de papel dobrado (e7) e pilha de documentos ao lado do laptop (e8). |
| Paleta e acento | 4 | `checagens.json` não registra erro (paleta cumprida); acento único e no ponto certo, junto à tela do laptop, como pede e4. Mas 13 cores ≥1% do quadro (teto orientativo é 3–7) e vários avisos de ΔE 8–16 mostram muita variação tonal entre facetas da fita; uma delas (#33644A) passa o teto de amplitude por folha (0.030 > 0.028), sinal de sombra/gradiente dentro de uma mesma folha. |
| Matéria de papel | 4 | Dobras, facetas e camadas são legíveis e dá para contar os planos, mas a variação tonal contínua ao longo da fita lembra mais shading progressivo do que folhas chapadas e uniformes — soa levemente contra o "flat" pedido. |
| Leitura em miniatura | 4 | A 200px resta um traço diagonal verde ligando um nó emaranhado (canto superior-esquerdo) a uma pequena massa retangular com silhueta (canto inferior-direito) sobre fundo preto; a leitura "caos virando trabalho" ainda se sustenta, mas mãos, xícara e pilha de documentos somem. |

**Bloqueantes:** B5 — o grupo mesa+executivo (foco, e1) e o apoio pilha-de-documentos (e8) se estendem até ~94% da largura do quadro (borda direita do tampo da mesa e da pilha de papéis), passando do limite direito da área segura de `brief.json` (fração 0,7875 de largura, ou seja, x máximo ≈0,894 do quadro). Esse é exatamente o corte usado no preview 14:10 do Substack e no recorte 1,91:1 (LinkedIn/OG) — ambos vão cortar a ponta da pilha de papéis e a quina da mesa nessa composição.

**Elementos do enriquecimento ausentes:** nenhum — todos os 8 elementos de v01.json estão presentes, incluindo o foco (e1).

**Checagens objetivas:** erros: nenhum. Avisos que importam: 13 cores ≥1% do quadro (teto orientativo 3–7) — visível na imagem como muitas variações de verde na fita, deixando-a com aspecto mais "sombreado" que chapado, mas sem quebrar a leitura de papel recortado; uma folha (#33644A) passa o teto de amplitude tonal (0,030 > 0,028), coerente com o aspecto de shading contínuo citado acima. Nenhum desses é bloqueante por si (padrão sobreponível, A2), mas somados reforçam a nota 4 (não 5) em paleta e matéria de papel.

**Em miniatura:** a 200px de largura, sobra um traço diagonal verde-escuro sobre fundo preto, ligando um nó emaranhado à esquerda a uma massa retangular com silhueta à direita — a ideia de "transformação" ainda passa, mas só como forma, sem nenhum detalhe de mesa de trabalho.

**O que mudar no prompt** (em ordem de impacto):
1. Recuar o conjunto mesa + executivo + pilha de documentos (e1/e8) para a esquerda, ou reduzir a largura da pilha de papéis ao lado do laptop, de forma que toda a extremidade direita da mesa fique dentro dos ~89% centrais do quadro — hoje ela avança a ~94% e seria cortada no preview 14:10 do Substack e no recorte 1,91:1 do LinkedIn.
2. Pedir tom único e chapado por faceta da fita (sem variação de sombra dentro da mesma folha), para reduzir a contagem de cores do quadro (hoje 13, teto orientativo é 3–7) e reforçar o caráter "flat" da peça.
3. Se o autor aceitar, aproximar um pouco mais o emaranhado (esquerda) e a mesa (direita) para reduzir o respiro central e deixar a leitura de "uma ideia só" ainda mais imediata — item de menor impacto, cede se o autor preferir manter o espaçamento atual.
