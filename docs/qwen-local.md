# Qwen-Image 2.1 local — o que foi testado e o veredito

Fase A do épico 13 (`specs/epicos/epico-13-qwen-local.md`), executada em 23/09/2026 nesta máquina
(RTX 3050 Laptop 6 GB, 14 GB RAM). **Veredito: roda, mas discorda do `agy` — não serve para validar
prompt de Nano Banana Pro.** Fase B não abre.

## 1. Instalação (A.1)

| Item | Valor |
| --- | --- |
| Executor | `stable-diffusion.cpp`, `sd-cli`, "version unknown, commit `28b454b`" |
| Backend | **Vulkan** (`libggml-vulkan.so`), não CUDA — a release baixada não tem CUDA compilado. Desvio da spec (que previa CUDA ou compilar com `-DSD_CUDA=ON`); não bloqueou o teste, registrado aqui |
| Denoiser | `qwen-image-2.1-Q4_K_M.gguf` (4,2 GB) — `sha256: 631d532e7ca71e8d90a87c71d3699761a812039d22e3370e87498d87754660fe` |
| Texto | `Qwen3-VL-8B-Instruct-Q4_K_M.gguf` (5,0 GB) — `sha256: 108e7ff92b78eefd3db4741885104acba514255c11b617d3c7b197a5f46efe89` |
| VAE | `qwen_image_2.1_vae_bf16.safetensors` (0,68 GB) — `sha256: 71879ffd5321e6d10c3c87513e2b474b1252efa7f3dec2969214a9bf06a6dd5c` |
| Q3_K_M (reserva) | não baixado — não foi necessário, Q4_K_M coube |
| Local dos pesos | `~/modelos/qwen-image-2.1/` e `~/modelos/sdcpp/`, fora do repo, nunca entraram no git |

**R18 (licença):** Qwen Research License Agreement — uso **não-comercial apenas**; comercial exige
licença separada. Decisão do autor (registrada em conversa, 23/09/2026): prosseguir, porque a imagem
de validação nunca é entregue nem publicada (A16) — uso interno de teste de prompt, não produto.

## 2. Fumaça — A.2

Prompt curto, 1024×576, 20 passos, `--offload-to-cpu`.

| Medida | Valor |
| --- | --- |
| Tempo total | 6m19s (378,14s no binário + carregamento) |
| Pico VRAM | 4914 MiB / 6144 MiB |
| Pico RAM | 13.582 MB / ~14.336 MB (máquina quase no limite) |
| Ocorrência | decodificação VAE quase estourou VRAM (`cannot make enough memory available`), caiu
  automaticamente para *tiling* espacial (3×3 blocos) e completou sem erro |

Já neste teste pequeno o tempo (6m19s) supera o teto de 5 min/imagem do critério de passagem — o
prenúncio se confirmou no teste real (§3).

## 3. O teste de verdade — A.3, piloto `cafe-lca`

Prompt: `output/2026-09-20_transformacao-da-producao-agricola-em-produto-financeiro/iteracoes/01/prompt_final.md`
(1.099 palavras), **literal, sem negativo**, o mesmo que deu gen_01 REVISAR / gen_02 APROVADO no
`agy`. Três sementes fixas, 1376×768 (resolução do `agy`), 30 passos, cfg 6,0, euler, Q4_K_M.

| Medida | agy (gen_02) | Qwen s1 (seed 1001) | Qwen s2 (seed 1002) | Qwen s3 (seed 1003) |
| --- | --- | --- | --- | --- |
| resolução | 1376×768 | 1376×768 | 1376×768 | 1376×768 |
| tempo por imagem | 26 s | 1501,7 s (25m02s) | 1502,2 s (25m02s) | 1507,7 s (25m08s) |
| pico VRAM | — | 5271 MiB | 5271 MiB | 5271 MiB |
| tokens cortou antes dos hex? | n/a (R1) | **não** | **não** | **não** |
| `checar`: erros · avisos · maior ΔE · nº cores ≥1% | 0 · 0 · 6,6 · 7 | 8 · 7 · 46,4 · 8 | 13 · 9 · 46,9 · 13 | 12 · 10 · 45,0 · 12 |
| fundo dominante | dentro da paleta | `#FEFCFA` 75,3% | `#FEFCFA` 77,6% | `#FDFBF9` 74,6% |
| texto/número/logo na imagem? | não | não | não | não |
| veredito do crítico · média | APROVADO · 4,33 | REVISAR · 1,33 | REVISAR · 1,50 | REVISAR · 1,33 |

**Pico RAM** não foi monitorado separadamente nesta rodada (o smoke test com os mesmos pesos mediu
13,6 GB — ordem de grandeza esperada aqui também, mas não é medida direta).

### O que aconteceu, além dos números

- **R19 (truncamento) não se confirmou.** O `-v` mostra o tokenizer processando o prompt inteiro,
  incluindo os sete hex do bloco de marca e a seção `## Technical` no fim — nada foi cortado.
- **O modelo ignorou a paleta por completo, nas três sementes.** Nenhuma cor da pilha dark
  (`#141414`…`#CDF163`) aparece; em vez disso, saiu uma composição em tons bege/marrom/branco
  realistas — o Qwen priorizou a semântica "saco de juta e grãos de café" sobre a instrução de cor
  explícita, mesmo com os hex intactos no contexto. ΔE mínimo registrado entre uma cor da imagem e a
  cor mais próxima da paleta foi 32,1 (ainda assim bem acima de qualquer tolerância aceitável).
- **As três imagens leem como díptico**, não como a transformação de material pedida: saca à
  esquerda, pilha de papéis à direita, vão vazio no meio — o foco do enriquecimento (`e1`, a costura
  que vira folha lisa) não aparece em nenhuma das três. Os três críticos, trabalhando às cegas e sem
  ver uns aos outros, marcaram o mesmo bloqueante (B6/B7) de forma independente.
- **Estilo é fotorrealista**, não papel recortado chapado: textura de tecido, sombra contínua,
  reflexo especular em metal — o oposto do `flat cut-paper` pedido.
- **Artefato de tiling:** as três imagens têm a mesma listra vertical fina verde/magenta perto do
  centro do quadro, no mesmo x — consequência visível do *fallback* de tiling do VAE por falta de
  VRAM (§2), não um elemento do prompt. Não teve papel na reprovação (a paleta já reprova sozinha),
  mas é um defeito a mais do caminho Q4_K_M nesta GPU.
- **Nenhuma das três** tem texto, número ou logo (R8/R20 não se confirmaram).

## 4. Critério de passagem (A.5) — não passou

| Condição | Resultado |
| --- | --- |
| Roda em ≥1376×768 e ≤5 min/imagem | Roda em 1376×768 ✔ · **25 min/imagem, 5× o teto** ✘ |
| Bloco de marca chega inteiro (sem truncar os hex) | ✔ |
| ≥1 de 3 sementes APROVADA sem erro em `checar`, nenhuma com cor fora da paleta | **0 de 3** ✘ — as três têm erro de paleta |

Dois dos três critérios falham, e o terceiro (cor fora da paleta em 100% das amostras) é o que a
spec já apontava como decisivo: "isso seria o modelo ignorando o prompt, não defeito de amostra."

**Veredito, entre os três resultados válidos da spec: roda, mas discorda do `agy` — fecha o épico.**
Não serve para validar prompt de Nano Banana Pro nesta configuração (Q4_K_M, `sd-cli`/Vulkan, prompt
literal sem ajuste). Fase B (`gerar --via qwen`) não abre.

## 5. Se algo mudar no futuro

Não investigado aqui, porque estava fora do escopo da Fase A (nenhum ajuste no texto "para ajudar o
Qwen" — regra do teste), mas evidenciado pelos achados acima como possíveis próximos passos **caso
alguém queira reabrir o épico**:
- Um prompt reescrito para nomear a paleta como propriedade das folhas (não como instrução separada
  no fim) poderia mudar o resultado — mas isso muda o entregável (R19 já previa essa discussão).
- Quant maior (Q5_K_M/Q8_0) ou compilar `sd-cli` com CUDA poderia reduzir o tempo por imagem, mas não
  ataca a causa da reprovação (paleta), que não é de memória nem de performance.
