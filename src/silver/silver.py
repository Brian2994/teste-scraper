from pathlib import Path
from datetime import datetime
import json

# Constantes
KM_BAIXA = 30000
KM_MEDIA = 80000
PRECO_BAIXO = 50000
PRECO_MEDIO = 80000
PRECO_ALTO = 120000
REGIOES = {
    "SP": "Sudeste",
    "RJ": "Sudeste",
    "MG": "Sudeste",
    "ES": "Sudeste",
    "PR": "Sul",
    "SC": "Sul",
    "RS": "Sul",
    "GO": "Centro-Oeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "DF": "Centro-Oeste",
    "BA": "Nordeste",
    "PE": "Nordeste",
    "CE": "Nordeste",
    "RN": "Nordeste",
    "PB": "Nordeste",
    "AL": "Nordeste",
    "SE": "Nordeste",
    "PI": "Nordeste",
    "MA": "Nordeste",
    "PA": "Norte",
    "AM": "Norte",
    "RO": "Norte",
    "RR": "Norte",
    "AC": "Norte",
    "AP": "Norte",
    "TO": "Norte",
}

def ler_bronze():
    pasta = Path("data/bronze")

    arquivos = sorted(
        pasta.glob("veiculos_*.json")
    )

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo Bronze encontrado.")

    arquivo = arquivos[-1]

    print(f"Lendo: {arquivo.name}")

    with open(arquivo, encoding="utf-8") as arquivo_json:
        dados = json.load(arquivo_json)

    print(f"Total de registros: {len(dados)}")

    return dados

def separar_localizacao(localizacao):
    if not localizacao:
        return None, None

    try:
        latitude, longitude = localizacao.split(",")
        return float(latitude), float(longitude)

    except Exception:
        return None, None

def para_float(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None

def transformar_silver(dados):

    dados_transformados = []

    # Capturar ano atual
    ano_atual = datetime.now().year

    for veiculo in dados:
        novo = veiculo.copy()

        # 1. Extração de objetos aninhados
        financiamento = novo.get("financiamento", {})

        novo["parcelas"] = financiamento.get("parcelas")

        novo["porcentagem_entrada"] = financiamento.get("porcentagem_entrada")

        novo["coeficiente"] = (
            float(financiamento["coeficiente"])
            if financiamento.get("coeficiente")
            else None
        )

        novo["valor_parcela"] = financiamento.get("valor_parcela")
        
        novo["valor_entrada"] = financiamento.get("valor_entrada")

        # remove o objeto
        novo.pop("financiamento", None)

        # 2. Conversões de tipos
        novo["preco"] = para_float(novo.get("preco"))

        novo["preco_0km"] = para_float(novo.get("preco_0km"))

        # validação
        if novo["preco"] is None or novo["preco_0km"] is None:
            print(
                f"Veículo {novo['id']} sem preço:",
                novo["preco"],
                novo["preco_0km"]
            )

        novo["dt_criacao"] = datetime.strptime(
            novo["dt_criacao"],
            "%Y-%m-%d %H:%M:%S"
        )

        novo["dt_atualizacao_elastic"] = datetime.fromisoformat(
            novo["dt_atualizacao_elastic"]
        )
        novo["data_coleta"] = datetime.strptime(
            novo["data_coleta"],
            "%Y-%m-%d %H:%M:%S"
        )

        # 3. Padronização
        novo["cidade"] = novo["cidade"].upper()
        novo["marca"] = novo["marca"].title()

        # 4. Enriquecimento (latitude/longitude)
        latitude, longitude = separar_localizacao(
            novo.get("localizacao")
        )

        novo["latitude"] = latitude
        novo["longitude"] = longitude

        # remove o objeto
        novo.pop("localizacao", None)

        # 5. Colunas derivadas
        novo["nome_veiculo"] = (            
            f"{novo['marca']} "
            f"{novo['modelo']} "
            f"{novo['versao']}"
        )

        novo["qtd_caracteristicas"] = len(
            novo["caracteristicas"] or []
        )

        novo["qtd_promocoes"] = len(
            novo["promocoes"] or []
        )

        # 6. Indicadores
        novo["idade_veiculo"] = (
            ano_atual - novo["ano_modelo"]
        )

        novo["idade_fabricacao"] = (
            ano_atual - novo["ano_fabricacao"]
        )

        # Regra de Negócio: Cálculo de desconto e percentual
        novo["desconto"] = None
        novo["economia_reais"] = None
        novo["percentual_desconto"] = None

        if (
            novo["preco"] is not None
            and novo["preco_0km"] not in (None, 0)
        ):

            desconto = novo["preco_0km"] - novo["preco"]

            novo["desconto"] = round(desconto, 2)
            novo["economia_reais"] = round(desconto, 2)

            novo["percentual_desconto"] = round(
                desconto / novo["preco_0km"] * 100,
                2
            )

        percentual = novo["percentual_desconto"]

        # Regra de Negócio: Média de quilômetros rodados por ano
        if (
            novo["idade_veiculo"] > 0
            and novo.get("quilometragem") is not None
        ):
            novo["km_por_ano"] = round(
                novo["quilometragem"]
                / novo["idade_veiculo"],
                2
            )
            
        else:
            novo["km_por_ano"] = None

        # 7. Flags
        if novo["preco"] is not None and novo["preco_0km"] is not None:
            # Indicador lógico (True ou False) se o usado é mais barato que o 0km
            novo["abaixo_preco_0km"] = (
                novo["preco"] < novo["preco_0km"]
            )

        else:
            novo["abaixo_preco_0km"] = None

        # 8. Categorizações
        if novo["preco"] is None:
            novo["faixa_preco"] = None

        elif novo["preco"] < PRECO_BAIXO:
            novo["faixa_preco"] = "Até 50 mil"

        elif novo["preco"] < PRECO_MEDIO:
            novo["faixa_preco"] = "50 a 80 mil"

        elif novo["preco"] < PRECO_ALTO:
            novo["faixa_preco"] = "80 a 120 mil"

        else:
            novo["faixa_preco"] = "Acima de 120 mil"

        # Classifica a qualidade do desconto em faixas (Excelente, Boa, Pequena)
        if percentual is None:
            novo["faixa_desconto"] = None

        elif percentual >= 25:
            novo["faixa_desconto"] = "Excelente"

        elif percentual >= 15:
            novo["faixa_desconto"] = "Boa"

        elif percentual >= 5:
            novo["faixa_desconto"] = "Pequena"

        else:
            novo["faixa_desconto"] = "Sem desconto"

        # Categoriza o desgaste do veículo com base na quilometragem (Baixa, Média ou Alta)
        km = novo.get("quilometragem")

        if km is None:
            novo["categoria_km"] = None

        elif km < KM_BAIXA:
            novo["categoria_km"] = "Baixa"

        elif km < KM_MEDIA:
            novo["categoria_km"] = "Média"

        else:
            novo["categoria_km"] = "Alta"

        # 9. Região
        novo["regiao"] = REGIOES.get(novo["uf"])

        dados_transformados.append(novo)

    return dados_transformados