# Portinari

Pipeline de ilustração da Syntaxis. Você escreve um pedido em três linhas; ele devolve um **prompt
pronto para colar** no Nano Banana Pro — um para a pilha escura, um para a clara — já com a paleta
da marca, o estilo, o enriquecimento da cena e o tamanho certo do canal.

Ele **não** entrega a imagem. A imagem que aparece no caminho é de validação: existe para provar
que o prompt funciona antes de você gastar uma geração boa com ele.

## Por que o entregável é o prompt

O gerador que o pipeline usa para validar (`gemini-3.1-flash-image`, pelo `agy`) sai em torno de
1K — 1376×768 em 16:9 — e não aceita parâmetro de modelo nem de resolução. O Nano Banana Pro, que
gera 2K e 4K nativos, só está disponível pela API do Gemini, que exige faturamento habilitado, ou
à mão, na interface.

Então o pipeline divide o trabalho: a máquina cuida do que é verificável — que a paleta chegue
íntegra, que nenhum detalhe da cena se perca, que o tamanho venha da marca, que nada de texto
apareça na imagem — e você cuida da geração final, com o prompt já provado na mão. Uma imagem de
validação a 1K custa quase nada e responde à única pergunta que importa antes de gerar a peça boa:
**este texto produz a imagem certa?**

## Como funciona

Quinze etapas. Cinco são subagentes (julgamento), sete são código (verificação), duas são suas
(decisão), uma é você gerando a peça.

| # | Etapa | Quem faz | O que sai |
| --- | --- | --- | --- |
| 1 | `ingest` | código | `brief.json` — pedido normalizado; o que estiver ambíguo vira pergunta, nunca chute |
| 2 | `marca` | código | `brand_snapshot.json` — paleta, tetos, formatos, estilos, tudo lido de `brand/` agora |
| 3 | Conceitos | `diretor-de-arte` | `conceitos.md` — três metáforas distintas, com ponto focal em coordenadas 0–1 |
| 4 | Crítica dos conceitos | `critico-conceito` | ranking com nota e motivo, e uma recomendação |
| 5 | **Gate 1** | **você** | escolhe o conceito |
| 6 | Enriquecimento | `enriquecedor-de-cena` | `enriquecimento/vNN.json` — a cena ganha ofício, ferramenta e detalhe de material |
| 7 | Prompt criativo | `prompter-tecnico` | `iteracoes/NN/prompt_criativo.md`, em inglês |
| 8 | `prompt` | código | `prompt_final.md` = criativo + bloco de marca + fragmento de estilo + técnico |
| 9 | `gerar` | código + `agy` | `gen_KK.jpg` — a imagem de validação |
| 10 | `checar` | código | `gen_KK.checagens.json` — paleta por ΔE, cores por token, fundo, acento, grão, proporção, par |
| 11 | Crítica visual | `critico-visual` | `critica.md` — APROVADO ou REVISAR, contra a rubrica |
| 12 | Variante do outro modo | agente + código | o mesmo, na outra pilha, por edição da imagem aprovada (`prompt --derivada`) |
| 13 | **Gate 2** | **você** | aprova **o prompt**, vendo a imagem de validação |
| 14 | `entregar` | código | `final/prompt_<modo>.md` + `COMO-GERAR.md` + `manifest.json` |
| 15 | A peça final | **você** + código | gera no Nano Banana Pro; `importar` + `checar` cada modo; só então `--concluir` |

O que cada divisão protege:

- **A marca é lida, nunca copiada.** Nenhum hex, tamanho, proporção ou fragmento de estilo mora no
  código. Mudar `brand/ILUSTRACOES/FORMATOS.md` muda o tamanho da entrega sem tocar em `.py`.
- **O bloco de marca é injetado por código**, depois que o Prompter escreve. O agente nunca tem a
  chance de resumir a paleta — e `gerar` confere, no transcript do `agy`, se os hex chegaram mesmo
  à ferramenta de imagem.
- **O enriquecimento vira contrato.** Cada elemento da cena carrega um termo em inglês obrigatório;
  `prompt` recusa (exit 2) um texto que perdeu qualquer um, e `entregar` confere de novo. É o que
  impede o detalhe de evaporar entre a cena e o gerador.
- **O crítico visual é cego ao prompt.** Ele só tem `Read` e as instruções o proíbem de abrir
  qualquer `prompt_*.md`. Julga o que está na imagem, não a intenção de quem a pediu.
- **Ninguém aprova sozinho.** Três voltas por etapa, teto de 12 gerações, e os dois gates são seus.
- **O que vai ao ar passa pela mesma régua.** O pedido só fecha quando a peça final de cada modo,
  gerada por você no Pro, foi importada e passou no `checar`.
- **Nada escreve fora daqui.** Um hook (`.claude/hooks/so_portinari.py`) recusa Write/Edit fora do
  pipeline: `brand/` e o hemingway são só leitura.

## Como rodar

```bash
cd pipelines/portinari && claude      # agentes e skill só carregam aqui dentro
/portinari pedidos/capa-cafe-lca.md
```

Você será chamado duas vezes: no **Gate 1**, para escolher entre três conceitos; no **Gate 2**,
para aprovar o prompt vendo a imagem de validação. Fora isso, o pipeline anda sozinho — e para
sozinho se estourar um limite.

No fim, `output/<data>_<slug>/final/` tem:

- `prompt_dark.md` e `prompt_light.md` — cole inteiro, um de cada vez;
- `COMO-GERAR.md` — modelo, proporção e resolução no Pro, tamanho de entrega, formato, área
  segura, o alt-text, o que conferir na imagem que voltar e os passos para fechar o pedido;
- `validacao/` — as imagens que aprovaram cada prompt.

## Como escrever um pedido

Copie `pedidos/_TEMPLATE.md`. Obrigatórios: `TITLE`, `USO`, `DESCRIPTION`.

```markdown
# TITLE: Transformação da produção agrícola em produto financeiro
**USO**: capa de post para substack
**DESCRIPTION**: a lavoura de café à esquerda se transforma num título financeiro à direita
**STYLE**: grain-textured + nostalgic
**CONTEXT**: @pipelines/hemingway/output/.../post.md
**REFERENCE IMAGES**:
```

- **USO** define tamanho, proporção, formato e área segura — vêm de `brand/ILUSTRACOES/FORMATOS.md`.
  Reconhecidos: capa e cabeçalho de e-mail do Substack, destaque do LinkedIn, post e story do
  Instagram, thumbnail do YouTube. Outro uso? informe `SIZE`.
- **STYLE** aceita **uma base** (`flat`, `grain-textured`, `risograph`, `geometric`) **e até um
  modo** (`nostalgic`, `surreal`, `minimal-vibrant`, `abstract`). Sem declarar, usa `flat`.
  `isometric` é restrito pela marca e só entra com `--piloto`. Pop art, pixel art, holográfico,
  psicodélico e doodle a marca recusa — e o pipeline diz por quê.
- **CONTEXT** aceita `@caminho/arquivo.md` (relativo à raiz do monorepo): o texto entra inteiro.
  Prefira o caminho do `post.md` a colar o post no pedido.
- Chaves em pt-BR funcionam (`TÍTULO`, `DESCRIÇÃO`, `ESTILO`, `PROPORÇÃO`, `TAMANHO`).
- `SIZE`, `ASPECT RATIO`, `RESOLUTION` e `FORMATO` servem ao USO sem preset (o template os deixa
  num comentário). Com preset, omita: a marca decide master e entrega. Se você escrever o **master**
  do uso no `SIZE` (ex.: `2560x1440` numa capa de Substack), o pipeline entende que é o tamanho de
  gerar e entrega no da marca (1456×816), com um aviso. Qualquer outro `SIZE` vence o preset.
  `pedidos/exemplo-cafe-lca.md` é a cópia byte a byte de uma fixture de teste e não deve ser editado.
- Escreveu algo ambíguo? O pipeline **pergunta**, não chuta.

## Os comandos

A skill chama todos por você; estes são os que você usa à mão.

| Comando | Para quê |
| --- | --- |
| `estado <execução>` | onde parou, quantas gerações foram gastas, qual é o próximo comando |
| `checar <execução> --iteracao N [--gen gen_KK] [--modo] [--par <imagem>]` | medir uma imagem contra a paleta, os tetos e a outra variante do par |
| `importar <execução> --iteracao N <imagem> [--modelo]` | trazer a peça final de volta para as checagens (não conta no teto) |
| `derivar <execução> <imagem> --modo <modo>` | cortar e reduzir o master para o tamanho exato do canal |
| `entregar <execução> --modo <modo> --aprovado [--concluir] [--sem-final]` | gravar o entregável; `--concluir` arquiva o pedido, e exige a peça final conferida |

Limites: `--variacoes` (padrão 1; peça 2 só para provar que o prompt aprovado é estável) e `--max-geracoes` (padrão 12, teto da
execução inteira: só imagens do `agy`, contadas em `geracoes.jsonl` e mantidas entre sessões).

## Como retomar

```bash
uv run portinari estado output/2026-09-20_meu-slug
```

Diz em que etapa parou, quantas gerações já foram gastas e qual é o próximo comando. Pode fechar o
Claude Code no meio: o estado vive em `manifest.json` e `geracoes.jsonl`, não na sessão.

## Depois, quando você gerar a peça final

```bash
# trazer cada peça de volta para as checagens (uma iteração nova por modo)
uv run portinari importar output/<execução> --iteracao 5 peca-dark.png --modelo nano-banana-pro
uv run portinari checar   output/<execução> --iteracao 5 --modo dark
uv run portinari importar output/<execução> --iteracao 6 peca-light.png --modelo nano-banana-pro
uv run portinari checar   output/<execução> --iteracao 6 --modo light --par peca-dark.png

# cortar e reduzir para o tamanho exato do canal (nunca distorce)
uv run portinari derivar  output/<execução> peca-dark.png --modo dark

# fechar: arquiva o pedido (recusa se faltar a peça conferida de algum modo)
uv run portinari entregar output/<execução> --modo light --aprovado --concluir
```

## Se algo der errado

| O que aparece | O que é | O que fazer |
| --- | --- | --- |
| `PERGUNTA AO AUTOR:` (exit 2) | o pedido está ambíguo | responda e rode de novo; nada foi chutado |
| `ERRO: brand/ está N commit(s) atrás` (exit 1) | a marca mudou no GitHub | `git -C brand pull` e rode de novo, ou `--permitir-desatualizada` se souber o que está fazendo |
| `ERRO: o prompt criativo perdeu N termo(s)` | um detalhe do enriquecimento sumiu na escrita do prompt | o prompter reescreve incluindo os termos listados |
| `ERRO: a ferramenta não recebeu os hex da paleta` (exit 4) | o LLM do `agy` reescreveu o prompt e cortou a paleta | regere o prompt; **não** siga com essa imagem |
| `ERRO:` em `checar` | regra da marca violada: cor fora da paleta, poucas cores, fundo <40%, acento >1%, grão no fundo, proporção | é reprovação: volte uma volta no prompt (o mesmo erro duas vezes: reveja o conceito) |
| `ERRO: … IoU de silhueta` | a variante não é a mesma composição da outra | derive por edição, com `prompt --derivada` |
| `PERGUNTA AO AUTOR: … informe FORMATO` | USO sem preset na marca | escreva `FORMATO: JPEG` ou `PNG` no pedido |
| ``não tem `alt` `` em `entregar` | o enriquecimento não trouxe o alt-text | peça uma versão nova ao enriquecedor |
| `falta a peça final conferida` em `--concluir` | a peça do Pro não passou pelo `checar` | `importar` + `checar`; ou `--sem-final`, que fica registrado |
| `aviso: esta execução usou a marca …` em `estado` | a marca mudou desde a execução | não reuse os prompts de `final/` sem rodar de novo |
| `teto de N gerações atingido` (exit 3) | o limite da execução acabou | `--max-geracoes` maior, conscientemente, ou pare e reveja o conceito |
| `o Gate 2 não foi declarado` | faltou `--aprovado` | só aprove depois de olhar a imagem de validação |

## O que o pipeline garante — e o que não

**Garante:** a paleta da marca chega íntegra ao gerador, e o código confere isso no transcript;
nenhum termo do enriquecimento se perde entre a cena e o prompt; o prompt entregue não depende de
nenhum arquivo deste repositório; o tamanho e o formato vêm da marca, nunca do código; nada é
aprovado sem você.

**Não garante:** que o Nano Banana Pro vá obedecer. Ele é um modelo: pode desenhar texto, inventar
cor, ignorar um detalhe — e duas amostras do mesmo prompt podem sair diferentes (no piloto, uma em
duas errou o ponto focal). Por isso `COMO-GERAR.md` traz a lista do que conferir, e `importar` +
`checar` existem para medir a peça final com a mesma régua.

**Pontos cegos conhecidos:** `checar` não vê sombra, espessura de papel, perspectiva, curva livre
nem texto desenhado (não há OCR); isso é do crítico visual. E um acento abaixo de 1% do quadro no
token errado (o `lime.500` do dark numa peça light) passa: o acento é medido pelo token do modo.

## Como rodar o validador e a avaliação de novo

```bash
uv run pytest                                  # 185 testes, um por checagem
uv run python scripts/avaliar.py               # o validador em toda imagem de output/, com a marca vigente
uv run python scripts/avaliar.py --json r.json # o mesmo, gravado para comparar com uma rodada anterior
```

A avaliação de 16/11/2026 e os números de referência estão em `auditoria/2026-11-16-avaliacao.md`;
os casos do par light/dark, em `output/_avaliacao/2026-11-16/`. Limiares e calibração estão
comentados em `src/portinari/imaging.py` (ΔE, par).

## Onde está o resto

`CLAUDE.md` tem as regras invioláveis e a fonte única de cada coisa. `docs/PLANO.md` tem as
decisões e por que cada uma foi tomada (o topo tem decisões já revogadas; vale o `SKILL.md`);
`docs/agy.md`, o que se sabe do gerador e como se sabe. `specs/epicos/` tem uma spec por épico.
`auditoria/` tem a auditoria de 16/11/2026 e a avaliação das correções.
