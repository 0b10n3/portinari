# Risograph — base

**Origem (Kasra):** imita a impressão risográfica — camadas de cor limitadas, textura granulada,
desalinhamento intencional, sensação analógica.

## O que a marca mantém e o que muda

- **Já existe na marca:** offset de registro de **2–4px, em cor chapada, sem gradiente**
  (`DESIGN.md` §7.2, regra 6). "Camadas de cor limitadas" é a regra de uma pilha por peça
  (`illustration.maxHues`). O grão é o de `grain-textured.md`.
- **Medido no tamanho de entrega** (`../FORMATOS.md`) — interpretação; o `DESIGN.md` não diz em que
  escala os 2–4px valem. Uma peça reduzida a metade perde metade do offset.
- **Muda — e é o ponto de atenção:** a risografia real **mistura tinta por sobreposição
  translúcida**, o que cria cores novas fora da paleta. Isso viola a regra vinculante (paleta).
  Aqui o offset é o **deslocamento de uma folha da mesma cor**, com aresta seca, e onde duas
  folhas se cruzam a de cima cobre a de baixo. Sem transparência, sem mistura.

## Onde usar

Capa editorial e retrato de dado, quando o argumento é ajuste, margem de erro ou "quase
alinhado". **Não** em thumbnail: 2–4px desaparece na redução.

## Fragmento de prompt

```text
Slight print-registration offset of 2 to 4 pixels on one flat sheet: the same solid color,
shifted, with a hard edge. Where sheets overlap, the top sheet fully covers the one below. Every
color is opaque and comes only from the stated palette.
```

## Checagem

- O offset existe em uma folha só e mede 2–4px na entrega.
- Nenhuma cor de mistura aparece na sobreposição (conferir por quantização: cores ≥1% dentro da
  paleta).
