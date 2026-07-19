#!/usr/bin/env python3
"""
Baixar resultados do batch e gerar cards markdown em cards_gerados/
"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

BATCH_ID_FILE = ".batch_id"
OUTPUT_DIR = "cards_gerados"

def load_batch_id():
    """Carrega o ID do batch salvo por enviar_batch.py"""
    try:
        with open(BATCH_ID_FILE, 'r') as f:
            batch_id = f.read().strip()
        if not batch_id:
            raise ValueError(f"{BATCH_ID_FILE} está vazio")
        return batch_id
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {BATCH_ID_FILE}")
        print("   Execute 'python scripts/enviar_batch.py' primeiro")
        return None

def extract_card_number(custom_id):
    """Extrai o número do card a partir do custom_id (ex: 'foto-001' -> '001')"""
    match = re.search(r"(\d+)$", custom_id)
    return match.group(1) if match else custom_id

def extract_text_from_message(message):
    """Concatena todos os blocos de texto da resposta do modelo"""
    text = "".join(
        block.text for block in message.content if block.type == "text"
    ).strip()

    # Remover blocos de código markdown se presentes (```markdown ... ```)
    if text.startswith("```markdown"):
        text = text[11:]  # Remove ```markdown
    if text.endswith("```"):
        text = text[:-3]  # Remove ```

    return text.strip()

def save_card(card_number, content):
    """Salva o card enriquecido em cards_gerados/{card_number}-enriched-card.md"""
    output_path = Path(OUTPUT_DIR) / f"{card_number}-enriched-card.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path

def process_results(client, batch_id):
    """Percorre os resultados do batch e gera um card para cada sucesso"""

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    saved = []
    failed = []

    for result in client.beta.messages.batches.results(batch_id):
        card_number = extract_card_number(result.custom_id)

        if result.result.type == "succeeded":
            content = extract_text_from_message(result.result.message)
            output_path = save_card(card_number, content)
            saved.append((result.custom_id, output_path))
            print(f"✅ {result.custom_id} → {output_path}")

        elif result.result.type == "errored":
            error = result.result.error.error
            failed.append((result.custom_id, error.message))
            print(f"❌ {result.custom_id} → erro: {error.message}")

        else:
            failed.append((result.custom_id, f"status inesperado: {result.result.type}"))
            print(f"⚠️  {result.custom_id} → status inesperado: {result.result.type}")

    return saved, failed

def main():
    print("=" * 70)
    print("Baixar Resultados - Claude API Batch")
    print("=" * 70)
    print()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Erro: ANTHROPIC_API_KEY não configurada no .env")
        return False

    client = Anthropic()

    batch_id = load_batch_id()
    if not batch_id:
        return False

    print(f"🎯 Batch: {batch_id}")
    print()

    batch = client.beta.messages.batches.retrieve(batch_id)
    print(f"📊 Status: {batch.processing_status}")
    print(f"   Processando: {batch.request_counts.processing}")
    print(f"   Sucesso: {batch.request_counts.succeeded}")
    print(f"   Erros: {batch.request_counts.errored}")
    print()

    if batch.processing_status != "ended":
        print("⏳ Batch ainda não terminou de processar. Tente novamente em instantes.")
        return False

    print("📥 Baixando e processando resultados...")
    print()

    saved, failed = process_results(client, batch_id)

    print()
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"✅ Cards gerados: {len(saved)} em {OUTPUT_DIR}/")
    if failed:
        print(f"❌ Falhas: {len(failed)}")
        for custom_id, message in failed:
            print(f"   - {custom_id}: {message}")

    return len(saved) > 0

if __name__ == "__main__":
    exit(0 if main() else 1)
