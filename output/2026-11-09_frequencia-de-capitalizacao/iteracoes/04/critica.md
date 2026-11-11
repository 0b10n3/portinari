# Crítica — gen_01 (modo light)

**Veredito: APROVADO**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | A escada em zigue-zague sobe, encolhe a cada lance e para num toco achatado logo abaixo do teto, com a figura olhando de baixo: a ideia "sobe sempre, nunca alcança" se lê de uma vez. |
| Uma ideia | 5 | Uma leitura só: a barra de acento e o toco no eixo central são o 1º plano, a escada é o 2º, a figura e as estrelas nas laterais vazias são o 3º. |
| Fidelidade ao enriquecimento | 4 | Todos os elementos com forma estão lá e o foco está no lugar. A fibra de papel (e9) não aparece e a barra de acento fica no meio da faixa do teto, sem encostar na borda de baixo, igual ao dark aprovado. |
| Paleta e acento | 4 | Céu em chalk (#F6F8F7 ≈ #F7F7F5), teto em mist (#D3DDE7 → #E2E8F0, ΔE 4,5) e acento oliva de `lime.700` num ponto só, mas as duas figuras saíram mais escuras que os tokens (ΔE 12,6 e 9,5). |
| Matéria de papel | 4 | Dá para contar as folhas (céu, teto, os quatro lances separados por frestas, figura, estrelas) com bordas retas de corte, mas o light parece mais vetor chapado que papel: a fibra que dava matéria no dark sumiu. |
| Leitura em miniatura | 4 | A 200 px o funil verde e a barra oliva sob a faixa clara ainda contam a ideia; o degrau teto/céu é fraco e a fresta do foco some. |

Média 4,17 · nenhuma nota abaixo de 3.

**Bloqueantes:** nenhum.
- B1/B2: zero erros; só a pilha clara (mist + chalk) mais as figuras grove; nenhum tom da pilha escura.
- B3: sem texto, número, sigla ou símbolo.
- B5: dentro da área segura universal (x 10,6–89,4 %, y 3,5–96,5 %). Toco em x 46–54 %, y 15–24 %; acento em y 5,5–9,2 %; figura em x 24–28 %; base da escada em y ≈ 93 %.
- B8: sem sombra, brilho nem gradiente (amplitude de luminância ≈ 0,006 em todas as massas). Na borda de baixo do teto aparece uma linha de transição de 1 px; a 1K ela se lê como borda de tom, não como parede escurecida. Conferir na peça final.
- B9: só polígonos. Estrelas em losango de lados retos, cabeça hexagonal, corpo em trapézio, degraus em dente de serra, sem perspectiva.
- B10: 4 cores ≥1 % · fundo 72,9 % (mínimo 40 %) · acento ≈ 0,5 % (barra de ≈ 186×29 px; máximo 1 %) · granulação 0,006 (máximo 0,028) · um matiz de pilha.

**Derivação (contra iteracoes/03/gen_01.jpg):**
- D1 (mesma composição): sim. Cada massa no mesmo pixel.
- D2 (mesmos elementos): sim. Quatro lances, um toco, uma barra, uma figura, quatro estrelas.
- D3 (pilha do modo novo, inteira): sim. Céu = pilha-3 chalk, teto = pilha-1 mist, como manda o e6 para o light.
- D4 (acento no mesmo ponto e tamanho): sim. #CDF163 (lime.500, dark) → oliva ≈ #5F7D1C (lime.700, light), o token certo.

**Elementos do enriquecimento ausentes:** só o e9 (fibra de papel no céu), invisível no chalk. e1–e8 presentes; e2 no meio da faixa do teto, como no dark.

**Checagens objetivas:** erros nenhum. Avisos: figura principal #228964 contra #2D9E67 (ΔE 12,6) e secundária #5DAF8E contra #78C9A4 (ΔE 9,5), mais escuras que o token — conferir no Pro. `acento_fracao: 0.0` é falha do checador (a barra tem ≈ 0,5 % e não vira cluster próprio); corrigir no código, não no prompt.

**Em miniatura:** a 200 px sobra o funil verde no centro, a barra oliva no alto, a figura à esquerda e quatro pontinhos. A faixa do teto quase se funde com o céu; quem marca o limite é a barra oliva. A fresta some e o toco parece encostar, como no dark aprovado.

**O que mudar no prompt:** nada; aprovado.
