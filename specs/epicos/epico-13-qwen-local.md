# Épico 13 — Validação local com Qwen-Image 2.1

**Status:** especificado (22/09/2026) · **Fase A primeiro; a Fase B só existe se a Fase A passar.**
**Não reabre** A16/A17: o entregável continua sendo o prompt, e a final continua sendo gerada à mão
no Nano Banana Pro. O que se testa aqui é **só o gerador de validação**.

## 1. A pergunta

Um modelo aberto, rodando nesta máquina, sem quota nem LLM no meio, consegue **substituir ou
complementar o `agy` como prova de que o prompt funciona**?

"Funciona" tem o sentido que o piloto `cafe-lca` já mediu. O mesmo prompt deu, no `agy`, gen_01
REVISAR e gen_02 APROVADO: o prompt **é** aprovável, e o gerador acerta em parte das amostras. O Qwen
serve se, com o mesmo prompt, chegar a uma imagem que o crítico visual e `portinari checar` aprovam
**pelas mesmas razões** (paleta, uma ideia, enriquecimento), e se as que ele reprovar falharem por
defeito de amostra, não porque o modelo ignora a marca. Qualidade da imagem, sozinha, não interessa.

Por que valeria a pena: o prompt chega **literal** (acaba o R1 no caminho local, `fiel=True` por
construção), não há teto de quota, e não há rede.

## 2. O modelo e a máquina (levantado em 22/09/2026)

| Item | Valor | Fonte |
| --- | --- | --- |
| Modelo | `Qwen/Qwen-Image-2.1`, DiT *single-stream* de 7B, codificador de texto Qwen3-VL-8B | [cartão no HF](https://huggingface.co/Qwen/Qwen-Image-2.1) · [blog](https://qwen.ai/blog?id=qwen-image-2.1) |
| Licença | **Qwen Research License**: ler antes da Fase A (§7, R18) | cartão no HF |
| Resolução nativa | até 2752×1536 em 16:9 (7 proporções), lados múltiplos de 32 | cartão no HF |
| Parâmetros sugeridos | Euler, 20–40 passos, CFG 6,0 | [unsloth GGUF](https://huggingface.co/unsloth/Qwen-Image-2.1-GGUF) |
| Denoiser GGUF | Q3_K_M ≈ 3,2 GB · **Q4_K_M ≈ 4,2 GB** · Q5_K_M ≈ 5,4 GB · Q8_0 ≈ 7,6 GB | unsloth / [leejet](https://huggingface.co/leejet/Qwen-Image-2.1-GGUF) |
| Texto | `Qwen3-VL-8B-Instruct` Q4_K_M/Q4_K_XL (GGUF) | [doc do sd.cpp](https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/qwen_image_2.1.md) |
| VAE | `qwen_image_2.1_vae_bf16.safetensors` (esse, não outro) | doc do sd.cpp |
| **Esta máquina** | RTX 3050 Laptop **6 GB**, **14 GB de RAM** (≈ 5 GB livres com a sessão aberta), sem `nvcc`, 278 GB de disco | `nvidia-smi`, `free`, `df` |

**Executor escolhido: `stable-diffusion.cpp` (`sd-cli`).** É um binário só, tem suporte oficial ao
2.1, lê GGUF e tem `--offload-to-cpu`. ComfyUI e diffusers (`QwenImage21Pipeline`) trazem PyTorch
com CUDA (vários GB) e um servidor para manter de pé, e nenhum dos dois cabe melhor em 6 GB. Ficam
de fora até o `sd-cli` falhar por um motivo que um deles resolveria.

A conta de memória está no limite: denoiser Q4_K_M (4,2 GB) na VRAM e o codificador de texto
(≈ 5 GB) na RAM, com 5 GB livres. **Q3_K_M é o plano B**, e fechar o navegador antes de gerar faz
parte do procedimento.

## 3. Fase A: teste sem código novo

O pipeline já sabe trazer imagem de fora: `portinari importar` (E5b). A Fase A usa isso e **não
escreve uma linha em `src/`**.

### A.1 Instalação (fora do repo)

- `sd-cli` com CUDA: *release* pré-compilada do `leejet/stable-diffusion.cpp` para Linux+CUDA; se
  não houver, compila com `-DSD_CUDA=ON`, o que exige instalar o CUDA Toolkit (que falta aqui).
  Anota a versão/commit.
- Pesos em `~/modelos/qwen-image-2.1/` (**nunca** dentro do pipeline: são GB e não entram no git):
  o denoiser Q4_K_M (e o Q3_K_M como reserva), o Qwen3-VL-8B Q4 e o VAE bf16.
- Nada de `pip install` no `pyproject.toml`: a Fase A não mexe nas dependências do pipeline.

### A.2 Fumaça

Uma imagem de 1024×576 com prompt curto, para provar que o binário, os pesos e a memória funcionam.
Anota o pico de VRAM (`nvidia-smi --query-gpu=memory.used --format=csv -lms 500`), o pico de RAM e
o tempo. Se estourar memória: Q3_K_M e, depois disso, a resolução. Se nem 1024×576 em Q3 couber,
**para aqui** e registra o motivo (resultado válido: "não roda nesta máquina").

### A.3 O teste de verdade: o piloto `cafe-lca`

Entrada: `output/2026-09-20_transformacao-da-producao-agricola-em-produto-financeiro/iteracoes/01/prompt_final.md`,
o mesmo prompt que gerou gen_01 (REVISAR) e gen_02 (APROVADO) no `agy`, a 1376×768.

```bash
sd-cli --diffusion-model ~/modelos/qwen-image-2.1/<denoiser>.gguf \
       --vae ~/modelos/qwen-image-2.1/qwen_image_2.1_vae_bf16.safetensors \
       --llm ~/modelos/qwen-image-2.1/<Qwen3-VL-8B-Q4>.gguf \
       -p "$(cat <execução>/iteracoes/01/prompt_final.md)" \
       -W <L> -H <A> --steps 30 --cfg-scale 6.0 --sampling-method euler \
       --seed <S> --offload-to-cpu -v -o <scratch>/qwen_<S>.png
```

Regras do teste:

1. **Prompt literal, sem prompt negativo.** O Nano Banana Pro não recebe negativo, então validar com
   negativo prova algo que o prompt entregue não faz. Pelo mesmo motivo, nenhum ajuste no texto
   para "ajudar o Qwen".
2. **Resolução:** 16:9, o maior múltiplo de 32 que couber na memória, começando em 1376×768 (o
   mesmo do `agy`, para comparar lado a lado) e subindo até 2752×1536 se couber (A1). Registra o
   maior que coube.
3. **Três sementes** fixas e anotadas (o `agy` não deixa escolher semente; aqui dá, e isso entra no
   relatório).
4. **Truncamento (R19):** o `prompt_final.md` tem ~1.100 palavras e o bloco de marca, com os hex,
   fica **no fim**. Com `-v`, conferir quantos tokens o `sd-cli` aceitou e se cortou. Se cortar
   antes dos hex, o resultado é **reprovado por construção** (o Qwen não viu a paleta), e isso vira
   o achado principal.
5. Importa como execução de teste, **numa cópia**, para não sujar a execução arquivada:

   ```bash
   cp -r output/2026-09-20_<slug> <scratch>/qwen-cafe-lca
   uv run portinari importar <scratch>/qwen-cafe-lca <scratch>/qwen_*.png \
       --iteracao 1 --modelo qwen-image-2.1-<quant> --max-geracoes 20
   uv run portinari checar <scratch>/qwen-cafe-lca --iteracao 1 --gen gen_03 --modo dark   # e gen_04, gen_05
   ```

   (Se `importar` recusar por causa do teto, `--max-geracoes` está ali para isso. O teto de 12 é da
   execução real, e esta é uma cópia.)
6. O **crítico visual** julga as três imagens do Qwen do jeito de sempre: imagem, `checagens.json`,
   rubrica e enriquecimento, **sem prompt** (D7) e **sem saber qual gerador** fez a imagem.

### A.4 Relatório: `docs/qwen-local.md`

No formato do `docs/agy.md`: o que foi instalado (versões e hashes dos pesos), a tabela de medidas e
o veredito.

| Medida | agy (gen_02) | Qwen s1 | Qwen s2 | Qwen s3 |
| --- | --- | --- | --- | --- |
| quant · resolução nativa | flash · 1376×768 | | | |
| tempo por imagem · pico VRAM · pico RAM | 26 s · — · — | | | |
| tokens aceitos / cortou antes dos hex? | n/a (R1) | | | |
| `checar`: erros · avisos · maior ΔE · nº de cores | 0 · 0 · 6,6 · 7 | | | |
| texto/número/logo na imagem? (R8, R20) | não | | | |
| veredito do crítico · média | APROVADO · 4,33 | | | |

### A.5 Critério de passagem (o autor decide, com `AskUserQuestion`)

A Fase A **passa** se as três condições valerem:

- ✔ roda nesta máquina em ≥ 1376×768 e ≤ 5 min por imagem;
- ✔ o bloco de marca chega inteiro ao codificador (sem truncar os hex);
- ✔ pelo menos 1 das 3 sementes é APROVADA pelo crítico, sem erro em `checar` (o `agy` teve 1 de
  2), e nenhuma das 3 tem cor fora da paleta nem texto na imagem, porque isso seria o modelo
  ignorando o prompt, não defeito de amostra.

Três resultados possíveis, todos válidos: **não roda** (fecha o épico, relatório registra), **roda
mas discorda do `agy`** (fecha o épico: não serve para validar prompt de Nano Banana), **passa**
(o autor decide se abre a Fase B). Em nenhum caso o pipeline troca de gerador sozinho.

## 4. Fase B: `gerar --via qwen` (só se a Fase A passar e o autor pedir)

O mínimo para não precisar copiar e colar comando:

```
portinari gerar <saida> --iteracao N --via qwen [--seed S] [--variacoes N] [--proporcao P]
```

- `--via` padrão continua `agy`; `qwen` é opção explícita. (O `--via gemini` do E10 continua
  adiado; os dois cabem no mesmo `--via`.)
- `agy.py` ganha **uma função** `gerar_local(...)` (ou `qwen.py`, se passar de ~60 linhas) que
  chama o `sd-cli` por `subprocess` e **reaproveita** `Geracao`, `_registrar`, `_contar`,
  `melhor_proporcao`, `geracoes.jsonl`, o teto de gerações e o layout `gen_KK.*`. Nada duplicado.
- Onde estão binário e pesos: variáveis de ambiente `PORTINARI_SDCPP` e `PORTINARI_QWEN_DIR`, no
  mesmo padrão do `PORTINARI_AGY_HOME`. Sem caminho da máquina no código.
- Dimensão: proporção do brief (`melhor_proporcao`) × o maior lado que a Fase A mediu como cabível,
  arredondado para múltiplo de 32. O teto vem de `--max-lado` (hardware, não marca), com o padrão
  medido na Fase A. Nenhum tamanho da **marca** entra em `.py` (regra 3).
- `Geracao`: `origem="qwen"`, `modelo_imagem=<nome do arquivo do denoiser>`, `fiel=True`,
  `efetivo.md` = o prompt enviado. Campo novo: `seed`. `comando` grava o `sd-cli` exato (sem
  segredo: aqui não há chave).
- Erros: `sd-cli` ausente ou pesos ausentes → exit 2 com o comando de instalação; falta de memória
  (CUDA OOM no stderr) → exit 3 com "tente o quant menor ou `--max-lado` menor", **sem descer
  sozinho** de quant (é decisão de qualidade); truncamento detectado no `-v` → exit 4, mesmo
  significado de hoje ("os hex não chegaram ao gerador").

### Testes da Fase B

`sd-cli` falso (script em `tests/`, como o `agy` falso do E3), **nenhum teste roda o modelo**:
sucesso grava `gen_KK.png` com dimensões, semente e `origem`; OOM → exit 3 sem retentar; binário
ausente → exit 2; saída com aviso de truncamento → exit 4; teto de gerações compartilhado com `agy`
e `importar`; `--via agy` idêntico ao de hoje.

### Aceite da Fase B

- ✔ `uv run pytest` verde, sem GPU.
- ✔ uma execução real, `gerar --via qwen` no piloto, reproduz a tabela da Fase A.
- ✔ `SKILL.md` diz quando usar `--via qwen` (decisão do autor na Fase A, não minha).

## 5. Fora do escopo

- Gerar a **final** no Qwen. A16 vale: a final é do autor, no Nano Banana Pro.
- Edição por referência (`-r`, derivação light/dark do E8). Fica para depois, se a Fase B entrar e
  a edição do `agy` virar gargalo.
- LoRA, ajuste fino, ComfyUI, diffusers, servidor HTTP.

## 6. Git

`epico/13-qwen-local`. A Fase A commita só `docs/qwen-local.md` e a atualização do PLANO. **Nenhuma
imagem e nenhum peso entram no git**; a cópia da execução fica no *scratch*. A Fase B é outra branch,
`epico/13b-via-qwen`, se chegar a existir.

## 7. Riscos novos

| # | Risco | Sev. | Mitigação |
| --- | --- | --- | --- |
| **R18** | A Qwen Research License pode restringir uso comercial, e a Syntaxis é uma marca | média | Ler a licença **antes** de baixar. A imagem de validação não é entregue (A16), o que provavelmente basta, mas quem decide é o autor, e a decisão fica no relatório |
| **R19** | O codificador trunca o prompt de ~1.100 palavras e corta o bloco de marca (hex no fim) | **alta** | Medir com `-v` na Fase A; truncou = reprovado. Se truncar, registrar o limite; reordenar o prompt é outra discussão, porque mudaria o entregável |
| **R20** | O 2.1 é forte em tipografia e tende a **escrever** (placas, rótulos): conflita com a regra 8 | média | Rubrica e crítico já barram (R8); o relatório conta a taxa de texto por semente |
| **R21** | 6 GB de VRAM e 5 GB de RAM livres: OOM, *swap* ou minutos por imagem | média | Q3_K_M como reserva, resolução medida, navegador fechado; "não roda aqui" é um resultado aceitável |
| **R22** | O Qwen concorda com o crítico por acaso em 3 sementes (amostra pequena) | baixa | A Fase A decide só se vale abrir a B; a B mede de novo na próxima execução real antes de virar recomendação na skill |
