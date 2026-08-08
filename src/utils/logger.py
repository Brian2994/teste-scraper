import logging
from pathlib import Path


def configurar_logger():

    pasta_logs = Path("logs")
    pasta_logs.mkdir(parents=True, exist_ok=True)

    arquivo_log = pasta_logs / "pipeline.log"

    logger = logging.getLogger("pipeline")

    # Evita adicionar handlers duplicados
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Arquivo
    file_handler = logging.FileHandler(
        arquivo_log,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    # Terminal
    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger