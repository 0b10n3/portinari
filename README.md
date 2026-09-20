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
| 10 | `checar` | código | `gen_KK.checagens.json` — paleta por ΔE, cores, fundo, acento, granulação |
| 11 | Crítica visual | `critico-visual` | `critica.md` — APROVADO ou REVISAR, contra a rubrica |
| 12 | Variante do outro modo | agente + código | o mesmo, na outra pilha, por edição da imagem aprovada |
| 13 | **Gate 2** | **você** | aprova **o prompt**, vendo a imagem de validação |
| 14 | `entregar` | código | `final/prompt_<modo>.md` + `COMO-GERAR.md` + `manifest.json` |
| 15 | A peça final | **você** | cola o prompt no Nano Banana Pro |

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
- `COMO-GERAR.md` — modelo, tamanho de geração, tamanho de entrega, formato, área segura e o que
  conferir na imagem que voltar;
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
- Chaves em pt-BR funcionam (`TÍTULO`, `DESCRIÇÃO`, `ESTILO`, `PROPORÇÃO`, `TAMANHO`).
- Você pode escrever `SIZE`, `ASPECT RATIO` e `RESOLUTION`: **o que você escreve vence o preset**.
  Cuidado com o efeito colateral — escrever `SIZE: 2560x1440` numa capa de Substack faz o pipeline
  entender 2560×1440 como a **entrega**, e você perde a distinção entre o que se gera e o que se
  publica. Omita `SIZE` para a marca decidir os dois (gerar 2560×1440, entregar 1456×816).
  `pedidos/exemplo-cafe-lca.md` traz o caso, de propósito: é a cópia byte a byte de uma fixture de
  teste e não deve ser editado; `pedidos/capa-cafe-lca.md` é a versão que deixa a marca decidir.
- Escreveu algo ambíguo? O pipeline **pergunta**, não chuta.

## Os comandos

A skill chama todos por você; estes são os que você usa à mão.

| Comando | Para quê |
| --- | --- |
| `estado <execução>` | onde parou, quantas gerações foram gastas, qual é o próximo comando |
| `checar <execução> --iteracao N [--gen gen_KK] [--modo]` | medir uma imagem contra a paleta e os tetos |
| `importar <execução> --iteracao N <imagem> [--modelo]` | trazer a peça final de volta para as checagens |
| `derivar <execução> <imagem> --modo <modo>` | cortar e reduzir o master para o tamanho exato do canal |
| `entregar <execução> --modo <modo> --aprovado [--concluir]` | gravar o entregável; `--concluir` arquiva o pedido |

Limites: `--variacoes` (padrão 2, amostras por geração) e `--max-geracoes` (padrão 12, teto da
execução inteira, contado em `geracoes.jsonl` e mantido entre sessões).

## Como retomar

```bash
uv run portinari estado output/2026-09-20_meu-slug
```

Diz em que etapa parou, quantas gerações já foram gastas e qual é o próximo comando. Pode fechar o
Claude Code no meio: o estado vive em `manifest.json` e `geracoes.jsonl`, não na sessão.

## Depois, quando você gerar a peça final

```bash
# trazer a final de volta para as checagens objetivas
uv run portinari importar output/<execução> --iteracao 1 minha-peca.png --modelo nano-banana-pro
uv run portinari checar   output/<execução> --iteracao 1 --modo dark

# cortar e reduzir para o tamanho exato do canal (nunca distorce)
uv run portinari derivar  output/<execução> minha-peca.png --modo dark
```

## Se algo der errado

| O que aparece | O que é | O que fazer |
| --- | --- | --- |
| `PERGUNTA AO AUTOR:` (exit 2) | o pedido está ambíguo | responda e rode de novo; nada foi chutado |
| `ERRO: brand/ está N commit(s) atrás` (exit 1) | a marca mudou no GitHub | `git -C brand pull` e rode de novo, ou `--permitir-desatualizada` se souber o que está fazendo |
| `ERRO: o prompt criativo perdeu N termo(s)` | um detalhe do enriquecimento sumiu na escrita do prompt | o prompter reescreve incluindo os termos listados |
| `ERRO: a ferramenta não recebeu os hex da paleta` (exit 4) | o LLM do `agy` reescreveu o prompt e cortou a paleta | regere o prompt; **não** siga com essa imagem |
| `ERRO:` em `checar` | cor fora da paleta na imagem | é reprovação: volte uma volta no prompt |
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

**Um ponto cego conhecido:** `checar` só enxerga cores que ocupam 1% ou mais do quadro. Um acento
de dois ou três pixels de largura — um fio, um fio de lâmina — aparece como `acento 0,0%`. Isso é
granularidade da medição, não ausência do acento; quem confirma se ele existe é o crítico visual,
olhando.

## Onde está o resto

`CLAUDE.md` tem as regras invioláveis e a fonte única de cada coisa. `docs/PLANO.md` tem as
decisões e por que cada uma foi tomada; `docs/agy.md`, o que se sabe do gerador e como se sabe.
`specs/epicos/` tem uma spec por épico, com os testes que cada um precisa passar.
