import os
from dotenv import load_dotenv
from datetime import datetime
import requests

def executar_extracao():
    # Carrega as variáveis do arquivo .env
    load_dotenv()
    URL = os.getenv("URL")

    # Variáveis
    pagina = 1          # Contador de páginas
    PAGE_SIZE = 1000    # Quantidade solicitada por lote
    from_ = 0           # Começa pelo primeiro índice
    veiculos = []       # Lista (Dados temporários)

    data_coleta = datetime.now()

    print("Iniciando coleta...\n")

    while True:
        payload = {
            "from": str(from_),
            "size": PAGE_SIZE,
            "localizacao": {
                "latitude": None,
                "longitude": None,
                "uf": None
            }
        }

        response  = requests.post(
            URL,
            json=payload,
            timeout=30
        )

        # Validação HTTP
        if response.status_code != 200:
            print(f"Erro HTTP: {response.status_code}")
            break

        json_response = response.json()
        dados = json_response.get("data", [])

        if not dados:
            print("Fim da coleta.")
            break

        # Armazena todos do dados encontrados na lista 'veiculos'
        veiculos.extend([
            {
                **veiculo,
                "data_coleta": data_coleta.strftime("%Y-%m-%d %H:%M:%S"),
                "fonte": "Seminovos Movida API"
            }
            for veiculo in dados
        ])

        print(f"Página {pagina} -> {len(dados)} veículos")
        print(f"Total coletado: {len(veiculos)}\n")

        # Atualiza contadores
        pagina += 1
        from_ += PAGE_SIZE

    print(f"\nColeta finalizada! Total de veículos: {len(veiculos)}")

    return veiculos, data_coleta