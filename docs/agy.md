# agy (Antigravity CLI) — o que foi confirmado e o que não foi

Levantamento da Fase 0, 18/09/2026. **Nenhuma imagem foi gerada.** A única chamada ao `agy` que
usou o modelo foi um prompt de texto trivial (`Responda apenas com a palavra: ok`) para capturar o
formato de saída headless.

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
Nenhum modelo de imagem aparece. O código do `agy-run.sh` e a skill `/agy:image` dizem "Imagen
under the hood" — afirmação do plugin, **não verificada**.

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

Enum de proporções embutido no binário (🟡, nomes de constantes `ASPECT_RATIO_*`): 2:3, 3:2, 3:4,
4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:8, 8:1 (+ 1:1).

**Campos que existem no protobuf mas nenhuma chamada real exercitou** (🟡, símbolos Go
`ActionGenerateImage`/`GenerateImage`/`GetImageGenerationRequest`): `ImagePaths` (imagens de
referência), `OutputPath`, `ModelName`, `InputImages`. A camada de API por baixo tem `ImageSize`
(inclui `IMAGE_SIZE_FOUR_K`), mas o schema da ferramenta **não** mostra `ImageSize`/resolução.

### 3.2 Modelo por trás — ❓ não confirmado

- Nas sessões reais, pedir "utilizando o nano banana pro" só levou o agente a chamar a mesma
  `generate_image` (a chamada saiu rotulada "Generating illustration with Nano Banana Pro", sem
  nenhum argumento de modelo). **Não há como escolher o modelo pela interface.**
- 🟡 As dimensões de saída batem com a tabela de 1K do Gemini 3 Pro Image ("Nano Banana Pro"):
  16:9 → 1376×768, 1:1 → 1024×1024, 3:4 → 896×1200, 4:3 → 1200×896. É coerente com Nano Banana
  Pro, mas não prova: o registro do passo tem um campo `ModelName` que ainda não localizei em
  formato legível. O smoke test S1 deve tentar ler esse campo.

### 3.3 Resolução — ✅ o que sai é ~1K

Todas as 30+ imagens reais em `brain/` têm exatamente as dimensões acima. Não há como pedir 2K
pela ferramenta observada. **2560×1440 exige ampliar 1376×768 em ×1,86** (ver PLANO, Q1).

### 3.4 Onde e em que formato a saída cai — ✅

- **JPEG**, não PNG: `~/.gemini/antigravity-cli/brain/<conversation_id>/<ImageName>_<epoch_ms>.jpg`.
- O passo `GENERATE_IMAGE` do transcript termina com
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

### 3.6 Imagem de referência / edição — ❓ não confirmado

`ImagePaths` existe no protobuf; nenhuma das 45 chamadas o usou e todas as pastas
`.user_uploaded/` estão vazias. A derivação light→dark por edição depende disso. Só o smoke test
S2 responde.

## 4. Erros e códigos de saída

| Situação | Estado | Detalhe |
| --- | --- | --- |
| Sucesso headless | ✅ | exit `0`, `status":"SUCCESS"` |
| Falha de agente/API em `-p` | 🟡 | changelog 1.2.6: linha `AGY_ERROR: {…}` (status canônico, código HTTP/gRPC, retryable, id) no **stderr** e exit **`3`** |
| Falha do passo de imagem | 🟡 | logs antigos: `CORTEX_STEP_TYPE_GENERATE_IMAGE: no image generated in response` (2 vezes em 11/08, seguidas). Não sei se em `-p` isso vira exit ≠ 0 ou `status` ≠ SUCCESS com resposta "desculpe" |
| Retentativa interna | 🟡 | changelog 1.2.1: 502/503/504/429 por minuto são retentados dentro do agy com backoff (teto de 30 s desde 1.2.7) |
| Latência por imagem | ✅ | ~10 s (timestamps de `Created At`/`Completed At` nos transcripts) |
| Custo/quota por imagem | ❓ | desconhecido; o Portinari contará gerações por conta própria |

## 5. Plano de verificação (só depois da aprovação do PLANO)

**S1 — 1 geração, headless.** `agy -p … --output-format json --model <flash>` com um prompt de
~2,5k caracteres (bloco de marca real), `AspectRatio 16:9`, dentro de um diretório de scratch.
Confirma: (a) funciona sem TUI e com quais permissões; (b) onde o arquivo cai; (c) exit code e
`status`; (d) **o prompt chegou íntegro?** (lê `Using prompt:` no transcript); (e) dimensões
reais; (f) se há `ModelName` legível; (g) se `OutputPath` funciona.

**S2 — 1 edição.** Passar a imagem de S1 como `ImagePaths` e pedir a troca de pilha de cor
mantendo composição. Confirma (ou derruba) a derivação light/dark por edição.

Total: **2 gerações**. Nada além disso antes do épico de wrapper estar testado com um `agy`
falso.
