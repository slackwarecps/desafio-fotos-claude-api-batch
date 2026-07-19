#!/usr/bin/env python3
"""
Enviar batch de imagens para Claude API Batch
Cada imagem será processada usando a skill remota
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

FOTOS_DIR = os.getenv("FOTOS_DIR", "fotos")
SKILL_ID_FILE = "skill_id.txt"
BATCH_ID_FILE = os.getenv("BATCH_ID_FILE", ".batch_id")
BATCH_REQUESTS_FILE = "batch_requests.jsonl"
MODEL = os.getenv("MODEL", "claude-sonnet-5")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

def load_local_skill_content():
    """Lê o conteúdo textual da skill (SKILL.md + templates) do disco local.

    A Files API não permite baixar de volta arquivos enviados por nós
    (só arquivos gerados pelo Claude), e system blocks só aceitam
    type='text' — então o conteúdo precisa ser embutido como texto,
    lido diretamente do mesmo diretório usado no upload_skill.py.
    """
    skill_dir = Path("skill/gerar-cards-enriquecidos")
    skill_md_path = skill_dir / "SKILL.md"

    if not skill_md_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {skill_md_path}")

    parts = [skill_md_path.read_text(encoding="utf-8")]

    templates_dir = skill_dir / "templates"
    template_files = sorted(templates_dir.glob("*.md")) if templates_dir.exists() else []

    if template_files:
        parts.append("\n\n---\n\n# 📎 Templates Anexados\n")
        for template_path in template_files:
            relative_ref = f"./templates/{template_path.name}"
            parts.append(
                f"\n## Template: `{relative_ref}`\n\n```markdown\n{template_path.read_text(encoding='utf-8')}\n```\n"
            )

    return "".join(parts)

def load_skill_id():
    """Carrega o ID da skill remota"""
    try:
        with open(SKILL_ID_FILE, 'r') as f:
            skill_id = f.read().strip()
        if not skill_id:
            raise ValueError("skill_id.txt está vazio")
        return skill_id
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {SKILL_ID_FILE}")
        print("   Execute 'python scripts/upload_skill.py' primeiro")
        return None

def load_image_as_base64(image_path):
    """Carrega imagem e converte para base64"""
    with open(image_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')

def get_mime_type(image_path):
    """Determina o MIME type baseado na extensão"""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
    }
    return mime_types.get(ext, 'image/png')

def create_batch_requests(skill_id, skill_text):
    """Cria requisições de batch para cada imagem"""

    fotos_path = Path(FOTOS_DIR)

    if not fotos_path.exists():
        print(f"❌ Diretório não encontrado: {FOTOS_DIR}")
        return None

    # Encontrar todas as imagens
    images = sorted([f for f in fotos_path.glob('*')
                    if f.suffix.lower() in ['.png', '.jpg', '.jpeg']])

    if not images:
        print(f"❌ Nenhuma imagem encontrada em {FOTOS_DIR}")
        return None

    print(f"📸 Encontradas {len(images)} imagem(ns):")
    for img in images:
        print(f"   - {img.name}")
    print()

    requests = []

    for idx, image_path in enumerate(images, 1):
        # Carregar imagem
        image_data = load_image_as_base64(image_path)
        mime_type = get_mime_type(image_path)

        # Criar requisição para o batch
        request = {
            "custom_id": f"foto-{idx:03d}",
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "system": [
                    {
                        "type": "text",
                        "text": "Você é um especialista em criar cards enriquecidos para aprendizado SRS. Use a skill abaixo como referência para gerar cards de alta qualidade.\n\n"
                        + skill_text,
                    },
                ],
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Gerar card enriquecido para esta imagem. Número do card: {idx:03d}\n\n⚠️ IMPORTANTE: Retorne APENAS o conteúdo markdown puro, SEM blocos de código (sem ```markdown).\nComece direto com: Scenario: ...\n\nSiga exatamente o template e instruções da skill fornecida.",
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": image_data,
                                },
                            },
                        ],
                    }
                ],
            },
        }

        requests.append(request)

    return requests

def save_batch_requests(requests):
    """Salva requisições em formato JSONL"""
    with open(BATCH_REQUESTS_FILE, 'w') as f:
        for req in requests:
            f.write(json.dumps(req) + '\n')
    print(f"✅ Requisições salvas em: {BATCH_REQUESTS_FILE}")

def submit_batch(client, requests):
    """Submete o batch para a API"""

    print(f"📤 Enviando batch com {len(requests)} requisição(ões)...")
    print()

    try:
        # Submeter batch para a API
        response = client.beta.messages.batches.create(
            requests=requests,
        )

        batch_id = response.id

        print("✅ Batch enviado com sucesso!")
        print()
        print(f"🎯 ID do Batch: {batch_id}")
        print(f"   Requisições: {len(requests)}")
        print(f"   Status: {response.processing_status}")
        print(f"   Enviado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Salvar batch_id
        with open(BATCH_ID_FILE, 'w') as f:
            f.write(batch_id)

        print()
        print(f"✅ ID do batch salvo em: {BATCH_ID_FILE}")

        return batch_id

    except Exception as e:
        print(f"❌ Erro ao enviar batch: {e}")
        return None

def main():
    print("=" * 70)
    print("Enviar Batch - Claude API Batch")
    print("=" * 70)
    print()

    # Verificar API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Erro: ANTHROPIC_API_KEY não configurada no .env")
        return False

    print(f"🤖 Modelo: {MODEL}")
    print(f"📊 Max tokens: {MAX_TOKENS}")
    print()

    client = Anthropic()

    # Carregar skill_id
    print("📋 Carregando skill remota...")
    skill_id = load_skill_id()
    if not skill_id:
        return False
    print(f"✅ Skill carregada: {skill_id}")
    print()

    # Criar requisições de batch
    print("📥 Lendo conteúdo local da skill (SKILL.md + templates)...")
    skill_text = load_local_skill_content()
    print(f"✅ Skill carregada ({len(skill_text)} caracteres)")
    print()

    print("🔧 Preparando requisições...")
    requests = create_batch_requests(skill_id, skill_text)
    if not requests:
        return False

    print()

    # Submeter batch
    batch_id = submit_batch(client, requests)

    if batch_id:
        print()
        print("=" * 70)
        print("✅ PRÓXIMOS PASSOS:")
        print("=" * 70)
        print()
        print("1. Monitorar processamento:")
        print("   python scripts/enviar_batch.py --status")
        print()
        print("2. Após conclusão, baixar resultados:")
        print("   python scripts/baixar_resultados.py")
        print()
        print(f"📌 Guarde este ID: {batch_id}")
        return True
    else:
        return False

if __name__ == "__main__":
    exit(0 if main() else 1)
