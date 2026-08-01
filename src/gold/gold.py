from pathlib import Path
import pandas as pd
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine

def criar_dataframe(dados_silver):

    return pd.DataFrame(dados_silver)


def resumo_geral(df):

    resumo = pd.DataFrame([{
        "total_veiculos": len(df),
        "marcas": df["marca"].nunique(),
        "modelos": df["modelo"].nunique(),
        "estados": df["uf"].nunique(),
        "preco_medio": df["preco"].mean(),
        "preco_minimo": df["preco"].min(),
        "preco_maximo": df["preco"].max(),
    }])

    return resumo.round(2)


def tabela_marcas(df):

    tabela = (
        df
        .groupby("marca")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_regioes(df):

    tabela = (
        df
        .groupby("regiao")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean")
        )
        .reset_index()
        .round(2)
    )

    return tabela


def tabela_estados(df):

    tabela = (
        df.groupby("uf").agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean")
        )
        .reset_index()
        .round(2)
        .sort_values(by="quantidade", ascending=False)
        .reset_index(drop=True)
    )

    return tabela


def tabela_categorias(df):

    tabela = (
        df.groupby("categoria").agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean")
        )
        .reset_index()
        .round(2)
        .sort_values(by="preco_medio", ascending=False)
        .reset_index(drop=True)
    )

    return tabela


def tabela_faixa_preco(df):

    ordem = [
        "Até 50 mil",
        "50 a 80 mil",
        "80 a 120 mil",
        "Acima de 120 mil",
        ]

    tabela = (
        df
        .groupby("faixa_preco")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
    )

    # Define uma ordem personalizada para as faixas de preço
    tabela["faixa_preco"] = pd.Categorical(
        tabela["faixa_preco"],
        categories=ordem,
        ordered=True,
    )

    # Ordena a tabela seguindo a ordem definida
    tabela = (
        tabela
        .sort_values("faixa_preco")
        .reset_index(drop=True)
    )

    return tabela


def tabela_modelos(df):

    tabela = (
        df
        .groupby("modelo")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_combustivel(df):

    tabela = (
        df
        .groupby("combustivel")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_transmissao(df):

    tabela = (
        df
        .groupby("transmissao")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            preco_minimo=("preco", "min"),
            preco_maximo=("preco", "max"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_descontos(df):

    ordem = [
        "Excelente",
        "Boa",
        "Pequena",
        "Sem desconto",
        ]

    tabela = (
        df
        .groupby("faixa_desconto")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
    )

    # Define uma ordem personalizada para as faixas
    tabela["faixa_desconto"] = pd.Categorical(
        tabela["faixa_desconto"],
        categories=ordem,
        ordered=True,
    )

    # Ordena a tabela seguindo a ordem definida
    tabela = (
        tabela
        .sort_values("faixa_desconto")
        .reset_index(drop=True)
    )

    return tabela


def tabela_categoria_km(df):

    ordem = [
        "Baixa",
        "Média",
        "Alta",
        ]

    tabela = (
        df
        .groupby("categoria_km")
        .agg(
            quantidade=("id", "count"),
            km_media=("quilometragem", "mean"),
            preco_medio=("preco", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
        )
        .reset_index()
        .round(2)
    )

    # Define uma ordem personalizada para as faixas
    tabela["categoria_km"] = pd.Categorical(
        tabela["categoria_km"],
        categories=ordem,
        ordered=True,
    )

    # Ordena a tabela seguindo a ordem definida
    tabela = (
        tabela
        .sort_values("categoria_km")
        .reset_index(drop=True)
    )

    return tabela


def tabela_ano_modelo(df):

    tabela = (
        df
        .groupby("ano_modelo")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            km_media=("quilometragem", "mean"),
            desconto_medio=("percentual_desconto", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="ano_modelo",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_lojas(df):

    tabela = (
        df
        .groupby("loja")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_cor(df):

    tabela = (
        df
        .groupby("cor")
        .agg(
            quantidade=("id", "count"),
            preco_medio=("preco", "mean"),
            km_media=("quilometragem", "mean"),
        )
        .reset_index()
        .round(2)
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def tabela_marca_categoria(df):

    tabela = (
        df
        .groupby(["marca", "categoria"])
        .agg(
            quantidade=("id", "count"),
        )
        .reset_index()
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return tabela


def salvar_tabelas_gold(df, nome_arquivo, engine):
    # Mantém o salvamento local em Parquet
    pasta = Path("data/gold")
    pasta.mkdir(parents=True, exist_ok=True)

    arquivo = pasta / f"{nome_arquivo}.parquet"

    df.to_parquet(
        arquivo,
        index=False,
    )

    print(f"\nArquivo Parquet salvo localmente: {arquivo}")
    print(f"Total de registros: {len(df)}")

    # Prepara uma cópia para o banco de dados para evitar corromper o Parquet
    df_para_banco = df.copy()

    # Percorre cada coluna para detectar e converter estruturas de dados complexas
    for coluna in df_para_banco.columns:
        # Puxa os valores não nulos para avaliar o tipo real dos dados armazenados
        valores_validos = df_para_banco[coluna].dropna()
        
        if not valores_validos.empty:
            # Se o primeiro valor da coluna for uma lista ou dicionário Python
            if isinstance(valores_validos.iloc[0], (dict, list)):
                # Converte os dados estruturados em uma string de texto puro formatada em JSON
                df_para_banco[coluna] = df_para_banco[coluna].apply(
                    lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x
                )

    # Envia o DataFrame diretamente como tabela para o Postgres
    # if_exists='replace' reconstrói a tabela a cada execução do pipeline
    df_para_banco.to_sql(
        name=nome_arquivo, 
        con=engine, 
        if_exists="replace", 
        index=False
    )

    print(f"Tabela '{nome_arquivo}' enviada com sucesso para o PostgreSQL!")