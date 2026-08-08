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
from src.utils.logger import configurar_logger

# Carrega variáveis do arquivo .env
load_dotenv()

logger = configurar_logger()

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

    try:

        logger.info("Iniciando pipeline")

        logger.info("Iniciando etapa EXTRACT")

        # EXTRACT
        dados, data_coleta = executar_extracao()

        logger.info(f"Extração concluída. Registros coletados: {len(dados)}")

        logger.info("Iniciando etapa BRONZE")

        # BRONZE
        salvar_bronze(
            dados,
            data_coleta
        )

        logger.info("Camada BRONZE salva com sucesso")

        logger.info("Iniciando etapa SILVER")

        # SILVER
        dados_silver = transformar_silver(dados)

        logger.info(
            f"Transformação SILVER concluída. "
            f"Registros: {len(dados_silver)}"
        )

        # SALVAR SILVER
        salvar_silver(
            dados_silver,
            data_coleta
        )

        logger.info("Camada SILVER salva com sucesso")

        logger.info("Iniciando etapa GOLD")

        # GOLD
        df = criar_dataframe(dados_silver)

        logger.info(
            f"DataFrame GOLD criado. "
            f"Linhas: {len(df)} | Colunas: {len(df.columns)}"
        )

        logger.info("Criando tabelas analíticas GOLD")

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

        logger.info("Salvando fato_veiculos no PostgreSQL")

        # SALVAR GOLD
        salvar_tabelas_gold(
            df,
            "fato_veiculos",
            engine
        )

        logger.info("Enviando fato_veiculos para BigQuery")

        load_to_bigquery(df, "fato_veiculos")

        logger.info("fato_veiculos carregada com sucesso")

        logger.info("Salvando kpi_resumo_geral no PostgreSQL")

        salvar_tabelas_gold(
            df_resumo,
            "kpi_resumo_geral",
            engine
        )

        logger.info("Enviando kpi_resumo_geral para BigQuery")

        load_to_bigquery(df_resumo, "kpi_resumo_geral")

        logger.info("kpi_resumo_geral carregada com sucesso")

        logger.info("Salvando dim_marcas no PostgreSQL")

        salvar_tabelas_gold(
            df_marcas,
            "dim_marcas",
            engine
        )

        logger.info("Enviando dim_marcas para BigQuery")

        load_to_bigquery(df_marcas, "dim_marcas")

        logger.info("dim_marcas carregada com sucesso")

        logger.info("Salvando dim_regioes no PostgreSQL")

        salvar_tabelas_gold(
            df_regioes,
            "dim_regioes",
            engine
        )

        logger.info("Enviando dim_regioes para BigQuery")

        load_to_bigquery(df_regioes, "dim_regioes")

        logger.info("dim_regioes carregada com sucesso")

        logger.info("Salvando dim_estados no PostgreSQL")

        salvar_tabelas_gold(
            df_estados,
            "dim_estados",
            engine
        )

        logger.info("Enviando dim_estados para BigQuery")

        load_to_bigquery(df_estados, "dim_estados")

        logger.info("dim_estados carregada com sucesso")

        logger.info("Salvando dim_categorias no PostgreSQL")

        salvar_tabelas_gold(
            df_categorias,
            "dim_categorias",
            engine
        )

        logger.info("Enviando dim_categorias para BigQuery")

        load_to_bigquery(df_categorias, "dim_categorias")

        logger.info("dim_categorias carregada com sucesso")

        logger.info("Salvando dim_faixa_preco no PostgreSQL")

        salvar_tabelas_gold(
            df_faixa_preco,
            "dim_faixa_preco",
            engine
        )

        logger.info("Enviando dim_faixa_preco para BigQuery")

        load_to_bigquery(df_faixa_preco, "dim_faixa_preco")

        logger.info("dim_faixa_preco carregada com sucesso")

        logger.info("Salvando dim_modelos no PostgreSQL")

        salvar_tabelas_gold(
            df_modelos,
            "dim_modelos",
            engine
        )

        logger.info("Enviando dim_modelos para BigQuery")

        load_to_bigquery(df_modelos, "dim_modelos")

        logger.info("dim_modelos carregada com sucesso")

        logger.info("Salvando dim_combustivel no PostgreSQL")

        salvar_tabelas_gold(
            df_combustivel,
            "dim_combustivel",
            engine
        )

        logger.info("Enviando dim_combustivel para BigQuery")

        load_to_bigquery(df_combustivel, "dim_combustivel")

        logger.info("dim_combustivel carregada com sucesso")

        logger.info("Salvando dim_transmissao no PostgreSQL")

        salvar_tabelas_gold(
            df_transmissao,
            "dim_transmissao",
            engine
        )

        logger.info("Enviando dim_transmissao para BigQuery")

        load_to_bigquery(df_transmissao, "dim_transmissao")

        logger.info("dim_transmissao carregada com sucesso")

        logger.info("Salvando dim_faixa_desconto no PostgreSQL")

        salvar_tabelas_gold(
            df_descontos,
            "dim_faixa_desconto",
            engine
        )

        logger.info("Enviando dim_faixa_desconto para BigQuery")

        load_to_bigquery(df_descontos, "dim_faixa_desconto")

        logger.info("dim_faixa_desconto carregada com sucesso")

        logger.info("Salvando dim_categoria_km no PostgreSQL")

        salvar_tabelas_gold(
            df_categoria_km,
            "dim_categoria_km",
            engine
        )

        logger.info("Enviando dim_categoria_km para BigQuery")

        load_to_bigquery(df_categoria_km, "dim_categoria_km")

        logger.info("dim_categoria_km carregada com sucesso")

        logger.info("Salvando dim_ano_modelo no PostgreSQL")

        salvar_tabelas_gold(
            df_ano_modelo,
            "dim_ano_modelo",
            engine
        )

        logger.info("Enviando dim_ano_modelo para BigQuery")

        load_to_bigquery(df_ano_modelo, "dim_ano_modelo")

        logger.info("dim_ano_modelo carregada com sucesso")

        logger.info("Salvando dim_lojas no PostgreSQL")

        salvar_tabelas_gold(
            df_lojas,
            "dim_lojas",
            engine
        )

        logger.info("Enviando dim_lojas para BigQuery")

        load_to_bigquery(df_lojas, "dim_lojas")

        logger.info("dim_lojas carregada com sucesso")

        logger.info("Salvando dim_cor no PostgreSQL")

        salvar_tabelas_gold(
            df_cor,
            "dim_cor",
            engine
        )

        logger.info("Enviando dim_cor para BigQuery")

        load_to_bigquery(df_cor, "dim_cor")

        logger.info("dim_cor carregada com sucesso")

        logger.info("Salvando dim_marca_categoria no PostgreSQL")

        salvar_tabelas_gold(
            df_marca_categoria,
            "dim_marca_categoria",
            engine
        )

        logger.info("Enviando dim_marca_categoria para BigQuery")

        load_to_bigquery(df_marca_categoria, "dim_marca_categoria")

        logger.info("dim_marca_categoria carregada com sucesso")

        logger.info("Todas as tabelas GOLD processadas com sucesso")

        logger.info(
            "Pipeline finalizada com sucesso. "
            "Dados locais, PostgreSQL e BigQuery atualizados."
        )

    except Exception:

        logger.exception(
            "Erro durante execução da pipeline"
        )

        raise

if __name__ == "__main__":
    main()