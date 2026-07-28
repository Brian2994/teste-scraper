from src.extract.apy import executar_extracao
from src.bronze.bronze import salvar_bronze


def main():
    dados, data_coleta = executar_extracao()
    salvar_bronze(dados, data_coleta)


if __name__ == "__main__":
    main()