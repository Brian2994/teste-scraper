"""
Responsável por:
- Conectar ao BigQuery
- Enviar DataFrame
"""

from google.oauth2 import service_account
from pandas_gbq import to_gbq

from src.config.config import (
    GOOGLE_APPLICATION_CREDENTIALS,
    BIGQUERY_PROJECT_ID,
    BIGQUERY_DATASET
)

# Credenciais
credentials = (
    service_account.Credentials
    .from_service_account_file(
        GOOGLE_APPLICATION_CREDENTIALS
    )
)

def load_to_bigquery(df, table_name):

    print(f"Enviando tabela {table_name} para o BigQuery...")

    # Destino
    table_id = (
        f"{BIGQUERY_PROJECT_ID}."
        f"{BIGQUERY_DATASET}."
        f"{table_name}"
    )

    # Envio para BigQuery
    to_gbq(
        dataframe=df,
        destination_table=table_id,
        project_id=BIGQUERY_PROJECT_ID,
        credentials=credentials,

        # replace | append
        if_exists="replace"
    )

    print(f"Tabela {table_name} enviada com sucesso!")