# Isometric — modo, **restrito**

**Origem (Kasra):** aparência tridimensional por um ângulo de câmera específico, mostrando
profundidade em vários eixos. Vídeos explicativos, guias, ilustração técnica.

> **Status: não usar em peça real até existir uma peça-piloto medida.** Este arquivo é a hipótese
> de tradução, ainda não validada com imagem.

## O conflito

- Isométrico verdadeiro usa arestas a **30°**. A regra de corte da marca é **0°, 90° ou ±45°**
  (`DESIGN.md` §5 e §7.3).
- Profundidade por **sombra** é proibida; `3D` e `bevel` são descritores proibidos (§7.5).
- Pedir "isometric" a um gerador devolve 30° e face sombreada — as duas coisas erradas.

## Tradução proposta

- **Projeção oblíqua a 45°:** frentes alinhadas aos eixos, arestas de fuga a exatamente 45°.
- **Faces por degrau de tom**, não por sombra: topo, frente e lateral são três degraus adjacentes
  da mesma pilha (`illustration.stack.*`) — a escada de `../_bloco-marca.md` faz o papel da luz.
- **Sem perspectiva, sem gradiente, sem 3D.** Cada face é uma cor uniforme.

## Onde usar (depois de validado)

Estrutura e arquitetura: camadas de um sistema, pilha de produtos, fluxo com profundidade. É a
única forma de sugerir volume dentro da regra "sombra proibida".

## Fragmento de prompt (a testar)

```text
Oblique projection: front faces aligned to the horizontal and vertical axes, receding edges at
exactly 45 degrees. Every face is a flat uniform tone, each face one step lighter or darker than
its neighbor from the stated palette. No perspective convergence.
```

Evite a palavra "isometric" no prompt — o gerador a resolve para 30°.

## Gate proposto para a peça-piloto

Uma peça só sai do status "restrito" se, medida: (1) as arestas de fuga ficam a 45° ±2°
(tolerância proposta aqui, não vem do `DESIGN.md`); (2)
nenhuma face tem rampa de luminância; (3) 3–7 cores. Se o gerador ativo não consegue 45°, o modo
continua fora — registre em `../README.md`, não force.
