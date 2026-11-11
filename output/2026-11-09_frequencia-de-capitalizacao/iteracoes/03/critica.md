# Crítica — iteração 03 (modo dark) · gen_01 e gen_02

Conceito julgado: C1 em zigue-zague vertical centrado (`enriquecimento/v02.json`). Volta 3 de 3.
Medidas a olho sobre 1376×768 px (±10 px). Área segura universal: x 146–1230, y 27–741.

## gen_01

**Veredito: APROVADO**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 4 | Uma escada de papel sobe encolhendo até um toco que para logo abaixo de um teto, sem tocá-lo. A ideia se lê de uma vez. O 2º lance quase não encolhe em relação ao 1º. |
| Uma ideia | 5 | A hierarquia é limpa: a escada e o toco no 1º plano, a figura no 2º, teto e estrelas no 3º. Não há díptico. |
| Fidelidade ao enriquecimento | 4 | Os nove elementos aparecem, com o foco no eixo central. Desvios: o acento flutua no meio da faixa do teto em vez de alinhar com a borda de baixo; a cabeça da figura não inclina para cima; o céu saiu em pilha-2 (#0F3D27) e o teto em pilha-3, um nível acima do previsto, mas dentro da paleta. |
| Paleta e acento | 4 | Só a pilha escura, e o acento lima num único ponto, acima do toco. A figura e as estrelas (#A1D98A, 1,4%) derivaram até ΔE 23,3 do #78C9A4, perto do limite de erro. |
| Matéria de papel | 4 | Cada lance é uma tira recortada à parte, com perfil em dente de serra e frestas de céu iguais entre si. As camadas são contáveis. A fibra do fundo quase não aparece a 1K. |
| Leitura em miniatura | 4 | A 200 px a ideia se mantém. |

Média 4,17, nenhuma nota abaixo de 3.

- **(a) Funil:** larguras dos lances 630 → 533 → 300 → 120 px; alturas 200 → 130 → 110 → 66 px. O 2º lance é só ~15% mais curto que o 1º; o 3º e o toco encolhem bem. O toco (120×66 px) é um toco de verdade.
- **(b) Fresta toco–teto:** ~9 px (1,2% da altura), igual às frestas entre lances (8–12 px).
- **(c) Área segura:** toco em x 628–748, y 119–185 (centro x 688, eixo do quadro); acento y 42–71; figura x ≈330; base y ≈715. Tudo dentro.

**Bloqueantes:** nenhum.

**Elementos do enriquecimento ausentes:** nenhum. e1–e8 presentes; e9 (fibra) tênue a ponto de quase não aparecer, dentro do teto de granulação. Ressalvas que não reprovam: acento não alinhado à borda de baixo do teto (y 71 contra 110); 2º lance com ~85% da largura do 1º; cabeça da figura reta.

**Checagens objetivas:** erros nenhum. Aviso que importa: #A1D98A (1,4%) a ΔE 23,3 do #78C9A4. Tetos: 4 cores ≥1%; fundo 73,2%; granulação 0,0087–0,0096 (limite 0,028); um só matiz. Acento: o checador registra 0,0%, mas a barra lima mede ~186×29 px, ≈0,5% do quadro, dentro do teto de 1%.

**Em miniatura** (200×112 px): um zigue-zague verde-claro (~92 px) que se estreita para o alto, a faixa de teto e um traço lima logo acima do topo. A figura ainda se lê como pessoa olhando a escada; as estrelas viram pontos. A fresta (~1,3 px) some e o toco parece encostar no teto — inerente a uma fresta fina. Lê-se "escada que sobe até um limite".

## gen_02

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 3 | A escada encolhe e para sob o teto, mas o topo afina numa agulha vertical (~47×80 px) em vez de se achatar no topo. |
| Uma ideia | 4 | Leitura única: uma torre escalonada sob um teto com acento. O peso da massa engole o zigue-zague. |
| Fidelidade ao enriquecimento | 3 | Os quatro lances alternados (e3) viraram cinco blocos maciços encaixados. O toco (e1) é estreito e alto. A figura (e7) está sobre o primeiro degrau. O acento (e2) está perfeito, alinhado à borda do teto. |
| Paleta e acento | 4 | Céu pilha-1 e teto pilha-2, como especificado, lima num só ponto. Escada em #58BB85 (12,4%), ΔE 11,4 do token. |
| Matéria de papel | 4 | Peças separadas por cortes finos em dente de serra, camadas contáveis. |
| Leitura em miniatura | 4 | Forma forte, mas o zigue-zague some. |

Média 3,67. **Bloqueantes:** nenhum de B1–B10; reprova pela média e pelo desvio de forma em e1 e e3. Funil: larguras 517 → ~250 → ~150 → ~96 → ~47 px; fresta ~13 px (1,7%); toco x 668–715, y 107–190, dentro da área segura.

**O que mudar** (só se o autor reproduzir esta forma no Pro): tiras finas com céu aberto embaixo, sem blocos cheios até a base; toco mais largo que alto, sem ponta/agulha/torre; figura no céu de fundo, afastada do primeiro degrau; reforçar o tom da escada.

## Qual está mais perto

O gen_01, e ele passa. Resolve os três defeitos que derrubaram as voltas anteriores: fresta fina (~1,2%), foco no eixo e na área segura, acento achatado e embutido no teto.

**Recado para o Gate 2:** o mesmo prompt gerou as duas formas; ele acerta, mas não sempre. Se o Nano Banana Pro devolver a torre do gen_02, regerar em vez de aceitar.

**Ponto em aberto (não bloqueante pela rubrica):** o bloco de marca diz "corte a faca reto ou a 45°". No gen_01, a face de baixo das tiras é diagonal a ~15–18°, e os losangos e o trapézio da figura também não são de 45°. B9 só reprova curva livre e perspectiva, e o bloco aceita a cabeça hexagonal como exemplo, o que sugere a leitura "só retas".
