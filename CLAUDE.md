# portinari — pipeline de ilustração Syntaxis

Transforma um pedido de ilustração escrito à mão (`pedidos/*.md`) num **prompt entregável**, um por
modo (dark e light), validado por uma imagem gerada no `agy`. A peça final é gerada pelo autor, à
mão, no Nano Banana Pro, colando o prompt.

Plano e decisões: [`docs/PLANO.md`](docs/PLANO.md). Levantamento do `agy`: [`docs/agy.md`](docs/agy.md).
Specs por épico: [`specs/epicos/`](specs/epicos/).

## Regras invioláveis

1. **O entregável é o prompt, não a imagem** (decisão A16). A imagem que o `agy` gera é ~1K, JPEG,
   e serve para provar que o prompt funciona. Ela não é entregue a ninguém.
2. **A paleta é a única regra vinculante da marca** (A2). Cor fora da paleta reprova. Sombra, grão,
   frame, ângulo de corte e tetos numéricos são padrão sobreponível: viram aviso e cedem quando o
   pedido do autor pede o contrário.
3. **Nunca edite `brand/`.** A marca é lida em runtime, nunca duplicada e nunca escrita. Nenhum
   tamanho, proporção, formato ou fragmento de estilo mora em `.py`.
4. **Nunca gere com a marca desatualizada** (A13). `portinari marca` sai com 1 se `brand/` está
   atrás do remoto. O pipeline nunca faz `git pull` sozinho.
5. **Dois gates são humanos.** Gate 1 escolhe o conceito; Gate 2 aprova o prompt. `AskUserQuestion`,
   sempre. `entregar` exige `--aprovado`.
6. **Três voltas por etapa, teto de 12 gerações.** Estourou, o pipeline para e entrega o melhor
   estado com diagnóstico — **nunca aprova sozinho para fechar**.
7. **O crítico visual não vê prompt** (D7). Controle por instrução, não por sandbox: ele só tem
   `Read` e o `SKILL.md` diz o que entregar a ele.
8. **Nada de texto na imagem.** Nenhuma palavra, número, sigla, logo ou símbolo monetário.
9. **Segredo nenhum no git.** `.env` (com `GEMINI_API_KEY`) está no `.gitignore`; confira o diff
   antes de cada commit.

## Estrutura

```
.claude/agents/     diretor-de-arte · critico-conceito · enriquecedor-de-cena
                    prompter-tecnico · critico-visual
.claude/skills/portinari/SKILL.md    o orquestrador (disable-model-invocation)
rubrica/rubrica.md  a régua do crítico visual (fora do código de propósito)
src/portinari/      brief · brand · agy · imaging · enriquecimento · entrega · cli
pedidos/            _TEMPLATE.md · <pedido>.md · _processados/
specs/epicos/       uma spec por épico
output/AAAA-MM-DD_slug/
  brief.json  brand_snapshot.json  conceitos.md  manifest.json  geracoes.jsonl
  enriquecimento/vNN.json|md
  iteracoes/NN/  prompt_criativo.md  prompt_final.md  gen_KK.*  critica.md
  final/  prompt_dark.md  prompt_light.md  COMO-GERAR.md  validacao/
```

Imagens não entram no git (`.gitignore`); todo o resto é texto e entra.

## Fonte única de cada coisa

| Coisa | Fonte | Nunca |
| --- | --- | --- |
| Cor, tetos numéricos | `brand/tokens/syntaxis.tokens.json` | hex escrito em `.py` |
| Regra de construção | `brand/DESIGN.md` §4.4, §5, §7 | reinterpretar de memória |
| Bloco injetável | `brand/ILUSTRACOES/_bloco-marca.md` (paleta e tetos **regerados** dos tokens — D2) | colar o `.md` inteiro |
| Tamanho, master, formato, área segura | `brand/ILUSTRACOES/FORMATOS.md` | preset no código |
| Estilo (base e modo) | `brand/ILUSTRACOES/estilos/` | inventar estilo |
| Régua do crítico | `rubrica/rubrica.md` | regra dentro do agente |
| Decisões do projeto | `docs/PLANO.md` | reabrir decisão já tomada |
| Estado da execução | `manifest.json` + `geracoes.jsonl` | arquivo de estado paralelo |

## O pipeline: `/portinari pedidos/<arquivo>.md`

Quinze etapas, detalhadas em `.claude/skills/portinari/SKILL.md`. O resumo:

```
ingest → marca → diretor-de-arte → critico-conceito → GATE 1 → enriquecedor-de-cena
→ prompter-tecnico → prompt → gerar (agy) → checar → critico-visual → (variante do outro modo)
→ GATE 2 → entregar → o autor gera a peça no Nano Banana Pro
```

Códigos de saída que mudam o que fazer: `2` = pergunta/recusa acionável · `3` = falha do `agy` ·
`4` = os hex da paleta não chegaram ao gerador (regere o prompt, não siga).

## Modelos

| Papel | Modelo | Como |
| --- | --- | --- |
| Validação | `gemini-3.1-flash-image` (Nano Banana 2) | pelo `agy`, quota da assinatura |
| Final | `gemini-3-pro-image` (Nano Banana Pro) | **à mão**, pelo autor |

Não existe modelo de **imagem** "3.8 flash" — `gemini-3.8-flash` é texto e é o *orquestrador* do
`agy`. A API do Gemini (`specs/epicos/epico-10-gemini.md`) está especificada e **adiada**: os
modelos de imagem exigem faturamento habilitado no projeto da chave.

## Git

Branch por épico (`epico/NN-slug`) ou por execução (`arte/<slug>`), commit em pt-BR
(`<tipo>(<escopo>): <imperativo>`), `merge --no-ff` em `main`, `push`, e o repositório **termina na
`main`**. Execução só mergeia depois do Gate 2. Nunca `push --force`, `reset --hard`, `rebase` de
histórico publicado, `clean -fd` ou deleção de branch remota.

## Ao rodar este repositório de novo

`cd pipelines/portinari && claude` — agentes e skill só carregam abrindo o Claude Code **dentro do
pipeline**. Depois, `uv run pytest` (deve ficar verde) e `uv run portinari estado <execução>` para
saber onde uma execução parou.
