# Épico 11 — Estilos e formatos vindos da marca

**Status:** especificado · **Decisão de origem:** A12, A13, A14 (20/09/2026, PLANO).
**Motivo:** `brand/` ganhou em 19/09/2026 (`97cfadd`) dois documentos que o Portinari ainda não lê —
`ILUSTRACOES/FORMATOS.md` (tamanho, master, área segura e formato por uso) e `ILUSTRACOES/estilos/`
(os 14 estilos de referência traduzidos para o paper cut). Hoje o tamanho está **no código**
(`brief.PRESETS`, com o comentário "brand/ não define") e o estilo é um valor só (`papercut`).

## 1. Princípio

A marca é a fonte; o código é o leitor. Nenhum tamanho, proporção, formato de arquivo ou fragmento
de estilo fica escrito em `.py` — tudo sai de `brand/`, em runtime, e entra no `brand_snapshot.json`
com fingerprint. Continua valendo A2: **o pedido do autor vence**, a paleta é a única vinculante.

## 2. `brand.py` — o que passa a ler

`ARQUIVOS` ganha `ILUSTRACOES/FORMATOS.md` e `ILUSTRACOES/estilos/README.md` + um arquivo por
estilo (`glob` de `estilos/*.md`, ordenado; entram no fingerprint como os outros).

### Formatos

Parseia a "Tabela por uso" de `FORMATOS.md`, ficando só com as linhas que têm **Chave** (as linhas
com `—` são referência, não uso do pipeline):

```jsonc
"formatos": {
  "substack-capa": {"proporcao": "16:9", "entrega": [1456, 816], "master": [2560, 1440],
                    "formato": "jpeg|png", "peso_max_mb": 2, "fonte": "herdada", "confianca": "secundária"}
}
```

Mais as **áreas seguras** da tabela derivada (recorte central por destino) e a universal
(`2016×1340` para master 16:9), guardadas como fração do quadro — assim valem para qualquer master.
A fórmula de recorte já está escrita em `FORMATOS.md` §"Áreas seguras" e é reimplementada em ~4
linhas (`a < ratio do master → largura = H·a`, senão `altura = W/a`).

### Estilos

Por arquivo de `estilos/*.md`: `nome`, `papel` (`base`|`modo`), `restrito` (bool, de um marcador
`**Status: não usar` no corpo) e o **fragmento de prompt** (o primeiro bloco ` ```text `).
A matriz de `estilos/README.md` dá os "Fora" (recusados) com o motivo, para a pergunta ao autor.

## 3. `brief.py` — o que sai do código

- `PRESETS` perde a tupla de tamanho: vira `USO (regex) → chave de FORMATOS.md`. O tamanho, a
  proporção, o formato e o peso vêm do snapshot da marca. Se o USO casa com uma chave que
  `FORMATOS.md` não tem, é **pergunta ao autor** (não chute).
- `SIZE`/`ASPECT RATIO`/`RESOLUTION` do pedido continuam vencendo o preset, com o mesmo aviso.
- `tamanho` no `Brief` passa a ser a **entrega**; campo novo `master` (da marca, ou derivado do
  maior que o gerador aceita).
- `ESTILOS`: `STYLE` aceita **uma base + até um modo** (`"grain-textured + nostalgic"`,
  `"flat"`, vazio = `flat`, que é o padrão declarado por `estilos/README.md`).
  - estilo **recusado** pela marca (pop art, pixel art, holographic, psychedelic retro, doodle) ⇒
    pergunta ao autor com o motivo e a alternativa que a própria marca sugere;
  - `isometric` ⇒ recusa, salvo `--piloto`, porque a marca o marca como restrito até existir peça
    medida; com `--piloto` entra com aviso e o gate da peça-piloto listado na crítica;
  - duas bases ou dois modos ⇒ pergunta.

## 4. Prompt

`montar_prompt` passa a receber o fragmento do estilo e o injeta **depois** do bloco de marca,
nunca no lugar dele (ordem exigida por `estilos/README.md`): criativo → bloco de marca → fragmento
da base → fragmento do modo → técnico. O técnico passa a citar o **master**, não a entrega.

## 5. Marca desatualizada bloqueia (A13)

`portinari marca` hoje devolve exit 2 com "PERGUNTA AO AUTOR" quando `brand/` está atrás do remoto.
Passa a ser **erro** (exit 1, mensagem dizendo quantos commits e como atualizar), com
`--permitir-desatualizada` para seguir conscientemente (registrado no snapshot e no manifesto).
Alteração local não commitada continua **aviso**. O pipeline nunca faz `pull` sozinho.

## 6. Pós-processamento (A14) — só para imagem importada

> **Revisto por A16:** o pipeline não entrega mais imagem, então nada disto está no caminho
> crítico. Vale quando o autor traz a final de volta com `portinari importar`. O tamanho, o
> formato e a área segura do uso continuam saindo de `FORMATOS.md` — só que agora o destino
> principal deles é o `COMO-GERAR.md` do E12, que é o que o autor lê antes de colar o prompt.

Uma peça = **um master** + N **entregas**. Cada entrega é corte central pela fórmula de
`FORMATOS.md` + redução Lanczos + gravação no formato/peso do uso (JPEG q90–92 **4:4:4**, ou PNG
onde a marca pede), sRGB. O ponto focal do conceito tem de cair dentro da **área segura universal**;
se não cair, é erro do recorte (não se distorce, não se "quase cabe"). O frame hairline não é
desenhado pelo pipeline (`FORMATOS.md` §2: depois da redução, no layout).

## 7. Testes

- **Runtime:** copiar `brand/` para tmp, trocar `1456×816` por outro valor em `FORMATOS.md` → a
  entrega muda **sem tocar em código** (o mesmo teste que o E2 já faz com os tokens).
- Parser de formatos: linha sem chave é ignorada; tabela com coluna a menos **falha alto**;
  fingerprint muda quando `FORMATOS.md` ou qualquer `estilos/*.md` muda.
- Estilos: `flat` é o padrão; `grain-textured + nostalgic` resolve os dois fragmentos na ordem;
  `pixel art` vira pergunta citando o motivo da marca; `isometric` recusa sem `--piloto`;
  duas bases viram pergunta.
- `brief`: `substack-email` e `youtube-thumb` deixam de gerar pergunta (agora `FORMATOS.md` define);
  `substack-capa` entrega 1456×816 com master 2560×1440; `SIZE` do autor continua vencendo.
- Marca atrás do remoto: exit 1; com `--permitir-desatualizada`, exit 0 e aviso no snapshot.
- Recorte: master 2560×1440 → 1456×816, 1200×627, 1080×1350 e 1080×1920 exatos; ponto focal fora da
  área segura universal falha com mensagem acionável.

## 8. Critérios de aceite

- ✔ `uv run pytest` verde.
- ✔ `grep -rn "2560\|1456\|1080" src/` não acha tamanho de entrega nenhum (só o que vier da marca).
- ✔ `brand_snapshot.json` traz formatos, áreas seguras e fragmentos de estilo, e o fingerprint
  cobre os arquivos novos.
- ✔ Nenhum arquivo de `brand/` é alterado por este épico (a marca é lida, nunca escrita).
