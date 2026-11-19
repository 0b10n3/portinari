# Crítica — gen_01 (modo dark, C4, volta 1 de 3)

**Veredito: REVISAR** — pela checagem objetiva, sem acionar o crítico visual (`SKILL.md`, passo 10:
exit 2 de `checar` já é REVISAR).

**Erro da checagem:** o acento #CDF163 ocupa 1,5% do quadro; o teto da marca é 1%
(`illustration.accentMaxCoverage`). Demais medidas: 4 cores de token ≥1%, fundo #141412 em 63%.

**Observações do orquestrador** (descrição do que se vê, não nota de rubrica):
- O que o C4 pedia e saiu: duas moedas octogonais iguais, do mesmo tamanho, na mesma linha de centro,
  com o octógono concêntrico da face; a da esquerda em três peças separadas por dois cortes retos que
  mostram o fundo; uma fita de acento só, só sobre a da esquerda. Nenhuma peça extra, nenhuma
  moldura, nenhum "=".
- A fita é larga e comprida: vai de x ~0,08 a ~0,48, passando bem das bordas da moeda, e por isso
  estoura o teto. A ponta esquerda (x ~0,08) fica fora da área segura do brief (x 0,106–0,894).
- As moedas inflaram: cada uma tem ~0,36 da largura do quadro, contra ~0,24 do conceito.
- Os cortes não deixam "duas tiras estreitas junto à borda esquerda": saíram em x ~0,21 e ~0,28 do
  quadro, deixando uma peça larga à esquerda, uma tira estreita no meio e uma peça larga à direita.
  A ordem cupom, cupom, principal se perde.
- Risco de leitura a confirmar pelo crítico numa volta sem erro de checagem: uma faixa horizontal
  sobre uma moeda pode ler como "riscado".

**O que mudar no prompt** (volta 2 de 3):
1. Fita de acento bem mais fina (cerca de metade) e mais curta, passando só um fio das bordas da
   moeda da esquerda, para ficar abaixo de 1% do quadro e dentro da área segura.
2. O par mais compacto e menor no quadro, descrito por relação (fundo vazio dos dois lados pelo
   menos tão largo quanto uma moeda), sem número absoluto.
3. Os dois cortes perto da borda esquerda da moeda, deixando duas tiras estreitas e iguais à
   esquerda e uma peça larga com o resto.
