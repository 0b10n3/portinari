# Avaliação das correções — 16/11/2026 (Fase 3)

Continua `auditoria/2026-11-16.md`. As correções estão na branch `epico/15-auditoria` (10 commits,
185 testes verdes), **sem merge e sem push** até a sua aprovação.

Gerações usadas: **7 de 12**, todas do `agy` (`gemini-3.1-flash-image`), sem falha, prompt literal
nas 7. Nenhuma execução original foi tocada: os casos de teste estão em `output/_avaliacao/2026-11-16/`.

## 1. O que foi corrigido

| Achado | Estado | Commit |
| --- | --- | --- |
| M2 cores contadas por token · M3 grão no fundo é erro · acento por pixel · proporção · lado ≥96 px · peça final cobre a entrega · par light/dark | feito | `25b68b2`, `0903986` |
| M1 o pedido só fecha com a peça final importada e conferida · G5 o teto conta só imagem do `agy` | feito | `0cc8a48` |
| M4 alt-text obrigatório · P6 `COMO-GERAR` com proporção e 1K/2K/4K do Pro e "anexe a peça dark" | feito | `a0b8d6e` |
| G3 USO sem preset pede FORMATO no ingest · G4 SIZE igual ao master vira master | feito | `f1c63fd` |
| G2 uma amostra por padrão · G6 modelo de imagem lido do `agy` · M5 `estado` avisa marca antiga | feito | `cfd5d38` |
| P2 prompt em positivo · P3 instruções coerentes com o épico 14 · P4 crítico recebe a imagem primária · G1 mesmo bloqueante duas vezes volta ao Gate 1 | feito | `5cb7c07` |
| P5 hook que recusa Write/Edit fora do pipeline | feito | `6ec6e6c` |
| **N1 (novo, desta fase)** `prompt --derivada` declara o papel da referência; `entregar` recusa sem ela | feito | `e466e0b` |
| M6 zona livre da peça social · P1 bloco de marca em inglês · P7 exemplos nos agentes · P8 resumo do CONTEXT | não feito (ver auditoria §8, decisão 1) | — |

## 2. Validador, antes × depois

Mesmas 34 imagens de validação (todas as que têm modo conhecido), marca vigente (tokens 3.1.0).

| | Antes | Depois |
| --- | --- | --- |
| Imagens sem erro | 7 de 34 (21%) | 22 de 34 (65%) |
| As 8 imagens que validaram prompts entregues | 3 passam | **8 passam** |
| Erros que contradizem a crítica (imagem aprovada reprovada) | 5 | **0** |
| Imagens com erro que o crítico também mandou revisar | 2 de 2 | 12 de 12 |
| Acento medido (as 34) | 0,0% em todas | 0,0–0,9% |

Os 12 erros que restam são todos reais: cor fora da paleta (borboletas light, juro 01, frequência 01)
ou fundo abaixo de 40% (TVM, samurais, frequência 01). As outras 14 imagens que o crítico reprovou
passam no código: falharam por composição, sombra, perspectiva ou metáfora, que só o olho vê.

**Limites que sobraram, medidos nesta fase:**

- Acento abaixo de 1% no token errado não é pego (o light do juro manteve o `lime.500` do dark).
- Sombra e espessura de papel não são medidas. As entregas antigas (borboletas, CRA, juro) passam no
  código e violam a regra de hoje à vista.
- O fundo é o maior entre duas medidas que só erram para menos (cluster e token). Se aparecer um
  fundo superestimado, a troca é por região conexa à borda (comentário `ponytail:` no código).

## 3. A hipótese do par light/dark

Mesmo prompt light aprovado em cada caso, gerado de dois jeitos. Medida: IoU da silhueta
figura+acento contra a peça dark aprovada (1 = mesma composição).

| Caso | Por edição da dark | Do zero | Por edição, com `--derivada` |
| --- | --- | --- | --- |
| frequência | **0,97** | 0,19 | — |
| CRA | **0,74** | 0,26 | — |
| juro | 0,29 | 0,27 | **0,54** |
| controle: peças diferentes | 0,07–0,13 | | |

Por olho, aplicando D1–D4 da rubrica. Eu li os prompts, então não sou o crítico cego que o pipeline
usa; trate como segunda leitura.

| Imagem | D1 composição | D2 elementos | D3 pilha | D4 acento |
| --- | --- | --- | --- | --- |
| frequência, edição | igual | igual | ok | ok |
| frequência, do zero | escada redesenhada | estrelas e figura mudaram | ok | ok |
| CRA, edição | igual | igual | prédio virou papel claro | ok |
| CRA, do zero | galpões e grua mudaram | papéis diferentes | ok | ok |
| juro, edição | grade 7→5 colunas, cercado mudou | painel de retícula mudou | ok | ok |
| juro, do zero | idem, e a praia mudou | idem | ok | ok |
| juro, edição com `--derivada` | **igual** | **igual** | calendário passou de figura a pilha | ficou `lime.500` (é do dark) |

**Conclusão.** Derivar por edição vence nos três casos (média 0,67 × 0,24), mas só quando o prompt
diz ao gerador o que fazer com a imagem anexada. Os prompts light da frequência e do CRA diziam ("keep
its composition… change only the tones"); o do juro redescrevia a cena e a edição seguiu o texto.
Com a instrução, a composição do juro ficou igual; o IoU de 0,54 vem do calendário que mudou de papel
de cor. Virou código: `portinari prompt --derivada` (N1).

Os limiares do par (erro < 0,40, aviso < 0,75) se mantêm com os 10 pares medidos até agora:
composição diferente ficou entre 0,19 e 0,29; mesma composição, entre 0,53 e 0,97.

## 4. Gerações até a aprovação

Medido no histórico (45 gerações, auditoria §1). Depois das correções não houve execução real com
os seus gates, então o "depois" é estimativa.

| Fonte de desperdício no histórico | Gerações | O que muda |
| --- | --- | --- |
| Duas amostras por volta (frequência, café) | 4 | G2: uma amostra por padrão |
| Falhas do `agy` contadas no teto (coqueiros) | 3 do teto | G5: não contam |
| Uso sem formato, recusado só em `entregar` (TVM) | 4 | G3: pergunta no ingest |
| Fundo denso insistido no prompt (samurais 4, TVM 3) | 7 | G1: volta ao Gate 1 na 2ª volta igual |
| Par que diverge na derivação (juro aprovado com 0,22) | — | P4 e o par no `checar` pegam; N1 previne |

## 5. Pendências fora deste repositório

| # | Onde | O quê |
| --- | --- | --- |
| F1 | `pipelines/hemingway` | trocar "projeto ainda não criado" pelo portinari e gravar o pedido em `pedidos/` (texto na auditoria §5) |
| B1 | `brand/ILUSTRACOES/_bloco-marca.md` | fragmento em inglês e positivo por seção injetável (resolve P1) |
| B2–B4 | `brand/` | referência de linha no bloco; alias `illustration.accentOnLight` |
| C1–C6 | `brand/` | contradições da auditoria §6 |
| C7 (nova) | `brand/ILUSTRACOES/FORMATOS.md` | `substack-email`: "gerar em 5:1; não cortar de 16:9". Nenhum gerador tem 5:1 (Pro vai até 21:9; o Nano Banana 2 tem 4:1). O pipeline manda gerar em 21:9 e cortar |

## 6. O que preciso de você para fechar a Fase 3

1. **Notas de 1 a 5** (aderência à marca, força da metáfora, consistência do par) para os pares
   abaixo. Basta abrir os arquivos.
   - frequência: `output/2026-11-09_frequencia-de-capitalizacao/iteracoes/03/gen_01.jpg` com
     `output/_avaliacao/2026-11-16/freq-edicao/iteracoes/01/gen_01.jpg` e `…/freq-zero/…`
   - CRA: `output/2026-10-02_a-anatomia-e-o-verdadeiro-risco-do-cra/iteracoes/03/gen_02.jpg` com
     `…/cra-edicao/…` e `…/cra-zero/…`
   - juro: `output/2026-10-30_o-juro-tira-folga/iteracoes/03/gen_01.jpg` com `…/juro-edicao/…`,
     `…/juro-zero/…` e `…/juro-edicao-derivada/…`
2. **Aprovação para fechar:** merge de `epico/15-auditoria` em `main`, push, e a Fase 4 (README,
   CLAUDE.md, como rodar o validador e esta avaliação de novo).
3. **Uma execução real** no próximo pedido de capa, para medir gerações até a sua aprovação com
   o pipeline novo. É o único número do briefing que esta fase não conseguiu medir.
