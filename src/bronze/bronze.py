from pathlib import Path
import json

def salvar_bronze(dados, data_coleta):
    pasta = Path("data/bronze")
    pasta.mkdir(parents=True, exist_ok=True)

    timestamp = data_coleta.strftime("%Y%m%d_%H%M%S")

    arquivo = pasta / f"veiculos_{timestamp}.json"

    with open(arquivo, "w", encoding="utf-8") as arquivo_json:        
        json.dump(
            dados,
            arquivo_json,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nArquivo salvo em: {arquivo}")
    print(f"Total de registros: {len(dados)}")