---
name: gerar-cards-enriquecidos-for-batch
description: Gera um cartão enriquecido e didático para flashcard SRS a partir de UMA FOTO anexada — otimizado para Batch API
---

# Skill: Gerar Cards Enriquecidos (Batch API)

Versão otimizada para **Batch API do Claude**: processa **UMA IMAGEM POR REQUEST**.

---

## 🎯 Contexto & Restrições (Batch API vs Local CLI)

A Batch API tem diferenças fundamentais do contexto local. Esta skill foi adaptada para:

| Aspecto | Local CLI | Batch API |
|---------|-----------|-----------|
| **Diretório** | Compartilhado (múltiplas fotos) | Isolado (uma imagem por request) |
| **Input** | Encontra fotos via `find` | Recebe imagem anexada no message |
| **Read tool** | Disponível (`/Users/.../foto.png`) | Não existe — image já em message |
| **Templates** | Path absoluto `/Users/.../templates/` | Path relativo `./templates/` |
| **Output** | Múltiplos files (001, 002, 003...) | Um card por request |
| **Scale** | Sequential (Fase 1→2→3) | Massively parallel via Batch API |

---

## 📋 Fluxo de Execução

### Passo 1: Receber Imagem (Batch Request)

A imagem já vem anexada no request como **image block** (não precisa Read tool).

**Exemplo de input:**
```
User message: "Gerar card 001 para esta pergunta de certificação"
[Anexa: pergunta.png]

Opcional:
- Número do card: 001
- Título customizado: "Developer Productivity"
```

### Passo 2: Extrair Conteúdo da Imagem

Analise a imagem e extraia:
- **Pergunta/Cenário**: Texto completo (em inglês)
- **Opções**: As 4 alternativas rotuladas A, B, C, D

Exemplo de extração:
```
Pergunta: "You are building developer productivity tools using the Claude Agent SDK..."
A - Instruct Claude to read every repository file first...
B - Proceed with direct execution, relying on test failures...
C - Start separate direct-execution sessions...
D - Use plan mode to map relevant flows...
```

### Passo 3: Analisar & Determinar Resposta Correta

Com base no conhecimento técnico/arquitetural, determine qual é a resposta correta.

**Validação:** Se possível, valide a resposta internamente (double-check).

### Passo 4: Gerar Card Enriquecido

Gere o card seguindo **EXATAMENTE** o template estrutural (`./templates/001-enriched-card.md`).

**Estrutura obrigatória:**

```markdown
Scenario: [Pergunta completa em inglês - TUDO NA MESMA LINHA]

---

[ ] A - [Opção A]
[ ] B - [Opção B]
[ ] C - [Opção C]
[ ] D - [Opção D]

---

### TRANSLATED QUESTION

[Pergunta traduzida em português - fiel, não literal]
Alternativas traduzidas:

A) [Opção A traduzida]
B) [Opção B traduzida]
C) [Opção C traduzida]
D) [Opção D traduzida]

---

### EXPLANATION (TECH LEAD)

Explicação:
[Introdução ao conceito testado - qual padrão/decisão arquitetural a pergunta testa - 2-3 linhas]

Por que a alternativa [X] é a correta:
[Análise técnica profunda de por que essa é a melhor solução - 5-7 linhas]

Por que as outras estão erradas:

A) [Análise específica de por que A está errada - 2-3 linhas]
B) [Análise específica de por que B está errada - 2-3 linhas]
C) [Análise específica de por que C está errada - 2-3 linhas]
D) [Análise específica de por que D está errada - 2-3 linhas]

Dica importante:
[Padrão recorrente ou conceito-chave a lembrar - 2-3 linhas]

---

### 🚸 CHILDREN EXPLANATION

Explicação:
[Introdução ao conceito testado em linguagem acessível e lúdica - 2-3 linhas. Use analogias e narrativa se apropriado]

Por que a alternativa [X] é a correta:
[Análise simples de por que funciona - 3-4 linhas, mas tecnicamente preciso]

Por que as outras estão erradas:

A) [Motivo específico de por que A não funciona - 2-3 linhas]
B) [Motivo específico de por que B não funciona - 2-3 linhas]
C) [Motivo específico de por que C não funciona - 2-3 linhas]
D) [Motivo específico de por que D não funciona - 2-3 linhas]

Dica importante:
[Padrão recorrente ou conexão com conceito maior - 2-3 linhas]

---

### CORRECT ANSWER

[X] [LETRA] - [Texto completo da alternativa correta]
```

---

## 📖 Padrões de Qualidade

### EXPLANATION (TECH LEAD)

**Critérios obrigatórios:**

1. **Explicação (2-3 linhas):**
   - Qual padrão/decisão arquitetural é testado?
   - Contextualize o problema
   
2. **Por que [X] é correta (5-7 linhas):**
   - Análise PROFUNDA (não superficial)
   - Conecte a princípios (Clean Architecture, DDD, SOLID)
   - Explique implicações e benefícios
   
3. **Por que outras erram (2-3 linhas cada):**
   - Motivo ESPECÍFICO de falha (nunca: "está errada")
   - Conecte a consequências/problemas
   - Refute TODAS as 4 alternativas
   
4. **Dica importante (2-3 linhas):**
   - Padrão recorrente (ex: "Least Privilege Pattern")
   - Conexão com tópicos maiores
   - Como aparece em outros contextos

### 🚸 CHILDREN EXPLANATION

**Tom:** Lúdico, narrativo, com analogias. Não infantilizado.

**Critérios obrigatórios:**

1. **Explicação (2-3 linhas):**
   - Conceito em linguagem simples
   - Analogias práticas (casa, restaurante, robô, etc.)
   - Tecnicamente preciso (sem jargão desnecessário)
   
2. **Por que [X] é correta (3-4 linhas):**
   - Como um dev iniciante deveria pensar
   - Mantendo precisão técnica
   - Analogias práticas
   
3. **Por que outras erram (2-3 linhas cada):**
   - Motivo ESPECÍFICO (nunca: "está errada")
   - Use emojis se apropriado (🤖, 🅰️, ❌, ✅)
   - Padrão: "A) [Problema específico] — [Consequência prática]"
   
4. **Dica importante (2-3 linhas):**
   - Padrão recorrente
   - Conexão com conceitos maiores
   - Transferência de aprendizado

### Tradução (TRANSLATED QUESTION)

- ✅ Fiel ao significado (não literal)
- ✅ Português brasileiro naturalizado
- ✅ Manter termos técnicos em inglês (ex: "fetch_url", "plan mode")
- ✅ Não traduzir nomes de padrões consolidados

### Análise de Alternativas — Critério de Qualidade

- ❌ NUNCA: "Essa alternativa está incorreta"
- ✅ SEMPRE: "Isso falha porque..." ou "Problema: ... Consequência: ..."
- ✅ Conecte o motivo da falha aos conceitos testados

---

## 🔗 Referências (Dentro do Pacote)

Templates de referência:
- `./templates/001-card.md` — Card simples (estrutura básica)
- `./templates/001-enriched-card.md` — Card enriquecido (exemplo completo)
- `./templates/deck-exemplo.md` — Formato para deck PDF

**Esses templates estão no pacote da skill — use-os como referência de tom, estrutura e profundidade.**

---

## 📤 Output (Batch API)

### Formato Recomendado: Markdown

Retorne o card enriquecido como markdown puro (compatível com SRS, exportação, etc.):

```markdown
Scenario: [pergunta]
...
### CORRECT ANSWER

[X] D - [opção correta]
```

### Alternativo: JSON Estruturado

Se integrar com sistema backend, pode retornar JSON:

```json
{
  "card_number": "001",
  "scenario": "...",
  "options": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  },
  "translated_question": "...",
  "explanation_tech_lead": "...",
  "explanation_children": "...",
  "correct_answer": "D"
}
```

---

## ✅ Checklist de Execução (Por Request)

- [ ] Receber imagem anexada (message.content com image block)
- [ ] Extrair pergunta + 4 opções
- [ ] Analisar conteúdo
- [ ] Determinar resposta correta com confiança
- [ ] Traduzir pergunta + opções para português
- [ ] Gerar EXPLANATION (TECH LEAD):
  - [ ] Contexto do padrão testado
  - [ ] Análise profunda da resposta correta
  - [ ] Motivo específico de cada alternativa errada
  - [ ] Dica sobre padrão recorrente
- [ ] Gerar 🚸 CHILDREN EXPLANATION (mesmo conteúdo, acessível)
- [ ] Estruturar card enriquecido completo (markdown)
- [ ] Validar contra template `./templates/001-enriched-card.md`
- [ ] Retornar card (markdown ou JSON conforme configuração)

---

## 🚀 Diferenças Chave: Local vs Batch API

| Fase | Local CLI | Batch API (esta skill) |
|------|-----------|----------------------|
| **Input** | find + rename múltiplas fotos | Recebe uma imagem anexada |
| **Processing** | Sequencial (001, 002, 003) | Paralelo (cada request é independente) |
| **State** | Compartilhado (mesmo diretório) | Isolado (nenhum estado entre requests) |
| **Templates** | Path absoluto (`/Users/.../`) | Path relativo (`./templates/`) |
| **Scale** | Até ~100 imagens localmente | Milhões via Batch API |
| **Output** | Múltiplos arquivos `.md` | Um card por response |

**Resultado:** Mesma qualidade de conteúdo, mas adaptado para a arquitetura paralela/stateless da Batch API.

---

## 📌 Resumo Executivo

1. **Receba uma imagem** (já vem no message)
2. **Extraia pergunta + opções**
3. **Gere card enriquecido** (seguindo template)
4. **Retorne output** (markdown ou JSON)
5. **Escale em paralelo** via Batch API

**Nenhuma dependência de diretório, path absoluto ou estado compartilhado. Puro e simples.**
