"""
Teste de conexão com Google BigQuery.

Objetivos:
- validar autenticação
- validar acesso ao projeto
"""

from google.cloud import bigquery
from google.oauth2 import service_account

from src.config.config import (
    GOOGLE_APPLICATION_CREDENTIALS,
    BIGQUERY_PROJECT_ID,
    BIGQUERY_DATASET
)

try:

    print("Iniciando conexão BigQuery...")

    # Cria credenciais
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS
    )

    # Cria cliente BigQuery
    client = bigquery.Client(
        credentials=credentials,
        project=BIGQUERY_PROJECT_ID
    )

    print("Conexão estabelecida!")

    dataset_ref = client.get_dataset(BIGQUERY_DATASET)

    print(dataset_ref.full_dataset_id)

    # Query simples
    query = "SELECT 'BigQuery conectado com sucesso!' AS message"

    query_job = client.query(query)

    results = query_job.result()

    for row in results:
        print(row.message)

except Exception as error:
    print(f"Erro ao conectar no BigQuery: {error}")