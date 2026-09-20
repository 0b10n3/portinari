# Portinari

Pipeline de ilustração da Syntaxis. Você escreve um pedido em três linhas; ele devolve um **prompt
pronto para colar** no Nano Banana Pro — um para a pilha escura, um para a clara — já com a paleta
da marca, o estilo, o enriquecimento da cena e o tamanho certo do canal.

Ele **não** entrega a imagem. A imagem que aparece no caminho é de validação: existe para provar
que o prompt funciona antes de você gastar uma geração boa com ele.

## Como rodar

```bash
cd pipelines/portinari && claude      # agentes e skill só carregam aqui dentro
/portinari pedidos/exemplo-cafe-lca.md
```

Você será chamado duas vezes: no **Gate 1**, para escolher entre três conceitos; no **Gate 2**, para
aprovar o prompt vendo a imagem de validação. Fora isso, o pipeline anda sozinho.

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
- Escreveu algo ambíguo? O pipeline **pergunta**, não chuta.

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

**Garante:** a paleta da marca chega íntegra ao gerador; nenhum termo do enriquecimento se perde
entre a cena e o prompt; o prompt entregue não depende de nenhum arquivo deste repositório; o
tamanho e o formato vêm da marca, nunca do código; nada é aprovado sem você.

**Não garante:** que o Nano Banana Pro vá obedecer. Ele é um modelo: pode desenhar texto, inventar
cor, ignorar um detalhe. Por isso `COMO-GERAR.md` traz a lista do que conferir, e `importar` +
`checar` existem para medir a peça final com a mesma régua.
