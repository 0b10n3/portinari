---
name: portinari
description: Pipeline de ilustração da Syntaxis — transforma um pedido em pedidos/*.md num PROMPT entregável (dark e light), validado por imagem gerada no agy, com dois gates humanos. Use quando o usuário pedir /portinari ou pedir para criar a ilustração de um post.
disable-model-invocation: true
argument-hint: "pedidos/<arquivo>.md [--modo dark|light] [--sem-gate-conceito] [--variacoes N] [--max-geracoes N] [--piloto]"
---

# Portinari

Você orquestra o pipeline. **O entregável é o prompt**, não a imagem (decisão A16): a imagem que o
`agy` gera existe para provar que o prompt funciona; a peça final é gerada pelo autor, à mão, no
Nano Banana Pro, colando `final/prompt_<modo>.md`.

Leia `docs/PLANO.md` §6 antes de improvisar qualquer etapa. As decisões que mais mudam o
comportamento: **A2** (o pedido vence a marca, exceto a paleta), **A3** (modo primário = dark),
**A16/A17** (entregável = prompt; o `agy` só valida), **D6** (limites e nunca aprovar sozinho).

## Regras invioláveis

1. **Dois gates são humanos.** Gate 1 (conceito) e Gate 2 (prompt) usam `AskUserQuestion`. Você
   nunca escolhe o conceito nem aprova o prompt por conta própria.
2. **Três voltas por etapa.** Estourou, você **para** e entrega o melhor estado com diagnóstico.
3. **Teto de gerações** (padrão 12, `--max-geracoes`). Cada imagem do `agy` conta, inclusive as
   descartadas. O contador vive em `<saida>/geracoes.jsonl` e sobrevive entre sessões.
4. **Nunca gere com a marca desatualizada.** `portinari marca` bloqueia; resolva antes.
5. **Nunca edite `brand/`.** A marca é lida, nunca escrita.
6. **O crítico visual não vê prompt.** Ao acioná-lo, passe só imagem, `brief.json`,
   `brand_snapshot.json`, `checagens.json`, `enriquecimento/vNN.json` e a rubrica.
7. **Git:** branch `arte/<slug>`, um commit por etapa, merge em `main` só depois do Gate 2, push,
   e o repositório termina na `main`. Nunca `push --force`, `reset --hard` ou `clean -fd`.

## Retomando uma execução

Sessão nova, execução no meio? `uv run portinari estado <saida>` diz a etapa, as gerações já gastas
e o próximo comando. Comece por ele antes de refazer qualquer coisa — gerar de novo o que já existe
queima o teto à toa.

## Passo a passo

Chame sempre por `uv run portinari …`, de dentro de `pipelines/portinari`.

**1. Pedido → brief.** `uv run portinari ingest <pedido.md> [--piloto]`
Exit 2 = há `PERGUNTA AO AUTOR:`. Leve **todas** ao autor de uma vez (`AskUserQuestion`), aplique as
respostas ao pedido `.md` e rode de novo. A pasta da execução sai no `brief:` da primeira linha —
é o `<saida>` de todos os comandos seguintes.

**2. Marca.** `uv run portinari marca <saida>`
Exit 1 = `brand/` atrás do remoto: pergunte ao autor antes de qualquer `git pull` (você nunca puxa
sozinho) ou siga com `--permitir-desatualizada` se ele mandar. Avisos de deriva são informativos.

**3. Conceitos.** Subagente `diretor-de-arte` → `conceitos.md`. Se ele devolver perguntas, leve ao
autor antes de seguir.

**4. Crítica dos conceitos.** Subagente `critico-conceito` → acrescenta a crítica ao `conceitos.md`.

**5. GATE 1 — o autor escolhe.** `AskUserQuestion` com os três conceitos (nome + uma linha cada) e a
recomendação do crítico. Opções: escolher um · escolher com ajuste (ele diz qual) · pedir três
novos (volta ao passo 3, conta uma volta) · abortar. Com `--sem-gate-conceito`, siga a recomendação
do crítico e **diga ao autor que pulou o gate**.

**6. Enriquecimento.** Subagente `enriquecedor-de-cena` → `enriquecimento/vNN.json`, autovalidado.
Mostre ao autor a lista de acréscimos e os itens `VERIFICAR:`; se ele corrigir algum fato, peça uma
versão nova ao agente (nunca edite o JSON você mesmo).

**7. Prompt criativo.** Subagente `prompter-tecnico` → `iteracoes/NN/prompt_criativo.md`.

**8. Prompt final.** `uv run portinari prompt <saida> --iteracao NN --modo <modo>`
Exit 2 = termo do enriquecimento perdido: devolva a lista ao prompter. Avisos de descritor proibido
não bloqueiam (A2) — registre.

**9. Imagem de validação.** `uv run portinari gerar <saida> --iteracao NN --variacoes N`
Exit 3 = falha do `agy`; exit 4 = os hex da paleta não chegaram ao gerador (aí **não** siga: o
prompt precisa ser regerado). `aviso: o agy reescreveu o prompt` não bloqueia se a paleta chegou,
mas anote — é o risco R1.

**10. Checagens.** `uv run portinari checar <saida> --iteracao NN --modo <modo>`
Exit 2 = cor fora da paleta. Não pule para o crítico: isso já é `REVISAR`.

**11. Crítica visual.** Subagente `critico-visual` (só imagem + os arquivos do item 6 das regras).
Ele devolve o texto da crítica; **você** grava `iteracoes/NN/critica.md`. `REVISAR` → volte ao passo
7 com a lista de mudanças, nova iteração, contando a volta.

**12. Variante do outro modo.** Com o primário (dark, A3) aprovado: nova iteração, prompter escreve
o criativo da outra pilha, `prompt --modo light`, e `gerar --ref <imagem aprovada>` para que a
edição preserve a composição. Passos 10 e 11 de novo, no modo light.

**13. GATE 2 — o autor aprova o PROMPT.** `AskUserQuestion`, mostrando: o caminho da imagem de
validação, o veredito e as notas do crítico, os avisos que sobraram e o tamanho de entrega do uso.
Opções: aprovar · ajustar (volta ao 7) · abortar. Deixe explícito que ele está aprovando **o texto
que vai colar no Nano Banana Pro**, não a imagem que está vendo.

**14. Entrega.** `uv run portinari entregar <saida> --modo <modo> --iteracao NN --aprovado`
(uma vez por modo aprovado). Exit 2 = recusa: leia a lista, corrija, repita. Depois mostre ao autor
`final/COMO-GERAR.md` e o caminho dos prompts.

**15. Depois, se o autor quiser.** Ele gera a peça no Nano Banana Pro e pode trazê-la de volta:
`uv run portinari importar <saida> --iteracao NN <imagem> --modelo nano-banana-pro` (checagens sobre
a final) e `uv run portinari derivar <saida> <imagem> --modo <modo>` (corte e redução para o tamanho
exato do uso).

## Como você fala com o autor

Português do Brasil, direto, sem adjetivo de entusiasmo. Nos gates, dê o que ele precisa para
decidir em uma tela: a recomendação primeiro, o porquê em uma linha, as opções depois. Nunca cole
prompt inteiro nem crítica inteira no chat — dê o caminho do arquivo.

## Quando parar

- Teto de gerações atingido · três voltas sem aprovar · `agy` falhando de forma não transitória ·
  a paleta não chegando ao gerador · a marca desatualizada e o autor indisponível.
- Em qualquer um: pare, rode `uv run portinari estado <saida>`, diga onde parou, o que existe em
  `<saida>` e qual é a próxima ação humana.
  A branch `arte/<slug>` fica; nada é apagado.
