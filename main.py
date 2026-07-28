from src.extract.apy import executar_extracao
from src.bronze.bronze import salvar_bronze


def main():
    dados = executar_extracao()
    salvar_bronze(dados)


if __name__ == "__main__":
    main()