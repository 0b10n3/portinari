# Épico 12 — O entregável é o prompt

**Status:** implementado · **Decisão de origem:** A16, A17 (20/09/2026, PLANO).

## 1. A virada

O pipeline deixa de entregar imagem. Ele entrega **um prompt por modo**, colável, que o autor
usa à mão no Nano Banana Pro. A imagem que o `agy` gera existe para **provar que o prompt
funciona** — é evidência, não produto.

```
prompt_final.md ─▶ agy (gemini-3.1-flash-image) ─▶ gen_KK.jpg   imagem de VALIDAÇÃO (~1K)
                                                      │
                          checagens + crítico visual ─┘   o prompt está bom?
                                                      │
                                    Gate 2: o autor aprova o PROMPT vendo a validação
                                                      │
                          portinari entregar ─▶ final/prompt_<modo>.md + COMO-GERAR.md
                                                      │
                                    autor cola no Nano Banana Pro ─▶ imagem final
```

**Consequência prática:** o que antes era "a imagem está boa?" vira "o prompt produz a imagem
boa?". Uma peça só sai daqui quando a mesma instrução, dada a um gerador limpo, reproduz o
resultado — e é por isso que o prompt tem de ser autossuficiente.

## 2. O que `entregar` grava

```
final/
  prompt_dark.md      o entregável
  prompt_light.md     idem, pilha clara (E8)
  COMO-GERAR.md       instruções de uso para o autor
  validacao/          a imagem do agy que aprovou cada prompt (fora do git)
manifest.json         rastro completo
```

### `prompt_<modo>.md`

É o `iteracoes/NN/prompt_final.md` aprovado, **sem nenhuma referência ao repositório**: parte
criativa (inglês) + bloco de marca do modo (hex em prosa) + fragmento do estilo + bloco técnico.
Quem abrir o arquivo num computador sem o monorepo consegue usá-lo. Cabeçalho curto em pt-BR com
título da peça, modo, uso e a data — o resto é o prompt, pronto para `Ctrl+A, Ctrl+C`.

### `COMO-GERAR.md`

O que o autor precisa saber na hora de colar, tudo vindo de `brand/ILUSTRACOES/FORMATOS.md` (E11),
nunca escrito no código:

- **modelo:** Nano Banana Pro (`gemini-3-pro-image`), e por quê (2K/4K nativos);
- **proporção** e **tamanho de entrega** do uso, mais o master recomendado;
- **formato e peso** (JPEG q90–92 4:4:4 ou PNG, limite da plataforma), sRGB;
- **área segura** do uso: onde o ponto focal tem de cair;
- **o que conferir** na imagem que voltar: sem texto/logo/número desenhado, acento em um ponto só,
  fundo dominante, nenhuma cor fora dos hex listados no prompt;
- o que fazer se sair errado: `portinari importar` para rodar as checagens sobre a final e,
  se preciso, voltar uma volta no Prompter.

## 3. Recusas (o que impede entregar)

Só o que o código sabe verificar sem opinar:

| # | Regra |
| --- | --- |
| T1 | Existe pelo menos um `final/prompt_<modo>.md`; cada arquivo é de **um** modo só |
| T2 | Todo hex da paleta do modo aparece no prompt (a paleta é a única parte vinculante — A2) |
| T3 | Todo `termo_en` do enriquecimento vigente aparece no prompt (mesma checagem do `portinari prompt`) |
| T4 | As seções do bloco de marca estão presentes e íntegras |
| T5 | O Gate 2 foi declarado: `entregar` só grava com `--aprovado` (o gate é humano; o manifesto registra qual geração o sustentou) |
| T6 | O `COMO-GERAR.md` tem tamanho, proporção e formato — ou seja, o uso resolveu em `FORMATOS.md` |

Falha em qualquer uma = exit 2 com a lista, nada gravado em `final/`.

Mover o pedido para `pedidos/_processados/` continua sendo do **E6** (`entregar` aqui só produz o
entregável). O `manifest.json` nasce neste épico com o que ele sabe — pedido, marca, estilo,
tamanhos e uma entrada por modo entregue — e o E6 o amplia sem trocar de arquivo (decisão D3).

### Interface

```
portinari entregar <saida> --modo dark|light [--iteracao N] [--gen gen_KK] --aprovado
```

Um modo por chamada. Sem `--iteracao`, usa a última; sem `--gen`, a última geração dela — e é por
isso que T1 existe: pedir `--modo dark` apontando para uma iteração que validou a pilha clara é
recusado, não entregue calado. O prompt entregue é o `gen_KK.prompt.md` — o texto que **de fato**
gerou a imagem aprovada, não o `prompt_final.md` que pode ter mudado desde então.

## 4. O que **não** é mais responsabilidade do pipeline

- Recorte, resize e assert de dimensão exata no fim (A16): quem gera a final é o autor. Continuam
  existindo em `portinari importar`, para quando ele quiser trazer a final de volta.
- Garantir resolução de entrega: a imagem de validação é ~1K de propósito e não vai para lugar nenhum.

## 5. Testes

- `entregar` de uma execução completa grava os quatro artefatos; o `prompt_dark.md` não cita
  nenhum caminho do repositório (regex de `/`, `output/`, `brand/`).
- Cada recusa T1–T6 tem um teste com mensagem acionável e `final/` intacto.
- O prompt entregue passa nas mesmas checagens de `portinari prompt` (nenhuma regressão entre a
  iteração aprovada e o arquivo final — comparação byte a byte do corpo).
- `manifest.json` liga cada prompt entregue à geração de validação (`gen_KK`) e ao Gate 2.

## 6. Critérios de aceite

- ✔ `uv run pytest` verde.
- ✔ O piloto café/LCA termina com `final/prompt_dark.md` e `prompt_light.md` colável, e o relatório
  do E9 compara a imagem de validação (flash, 1K) com a final que o autor gerou no Pro.
- ✔ Nenhuma imagem é necessária para o pipeline terminar.
