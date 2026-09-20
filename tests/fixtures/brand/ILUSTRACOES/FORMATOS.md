# Formatos — tamanho e resolução por uso

Com que dimensão gerar e entregar cada peça de ilustração. Escopo: o mesmo do restante de
`ILUSTRACOES/` (README.md) — **nunca app, nunca site**. Regras de cor/construção não moram aqui:
`_bloco-marca.md`. Verificado em **19/09/2026**.

## Como ler

- **Master** = o que se gera (o maior que o gerador permitir; ampliar além do nativo é
  ampliação — registre o fator, e acima de ×2 peça olho humano na borda do recorte e no grão).
- **Entrega** = o que se sobe na plataforma. Sempre **derivada** do master por corte central +
  redução, nunca gerada de novo por plataforma.
- **Chave** = o nome do uso no pedido do `portinari` (`brief.py`, `PRESETS`).
- **Confiança:** `oficial` (página da plataforma lida) · `oficial*` (trecho oficial visto só na
  busca; a página bloqueou fetch) · `secundária` (blogs/agregadores — reverificar na primeira
  publicação no canal) · `herdada` (outro documento deste repositório) · `derivada` (aritmética).

## Tabela por uso

| Chave               | Uso                                    | Proporção                                           | Entrega                                         | Master                                                 | Formato / peso                                                     | Fonte                                                                                                                                         |
| ------------------- | -------------------------------------- | --------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `substack-capa`     | Capa de post (também preview social)   | 16:9                                                | **1456×816**                                    | 2560×1440                                              | JPEG ou PNG, ≤2 MB (sem limite oficial achado)                     | `herdada` (hemingway, 09/2026 — `[VERIFICAR]` no editor); preview recorta 14:10 e 1,91:1, mín. 1200×630, recomendado ≥1456×1048: `secundária` |
| `substack-email`    | Cabeçalho de e-mail                    | 5:1                                                 | **1100×220**                                    | 2200×440 (gerar em 5:1; não cortar de 16:9)            | PNG                                                                | `secundária` (blogs citando o artigo do Substack; "pode ser mais alto")                                                                       |
| —                   | Retrato de dado dentro do post         | ≤1:1 (mais alto que isso o Substack corta para 1:1) | largura 1456                                    | 2560 de largura                                        | JPEG ≤2 MB                                                         | `secundária`                                                                                                                                  |
| `linkedin-destaque` | Imagem de link/artigo compartilhado    | 1,91:1                                              | **1200×627**                                    | 2560×1340 (corte de 2560×1440)                         | JPEG (LinkedIn recomenda JPEG a PNG), **≤3 MB**                    | LinkedIn `oficial`                                                                                                                            |
| —                   | Imagem de post no feed                 | 4:5                                                 | **1080×1350**                                   | 2160×2700                                              | JPEG ≤3 MB                                                         | `secundária`                                                                                                                                  |
| —                   | Capa de artigo                         | 16:9                                                | 1920×1080                                       | 2560×1440                                              | JPEG ≤3 MB                                                         | `secundária`; aplique a área segura universal (abaixo)                                                                                        |
| `instagram-post`    | Post de feed                           | 4:5                                                 | **1080×1350** (1:1 = 1080×1080, ver D2 da spec) | 2160×2880 em 3:4, derivar 4:5 cortando 6,25% da altura | JPEG. **Largura exata 1080**: acima disso a plataforma reduz       | proporção 1,91:1–4:5 e largura 320–1080: `oficial*`; 3:4 aceito desde 11/11/2025: `secundária`                                                |
| `instagram-story`   | Story · capa de Reels                  | 9:16                                                | **1080×1920**                                   | 2160×3840                                              | JPEG/PNG                                                           | tamanho `secundária`; zonas em "Áreas seguras"                                                                                                |
| `youtube-thumb`     | Thumbnail                              | 16:9                                                | **1920×1080** (mín. 1280×720; largura mín. 640) | 2560×1440                                              | JPG/PNG, **≤2 MB** (limite do upload no celular; 50 MB no desktop) | YouTube `oficial` (recomenda até 3840×2160 — ampliar não ganha detalhe)                                                                       |
| —                   | Thumbnail de Short                     | 9:16                                                | 1080×1920                                       | 2160×3840                                              | JPG/PNG ≤2 MB                                                      | YouTube `oficial` (2160×3840 recomendado; a plataforma pode trocar por um 4:5 automático em algumas páginas)                                  |
| —                   | Facebook: post/link (**pendente**, D4) | 1,91:1                                              | 1200×630 (mín. 600×315)                         | 2560×1340                                              | JPEG ≤8 MB                                                         | `secundária`                                                                                                                                  |

Facebook e X estão fora da matriz de `APLICACAO.md` §0 (lá só existe camada de sistema). Até o
founder decidir se a camada de ilustração vale nesses canais, a linha acima é medida de
referência, não autorização.

## Áreas seguras — derivadas do master 16:9

O recorte central de um master `W×H` para uma proporção `a = largura/altura`: se `a` < 16:9,
mantém a altura inteira e a largura vira `H·a`; se `a` > 16:9, mantém a largura e a altura vira
`W/a`. Para o master de **2560×1440**:

| Destino                               | Recorte central                 | Deslocamento |
| ------------------------------------- | ------------------------------- | ------------ |
| 16:9                                  | 2560×1440                       | —            |
| 14:10 (preview do Substack)           | 2016×1440                       | x 272        |
| 1,91:1 (LinkedIn, Facebook, OG)       | 2560×1340                       | y 50         |
| 1:1                                   | 1440×1440                       | x 560        |
| 4:5                                   | 1152×1440                       | x 704        |
| 3:4                                   | 1080×1440                       | x 740        |
| **Universal** (16:9 ∩ 14:10 ∩ 1,91:1) | **2016×1340** (78,75% × 93,06%) | x 272 · y 50 |

**Regra:** ponto focal e qualquer região que o texto de Canva vá cobrir ficam dentro da
universal. O fundo (≥40% do quadro, `_bloco-marca.md`) é o que sangra para as bordas.

**Instagram, peça 1080×1350** — a grade de perfil mostra um recorte 3:4: mantenha o essencial em
`x 34–1046` (1012 de largura). A margem de segurança de 72px de `INSTAGRAM.md` §2 já cumpre isso.

**Story e capa de Reels (1080×1920):**

| Zona                                                    | Faixa                   | Fonte                          |
| ------------------------------------------------------- | ----------------------- | ------------------------------ |
| Conteúdo de leitura durante o play                      | x 72–840 · y 220–1650   | `herdada` (`INSTAGRAM.md` §12) |
| Feed (recorte 4:5)                                      | y 285–1635              | `derivada`                     |
| Grade de perfil (recorte 3:4 → 1:1, as fontes divergem) | y 240–1680 → y 420–1500 | `derivada`                     |
| **Gancho/título — cabe em todas**                       | **y 420–1500**          | `derivada` (D3 da spec)        |

**YouTube thumbnail:** o contador de duração cobre o canto inferior direito — nada essencial ali.

## Regras de resolução e exportação

1. **Um master por peça**, arquivado em PNG sRGB 8 bits. Entregas são derivações.
2. **Frame depois do redimensionamento.** O hairline de 1px (`DESIGN.md` §5) é desenhado no
   tamanho final de entrega. Se for reduzido junto (2560→1456 = ×0,57) vira 0,57px borrado.
3. **JPEG de entrega:** qualidade 90–92, **croma 4:4:4** (sem subamostragem). Com 4:2:0 as bordas
   retas do corte e o acento Lime (≤1% do quadro) ganham franja. Qualidade abaixo de ~85 achata o
   grão — que já sobrevive só 47–59% da amplitude nas plataformas (`DESIGN.md` §11, item 4): mire
   a metade superior da faixa aceitável de grão.
4. **PNG** só onde a plataforma o pede (cabeçalho de e-mail) ou o arquivo cabe no limite; o
   LinkedIn recomenda JPEG de alta qualidade em vez de PNG.
5. **sRGB.** Não exporte em Display P3 — o hex dos tokens é sRGB. Confira um token no arquivo
   exportado com conta-gotas.
6. **Sem texto na imagem gerada.** Título/eyebrow entram por cima, no tamanho de entrega
   (`INSTAGRAM.md` §1), dentro da área segura.
7. **Abaixo de 96px não existe ilustração** (`DESIGN.md` §7.4). Capa de destaque de story do
   Instagram aparece pequena no perfil (ordem de 70px — estimativa, `secundária`; confira no
   app): use o símbolo (`brand/LOGO/`). Thumbnail de YouTube na
   barra lateral fica acima do limiar, mas mantenha o teto de três camadas.
8. **Nome de arquivo:** `<conceito>-<variante>-<L>x<A>.<ext>` (extensão de `_como-gerar.md` passo
   7 com o tamanho no sufixo, porque uma peça tem várias entregas).

## Fora deste arquivo

Avatar, banners e capas de perfil são camada de sistema e já estão em `../SOCIAL/README.md`.
Uma divergência a saber: a capa de página do LinkedIn tem `oficial` **1512×256**; o
`linkedin-cover.png` de `SOCIAL/` é 1128×191 (mesma proporção, resolução menor). Banner do
YouTube: `oficial` ≥2560×1440, ≤6 MB.
