# Desafio Fotos - Claude API Batch

## Objetivo

Criar um script Python que utiliza o SDK do Claude para enviar imagens para a **Batch API** e processar cada imagem usando uma **skill local** já disponível no repositório.

O objetivo final é gerar cards enriquecidos (em markdown) para cada imagem processada, aproveitando o processamento em lote (batch) para otimizar custos e tempo de processamento.

**Fase 1 (Atual)**: Testar o processo com **3 imagens**  
**Fase 2 (Futuro)**: Escalar para **60+ imagens**

## Visão Geral

### Fluxo Principal
1. **Listar imagens** do diretório `fotos/`
2. **Preparar requisições** para a Batch API usando a skill local
3. **Enviar batch** com todas as 60 imagens
4. **Monitorar processamento** até conclusão
5. **Baixar resultados** e gerar cards markdown em `cards_gerados/`

## Estrutura do Projeto

```
desafio-fotos-claude-api-batch/
├── skill/
│   └── gerar-cards-enriquecidos/     # Skill local para processar imagens
│       ├── SKILL.md
│       └── templates/
│           └── 001-enriched-card.md
├── fotos/                             # Imagens a processar (60 arquivos PNG/JPG)
│   ├── foto-001.png
│   ├── foto-002.png
│   └── ...
├── cards_gerados/                     # Saída: cards markdown gerados
│   ├── 001-card.md
│   ├── 002-card.md
│   └── ...
├── scripts/
│   ├── upload_skill.py               # Upload da skill (se necessário)
│   ├── enviar_batch.py               # Enviar batch para Claude API
│   └── baixar_resultados.py          # Download e processamento de resultados
├── .env                               # Variáveis de ambiente (API Key)
├── skill_id.txt                       # ID da skill (gerado após upload)
└── README.md
```

## Pré-requisitos

- Python 3.8+
- SDK do Claude: `pip install anthropic`
- Arquivo `.env` com a chave da API: `ANTHROPIC_API_KEY=sk-...`
- 3+ imagens em `fotos/` para teste (formatos: PNG, JPG, JPEG)
- Skill local disponível em `skill/gerar-cards-enriquecidos/`

## Instalação

### 1. Clone ou configure o projeto
```bash
cd desafio-fotos-claude-api-batch
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite .env e adicione sua ANTHROPIC_API_KEY
```

### 4. Coloque as 60 imagens
```bash
# Copie suas 60 imagens para:
cp seu/caminho/fotos/*.png fotos/
```

## Uso

### Passo 1: Enviar Batch
```bash
python scripts/enviar_batch.py
```

Isso irá:
- Listar todas as imagens em `fotos/` (atualmente: 3 imagens de teste)
- Preparar requisições para a Batch API usando a skill local
- Enviar o batch e retornar um `batch_id`
- Salvar o ID em arquivo de rastreamento

**Saída esperada:**
```
✓ 3 imagens encontradas
✓ Batch enviado com sucesso
ID do Batch: batch_19700101t000000_abc123xyz
Monitorando processamento...
```

### Passo 2: Monitorar Processamento
```bash
python scripts/enviar_batch.py --status
```

Ou, aguarde a conclusão automática (o script verifica o status periodicamente).

### Passo 3: Baixar Resultados
```bash
python scripts/baixar_resultados.py
```

Isso irá:
- Recuperar o `batch_id` do arquivo de rastreamento
- Fazer download dos resultados
- Processar cada resultado e gerar card markdown
- Salvar cards em `cards_gerados/`

**Saída esperada:**
```
✓ Conectando ao batch: batch_19700101t000000_abc123xyz
✓ 3 resultados recuperados
✓ 3 cards gerados em cards_gerados/
✓ Processamento concluído!
```

## Tecnologias

- **Claude API**: Para processamento de imagens
- **Batch API**: Para otimizar custos e enviar múltiplas requisições
- **Python SDK**: `anthropic` package
- **Skill Local**: Lógica de processamento de imagens e geração de cards

## Custo e Performance

### Batch API vs Regular API
- **Batch API**: 50% de desconto, ideal para grandes volumes
- **Latência**: Processamento em ~24h (check periodicamente)
- **Economia**: Para 60 imagens, economiza ~50% do custo

### Estimativa (Fase 1 - Teste)
- 3 imagens × processamento = teste rápido da pipeline
- Tempo total: ~5-15 minutos de processamento

### Estimativa (Fase 2 - Produção)
- 60 imagens × processamento = economia ~50% com Batch API
- Tempo total: ~30-60 minutos de processamento (depende da fila)

## Próximos Passos

### Fase 1 - Teste (3 imagens)
- [ ] Implementar `enviar_batch.py`
- [ ] Implementar `baixar_resultados.py`
- [ ] Validar integração com skill local
- [ ] Testar fluxo completo (enviar → processar → baixar)
- [ ] Validar formato dos cards gerados

### Fase 2 - Produção
- [ ] Escalar para 60+ imagens
- [ ] Otimizar performance
- [ ] Implementar tratamento de erros robusto
- [ ] Adicionar logging detalhado
- [ ] Documentar resultados gerados

## Documentação

- [Claude API Documentation](https://docs.anthropic.com)
- [Batch API Guide](https://docs.anthropic.com/batch-api)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)

## Licença

MIT

---

**Autor**: Fabão  
**Projeto**: Desafio Fotos - Claude API Batch  
**Status**: Em desenvolvimento
