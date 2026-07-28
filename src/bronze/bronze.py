import json
from pathlib import Path

def salvar_bronze(dados):
    pasta = Path("data/bronze")
    pasta.mkdir(parents=True, exist_ok=True)

    arquivo = pasta / "veiculos.json"

    with open(
        arquivo,
        "w",
        encoding="utf-8"
    ) as arquivo_json:
        json.dump(
            dados,
            arquivo_json,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nArquivo salvo em: {arquivo}")
    print(f"Total de registros: {len(dados)}")