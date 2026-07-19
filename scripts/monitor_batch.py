#!/usr/bin/env python3
"""
Monitorar status do batch com logging detalhado
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from setup_logging import setup_logger

load_dotenv()

BATCH_ID_FILE = os.getenv("BATCH_ID_FILE", ".batch_id")
logger, log_file = setup_logger("monitor_batch")

def load_batch_id():
    """Carrega o ID do batch"""
    try:
        batch_id = Path(BATCH_ID_FILE).read_text().strip()
        if not batch_id:
            raise ValueError("Arquivo vazio")
        return batch_id
    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {BATCH_ID_FILE}")
        return None

def monitor_batch(batch_id, check_interval=15, max_duration=3600):
    """Monitora batch até conclusão ou timeout"""

    client = Anthropic()
    start_time = time.time()
    last_status = None

    logger.info(f"Iniciando monitoramento do batch: {batch_id}")
    logger.info(f"Intervalo de verificação: {check_interval}s")
    logger.info(f"Duração máxima: {max_duration}s ({max_duration//60} minutos)")
    logger.info("")

    while True:
        elapsed = int(time.time() - start_time)

        try:
            batch = client.beta.messages.batches.retrieve(batch_id)

            status_line = (
                f"[{elapsed}s] Status: {batch.processing_status} | "
                f"Processando: {batch.request_counts.processing} | "
                f"Sucesso: {batch.request_counts.succeeded} | "
                f"Erros: {batch.request_counts.errored}"
            )

            if batch.processing_status != last_status:
                logger.info(status_line)
                last_status = batch.processing_status

            if batch.processing_status == "ended":
                logger.info("")
                logger.info("=" * 70)
                logger.info("✅ BATCH CONCLUÍDO")
                logger.info("=" * 70)
                logger.info(f"Sucesso: {batch.request_counts.succeeded}/3")
                logger.info(f"Erros: {batch.request_counts.errored}/3")
                logger.info(f"Tempo total: {elapsed}s ({elapsed//60}m{elapsed%60}s)")
                logger.info("")
                return True

            if elapsed > max_duration:
                logger.warning("❌ TIMEOUT: Duração máxima atingida")
                return False

            time.sleep(check_interval)

        except Exception as e:
            logger.error(f"Erro ao consultar API: {e}")
            return False

def main():
    logger.info("=" * 70)
    logger.info("Monitor de Batch - Claude API Batch")
    logger.info("=" * 70)
    logger.info(f"Log: {log_file}")
    logger.info("")

    batch_id = load_batch_id()
    if not batch_id:
        return False

    success = monitor_batch(batch_id)

    if success:
        logger.info("Execute: python scripts/baixar_resultados.py")
    else:
        logger.info("Tente novamente mais tarde")

    return success

if __name__ == "__main__":
    exit(0 if main() else 1)
