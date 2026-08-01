import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.extract.apy import executar_extracao
from src.bronze.bronze import salvar_bronze
from src.silver.silver import transformar_silver, salvar_silver
from src.gold.gold import (
    criar_dataframe,
    resumo_geral,
    tabela_marcas,
    tabela_regioes,
    tabela_estados,
    tabela_categorias,
    tabela_faixa_preco,
    tabela_modelos,
    tabela_combustivel,
    tabela_transmissao,
    tabela_descontos,
    tabela_categoria_km,
    tabela_ano_modelo,
    tabela_lojas,
    tabela_cor,
    tabela_marca_categoria,
    salvar_tabelas_gold
)
from src.bigquery.bigquery import load_to_bigquery

# Carrega variáveis do arquivo .env
load_dotenv()

# Configura a conexão com o PostgreSQL
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME") 

# Cria o motor de conexão (Engine) do SQLAlchemy
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)


def main():
    # EXTRACT
    dados, data_coleta = executar_extracao()

    # BRONZE
    salvar_bronze(
        dados,
        data_coleta
    )

    # SILVER
    dados_silver = transformar_silver(dados)

    # SALVAR SILVER
    salvar_silver(
        dados_silver,
        data_coleta
    )

    # GOLD
    df = criar_dataframe(dados_silver)

    df_resumo = resumo_geral(df)
    df_marcas = tabela_marcas(df)
    df_regioes = tabela_regioes(df)
    df_estados = tabela_estados(df)
    df_categorias = tabela_categorias(df)
    df_faixa_preco = tabela_faixa_preco(df)
    df_modelos = tabela_modelos(df)
    df_combustivel = tabela_combustivel(df)
    df_transmissao = tabela_transmissao(df)
    df_descontos = tabela_descontos(df)
    df_categoria_km = tabela_categoria_km(df)
    df_ano_modelo = tabela_ano_modelo(df)
    df_lojas = tabela_lojas(df)
    df_cor = tabela_cor(df)
    df_marca_categoria = tabela_marca_categoria(df)

    # SALVAR GOLD
    salvar_tabelas_gold(
        df,
        "fato_veiculos",
        engine
    )

    load_to_bigquery(df, "fato_veiculos") 

    salvar_tabelas_gold(
        df_resumo,
        "kpi_resumo_geral",
        engine
    )

    load_to_bigquery(df_resumo, "kpi_resumo_geral")

    salvar_tabelas_gold(
        df_marcas,
        "dim_marcas",
        engine
    )

    load_to_bigquery(df_marcas, "dim_marcas")

    salvar_tabelas_gold(
        df_regioes,
        "dim_regioes",
        engine
    )

    load_to_bigquery(df_regioes, "dim_regioes")

    salvar_tabelas_gold(
        df_estados,
        "dim_estados",
        engine
    )

    load_to_bigquery(df_estados, "dim_estados")

    salvar_tabelas_gold(
        df_categorias,
        "dim_categorias",
        engine
    )

    load_to_bigquery(df_categorias, "dim_categorias")

    salvar_tabelas_gold(
        df_faixa_preco,
        "dim_faixa_preco",
        engine
    )

    load_to_bigquery(df_faixa_preco, "dim_faixa_preco")

    salvar_tabelas_gold(
        df_modelos,
        "dim_modelos",
        engine
    )

    load_to_bigquery(df_modelos, "dim_modelos")

    salvar_tabelas_gold(
        df_combustivel,
        "dim_combustivel",
        engine
    )

    load_to_bigquery(df_combustivel, "dim_combustivel")

    salvar_tabelas_gold(
        df_transmissao,
        "dim_transmissao",
        engine
    )

    load_to_bigquery(df_transmissao, "dim_transmissao")

    salvar_tabelas_gold(
        df_descontos,
        "dim_faixa_desconto",
        engine
    )

    load_to_bigquery(df_descontos, "dim_faixa_desconto")

    salvar_tabelas_gold(
        df_categoria_km,
        "dim_categoria_km",
        engine
    )

    load_to_bigquery(df_categoria_km, "dim_categoria_km")

    salvar_tabelas_gold(
        df_ano_modelo,
        "dim_ano_modelo",
        engine
    )

    load_to_bigquery(df_ano_modelo, "dim_ano_modelo")

    salvar_tabelas_gold(
        df_lojas,
        "dim_lojas",
        engine
    )

    load_to_bigquery(df_lojas, "dim_lojas")

    salvar_tabelas_gold(
        df_cor,
        "dim_cor",
        engine
    )

    load_to_bigquery(df_cor, "dim_cor")

    salvar_tabelas_gold(
        df_marca_categoria,
        "dim_marca_categoria",
        engine
    )

    load_to_bigquery(df_marca_categoria, "dim_marca_categoria")

    print("\nPipeline finalizada! Dados locais e na nuvem atualizados.")

if __name__ == "__main__":
    main()