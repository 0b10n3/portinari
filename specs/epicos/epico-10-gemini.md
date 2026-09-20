# Épico 10 — Gerador pela API do Gemini (flash para avaliar, Pro para a final)

**Status:** especificado · **ADIADO por A17 (20/09/2026)** — não implementar por ora.
**Decisão de origem:** A10, A11, A15 (20/09/2026, PLANO).

> A16/A17 mudaram o alvo: o entregável é o prompt, a validação roda no `agy` (sem faturamento) e a
> imagem final é gerada à mão no Nano Banana Pro. Esta spec fica de pé, pronta, para o dia em que
> houver faturamento habilitado **e** valer a pena automatizar a geração da final.

## 1. O que muda

O `agy` (E3) entrega imagem, mas com três defeitos conhecidos: modelo fixo em
`gemini-3.1-flash-image`, saída ~1K e um LLM de texto que pode reescrever o prompt (R1). A API do
Gemini resolve os três: o modelo é parâmetro, o Pro gera 2K/4K nativos e o prompt chega **literal**.

```
prompt_final.md ─▶ portinari gerar --via gemini --papel rascunho   (gemini-3.1-flash-image)
                        │                                           iteração barata, crítico visual
                        └─ Gate 2 aprovado ─▶ --papel final         (gemini-3-pro-image)
```

**Regra de custo (A10):** toda volta de crítica roda no **flash**. O **Pro** só entra depois que a
composição está aprovada — e nas derivações light/dark dessa composição (E8).

## 2. Modelos (verificados na API em 20/09/2026)

| Papel | Modelo | Nome comercial |
| --- | --- | --- |
| `rascunho` (padrão) | `gemini-3.1-flash-image` | Nano Banana 2 |
| `final` | `gemini-3-pro-image` | Nano Banana Pro |

Não existe modelo de **imagem** "3.8 flash": `gemini-3.8-flash` é texto. Também disponíveis, não
usados por padrão: `gemini-3.1-flash-lite-image`, `gemini-2.5-flash-image`, e os `-preview` dos dois
principais. Constantes nomeadas em `gemini.py`; `--modelo` sobrepõe.

## 3. Interface

```
portinari gerar <saida> --iteracao N [--via gemini|agy] [--papel rascunho|final]
                        [--modelo ID] [--tamanho 1K|2K|4K] [--variacoes N]
                        [--ref IMG]… [--max-geracoes N]
```

- `--via` padrão `gemini`; `--via agy` mantém o caminho do E3 inteiro (fallback testado).
- `--tamanho` padrão: **o maior que o modelo aceitar** (A1), caindo para o menor em erro de
  parâmetro — e registrando a queda no `gen_KK.json`.
- `--ref` vira `inlineData` na requisição (edição/derivação); os mesmos caminhos que o `agy` recebia.

### Requisição

`POST https://generativelanguage.googleapis.com/v1beta/models/<modelo>:generateContent`,
cabeçalho `x-goog-api-key`, corpo:

```jsonc
{"contents": [{"parts": [{"text": "<prompt_final.md literal>"},
                         {"inlineData": {"mimeType": "image/png", "data": "<base64>"}}]}],
 "generationConfig": {"responseModalities": ["IMAGE"],
                      "imageConfig": {"aspectRatio": "16:9", "imageSize": "4K"}}}
```

A imagem volta em `candidates[0].content.parts[].inlineData.data` (base64). `finishReason`
diferente de `STOP` sem parte de imagem = erro com a razão no texto (ex.: `PROHIBITED_CONTENT`).

**A chave nunca é gravada:** não entra em `gen_KK.json`, `geracoes.jsonl`, comando logado nem
mensagem de erro. `gemini.py` a lê de `GEMINI_API_KEY` (ambiente) ou do `.env` do pipeline
(`.gitignore`, A15) — 3 linhas de regex, sem `python-dotenv`.

## 4. O que **não** muda

Reaproveita `agy.py` inteiro no que é comum: `Geracao`, `_registrar`, `geracoes.jsonl`, `_contar`,
`melhor_proporcao`, `montar_prompt`, teto de gerações, layout `gen_KK.{ext,prompt.md,efetivo.md,json}`.
Campos novos na `Geracao`: `papel` e `tamanho_pedido`; `origem` ganha o valor `"gemini"`;
`modelo_imagem` passa a ser preenchido sempre (hoje só na importação manual).
`fiel` = `True` por construção e `efetivo.md` grava o prompt enviado (que é o pretendido).

## 5. Erros e retentativa

| Situação | Comportamento |
| --- | --- |
| 429 / 500 / 503 | retentativa com *backoff* exponencial (mesma escada do `agy`: 5s, 10s, 20s) |
| 429 com `free_tier_requests, limit: 0` | **não retenta**: erro acionável — "modelo de imagem exige faturamento habilitado no projeto desta chave" (R14) |
| 400 em `imageConfig` | cai para o `imageSize` menor seguinte e retenta uma vez; registra a queda |
| resposta sem parte de imagem | erro com `finishReason` e o texto devolvido |
| 401/403 | erro imediato: chave inválida ou sem acesso ao modelo |

## 6. Testes

Servidor HTTP falso (`http.server` em *thread*, base URL injetada) — **nenhum teste toca a rede**:

- sucesso no flash e no Pro: grava `gen_01.png`, dimensões nativas corretas, `papel`/`modelo_imagem`
  no JSON, linha em `geracoes.jsonl`;
- 429 transitório → sucesso na 2ª tentativa; 429 `limit: 0` → falha sem retentar, mensagem cita
  faturamento; 500 esgotando as tentativas;
- 400 de `imageSize` → cai de 4K para 2K e registra;
- resposta sem imagem (`PROHIBITED_CONTENT`) → erro com a razão;
- referência (`--ref`) vira `inlineData` com o mimeType certo;
- teto de gerações compartilhado com o `agy` (contagem única por execução);
- **a chave não aparece** em nenhum arquivo gravado nem em `str(excecao)`.

## 7. Critérios de aceite

- ✔ `uv run pytest` verde, sem rede.
- ✔ `portinari gerar --via agy` continua idêntico ao E3 (teste do `agy` falso intacto).
- ✔ `gen_KK.json` diz modelo, papel, tamanho pedido e obtido, e as dimensões nativas.
- ✔ Uma geração real no flash (1 imagem, sua autorização) confirma `imageConfig` e as dimensões —
  **depende de faturamento habilitado**; até lá, o épico fecha com o servidor falso e o bloqueio
  fica registrado aqui e no PLANO (R14).
