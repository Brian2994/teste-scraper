"""
Centraliza configurações do projeto.
Responsável por carregar variáveis de ambiente.
"""

from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env
load_dotenv()

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)

# BigQuery
BIGQUERY_PROJECT_ID = os.getenv("BIGQUERY_PROJECT_ID")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET")
BIGQUERY_TABLE = os.getenv("BIGQUERY_TABLE")