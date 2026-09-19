# agy (Antigravity CLI) — o que foi confirmado e o que não foi

Levantamento da Fase 0 (só leitura e prompts de texto) e resultados do smoke test S1/S2 (§6), todos de
18/09/2026. As duas únicas gerações reais até aqui são as do S1 (1 geração) e S2 (1 edição).

Legenda: ✅ confirmado por execução ou por registro real em disco · 🟡 evidência indireta ·
❓ não confirmado (só um smoke test resolve).

## 1. Binário e interface geral

| Item | Estado | Detalhe |
| --- | --- | --- |
| Binário | ✅ | `/home/saga/.local/bin/agy` (Go, 224 MB). Não existe `--version`; a versão vem de `agy changelog` (topo: **1.2.7**) |
| Modo não interativo | ✅ | `agy -p "<prompt>"` (`--print`/`--prompt`). Uma execução, imprime a resposta e sai |
| Saída estruturada | ✅ | `--output-format json` devolve uma linha: `{"conversation_id","status":"SUCCESS","response","duration_seconds","num_turns","usage":{…}}`. Também há `stream-json` e `--input-format stream-json` |
| Seleção de modelo | ✅ | `--model <id>`, ids de `agy models`. Testado com `gemini-3.8-flash-low`, exit 0 |
| Timeout | ✅ | `--print-timeout` (padrão era 5 min, virou ilimitado na 1.2.6 — changelog) |
| Diretório de trabalho | ✅ | `--add-dir` (repetível), `--project`, `--new-project` |
| Permissões | 🟡 | `--dangerously-skip-permissions` auto-aprova tudo; `--sandbox` restringe; allowlist em `~/.gemini/antigravity-cli/settings.json` (`permissions.allow`). Não sei qual permissão `generate_image` exige em `-p` |
| Subcomandos | ✅ | `agent(s)`, `changelog`, `help`, `install`, `mcp`, `mic-serve`, `models`, `plugin(s)`, `remote-control`, `update` |
| Plugins / MCP no agy | ✅ | Nenhum plugin importado, nenhum MCP configurado (`agy plugin list`, `agy mcp list`) |
| Skills relevantes em `.agents/skills/` | ✅ | Só `design-taste-frontend` (UI). Nada de geração de imagem. O plugin `agy` do Claude Code (`~/.claude/plugins/.../agy/0.4.1`) traz `/agy:image`, um wrapper fino sobre `agy -p` |

## 2. `agy models` — não há Nano Banana Pro

```
gemini-3.8-flash-{high,medium,low} · gemini-3.7-flash-{high,medium,low} · gemini-3.6-flash-{high,medium,low}
gemini-3.1-pro-{high,low} · claude-sonnet-4-6 · claude-opus-4-6-thinking · gpt-oss-120b-medium
```

`--model` escolhe o **LLM de texto que orquestra a sessão** (o que decide chamar a ferramenta).
Nenhum modelo de imagem aparece. O plugin `/agy:image` diz "Imagen under the hood"; os registros
do S1 mostram outra coisa (§3.2: `gemini-3.1-flash-image`).

## 3. Geração de imagem: é uma *ferramenta* do agente, não um comando

Não existe `agy generate-image`. O caminho é pedir ao agente, em linguagem natural, que use a
ferramenta interna **`generate_image`** ("Use your built-in generate_image tool to create the
following image. Description: …" — é assim que o wrapper do plugin e as sessões antigas fazem).

### 3.1 Schema da ferramenta (✅ 45 chamadas reais em `~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript_full.jsonl`)

| Argumento | Observado |
| --- | --- |
| `Prompt` | texto livre, 900–2.500 caracteres nas chamadas reais |
| `ImageName` | slug sem extensão |
| `AspectRatio` | `16:9` (18×), `1:1` (17×), `4:3` (5×), `3:4` (3×); omitido em 2 |

**Declaração da ferramenta, transcrita pelo próprio agente (✅ S0, texto-only):** `Prompt` (obrigatório),
`ImageName` (obrigatório, minúsculas com sublinhado, até 3 palavras), `AspectRatio` (opcional, padrão
`1:1`; enum **`1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9`** — o binário tem mais constantes, como 21:9 e
8:1, mas elas **não** são oferecidas ao modelo), `ImagePaths` (opcional, **até 3** caminhos absolutos
"de referência ou edição/combinação"), mais `toolAction`/`toolSummary` (metadados).

**Campos que existem no protobuf mas nenhuma chamada real exercitou** (🟡, símbolos Go
`ActionGenerateImage`/`GenerateImage`/`GetImageGenerationRequest`): `ImagePaths` (imagens de
referência), `OutputPath`, `ModelName`, `InputImages`. A camada de API por baixo tem `ImageSize`
(inclui `IMAGE_SIZE_FOUR_K`), mas o schema da ferramenta **não** mostra `ImageSize`/resolução.

### 3.2 Modelo por trás — ✅ **NÃO é o Nano Banana Pro** (achado do S1)

O banco da conversa do S1 (`~/.gemini/antigravity-cli/conversations/<id>.db`, tabela `steps`) grava o
modelo do passo de imagem como **`gemini-3.1-flash-image`** (família "Nano Banana 2"), e a mesma
string está embutida no binário do `agy` ao lado de `GenerateContent`. O Nano Banana Pro seria
`gemini-3-pro-image`. Não há configuração local para trocar: o binário lê a lista
`image_generation_model_ids` do servidor, `settings.json` só tem `model` (orquestrador),
`permissions` e `trustedWorkspaces`, e a ferramenta não tem parâmetro de modelo. Pedir "use o nano
banana pro" no prompt não muda nada (as sessões antigas só rotulavam a chamada assim).

**Consequência:** a premissa "Nano Banana Pro via `agy`" não se cumpre nesta conta/versão (agy
1.2.7). A qualidade observada é boa (ver §6), mas a decisão é sua: ver PLANO, "Achados do S1".

### 3.3 Resolução — ✅ ~1K, e não dá para pedir mais (S1)

Todas as imagens reais (30+ antigas, S1 e S2) saem no tier ~1K: 16:9 → 1376×768. Uma frase no prompt
pedindo "highest resolution / target 2560x1440" **não mudou nada** (S1). Não há parâmetro de tamanho
(a camada de API tem `ImageSize`, incluindo `IMAGE_SIZE_FOUR_K`, mas a ferramenta não o expõe).
**2560×1440 exige ampliar 1376×768 em ×1,86.**

### 3.4 Onde e em que formato a saída cai — ✅

- **JPEG**, não PNG: `~/.gemini/antigravity-cli/brain/<conversation_id>/<ImageName>_<epoch_ms>.jpg`.
- O passo de geração do transcript (tipo `GENERATE_IMAGE` nas sessões antigas, **`GENERIC`** no agy 1.2.7 em headless) termina com
  `Generated image is saved at <caminho absoluto>.jpg.` — parseável.
- `conversation_id` vem no JSON do `--output-format json`, então dá para achar a pasta sem
  depender de o modelo imprimir o caminho (o wrapper do plugin depende de o modelo escrever
  `IMAGE_PATH:`, frágil).
- Em duas sessões o agente ainda converteu/copiou o JPEG para PNG dentro do post por conta
  própria — comportamento do LLM, não da ferramenta.
- ❓ Se `OutputPath` é aceito e grava direto na pasta da execução.

### 3.5 O prompt NÃO chega intacto — ✅ medido

Há um LLM de texto entre nós e a ferramenta. Comparei a `Description:` enviada com o `Prompt` que
o agente passou à `generate_image` em 14 sessões antigas (similaridade de sequência):

- 9 sessões: 0,89–0,97 — quase literal, mas **~5–20% mais curto** (o agente resumiu/cortou;
  comparação aproximada, a extração da `Description:` é por regex);
- 5 sessões: 0,01–0,22 — **reescrito por inteiro** (uma delas, `e397df47`, era um teste
  degenerado com prompt `--help`; sem ela, 4 de 13).

Consequência: a "injeção determinística do bloco de marca" só é garantida se o código
**verificar depois** o `Using prompt:` registrado no passo do transcript e recusar/retentar quando
o bloco não estiver lá. Ver PLANO, risco R1.

### 3.6 Imagem de referência / edição — ✅ funciona (S2)

`ImagePaths` é aceito em headless e edita de fato: a composição, os elementos e o enquadramento se
mantiveram e só a paleta mudou (dark → light). Saída de novo 1376×768 JPEG. Detalhes e defeitos em §6.

## 4. Erros e códigos de saída

| Situação | Estado | Detalhe |
| --- | --- | --- |
| Sucesso headless | ✅ | exit `0`, `"status":"SUCCESS"`. **Mas `status` não é confiável:** numa sondagem de texto veio `"status":"ERROR"` (`error`: filtro de segurança "material que se assemelha a obras protegidas") com exit `0` e resposta válida. O critério de sucesso do Portinari é existir o passo de geração no transcript |
| Falha de agente/API em `-p` | 🟡 | changelog 1.2.6: linha `AGY_ERROR: {…}` (status canônico, código HTTP/gRPC, retryable, id) no **stderr** e exit **`3`** |
| Falha do passo de imagem | 🟡 (não reproduzida) | logs antigos: `CORTEX_STEP_TYPE_GENERATE_IMAGE: no image generated in response` (2 vezes em 11/08, seguidas). Não sei se em `-p` isso vira exit ≠ 0 ou `status` ≠ SUCCESS com resposta "desculpe" |
| Retentativa interna | 🟡 | changelog 1.2.1: 502/503/504/429 por minuto são retentados dentro do agy com backoff (teto de 30 s desde 1.2.7) |
| Latência por imagem | ✅ | ~10 s (timestamps de `Created At`/`Completed At` nos transcripts) |
| Custo/quota por imagem | ❓ | desconhecido; o Portinari contará gerações por conta própria |

## 5. Plano de verificação — executado em 18/09/2026

S1 (1 geração, headless) e S2 (1 edição) rodaram pela CLI do próprio Portinari, numa pasta de
scratch fora do repo. Total: **2 gerações**.

## 6. Resultados do smoke test

| Pergunta | S1 (geração) | S2 (edição por `ImagePaths`) |
| --- | --- | --- |
| Funciona sem TUI? Permissões? | ✅ `agy -p … --output-format json --model gemini-3.8-flash-low`, **sem** `--dangerously-skip-permissions` e sem allowlist extra | ✅ idem, com `--add-dir` da pasta da referência |
| Tempo | ~24 s por imagem (wall ~29 s incl. `uv`) | ~28 s |
| Onde cai o arquivo | ✅ `brain/<conversation_id>/gen_01_<ms>.jpg`; o passo do transcript diz `Generated image is saved at <abs>.jpg.` | idem |
| **Tipo do passo no transcript** | ✅ **`GENERIC`** (não `GENERATE_IMAGE`, que só aparece nas sessões antigas) — o parser identifica pelo conteúdo, não pelo tipo | idem |
| Prompt chegou íntegro? | ✅ **sim**: 3.551 caracteres, comparação com espaços normalizados idêntica, orquestrador `gemini-3.8-flash-low` (instrução de literalidade + delimitadores `<<<PROMPT`/`PROMPT>>>`). 1 amostra — R1 continua aberto | ✅ sim (2.755 caracteres) |
| Dimensões | 1376×768 JPEG, mesmo com pedido de maior resolução no prompt | 1376×768 JPEG |
| Modelo de imagem | ✅ `gemini-3.1-flash-image` (§3.2) | idem |
| Qualidade | boa: paper cut plano, conceito legível, uma ideia, acento só na transformação; sombras coerentes (o pedido as quer) | composição preservada; paleta clara aplicada |
| Defeitos | cerejas **vermelhas** (erro do meu prompt: fora da paleta vinculante) | (1) **legenda de amostras com nomes de token e hex desenhada na imagem** — vinda da tabela de paleta do bloco injetado; (2) certificado virou bloco grande de lime.700 (acento ≫ 1%); (3) algumas listras do morro mudaram de forma |

Correções feitas por causa disto: o bloco injetado passou a listar **só hex, em prosa, sem tabela
nem nome de token** (E3); o Prompter deve usar apenas cores da paleta para objetos (cerejas etc.) e
dizer onde o acento deve aparecer também nas edições.

**Ainda não confirmado:** `OutputPath`; exit code quando só o passo de imagem falha; comportamento
sob o filtro de segurança do orquestrador durante uma geração real; quota por imagem.
