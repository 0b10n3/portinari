# Crítica — iteração 01 (modo dark) · gen_01 e gen_02

Volta 1 de 3. A gen_01 é a mais próxima; as duas reprovam.

---

## gen_01

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | Escada, teto, céu noturno, figura e estrelas estão lá, mas os cinco degraus têm a mesma altura (~93 px cada), e o salto final até o platô é ainda maior (~107 px): a imagem diz "escada comum", não "retorno decrescente". |
| Uma ideia | 3 | Leitura única (escada → teto → acento), mas o platô parece uma caixa à parte, colada na escada, e não o achatamento dela. |
| Fidelidade ao enriquecimento | 2 | O foco (lasca final quase encostando no teto, fresta fina e constante) não existe: o topo do platô fica a ~67 px (≈9% da altura) do teto, e não há lasca. |
| Paleta e acento | 3 | Todas as cores são da pilha escura e o acento é um só, no ponto certo, mas os papéis estão trocados: a escada está em #125233 (pilha) em vez de #2D9E67 (figura), e o teto em #1B6A45 em vez de #0F3D27. |
| Matéria de papel | 3 | Dá para contar as folhas (teto, céu, escada, platô, figura) com corte reto, mas as frestas do platô são lentes de ponta afilada, e o conjunto lê mais vetor do que papel. |
| Leitura em miniatura | 3 | Sobram a massa verde em L, a tira de teto e o traço lima: lê-se "escada até uma prateleira sob um teto"; que os degraus encolhem, não se lê. |

**Bloqueantes:**
- **B10** — erro em checagens: o fundo medido ocupa 26%. A medição pegou a moldura verde de ~20 px (#135032, mesmo tom da escada) como fundo; o céu #161616 ocupa 57%. A moldura em si também é defeito (não é hairline e não deveria estar na imagem).
- **B7** — o elemento `foco` e1 está ausente: não há lasca final rente ao teto nem fresta fina; o vão é largo e o platô sobe acima do último degrau num salto.
- **B9** — as três frestas do platô são lentes de ponta afilada (curva livre), não cortes retos.

**Elementos do enriquecimento ausentes:**
- e1 (foco) **ausente**: vão largo, sem lasca final.
- e3 (apoio) sem a propriedade central: os cinco degraus existem, mas não encolhem.
- e4 (apoio) parcial: o platô vai do joelho à borda direita, mas é uma caixa grossa, não fica rente ao teto e não continua a escada.
- e5 (textura) parcial: três frestas, em lente, que não se apertam perto do joelho.
- e2 presente: retângulo lima colado no teto, bem acima do início do platô.
- e6 presente (cor errada).
- e7 presente, mas a ~6% da borda esquerda (o pedido era >10%, e o recorte 14:10 corta em 10,6%), pés cortados pela borda de baixo, cabeça sem inclinação clara para cima.
- e8 presente: quatro estrelas, mas de lados côncavos, não losango.
- e9 quase imperceptível.

**Checagens objetivas:** erro: o fundo ocupa 26% (artefato da moldura; ver B10) · aviso #59AC70 (1,1%, ΔE 8,9 de #2D9E67), deriva da cor da figura, sem peso · acento medido em 0,0%, embora o retângulo lima esteja visível (~0,25% do quadro); a deriva do JPEG tira da tolerância e não é defeito.

**Em miniatura:** um campo preto com a massa verde da escada em L ocupando a metade esquerda, um retângulo preto vazio embaixo à direita, a tira verde do teto e um traço lima no meio do alto. A figura vira um ponto verde no canto. Lê-se "subir até perto de um teto"; "cada degrau sobe menos", não.

**O que mudar** (em ordem de impacto):
1. Os degraus devem encolher de forma visível: cada um com metade da altura do anterior, o primeiro tão alto quanto todos os outros somados, o quinto uma lasca.
2. A lasca final e o platô ficam na mesma altura, logo abaixo do teto, separados dele por uma fresta fina e constante (cerca de 1–2% da altura), sem salto entre a escada e o platô.
3. O platô vira uma única tira horizontal fina, contínua com a lasca, até a borda direita, com duas ou três frestas retangulares retas que se apertam perto do joelho.
4. Remover a moldura: a colagem vai até as bordas da imagem.
5. Escada e platô em #2D9E67, figura e estrelas em #78C9A4, teto em #0F3D27, céu em #141414.
6. A figura a mais de um décimo da borda esquerda, pés inteiros sobre a linha de base, cabeça hexagonal inclinada para o acento.
7. Estrelas em losango de lados retos, quatro.

---

## gen_02

**Veredito: REVISAR**

| Critério | Nota | Por quê |
| --- | --- | --- |
| Fidelidade ao pedido | 2 | Escada, teto, céu, figura e estrelas presentes, mas os degraus sobem por igual (~98 px, salvo um primeiro degrau anômalo de ~22 px), e o platô é uma laje que flutua acima da escada. |
| Uma ideia | 2 | Escada de banzo diagonal mais laje inclinada em 45° leem como dois objetos (escada e prateleira), e a margem branca transforma a peça em "quadro emoldurado". |
| Fidelidade ao enriquecimento | 2 | O foco não existe: a laje fica a ~120 px (≈16% da altura) do teto; não há lasca nem fresta fina. |
| Paleta e acento | 1 | #FFFFFF em 19% do quadro (ΔE 42,9): cor fora da paleta e, na prática, o tom da pilha clara (#F7F7F5) dentro de uma peça escura. |
| Matéria de papel | 3 | A fibra no céu dá papel, e as folhas são contáveis, mas os filetes escuros sob as lâminas (#072213) sugerem espessura ou sombra. |
| Leitura em miniatura | 2 | A escada #145A36 sobre o céu #0A3A24 quase some; o que sobra é a moldura branca, a tira preta, o traço lima, a figura clara e as estrelas. |

**Bloqueantes:**
- **B1** — #FFFFFF ocupa 19,1% do quadro (erro em checagens).
- **B2** — a margem branca é, na prática, o tom de chalk, da pilha clara, numa peça escura.
- **B10** — erro em checagens: o fundo medido ocupa 19% (a medição tomou a margem branca por fundo; o céu ocupa 55%).
- **B7** — o foco e1 está ausente: vão largo entre a laje e o teto, sem lasca final.
- **B8** (provável) — filetes escuros sob as tiras do platô (#072213, ΔE 13,5, a cor mais escura da imagem e fora da escada de tons): leio como sombra de contato ou espessura de papel.

**Elementos do enriquecimento ausentes:**
- e1 (foco) **ausente**.
- e3 (apoio) sem a propriedade central: degraus de altura igual, mais um banzo diagonal que não foi pedido.
- e4 (apoio) parcial: laje com ponta em 45°, solta acima da escada e longe do teto (pode ler como uma face oblíqua, ou seja, perspectiva).
- e5 (textura) parcial: dois cortes entre tiras, sem o aperto perto do joelho.
- e2 presente: retângulo lima colado no teto, sobre o início do platô.
- e6 presente: teto em #141414 em vez de #0F3D27 (céu e teto trocados).
- e7 presente e bem posicionada (~14% da borda, de pé no primeiro degrau, cabeça facetada levemente inclinada).
- e8 presente: cinco losangos (o pedido fixava quatro; o autor aceita de 3 a 5).
- e9 presente: fibra visível no céu.

**Checagens objetivas:** erros: #FFFFFF em 19,1% e fundo em 19% · avisos que importam: #072213 (1,3%, ΔE 13,5), ver B8; #A8D8AE (1,3%, ΔE 12,7 de #78C9A4), a figura e as estrelas derivam para mais claro · acento medido em 0,0% pela mesma deriva de JPEG da gen_01.

**Em miniatura:** uma moldura branca grossa domina; dentro, um retângulo verde-escuro com uma tira preta no alto e um traço lima. A escada some no céu. Ficam a figura clara e os cinco losangos. O argumento não chega à miniatura.

**O que mudar** (em ordem de impacto):
1. Remover a margem branca: a colagem ocupa a imagem inteira, de borda a borda.
2. Os degraus devem encolher (cada um com metade da altura do anterior, o quinto uma lasca), sem banzo diagonal por baixo.
3. O platô vira uma tira fina, contínua com a lasca, na mesma altura, rente ao teto por uma fresta fina, sem a ponta em 45° e sem flutuar.
4. Nenhum filete escuro sob as tiras: cada tira encosta direto no céu.
5. Escada e platô em #2D9E67, para contrastar com o céu na miniatura; teto em #0F3D27, céu em #141414.

---

**Qual está mais perto:** a gen_01. Não tem cor fora da paleta, o céu já é o fundo dominante, a escada contrasta com o céu e o acento está exatamente sobre o início do platô. A gen_02 só ganha na posição da figura e no recorte das estrelas, e as duas coisas valem levar para a próxima volta.

**O argumento central aparece?** Pela metade. "Sob o teto, sem tocá-lo" se lê nas duas: o acento pende do teto e há um vão, mais claro na gen_01. "Degraus que encolhem até um platô" não se lê em nenhuma. Os degraus sobem por igual, o vão é largo em vez de fino e o platô é um objeto separado (caixa na gen_01, laje na gen_02), não o achatamento da escada. A mudança 1 (progressão em metades) e a mudança 2 (lasca e platô colados ao teto por uma fresta fina) são as que decidem a próxima volta.
