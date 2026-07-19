#!/usr/bin/env python3
"""
Upload skill para Claude API e retorna o ID do arquivo remoto
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

SKILL_DIR = "skill/gerar-cards-enriquecidos"
SKILL_ID_FILE = "skill_id.txt"
TEMPLATES_DIR = "templates"

def build_merged_skill_content():
    """Mescla SKILL.md + todos os templates/*.md num único documento.

    A Files API aceita um arquivo por upload, então os templates
    referenciados pela skill (./templates/*.md) precisam ser embutidos
    no mesmo arquivo para que o modelo tenha acesso a eles.
    """

    skill_md_path = Path(SKILL_DIR) / "SKILL.md"

    if not skill_md_path.exists():
        print(f"❌ Arquivo não encontrado: {skill_md_path}")
        return None

    skill_text = skill_md_path.read_text(encoding="utf-8")

    templates_dir = Path(SKILL_DIR) / TEMPLATES_DIR
    template_files = sorted(templates_dir.glob("*.md")) if templates_dir.exists() else []

    parts = [skill_text]

    if template_files:
        parts.append("\n\n---\n\n# 📎 Templates Anexados\n")
        for template_path in template_files:
            relative_ref = f"./{TEMPLATES_DIR}/{template_path.name}"
            template_text = template_path.read_text(encoding="utf-8")
            parts.append(
                f"\n## Template: `{relative_ref}`\n\n```markdown\n{template_text}\n```\n"
            )
        print(f"📎 {len(template_files)} template(s) anexado(s):")
        for template_path in template_files:
            print(f"   - {template_path.relative_to(Path(SKILL_DIR))}")
    else:
        print("⚠️  Nenhum template encontrado em templates/")

    return "".join(parts)

def upload_skill():
    """Upload da skill (SKILL.md + templates mesclados) para a API Claude e salva o ID"""

    client = Anthropic()

    merged_content = build_merged_skill_content()

    if merged_content is None:
        return False

    print(f"📤 Fazendo upload da skill mesclada ({SKILL_DIR})")

    skill_content = merged_content.encode("utf-8")

    try:
        # Upload do arquivo usando Files API
        response = client.beta.files.upload(
            file=("SKILL.md", skill_content, "text/markdown"),
        )

        skill_id = response.id

        print(f"✅ Skill enviada com sucesso!")
        print(f"   ID da Skill: {skill_id}")
        print(f"   Nome: {response.filename}")
        print(f"   Tamanho: {response.size_bytes} bytes")

        # Salvar ID em arquivo
        with open(SKILL_ID_FILE, 'w') as f:
            f.write(skill_id)

        print(f"✅ ID salvo em: {SKILL_ID_FILE}")

        return True

    except Exception as e:
        print(f"❌ Erro ao fazer upload: {e}")
        return False

def main():
    print("=" * 60)
    print("Upload de Skill - Claude API Batch")
    print("=" * 60)
    print()

    # Verificar se API key está configurada
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Erro: ANTHROPIC_API_KEY não configurada no .env")
        return False

    print(f"🎯 Diretório da skill: {SKILL_DIR}")
    print()

    success = upload_skill()

    print()
    if success:
        print("✅ Processo concluído com sucesso!")
        print(f"   Use o ID '{Path(SKILL_ID_FILE).read_text().strip()}' nos próximos passos")
    else:
        print("❌ Processo falhou")

    return success

if __name__ == "__main__":
    exit(0 if main() else 1)
