# Portinari — Plano (Fase 1)

18/09/2026 · revisado em **20/09/2026** (ver "Decisões do autor (20/09/2026)") · Fase 2 em curso.
Base: leitura de `PROJECT_MAP.md`, dos `CLAUDE.md`/`README.md` de `hemingway` e `gary_halbert`, de
toda a camada de ilustração de `brand/`, e do `agy` (detalhe em [`agy.md`](./agy.md)).

## Decisões do autor (18/09/2026) — prevalecem sobre o texto abaixo

| # | Decisão | Consequência no plano |
| --- | --- | --- |
| A1 | **Q1:** ampliação aceita, mas **sempre gerar na melhor resolução possível** | O wrapper tenta a maior resolução que a ferramenta permitir e só cai para a menor se falhar; S1 **sonda** resolução (parâmetro, se existir; instrução no prompt) em vez de assumir 1K. O manifesto registra dimensão nativa e fator de ampliação de cada imagem |
| A2 | **Q2: o pedido vence a marca, exceto paleta de cores** | C1 resolvida a favor do pedido. **Bloqueante = só a paleta** (tokens do modo, uma pilha por modo). Sombras coerentes com uma única fonte de luz e textura de papel (rubrica do pedido) **valem**. As demais regras da marca (proibição de sombra, granulação < 0,028, frame/hairline, corte a 0°/45°, tetos de nº de cores/fundo/lime, descritores proibidos) viram **padrão sobreponível**: entram no prompt/rubrica como padrão, geram **aviso** (não reprovação) e cedem quando o pedido pedir o contrário |
| A3 | **Q4:** modo primário = **dark** | E8 deriva o light a partir do dark aprovado |
| A4 | **Q5:** recomendação aceita — injeta só a pilha do modo; "descritores proibidos" só como lint (agora aviso, por A2) | E2 |
| A5 | **Q3, Q6, Q7, Q9, Q11** nos defaults propostos (Q7: `capa de post para substack` = 16:9, 2560×1440) | — |
| A6 | **Novo:** salvar os **prompts completos e detalhados** que geraram cada imagem | Ver "Prompts completos" abaixo |
| A7 | **Novo:** manter **sincronizado com o GitHub**: commitar, mergear e voltar para a `main` ao final. Substitui D4 e "sem push" (autorização de push ao remote `origin` do próprio repo, sem force) | Ver "Fluxo git" abaixo |
| A8 | **Alternativa A** para o gerador (`agy`, `gemini-3.1-flash-image`). **O autor também gera manualmente no Nano Banana Pro** copiando o prompt salvo | O prompt de cada iteração é **autossuficiente e colável** (`prompt_final.md`, `final/prompts.md`); comando `importar` traz para a execução as imagens geradas à mão (E5b), que seguem pelas mesmas checagens, crítico, recorte e entrega. Não implemento API do Gemini |
| A9 | **Novo épico:** etapa de **enriquecimento do prompt** (trabalhadores, ferramentas, detalhes nos papéis do título etc.) para imagens mais profissionais | **E4** (spec em `specs/epicos/epico-04-enriquecimento.md`) |

**Interpretação de A2, a confirmar de passagem:** "pedido" = o que você escreveu (o pedido `.md` e
a rubrica do prompt de implementação). Como sombra cria tons novos, a checagem de paleta tolera
variantes mais escuras do token da camada (calibração em E5, valores só depois de imagens reais) e o
limite de 3–7 cores deixa de reprovar. O bloco de marca **não** injeta a seção "A escada" (a parte
anti-sombra); mantém âncora de hex absoluto por folha, que é a lição de paleta.

### Prompts completos (A6)

Para **cada geração** o pipeline grava, em `iteracoes/NN/`:

- `gen_K.prompt.md` — o prompt **completo** que pretendíamos enviar (parte criativa + bloco
  injetado), sem cortes;
- `gen_K.efetivo.md` — o prompt que a `generate_image` **de fato recebeu** (extraído do
  `Using prompt:` do transcript do `agy`, já que o LLM do `agy` pode reescrever — ver R1), mais o
  resultado do diff contra o pretendido;
- `gen_K.json` — comando `agy` exato, `conversation_id`, `AspectRatio`, `ImageName`, modelo do
  orquestrador, tempos, caminho e dimensões nativas do JPEG, hash;
- as versões de `prompt_criativo.md` de cada volta (nunca sobrescritas).

Na entrega, `final/prompts.md` reúne o prompt completo (e o efetivo) que gerou cada variante final,
inclusive o prompt de **edição** da derivação. `manifest.json` referencia esses arquivos e também
guarda os textos. Todos entram no git (são texto); só as imagens ficam fora.

### Fluxo git (A7)

Repo: `pipelines/portinari` (remote `origin` = `git@github.com:0b10n3/portinari.git`), sempre
terminando na `main` sincronizada.

- **Desenvolvimento (épicos):** `git checkout -b epico/NN-slug` → commit(s) em pt-BR
  (`<tipo>(<escopo>): <imperativo>`) → `git checkout main` → `git merge --no-ff epico/NN-slug` →
  `git push origin main` (e a branch do épico) → **volta e fica na `main`**. Antes de cada commit,
  confere que não há segredo/chave no diff.
- **Execução do pipeline:** branch `arte/<slug>` (mesmo padrão de `copy/<slug>` e `post/<slug>`),
  **um commit por etapa**, merge em `main` **somente depois do Gate 2 aprovado**, push e volta à
  `main`. Se abortar: a branch fica (pushada, nunca apagada) e o repo volta à `main`.
- **Nunca:** `push --force`, `reset --hard`, `rebase` de histórico publicado, `clean -fd`,
  `filter-branch`, deleção de branch remota (deny-list igual à dos irmãos).
- O primeiro commit (docs) vai direto na `main`, porque o repo ainda não tem nenhum.

## Decisões do autor (20/09/2026) — novo rumo; prevalecem sobre tudo acima

| # | Decisão | Consequência no plano |
| --- | --- | --- |
| **A10** | **Gerador = API do Gemini direto** (alternativa **D**, híbrida). Rascunho/avaliação no **flash**; imagem **final** só no **Nano Banana Pro** | Novo épico **E10** (`gemini.py`). O `agy` (E3) vira **fallback testado**, não o caminho principal. Cai o risco **R1** (nenhum LLM reescreve o prompt) e boa parte do **R2** (2K/4K nativos) |
| **A11** | **Nome real dos modelos** (verificado na API com a chave do `.env`, 20/09/2026): não existe modelo de **imagem** "3.8 flash" — `gemini-3.8-flash` é **texto**. Os de imagem são `gemini-3.1-flash-image` (**Nano Banana 2**), `gemini-3.1-flash-lite-image`, `gemini-2.5-flash-image` e `gemini-3-pro-image` (**Nano Banana Pro**) | Avaliação = `gemini-3.1-flash-image`; final = `gemini-3-pro-image`. Constantes nomeadas em `gemini.py`, sobreponíveis por `--modelo` |
| **A12** | **A marca manda no tamanho e no estilo.** `ILUSTRACOES/FORMATOS.md` e `ILUSTRACOES/estilos/` entram na lista de arquivos lidos em runtime | Novo épico **E11**. `brief.py` **para** de trazer tamanho no código (os `PRESETS` viram só o mapa USO→chave da marca); `STYLE` passa a ser `base + modo` |
| **A13** | **Nunca gerar com marca desatualizada.** `portinari marca` confere `brand/` antes de qualquer execução: atrás do remoto = **erro** (hoje é só pergunta), alteração local não commitada = aviso | `cli._marca` exit 2 → exit 1 quando atrás; `--permitir-desatualizada` para sobrepor conscientemente |
| **A14** | **Master × entrega.** Gera-se o **master** (a maior resolução que o modelo permitir), entrega-se a derivação por **corte central + redução**, respeitando a área segura universal de `FORMATOS.md` | Reescreve o pós-processamento do **E5**; o manifesto passa a registrar master e cada entrega |
| **A15** | Chave em `.env` na raiz do pipeline, fora do git | `.gitignore` += `.env`; `gemini.py` lê `GEMINI_API_KEY` do ambiente ou do `.env` |
| **A16** | **O entregável final é o PROMPT, não a imagem.** O pipeline entrega `final/prompt_<modo>.md` — autossuficiente e colável — e o autor gera a imagem final à mão no Nano Banana Pro | Reescreve o fim do pipeline: **E12** (novo, spec própria). E5 perde o recorte/resize do caminho crítico; E6 `entregar` recusa por prompt incompleto, não por imagem faltando; E9 muda o critério de pronto |
| **A17** | **O `agy` gera só imagem de validação.** A imagem do `gemini-3.1-flash-image` existe para **provar que o prompt funciona** (composição, paleta, uma ideia, sem texto) — nunca para ser entregue | `--via agy` é o padrão e não precisa de faturamento (R14 deixa de bloquear). **E10 (API do Gemini) fica adiado**, especificado e não implementado, até haver motivo |

**Bloqueio conhecido (20/09/2026), hoje sem efeito:** a chave é válida (texto responde), mas os
modelos de **imagem** devolvem **429 · `free_tier_requests, limit: 0`** — o projeto está no *free
tier*. Por A17 isso deixa de bloquear qualquer coisa: a validação roda no `agy` (quota da
assinatura do Antigravity) e a final é manual. O E10 só volta à fila se o faturamento for
habilitado **e** houver ganho em automatizar a final.

**Por que o `agy` basta para validar (medido em 20/09/2026):** `FORMATOS.md` reposicionou
2560×1440 como **master** ("o maior que o gerador permitir") e a entrega real é menor — a capa de
Substack é 1456×816. Contra o nativo do `agy` (1376×768 em 16:9), o fator de ampliação por uso fica
em ×1,06 (substack-capa), ×0,80 (substack-email), ×0,87 (linkedin-destaque), ×1,21
(instagram-post), ×1,41 (instagram-story e youtube-thumb) — todos abaixo do ×2 a partir do qual a
própria marca exige olho humano. Exceção: `substack-email` é 5:1, que **não** está no enum de
`AspectRatio` do `agy`, e `FORMATOS.md` proíbe cortá-lo de 16:9 — esse uso nasce manual.
O schema de `generate_image` foi reconferido em 20/09 (agy 1.2.7): **sem** parâmetro de modelo e
**sem** parâmetro de tamanho. O nativo de 9:16 (768×1376) é simetria, ainda não medido.

**O que continua valendo:** A2 (só a paleta é vinculante), A3 (primário dark), A6 (prompts
completos salvos), A7 (fluxo git), A9 (enriquecimento). **A8 fica superada por A10** — a geração
manual no Nano Banana Pro (E5b) continua existindo como caminho alternativo e não muda.

## Achados do S1/S2 (18/09/2026) — decidido: **alternativa A** (A8)

Detalhe e evidência em [`agy.md`](./agy.md) §3.2, §3.3, §6. Resumo:

1. **O modelo de imagem do `agy` é `gemini-3.1-flash-image` ("Nano Banana 2"), não o Nano Banana
   Pro.** Está no banco da conversa e no binário; não há parâmetro nem configuração local para
   trocar. Isso cai na condição que você definiu como bloqueador ("se o agy não suportar geração
   com Nano Banana Pro… descreva as alternativas e não contorne sozinho"). **Não contornei.**
2. **Resolução nativa ~1K** (16:9 = 1376×768); pedir mais no prompt não muda. 2560×1440 = ampliação ×1,86.
3. **O que funciona e está testado:** headless sem flags de permissão, ~25 s por imagem, prompt de
   3,5 mil caracteres chegou **literal** ao gerador, **edição por `ImagePaths` funciona** (base da
   derivação light/dark), qualidade boa de paper cut.
4. **Defeitos encontrados (e o que já corrigi):** legenda de amostras com nomes de token desenhada
   na imagem (vinha da tabela de paleta que eu injetava → corrigido: só hex, em prosa); cerejas
   vermelhas fora da paleta (erro de prompt meu → regra do Prompter); acento lime estourando 1% na
   edição (→ o prompt de edição deve dizer onde o acento aparece).

**Alternativas (escolha sua; nenhuma foi implementada):**

| | Como | Ganha | Perde |
| --- | --- | --- | --- |
| **A. Ficar com o `agy` como está** | `gemini-3.1-flash-image`, 1K + ampliação Lanczos | zero chave/custo novo; tudo já testado; edição funciona | não é Nano Banana Pro; 2560×1440 por ampliação (macio); R1 (LLM no meio) permanece |
| **B. Nano Banana Pro direto pela API do Gemini** | chamada REST (`urllib`, sem SDK) ao modelo `gemini-3-pro-image-preview`, com `GEMINI_API_KEY` no ambiente | Nano Banana Pro de verdade; **2K/4K nativos** (atende "sempre a melhor resolução"); sem LLM no meio (prompt exato, some o R1); referências para edição | deixa de ser "via `agy`"; exige chave e custo por imagem; nome do modelo, tamanhos e preço **precisam ser confirmados** (não consegui verificar daqui) |
| **C. Testar se o `agy` com `GEMINI_API_KEY` usa o Pro** | o binário tem backend `BackendGeminiAPI` e `imageGenerationModelName` | pode dar Pro mantendo o `agy` | não confirmado, é palpite; custa 1 geração + chave |
| **D. Híbrido** | `agy` para explorar conceitos/iterar barato; render final no Pro (B) | melhor custo × qualidade | duas integrações |

*Minha recomendação:* **B** (ou D), porque a exigência de "melhor resolução possível" e o
Nano Banana Pro só se cumprem de verdade por aí, e ainda elimina o risco de o LLM do `agy`
reescrever o prompt. É uma opção sua: envolve chave, custo e sair do `agy`. O E5–E7 (imagem,
manifesto, agentes) não dependem dessa escolha; o E3 (wrapper) e o E8 (derivação) sim.

## 0. Resumo executivo

1. **O `agy` não é um bloqueador total, mas há três pontos que mudam o desenho** e que só o
   smoke test resolve: (a) **não dá para escolher o modelo** — `generate_image` não tem parâmetro
   de modelo (o S1 mostrou que o modelo é `gemini-3.1-flash-image`, não o Nano Banana Pro — ver "Achados do S1/S2"); (b) **a
   saída é ~1K** (1376×768 em 16:9) — 2560×1440 exige ampliar ×1,86; (c) **um LLM de texto
   reescreve o prompt** antes da ferramenta (medido em 14 sessões antigas: 5 reescritas por
   inteiro, 9 quase literais porém ~5–20% mais curtas), o que ameaça a injeção determinística
   do bloco de marca.
2. **A marca e o pedido se contradizem em um ponto central**: a rubrica pede "sombras projetadas
   coerentes com uma única fonte de luz"; a marca **proíbe sombra em qualquer forma** (profundidade
   é degrau de tom). Proponho que a marca vença (§2.3, C1).
3. **A marca ainda não sabe que o Portinari existe**: todos os arquivos dizem "único consumidor:
   `pipelines/hemingway`" (C2). Não altero `brand/`; reporto.
4. **O repositório está em dois repos git**: `pipelines/portinari/` tem `.git` próprio (remote
   `0b10n3/portinari`, 0 commits) e a raiz o lista como não rastreado (C11).
5. Preciso de **5 respostas bloqueantes** (§8: Q1, Q2, Q4, Q5, Q7). As demais têm default proposto.

## 1. Arquitetura final

Orquestração nativa do Claude Code, como `hemingway`/`gary_halbert`: skill orquestradora
(sessão principal, porque há gate humano) + subagentes de trabalho isolado + Python só para o
determinístico. Sem frameworks de agentes, sem SDK de LLM.

```
/portinari pedidos/<arquivo>.md [--sem-gate-conceito] [--variacoes N] [--max-geracoes N]

 1 ingestão ────────── script   parse → brief.json + lacunas/perguntas
 2 marca ───────────── script   tokens + bloco → brand_snapshot.json (versão, fingerprint, drift)
 3 diretor-de-arte ─── agente   3 conceitos distintos  ⇢ conceitos.md   (ou perguntas ao autor)
 4 critico-conceito ── agente   ranqueia e justifica    ⇢ conceitos.md
 5 GATE 1 ──────────── humano   escolhe / ajusta / pede novos   (pulável por flag)
 5b enriquecer ──────── agente+script  cena com detalhes; código valida paleta/texto/densidade; autor vê a lista
 6 prompter-tecnico ── agente   parte criativa           ⇢ iteracoes/NN/prompt_criativo.md
 7 prompt ──────────── script   criativo + bloco injetado + lint de descritores proibidos
 8 gerar ───────────── script   API do Gemini: flash p/ avaliar, Pro p/ a final (agy = fallback)
 9 checar ──────────── script   checagens objetivas na imagem de VALIDAÇÃO (paleta ΔE, nº de cores, fundo, lime)
10 critico-visual ──── agente   rubrica + checagens → o PROMPT está aprovado? (≤ 3 voltas por etapa)
11 derivar variante ── script+agente   prompt da outra pilha, validado por edição (ImagePaths)
12 GATE 2 ──────────── humano   aprova o PROMPT (vendo a imagem de validação) / ajusta / aborta
13 entregar ────────── script   final/prompt_<modo>.md + COMO-GERAR.md + manifest.json
14 (fora do pipeline)  autor    cola o prompt no Nano Banana Pro e gera a final; opcional: `importar`
```

**Onde as coisas vivem (convenção dos irmãos):** skills e agentes ficam em
`pipelines/portinari/.claude/{skills,agents}/`, descobertos ao abrir o Claude Code **dentro do
pipeline** (`cd pipelines/portinari && claude`), igual ao README do `hemingway`. Abrindo da raiz
do monorepo eles não carregam. O pedido do prompt sugere `agentes/`; a convenção manda
`.claude/agents/`, então sigo a convenção.

**Python (`src/portinari/`, `uv`, Pydantic, Pillow, pytest).** Seis módulos, um CLI
(`uv run portinari <subcomando>`):

| Módulo | Responsabilidade |
| --- | --- |
| `brief.py` | parser tolerante, schemas, presets por USO, validação cruzada, download/validação de referências |
| `brand.py` | resolve tokens (aliases `{color.x.y}`), monta o bloco, fingerprint, drift, `git fetch` |
| `agy.py` | wrapper **fallback**: monta o comando, chama, acha a imagem por `conversation_id`, verifica o prompt, retenta, conta gerações |
| `gemini.py` | **gerador principal (A10)**: `generateContent` por `urllib`, papel rascunho (flash) × final (Pro), referências para edição, grava a mesma `Geracao` |
| `imaging.py` | checagens objetivas + pós-processamento **master → entrega(s)** (corte no ponto focal dentro da área segura, resize, PNG/JPEG) |
| `manifest.py` | `manifest.json` (também é o estado/retomada — ver decisão D3) |
| `cli.py` | cola os subcomandos que o orquestrador chama |

**Dependências:** `pydantic`, `pillow` (runtime); `pytest` (dev). Nada mais — API do Gemini e download por
`urllib`, tokens por `json`, ΔE por fórmula própria (~15 linhas), sem numpy, sem OCR, sem YAML.

### Decisões que já tomei (e que você pode reverter)

- **D1 — Modo do gerador:** a parte criativa do prompt sai em **inglês** e o bloco de marca entra
  como está (misto). É o que as sessões reais bem-sucedidas fizeram; a marca cita frases em
  inglês dentro do bloco. Reversível no smoke test.
- **D2 — Bloco de marca montado, não colado.** `_bloco-marca.md` tem hex literal em tabelas;
  se eu injetasse o arquivo, alterar `tokens.json` não mudaria o bloco (e o critério de pronto
  exige que mude). Logo: **Paleta** e **Tetos numéricos** são **gerados a partir dos tokens**;
  as demais seções (escada, borda/retícula, escala pequena, descritores proibidos, sem texto)
  entram **verbatim**, por título de seção. Um lint compara os hex do `_bloco-marca.md` com os
  tokens e avisa se derivarem (hoje estão iguais — verifiquei os 11).
- **D3 — `manifest.json` é também o estado.** Os irmãos usam `estado.json`; aqui o manifesto
  pedido já registra etapa, iterações e gerações, então um arquivo só (menos um schema a manter).
  A retomada lê dele.
- **D4 — ~~Um commit por épico, direto em `main`, sem push.~~ Superado por A7** (branch por épico,
  merge, push e volta à `main`). Estilo dos irmãos mantido: `<tipo>(<escopo>): <imperativo>`, pt-BR.
- **D5 — Só `AskUserQuestion` faz os gates**, como no `gary_halbert` (etapa 8).
- **D6 — Limites:** ≤ 3 voltas de crítica por etapa; `--variacoes` padrão 2; `--max-geracoes`
  padrão 12 (pior caso previsto ≈ 9: 3 voltas × 2 variações no primário + 3 derivações); ao
  estourar, o pipeline para e entrega o melhor estado com diagnóstico, **nunca aprova sozinho**
  (regra do `revisor-final` do `gary_halbert`).
- **D7 — Isolamento do crítico visual (limite honesto).** O agente tem só `Read`; o orquestrador
  passa a ele apenas `brief.json`, `brand_snapshot.json`, imagens, `checagens.json` e a rubrica.
  Não há como impedir tecnicamente que ele leia `prompt_*.md`; a instrução proíbe e o manifesto
  registra o que foi entregue a ele. É controle por instrução, não por sandbox.

## 2. Mapa da marca

### 2.1 Hierarquia de autoridade (para paleta e ilustração)

| # | Arquivo | Papel | Autoridade |
| --- | --- | --- | --- |
| 1 | `tokens/syntaxis.tokens.json` (v2.7.0) | **valor** — paleta, `illustration.*` (escada, tetos numéricos) | **fonte de verdade de cor e de números**. Vence todos os outros |
| 2 | `DESIGN.md` (v3.1) §4.4, §5, §7 | **regra** — sombra proibida, contrato de camadas, mecanismo de profundidade | fonte de verdade de regra |
| 3 | `ILUSTRACOES/_bloco-marca.md` | bloco operacional injetável | subordinado a 1 e 2 (deriva deles) |
| 4 | `ILUSTRACOES/meta-prompt-collage-paper-cut.md` | subconjunto só de cor do bloco | subordinado; **declara** que tokens e DESIGN §7 vencem |
| 5 | `ILUSTRACOES/_como-gerar.md`, `README.md` | processo e taxonomia | procedimento (com referências quebradas — C3) |
| 6 | `REVOGACOES.md` | regra morta | **filtro negativo**: se está aqui, não vale — vence qualquer citação antiga |
| 7 | `APLICACAO.md`, `CHECKLIST-PR.md`, `BRAND_KIT.md` | matriz de superfície, checklist, resumo | derivados; úteis para conferir |
| 8 | `SOCIAL/README.md`, `INSTAGRAM.md` | **tamanhos de plataforma** (não ilustração) | fonte de tamanhos; `SOCIAL` é camada de **sistema** ("nunca collage") |
| 9 | `PATTERNS/`, `LOGO/`, `templates/` | camada de sistema | fora do escopo do Portinari |
| 10 | `revisao-2026/` | rastro de processo; `refs/` são referências reais | histórico, mas `refs/` serve de **calibração** das checagens |
| — | `_arquivo/` | morto | não uso como regra. **Exceção declarada:** `DECISOES-HERDADAS.md` R22–R26 traz lições empíricas do gerador (âncora absoluta > comparativo; "scanner de mesa"; parede do recorte; "não lê negative prompt"). Trato como **hipótese a reverificar** no smoke test, não como regra |

### 2.2 O que a marca diz que o Portinari deve gerar

- Collage/paper cut plano; **uma** pilha por peça (escura *ou* clara, nunca mistura).
  Escura: Ink `#141414` → Deep Forest `#0F3D27` → forest.700 `#125233` → forest.500 `#1B6A45`.
  Clara: Mist `#E2E8F0` → Mint `#E6F4EE` → Chalk `#F7F7F5`. Figura: grove.500 `#2D9E67` /
  grove.300 `#78C9A4`. Acento: Lime `#CDF163` (ou lime.700 `#5F7D1C` sobre pilha clara).
- Profundidade por degrau de tom; **nunca sombra**. Corte reto ou 45°. Sem texto na imagem.
- Tetos verificáveis (`illustration.*`): 1 matiz de pilha + 1 neutro; 3–7 cores ≥1% do quadro;
  fundo ≥40%; lime ≤1%; granulação só no fundo, amplitude < 0,028; < 96 px não é ilustração.
- Onde vale: capa editorial (Substack, LinkedIn), retrato de dado, thumbnail YouTube, cabeçalho de
  e-mail / capa de destaque social (`APLICACAO.md` §0). Nunca app, nunca site.

### 2.3 Contradições e lacunas encontradas (não resolvi nenhuma sozinho)

| # | Onde | O quê | Como trato no plano |
| --- | --- | --- | --- |
| **C1** | pedido §5 × marca | Rubrica do pedido: "**sombras projetadas** coerentes com uma única fonte de luz", "textura de papel". Marca: sombra proibida em qualquer camada (`DESIGN.md` §4.4/§7.2, `CHECKLIST-PR`, `REVOGACOES` S1/S3/S7); granulação só no fundo, < 0,028 | Rubrica reescrita para a marca: "sem sombra; degrau de tom; luz de scanner; sem parede de recorte". **Q2** |
| **C2** | `ILUSTRACOES/README`, `_bloco-marca`, `_como-gerar`, `DESIGN.md` §5/§7, tokens `illustration.$description`, `CHECKLIST-PR`, `BRAND_KIT` | "Único consumidor: `pipelines/hemingway`". O `hemingway` (nota de 09/09/2026 em `prompts-visuais.md`) disse que capa/ilustração viraram "projeto próprio, ainda não criado" — é o Portinari. A regra binária "por repositório" formalmente o reprovaria | Reporto. Sugestão para a marca: nomear `pipelines/portinari` como consumidor. **Q3** |
| **C3** | `_como-gerar.md` | Cita `hemingway/.claude/skills/prompts-visuais/references/{briefing-ilustracao.md, geradores/, estilos-ilustracao.md}` — **não existem** (`prompts-visuais` virou agente; esses arquivos não estão em lugar nenhum de `hemingway/.claude`). Cita também `revisao-2026/01-referencias.md`, hoje em `_arquivo/`. Os passos 2, 4 e a calibração do passo 5 ficam sem fonte. `REVOGACOES` S5/S7 também apontam para um `estilos-ilustracao.md`, que hoje não existe na árvore do `hemingway` | O Portinari passa a ser dono do briefing conceitual (agente Diretor de Arte) e do "gerador ativo" (`docs/agy.md`) |
| **C4** | `ILUSTRACOES/README` §Gate, `_como-gerar` §5 | `brand/scripts/check-ilustracao.py` **não existe**. O método de medição (quantização, o que é "fundo", tolerância) não está definido em lugar vivo | Defino e calibro as checagens no épico E5 contra `revisao-2026/refs/*` (13 referências) e as primeiras gerações reais. Números iniciais na §6/E5 |
| **C5** | `DESIGN.md` §5, `CHECKLIST-PR` × pedido | Marca: "toda ilustração é contida por frame retangular, radius 0, hairline 1px; nada sangra". Pedido: entrega de 2560×1440 cheia | Assumo que o frame é aplicado no layout (Substack/Canva), não na imagem. **Q6** |
| **C6** | pedido §6 × `SOCIAL`/`INSTAGRAM` | A tabela de presets "derivada de SOCIAL e INSTAGRAM" **não cobre** o USO do exemplo: não há preset de capa de Substack, nem de thumbnail YouTube, nem de cabeçalho de e-mail. `SOCIAL` traz 1200×627 (destaque LinkedIn), 1080×1080, 1080×1920, mas são peças de sistema | USO sem preset ⇒ pergunta ao autor, nunca chute. **Q7** |
| **C7** | marca × pedido §3 | Nenhuma regra define qual modo (claro/escuro) é primário por USO. `INSTAGRAM` §5 escolhe fundo por *categoria de conteúdo*, não por superfície | **Q4** |
| **C8** | `lime.700` | `_bloco-marca` manda lime.700 sobre pilha clara, mas `illustration.accent` só aponta lime.500; lime.700 vive em `color.lime.700` sem alias em `illustration.*` | Leio `color.lime.700` direto do token; a regra "clara → 700" fica em código, com comentário. Sugestão à marca: criar `illustration.accent.onLight` |
| **C9** | `_bloco-marca` × ele mesmo | O bloco manda **não usar** os "descritores proibidos" no prompt **e** manda colar o bloco inteiro — que **contém a lista** (`drop shadow`, `gradient`, `text`…). Colar o bloco inteiro coloca essas palavras no prompt | **Q5** |
| **C10** | `_bloco-marca` "colar inteiro" × `DESIGN` "uma pilha por peça" | O bloco lista as duas pilhas; um prompt claro que carrega os hex da pilha escura convida contaminação de cor (lição de âncora absoluta) | **Q5** |
| **C11** | repositórios | `pipelines/portinari/` tem `.git` próprio (remote `git@github.com:0b10n3/portinari.git`, `main`, 0 commits). A raiz **não** o ignora (o `.gitignore` da raiz lista os 4 irmãos, não o Portinari) e mostra `?? pipelines/portinari/`. A raiz **não tem remote** — então "`brand/` atrás do remoto" não tem o que comparar. `PROJECT_MAP` §1/§3 ainda diz que a raiz "não é um repositório git" (hoje é; `brand/` está versionada: 119 arquivos) | Sugiro adicionar `/pipelines/portinari/` ao `.gitignore` da raiz (fora do meu escopo). **Q8** |
| **C12** | docs de marca desatualizados (baixo impacto) | `DESIGN.md` §10 lista a tipografia revogada (Space Grotesk/Hanken/Space Mono) vs §4.2 (Montserrat/Source Sans 3/IBM Plex Mono); linha de tabela órfã na linha 305 (`Texto renderizado dentro de imagem gerada`, colada depois da §4.5); `PROJECT_MAP` §2/§4 citam v3.0/tokens v2.2.0 (a §F10 já diz v3.1/v2.7.0); `hemingway/.claude/skills/marca-syntaxis/SKILL.md` ainda cita Space Grotesk, DESIGN v3.0 e `nodeBranch` | Só reporto. Tipografia não entra no Portinari (a imagem não tem texto) |

## 3. Interface do `agy` (resumo; detalhe em [`agy.md`](./agy.md))

- ✅ `agy -p "<prompt>" --output-format json --model <id>` roda sem TUI; devolve `conversation_id`.
- ✅ Imagem = ferramenta `generate_image(Prompt, ImageName, AspectRatio)`; JPEG em
  `~/.gemini/antigravity-cli/brain/<conversation_id>/<ImageName>_<ms>.jpg`; ~10 s por imagem.
- 🟡 Saída ~1K: 16:9 → 1376×768, 1:1 → 1024², 4:3 → 1200×896, 3:4 → 896×1200.
- 🟡 Erros: `AGY_ERROR: {…}` no stderr + exit `3` (changelog 1.2.6); falha de imagem observada em
  log: `no image generated in response`.
- ❓ Modelo por trás; resolução > 1K; `ImagePaths` (referência/edição); `OutputPath`; permissões
  necessárias em `-p`; exit code quando só o passo de imagem falha.

**Veredito do gate:** geração de imagem headless é **provável**, não confirmada. Não considero
bloqueio; considero **risco alto** com dois testes baratos (S1, S2 — 2 gerações) antes de gastar
esforço no épico de derivação. Se S1 falhar em `-p`, paro e trago alternativas (ver R1–R3).

## 4. Estrutura de pastas

```
pipelines/portinari/
  CLAUDE.md  README.md  pyproject.toml  uv.lock  .gitignore
  .claude/
    skills/portinari/SKILL.md            orquestrador (disable-model-invocation: true)
    agents/diretor-de-arte.md  critico-conceito.md  prompter-tecnico.md  critico-visual.md
  rubrica/rubrica.md                     rubrica do crítico (arquivo próprio, não no código)
  pedidos/  _TEMPLATE.md  exemplo-cafe-lca.md  _processados/
  src/portinari/  brief.py  brand.py  agy.py  imaging.py  manifest.py  cli.py
  docs/  PLANO.md  agy.md
  specs/epicos/                          especificação + testes por épico (padrão do gary_halbert)
  tests/  fixtures/pedidos/cafe-lca.md  fixtures/tokens.json  test_*.py
  output/AAAA-MM-DD_slug/
    brief.json  brand_snapshot.json  conceitos.md  manifest.json
    referencias/                          imagens baixadas
    enriquecimento/  vNN.json  vNN.md      cena enriquecida (validada por código) + visão para o autor
    iteracoes/NN/  prompt_criativo.md  prompt_final.md  gen_*.jpg  checagens.json  critica.md
                   (gen_*.jpg = imagem de VALIDAÇÃO, nunca entregue; fora do git)
    final/  prompt_dark.md  prompt_light.md   ENTREGÁVEL: colável, autossuficiente
            COMO-GERAR.md                     modelo, proporção, tamanho, o que conferir
            validacao/                        cópia da imagem que aprovou cada prompt (fora do git)
```

Desvio da §7 do pedido: agentes em `.claude/agents/` (convenção), `estado.json` fundido em
`manifest.json` (D3), e `critico-conceito` como agente próprio (entradas diferentes do crítico
visual, que precisa ficar cego ao raciocínio do Prompter).

## 5. Formato do pedido — decisões de parsing

- Chaves: `**CHAVE**:` / `CHAVE:` / `# TITLE:`, sem distinção de caixa, com ou sem espaço após
  `:`, EN + pt-BR (`DESCRIÇÃO`, `ESTILO`, `CONTEXTO`, `TÍTULO`, `PROPORÇÃO`, `RESOLUÇÃO`,
  `TAMANHO`, `IMAGENS DE REFERÊNCIA`). Só uma chave **reconhecida no início de linha** encerra o
  campo anterior — `CONTEXT` pode ter `## Títulos` e `**negritos**` à vontade.
- Ruído do fixture tratado, cada um registrado em `brief.json.avisos`: `16:9]` → `16:9`;
  `2560 × 1440 ` (× Unicode, espaço final) → `2560x1440`; campos vazios → default do USO.
- `CONTEXT: @caminho.md` resolve relativo à **raiz do monorepo** (`../..` a partir do
  pipeline), lê e anexa; caminho inexistente vira erro explícito.
- `REFERENCE IMAGES`: um por linha ou separados por vírgula; URL baixada para
  `output/…/referencias/`; tudo aberto com Pillow para validar que é imagem.
- **`RESOLUTION` é faixa, não valor:** `1k` = aresta maior ≤ 1536; `2k` = 1537–3071; `4k` ≥ 3072.
  `2560×1440` cai em `2k` (coerente). Divergência de `SIZE` × proporção × faixa vira **pergunta**.
- Obrigatórios: `TITLE`, `USO`, `DESCRIPTION`. `USO` sem preset conhecido ⇒ pergunta.
- **Revisado por A12 (20/09/2026):** a tabela abaixo virou histórica. A fonte de tamanho passa a
  ser `brand/ILUSTRACOES/FORMATOS.md`, lida em runtime (E11): a coluna **Chave** de lá é a mesma
  chave dos `PRESETS`, e o pipeline usa dali **entrega**, **master**, proporção, formato/peso e
  área segura. O que muda na prática: `substack-capa` entrega **1456×816** com master 2560×1440
  (antes o código entregava 2560×1440), e `substack-email` (1100×220) e `youtube-thumb`
  (1920×1080) deixam de ser pergunta ao autor. O pedido do autor continua vencendo o preset.

- Presets propostos em 18/09 (só o que tinha fonte; **superados por `FORMATOS.md`**):

  | USO | proporção | tamanho | fonte |
  | --- | --- | --- | --- |
  | capa de post para substack | 16:9 | 2560×1440 | **só o exemplo do pedido** — a marca não define |
  | destaque de post no linkedin | 1,91:1 | 1200×627 | `SOCIAL/README.md` |
  | post de instagram | 1:1 | 1080×1080 | `INSTAGRAM.md` §2 |
  | story / capa de reels / destaque | 9:16 | 1080×1920 | `SOCIAL/README.md`, `INSTAGRAM.md` §12 |
  | thumbnail youtube | — | — | **sem fonte** |
  | cabeçalho de e-mail substack | — | — | **sem fonte** |

## 6. Épicos e critérios de aceite

Cada épico: testes verdes (`uv run pytest`) + um commit em pt-BR.

**E1 — Fundação e parser de pedido** · `feat(parser)`
- ⚠️ **Revisado em 20/09/2026:** os tamanhos saem do código e passam a vir de `FORMATOS.md` (A12, E11); `STYLE` passa a aceitar `base + modo` dos `estilos/`.
- `pyproject.toml`/`uv.lock`, pacote `portinari`, `.gitignore`.
- `pedidos/_TEMPLATE.md` e `pedidos/exemplo-cafe-lca.md`; `tests/fixtures/pedidos/cafe-lca.md`
  **byte a byte igual** ao exemplo da §6 do pedido (teste compara hash entre os dois).
- ✔ o exemplo com ruído gera `brief.json` com `aspect_ratio="16:9"`, `size=(2560,1440)`,
  `resolution="2k"`, `style="papercut"`, `context=""`, `referencias=[]` e ≥ 2 avisos
  (`]` sobrando, `×`).
- ✔ casos de borda: `CONTEXT` longo com títulos/negritos e chave falsa no meio de uma linha;
  `CONTEXT: @arquivo`; chaves em pt-BR; campo obrigatório ausente; URL de imagem (servidor local
  de teste) e arquivo que não é imagem; `SIZE` incoerente com a proporção ⇒ pergunta; USO sem
  preset ⇒ pergunta; arquivo vazio.

**E2 — Resolução de marca** · `feat(marca)`
- Resolve aliases de `tokens.json`; monta o bloco (D2); grava `brand_snapshot.json` com versão
  (`$extensions.br.com.syntaxis.version`), fingerprint SHA-256 dos arquivos lidos, paletas
  light/dark, tetos, restrições, bloco por modo, e lista de avisos (drift bloco×tokens).
- `git fetch` seguro: se há remote, avisa e **pergunta** antes de qualquer atualização; se não
  há (caso atual), registra "sem remoto" e segue; nunca `pull`.
- ✔ **teste de runtime:** copia `tokens.json` para tmp, muda `illustration.stack.dark.layer2`,
  gera o bloco → o novo hex aparece e o antigo some, **sem tocar em código**.
- ✔ o fingerprint muda quando qualquer arquivo-fonte muda; o lint aponta hex divergente no
  bloco; seções ausentes em `_bloco-marca.md` falham alto (não silenciosamente).

**E3 — Wrapper do `agy` + smoke tests** · `feat(agy)`
- ⚠️ **Revisado em 20/09/2026:** **entregue e mantido, mas rebaixado a fallback** por A10. O caminho principal passa a ser a API do Gemini (E10). Nada aqui é removido; `gerar --via agy` continua funcionando.
- `agy.py`: comando exato logado; `--print-timeout`; retentativa só em falha transitória
  (exit 3 com `retryable`); localiza o JPEG por `conversation_id`; **verifica o prompt real**
  (`Using prompt:` do transcript) contra o esperado e retenta com instrução de literalidade;
  contador de gerações com teto.
- Testes com um `agy` falso (script no PATH) cobrindo: sucesso, falha transitória, falha
  permanente, prompt reescrito, timeout, teto de gerações.
- **S1 e S2 (2 gerações reais, com sua autorização — Q10)** documentados em `docs/agy.md`.
- ✔ S1 confirma/derruba: headless, permissões, exit codes, prompt íntegro, dimensões, `ModelName`,
  `OutputPath`. ✔ S2 confirma/derruba edição por `ImagePaths`.
- **Ponto de decisão:** se S2 falhar, escolho com você entre F1 (duas gerações independentes com
  a mesma composição descrita + crítico de consistência) e F2 (remapeamento determinístico de
  paleta com Pillow); o E8 é reescrito.

**E4 — Enriquecimento do prompt** · `feat(enriquecimento)` · spec: `specs/epicos/epico-04-enriquecimento.md`
- Nova etapa entre o Gate 1 e o Prompter: o agente `enriquecedor-de-cena` expande o conceito
  escolhido em uma **cena rica e verificável** — trabalhadores, ferramentas de ofício, detalhes
  nos documentos do título, camadas e recortes do papel — sem trocar a ideia nem o ponto focal.
- Saída estruturada (`enriquecimento/vNN.json`), validada por **código**: um único foco; nº de
  elementos e de acréscimos dentro dos limites; cada elemento com **papel de cor da paleta** (nenhuma
  cor fora dela — pegaria as cerejas vermelhas do S1); nada de texto/número/logo; itens incertos
  marcados `verificar` e levados ao autor. `portinari enriquecer` valida e renderiza; `portinari
  prompt` **recusa** um `prompt_criativo.md` que perdeu algum termo do enriquecimento.
- ✔ o exemplo café/LCA ganha ≥ 10 elementos válidos; o prompt do S1 (sem trabalhadores, sem
  ferramentas, papéis lisos) falha na checagem de cobertura; cor fora da paleta, 2 focos, texto,
  excesso de elementos e acréscimos insuficientes são recusados com mensagem acionável.

**E5 — Imagem: checagens objetivas e pós-processamento** · `feat(imaging)` · **implementado em 20/09/2026**
- ⚠️ **Revisado em 20/09/2026 (A16/A17):** as **checagens objetivas ficam** (agora rodam na imagem de validação e é o que sustenta a aprovação do prompt). O **pós-processamento sai do caminho crítico**: corte/resize só existem para uma imagem **importada** (E5b). Sem imagem entregue, não há assert de dimensão exata no fim do pipeline.
- ⚠️ **Revisado em 20/09/2026:** o pós-processamento passa a ser **master → entrega(s)** (A14): corte central pela fórmula de `FORMATOS.md`, área segura universal, JPEG 4:4:4 q90–92 ou PNG conforme o uso, sRGB, frame só depois da redução. Uma peça pode ter várias entregas.
- Checagens (todas com limiar em constante nomeada e comentada, calibradas nesta etapa):
  paleta por **ΔE (CIE76)** entre cada cor dominante (≥ 1% do quadro, após quantização) e a
  paleta do modo — **calibrado nas duas imagens reais do S1/S2**: folha certa 1,0–4,3 · mistura
  de borda 6,5–17,3 · cor inventada 36,7, daí aviso ΔE > 8 e falha ΔE > 25; nº de cores ≥1%
  ∈ [3,7]; fundo ≥ 40% (fundo = cluster dominante na borda do quadro); lime ≤ 1%; 1 matiz de
  pilha + neutro; dispersão interna de luminância por camada (proxy de sombra/gradiente; a
  marca cita 0,008–0,030 aceitável × 0,05–0,20 reprovado, mas o método original não está em
  lugar vivo — recalibro nas 13 refs). O que **não** mede: texto na imagem, corte reto/45°,
  ponto focal (ficam com o crítico visual, e a rubrica diz isso).
- Pós-processamento: recorte para a proporção-alvo **deslizando a janela em torno do ponto
  focal** declarado no conceito, nunca distorção; resize Lanczos; grava PNG; **assert** de
  dimensões exatas; registra fator de ampliação no manifesto.
- ✔ imagens sintéticas (pilha correta passa; sombra/gradiente injetados falham; lime a 3%
  falha); ponto focal no canto não é cortado; `2560×1440` sai exato de 1376×768; o mesmo para
  1080×1080 e 1200×627 (fora da proporção de origem).

**E5b — Geração manual (Nano Banana Pro) e importação** · `feat(manual)` (A8)
- ⚠️ **Revisado em 20/09/2026 (A16/A17):** deixa de ser caminho alternativo e vira **o caminho da imagem final**. `importar` continua opcional: serve para trazer a final de volta e rodar checagens/recorte sobre ela, não para o pipeline poder terminar.
- `portinari importar <saida> --iteracao N <imagem>…` copia imagens geradas fora do `agy` para
  `iteracoes/NN/gen_KK.<ext>` com `gen_KK.json` (`origem: "manual"`, dimensões nativas, hash) e o
  prompt usado (`--prompt` = arquivo colado; padrão `prompt_final.md`); conta como geração no teto.
- ✔ imagem PNG 2K/4K importada aparece no log de gerações e segue para checagem/recorte; formato não
  imagem é recusado; o prompt é gravado íntegro.

**E6 — Manifesto, estado e CLI** · `feat(manifest)` · **implementado em 20/09/2026**
- ⚠️ **Revisado em 20/09/2026 (A16/A17):** `entregar` recusa por **prompt** incompleto (falta um modo, falta o bloco de marca, termo do enriquecimento ausente), nunca por imagem faltando. O manifesto registra qual imagem de validação aprovou cada prompt.
- `manifest.json` conforme §7 do pedido (pedido de origem, versão e fingerprint da marca,
  conceito escolhido, prompts finais **com o bloco injetado**, comandos `agy`, nº de gerações,
  notas por iteração, decisões dos gates) + `etapa_atual` para retomar. Subcomandos:
  `ingest`, `marca`, `prompt`, `gerar`, `checar`, `derivar`, `finalizar`, `entregar`, `estado`.
- `entregar` copia o pedido para `output/…/pedido.md`, **move** o original para
  `pedidos/_processados/` (não o edita), e recusa se `final/` estiver incompleto.
- ✔ retomada: matar no meio, `estado` diz onde parou; teto de gerações persiste entre sessões.

**E7 — Agentes, rubrica e skill orquestradora** · `feat(agentes)` · **implementado em 20/09/2026**
- Quatro agentes em pt-BR + `rubrica/rubrica.md` (notas 1–5; **bloqueantes**: alucinação de
  texto/logo/símbolo — inclui `$` onde deveria ser `R$`; sombra/gradiente; pilhas misturadas;
  violação de teto numérico; elementos factualmente errados) + `SKILL.md` com os dois gates,
  o limite de 3 voltas e as flags.
- Diretor de Arte: 3 conceitos distintos (metáfora, composição, **ponto focal em coordenadas
  0–1**, hierarquia, leitura em miniatura, riscos); pergunta em vez de supor; sem clichês
  financeiros (touro/urso, moedas, gráfico subindo) salvo pedido; contexto visual brasileiro.
- ✔ verificação por leitura + um ensaio a seco sem `agy` (fixtures) que percorre gates e limites.

**E8 — Variante light/dark** · `feat(variante)` · **coberto sem código novo em 20/09/2026**
- ✅ **20/09/2026:** não precisou de módulo novo — `prompt --modo light`, `gerar --ref <imagem aprovada>` (edição por `ImagePaths`, confirmada no S2), `checar --modo light` e `entregar --modo light` já cobrem o fluxo. O que faltava era a régua: `rubrica/rubrica.md` ganhou D1–D4 (mesma composição, mesmos elementos, pilha do modo novo, acento no mesmo ponto) e a skill, o passo 12.
- ⚠️ **Revisado em 20/09/2026 (A16/A17):** entrega **dois prompts** (dark e light). A edição por `ImagePaths` continua sendo como se **valida** que a derivação preserva a composição — o autor gera as duas finais à mão, cada uma do seu prompt.
- ⚠️ **Revisado em 20/09/2026:** a derivação usa edição por imagem de referência **na API** (E10), não mais `ImagePaths` do `agy`.
- Deriva a segunda pilha por edição a partir da aprovada; crítico verifica mesma composição e
  elementos, só a paleta muda; checagens objetivas rodam com a paleta **do modo**.
- ✔ ambas as variantes passam nas checagens do próprio modo; consistência registrada.

**E10 — Gerador pela API do Gemini (flash para avaliar, Pro para a final)** · `feat(gemini)` · spec: `specs/epicos/epico-10-gemini.md`
- ⛔ **Adiado em 20/09/2026 (A17):** **ADIADO** por A17. A spec fica de pé e não é implementada: a validação roda no `agy` (sem faturamento) e a final é manual. Volta à fila se o faturamento for habilitado e automatizar a final valer a pena.
- `gemini.py`: `generateContent` por `urllib` (sem SDK), chave de `GEMINI_API_KEY` (ambiente ou
  `.env`), `imageConfig` (proporção + `imageSize`), imagens de referência para edição/derivação.
- **Dois papéis:** `--papel rascunho` (padrão) = `gemini-3.1-flash-image`; `--papel final` =
  `gemini-3-pro-image`. Só a final gasta Pro; toda iteração de crítica roda no flash.
- Reaproveita `Geracao`, `geracoes.jsonl`, teto de gerações e o layout `gen_KK.*` do `agy.py`
  (nada duplicado). `fiel` passa a ser **sempre verdadeiro**: o prompt vai literal, sem LLM no meio.
- ✔ testes com servidor HTTP falso: sucesso, 429/500 com retentativa e *backoff*, resposta sem
  imagem, `SAFETY`/`PROHIBITED_CONTENT`, teto de gerações, master 2K/4K gravado com as dimensões
  nativas corretas; nenhum teste toca a rede real. ✔ o mesmo `prompt_final.md` serve aos dois
  caminhos (API e colagem manual do E5b).
- **Dependência externa:** faturamento habilitado no projeto da chave (hoje 429 no free tier).

**E11 — Estilos e formatos da marca** · `feat(estilos)` · **implementado em 20/09/2026** · spec: `specs/epicos/epico-11-estilos-formatos.md`
- 📌 **Reforçado em 20/09/2026 (A16):** **fica mais importante**, não menos: como o entregável é texto, o prompt é o único lugar onde o estilo e o tamanho-alvo chegam ao autor. O §6 daquela spec (master → entregas) passa a valer só para imagem importada.
- `brand.py` passa a ler `ILUSTRACOES/FORMATOS.md` e `ILUSTRACOES/estilos/*.md`; os dois entram no
  fingerprint e no `brand_snapshot.json` (tabela de formatos parseada + fragmento de prompt por estilo).
- `brief.py`: `PRESETS` vira só USO→chave de `FORMATOS.md`; `STYLE` aceita **uma base + até um modo**
  (padrão `flat`, conforme `estilos/README.md`); `isometric` exige `--piloto` e avisa que é restrito;
  estilo "Fora" (pop art, pixel art…) vira pergunta ao autor com o motivo da marca.
- O fragmento do estilo entra no prompt **depois** do bloco de marca, nunca no lugar dele.
- `portinari marca` **bloqueia** execução com `brand/` atrás do remoto (A13).
- ✔ mudar `FORMATOS.md` num `brand/` de teste muda o tamanho de entrega **sem tocar em código**;
  estilo recusado gera pergunta; base+modo incompatíveis geram aviso; `isometric` sem `--piloto` recusa.

**E12 — Entrega do prompt** · `feat(entrega)` · **implementado em 20/09/2026** · spec: `specs/epicos/epico-12-entrega-prompt.md`
- `portinari entregar` grava `final/prompt_<modo>.md` (colável, autossuficiente: criativo + bloco de
  marca + fragmento de estilo + técnico), `final/COMO-GERAR.md` (modelo, proporção, tamanho e
  formato do uso conforme `FORMATOS.md`, área segura, o que conferir na imagem) e `manifest.json`.
- Recusa entregar prompt que não passou pelas checagens que o código sabe fazer: hex da paleta
  presentes, termos do enriquecimento cobertos, bloco de marca íntegro, um modo por arquivo.
- ✔ o prompt entregue, colado num gerador limpo, não depende de nenhum arquivo do repo; ✔ prompt
  sem bloco de marca ou com termo do enriquecimento faltando é recusado com mensagem acionável.

**E9 — Documentação e piloto** · `docs(portinari)` · **documentação feita em 20/09/2026; piloto pendente**
- ⚠️ **Revisado em 20/09/2026 (A16/A17):** o critério de pronto deixa de ser "PNG em exatamente 2560×1440" e passa a ser: prompt colável que, colado no Nano Banana Pro pelo autor, produz peça aprovada no Gate 2. O relatório do piloto compara a imagem de validação (flash, 1K) com a final do autor (Pro).
- `CLAUDE.md` (regras invioláveis, estrutura, fonte única de cada coisa, git) e `README.md`
  (como escrever um pedido, como rodar, como retomar, "se algo der errado") no padrão dos irmãos.
- **Fase 3:** execução de ponta a ponta com `exemplo-cafe-lca.md`, gates comigo, e relatório
  (o que funcionou, o que o crítico reprovou e por quê, nº de gerações, melhorias).
- ✔ ~~`final/<slug>_light.png` e `_dark.png` em exatamente 2560×1440~~ → por A16: `final/prompt_dark.md` e `prompt_light.md` coláveis, `COMO-GERAR.md` e manifesto completo. **Falta rodar o piloto de ponta a ponta com você nos dois gates.**

## 7. Riscos

| # | Risco | Sev. | Mitigação |
| --- | --- | --- | --- |
| **R1** | ~~(A10: some no caminho da API — a `generateContent` recebe o prompt literal; vale só para o fallback `agy`)~~ O LLM do `agy` reescreve/encurta o prompt → o bloco de marca não chega íntegro | alta | Verificação pós-fato do `Using prompt:`; retentativa com instrução de literalidade; se nunca vier íntegro, **paro e trago alternativas** (não aprovo peça sem bloco verificado). Medido: 5/14 sessões reescritas |
| **R2** | ~~(A10: o Pro gera 2K/4K nativos)~~ Saída 1K → 2560×1440 por ampliação ×1,86 fica mole; o "grão" de papel some/vira borrão | alta | Lanczos; medir em S1; **Q1**. Alternativas fora do `agy` exigem chave/API e decisão sua |
| **R3** | ~~(A10: o modelo é parâmetro explícito da API e vai para o manifesto)~~ Nano Banana Pro não verificável | média | Ler `ModelName` em S1; se ilegível, documento como "não verificado" no manifesto de toda execução |
| **R4** | Edição por referência (`ImagePaths`) pode não existir/funcionar → derivação light/dark cai | alta p/ E8 | S2 antes de E8; planos F1/F2 |
| **R5** | Saída JPEG: artefatos de compressão distorcem a checagem de paleta e a "granulação" | média | Tolerância calibrada em imagens reais (E5); checar antes de qualquer reamostragem |
| **R6** | Checagens objetivas mal calibradas (falso positivo/negativo) | média | Calibrar nas 13 refs + gerações reais; aviso vs falha em dois níveis; crítico humano no gate 2 |
| **R7** | Crítico visual subjetivo / viés de aprovar | média | Bloqueantes explícitos; recebe `checagens.json`; nunca vê o prompt (D7 — controle por instrução) |
| **R8** | Modelo alucinando texto/logo/`$` numa imagem de LCA (finanças brasileiras) | média | Prompt "sem texto"; crítico confere; bloqueante na rubrica |
| **R9** | Permissões de `-p` para `generate_image` desconhecidas; `--dangerously-skip-permissions` é amplo | média | Preferir allowlist; se precisar da flag, só no smoke test e com `--sandbox`/`--add-dir` restritos — **Q10** |
| **R10** | Quota/custo por imagem desconhecido; conversas acumulam em `~/.gemini/antigravity-cli/brain/` | baixa | Contador e teto próprios; imagem copiada para `output/`; não apago nada em `~/.gemini` |
| **R11** | Skills/agentes só carregam abrindo o Claude Code em `pipelines/portinari` | baixa | Documentar no README (mesmo aviso do `hemingway`) |
| **R12** | Dois repos git aninhados (C11): `git add -A` na raiz pode gerar gitlink acidental | baixa | Commits só dentro de `pipelines/portinari`; pedir `.gitignore` na raiz (Q8) |
| **R13** | O piloto (café → LCA) mistura dois mundos visuais numa imagem só; risco de "duas ideias" | média | Diretor de Arte deve propor **uma** metáfora de transformação, não duas metades ilustradas |

**Riscos novos (20/09/2026)**

| # | Risco | Sev. | Mitigação |
| --- | --- | --- | --- |
| **R14** | Faturamento não habilitado: todo modelo de imagem devolve 429 `limit: 0` | **alta** | Mensagem de erro do `gemini.py` diz exatamente isso e aponta o console; E5b (colagem manual) segue como caminho alternativo |
| **R15** | Custo por imagem no Pro × nº de iterações | média | Papéis: toda iteração no flash, só a final no Pro (A10); teto de gerações já existente, contado por papel no manifesto |
| **R16** | Chave vazando em commit/log | **alta** | `.env` no `.gitignore` (feito); a chave nunca entra em `gen_KK.json`, em `geracoes.jsonl` nem em mensagem de erro |
| **R17** | `FORMATOS.md`/`estilos/` mudam de estrutura e o parser quebra em silêncio | média | Parser falha alto (como `_bloco-marca.md` já faz), fingerprint cobre os dois, teste de runtime com `brand/` de fixture |

## 8. Perguntas

**Bloqueantes** (preciso da resposta para começar os épicos indicados):

- **Q1 (E5, E9) — Resolução.** A ferramenta entrega ~1376×768. Aceita **ampliar por Lanczos
  até 2560×1440** (ficará mais macio, sem detalhe novo), ou 2560×1440 *nativos* são requisito?
  Se forem, o caminho deixa de ser `agy` e preciso que você decida a alternativa.
  *Recomendo aceitar a ampliação, medir em S1 e reavaliar com a imagem real na mão.*
- **Q2 (E7) — Sombras.** Confirma que a **marca vence** o pedido: rubrica exige *ausência* de
  sombra e profundidade por degrau de tom (C1)? *Recomendo sim.*
- **Q4 (E8, E9) — Modo primário.** Sem regra na marca (C7). Qual é o primário para "capa de
  post para substack" — **dark** ou light? *Recomendo dark: a pilha escura tem 4 níveis e a
  clara 3; derivar do mais rico para o mais pobre é menos arriscado que o inverso — é raciocínio
  meu, não regra da marca.*
- **Q5 (E2) — Bloco de marca (C9, C10).** (a) Injetar **as duas pilhas** ou só a do modo?
  (b) A seção "descritores proibidos" entra no prompt (literal ao "colar inteiro") ou vira
  **só lint** da parte criativa? *Recomendo: só a pilha do modo + a lista como lint apenas.
  Isso contraria "colar inteiro, não resumido" do `CHECKLIST-PR`; se preferir o literal, faço o
  literal e comparo em S1.*
- **Q7 (E1) — Presets.** Confirma `capa de post para substack = 16:9, 2560×1440` (única fonte é
  o seu exemplo) e me dá, se quiser cobrir agora, thumbnail do YouTube e cabeçalho de e-mail do
  Substack. *Sem resposta, esses USOs geram pergunta ao autor.*

**Não bloqueantes** (sigo com o default se você não disser nada):

- **Q3 — Portinari como consumidor (C2).** Confirma que devo tratar o Portinari como
  consumidor legítimo da camada de ilustração e que a atualização de `brand/` é sua? *Default:
  sim, e só reporto.*
- **Q6 — Frame/hairline (C5).** Frame retangular 1 px é aplicado depois, no layout? *Default:
  sim; a imagem entregue é cheia, sem moldura.*
- **Q8 — Git.** (a) Commitar tudo no repo `pipelines/portinari` (remote próprio), sem push;
  (b) você adiciona `/pipelines/portinari/` ao `.gitignore` da raiz; (c) como a raiz não tem
  remote, o passo "`brand/` atrás do remoto?" registra "sem remoto" e, no lugar, avisa se
  `brand/` tem **alterações não commitadas** — serve? *Default: sim aos três.*
- **Q9 — `output/`.** JPEG brutos e PNG finais ficam **fora** do git (`.gitignore`); versiono só
  `brief.json`, `brand_snapshot.json`, `conceitos.md`, prompts, críticas e `manifest.json`.
  Quer as finais em Git LFS como o `hemingway` faz com áudio? *Default: fora do git.*
- **Q10 — Smoke tests.** Autoriza **2 gerações reais** (S1 headless; S2 edição), rodando o `agy`
  em pasta de scratch com `--add-dir` restrito, e, **só se `-p` pedir permissão**, usar
  `--dangerously-skip-permissions` nessas duas chamadas? *Default: sim às duas gerações, sem a
  flag até ser necessária.*
- **Q11 — Idioma do prompt (D1).** Parte criativa em inglês + bloco de marca como está. *Default:
  sim.*

## 9. Próximo passo

Com **Q1, Q2, Q4, Q5 e Q7** respondidas (ou "seguir as recomendações"), começo pelo E1 e sigo
épico a épico; o primeiro contato real com o `agy` é o E3 (S1/S2), depois de o wrapper estar
testado com um `agy` falso. Nada foi commitado ainda — sugiro que o primeiro commit do repo seja
"docs: plano e levantamento do agy", junto com a sua aprovação.
