# Épico 4 — Enriquecimento do prompt

**Status:** implementado neste épico · **Decisão de origem:** A9, 18/09/2026 (PLANO).
**Motivo (achado do S1):** o pedido do exemplo (café → LCA) gerou uma imagem correta e limpa, mas
**rala**: nenhum trabalhador na lavoura, nenhuma ferramenta, papéis do título lisos. O prompt só
tinha o que o autor escreveu. Imagem profissional precisa de **camadas de leitura** — escala
humana, ofício, detalhe de material — que o autor não escreve num pedido de três linhas.

## 1. O que a etapa faz

Entre o **Gate 1** (conceito escolhido) e o **Prompter Técnico**, o agente `enriquecedor-de-cena`
transforma o conceito em uma **cena enriquecida e estruturada**. Ele **acrescenta**, nunca troca:
a ideia, a disposição pedida e o ponto focal do conceito escolhido permanecem.

```
conceito escolhido ─▶ enriquecedor-de-cena ─▶ enriquecimento/vNN.json
                                                   │
                       portinari enriquecer ◀──────┘   valida (código) + renderiza vNN.md
                                                   │
                          autor vê a lista de acréscimos e itens [VERIFICAR] (≤ 3 rodadas)
                                                   │
                       prompter-tecnico ─▶ prompt_criativo.md ─▶ portinari prompt
                                                                 (recusa se perdeu algum termo)
```

## 2. Entradas e saída

**Entradas do agente:** `brief.json`, `brand_snapshot.json`, `conceitos.md` (o escolhido), o
`CONTEXT` do pedido, imagens de referência.
**Saída:** `enriquecimento/vNN.json` (uma versão por rodada, nunca sobrescrita) no schema abaixo.
O código gera `vNN.md` (visão para o autor).

### Schema

```jsonc
{
  "conceito": "C2",                        // id do conceito escolhido em conceitos.md
  "pedido_preservado": ["produção agrícola de café à esquerda", "LCA à direita"],
  "elementos": [{
    "id": "e1",
    "zona": "esquerda|centro|direita|fundo|primeiro-plano",
    "papel": "foco|apoio|textura",
    "elemento": "o que é, em pt-BR, específico e visual",
    "termo_en": "frase curta em inglês que TEM de aparecer no prompt criativo",
    "cor": "pilha-N | figura-principal | figura-secundaria | acento | neutro",
    "origem": "pedido|contexto|dominio|oficio",
    "justificativa": "por que este detalhe existe",
    "verificar": false,                    // true = factual incerto; vai ao autor
    "nota_verificacao": ""
  }],
  "descartados": [{"elemento": "...", "motivo": "..."}],
  "cena": "parágrafo corrido em pt-BR descrevendo a cena enriquecida"
}
```

`origem`: **pedido** = está no pedido do autor · **contexto** = veio do `CONTEXT`/referências ·
**dominio** = conhecimento do assunto (ex.: como se colhe café) · **ofício** = detalhe de
construção do papel/composição (camadas, recortes, selo, dobra).

## 3. Princípios (o que o agente deve fazer)

1. **Uma ideia, um foco.** Exatamente um elemento `foco`. Enriquecer é dar camadas ao mesmo
   argumento, não empilhar uma segunda ideia.
2. **Escala humana e trabalho.** Pessoas como figuras planas de papel, **sem rosto** e sem
   caricatura; ferramentas e materiais do ofício, com exatidão. Incerteza factual vira `verificar`,
   nunca invenção (regra dos irmãos: "não invente"). Ideia boa mas arriscada vai para `descartados`.
3. **Detalhe de material.** Camadas de papel legíveis, bordas cortadas, folhas recortadas,
   perfurações, dobras, selos. Em documentos (títulos, certificados): selo, fita, borda picotada,
   canto dobrado, clipe, trama geométrica — **tudo sem nada legível**.
4. **Hierarquia e respiro.** 1 foco, poucos apoios, texturas discretas; preserve espaço negativo
   (recorte por USO, fundo mínimo da marca).
5. **Contexto brasileiro** quando pertinente (relevo, culturas, ferramentas, sacaria).
6. **Sem clichês financeiros** (touro/urso, moedas, gráfico subindo) salvo pedido explícito.
7. **A paleta é a única regra vinculante da marca (A2).** Todo elemento recebe um **papel de cor**
   (`pilha-N`, `figura-principal`, `figura-secundaria`, `acento`, `neutro`); objetos que "têm outra
   cor" na vida real (cereja vermelha, madeira, ouro) são reinterpretados na paleta. O acento
   aparece **em um ponto** (a virada).
8. **Densidade contida.** No máximo 12 elementos; pelo menos 3 acréscimos além do que o pedido já
   dizia (`origem` ≠ `pedido`), senão a etapa não enriqueceu nada.

## 4. Validador (código) — `portinari enriquecer`

**Erros (bloqueiam; o agente refaz, ≤ 3 rodadas por versão):**

| # | Regra |
| --- | --- |
| V1 | JSON válido no schema; `id` único; `termo_en` e `elemento` não vazios |
| V2 | Exatamente um elemento com `papel: foco` |
| V3 | Nº de elementos ≤ `--max-elementos` (padrão 12) |
| V4 | Acréscimos (`origem` ≠ `pedido`) ≥ `--min-acrescimos` (padrão 3) |
| V5 | `pedido_preservado` não vazio e ≥ 1 elemento de `origem: pedido` |
| V6 | `cor` ∈ papéis válidos **do modo** (`pilha-1..N` conforme a pilha do snapshot) |
| V7 | Nenhuma **palavra de cor fora da paleta** (vermelho/red, azul/blue, amarelo, laranja, roxo, rosa, marrom/brown, dourado/gold, prata…) em `elemento`, `termo_en` ou `cena` |
| V8 | Nenhuma referência a **texto na imagem** (texto, letra, número, legenda, rótulo, logo, código de barras, R$/$…), salvo `--texto` (o pedido exige texto). Negações ("sem texto", "no text") não contam |

**Avisos (não bloqueiam):** mais de 2 elementos `acento`; `pilha-4` no modo dark (não existe no
light: a derivação terá de mapear); descritores proibidos da marca na `cena` (aviso por A2);
elementos com `verificar: true` (listados com `VERIFICAR:` para o autor).

## 5. Integração com o Prompter

`portinari prompt` (já existente) passa a **checar cobertura**: se existir `enriquecimento/`, cada
`termo_en` do enriquecimento vigente precisa aparecer (sem distinção de caixa) no
`prompt_criativo.md`. Termo ausente = **erro** (exit 2) listando os termos: o Prompter os inclui ou o
agente enriquecedor ajusta o `termo_en`. É o que impede o "telefone sem fio" de perder os detalhes
justamente na tradução para o prompt.

O crítico visual (E7) recebe a lista de elementos e reprova/aciona revisão se elementos do
enriquecimento sumiram da imagem (rubrica: "fidelidade ao enriquecimento").

## 6. Testes

- Fixture boa: `tests/fixtures/enriquecimento/cafe-lca-v01.json` (11 elementos) valida sem erro.
- Recusas: 2 focos · 0 focos · cor fora dos papéis · palavra "red"/"vermelho" · "legenda"/"number" ·
  "sem texto" **não** dispara · excesso de elementos · poucos acréscimos · `id` repetido ·
  `pilha-4` no modo light (V6) e aviso no dark · JSON inválido.
- Cobertura do prompt: o prompt bom da fixture cobre todos os termos; o prompt criativo do **S1**
  (sem trabalhadores, ferramentas nem detalhes de papel) falha listando os termos ausentes.
- CLI: `enriquecer` grava `vNN.md` com o hex de cada papel de cor e lista os `VERIFICAR:`; exit 2
  em erro; `--versao` escolhe a versão (padrão: a mais recente).

## 7. Critérios de aceite

- ✔ `uv run pytest` verde.
- ✔ O exemplo café/LCA tem enriquecimento válido com trabalhadores, ferramentas, sacaria, selo,
  borda picotada, canto dobrado e trama geométrica — e o prompt criativo enriquecido correspondente
  passa na checagem de cobertura.
- ✔ O agente `enriquecedor-de-cena` existe em `.claude/agents/` e usa `portinari enriquecer` para
  se autovalidar.
- ✔ Nada do enriquecimento altera o bloco de marca (continua injetado por código).
