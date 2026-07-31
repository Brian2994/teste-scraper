from pprint import pprint
from collections import Counter
from src.silver.silver import ler_bronze, transformar_silver

# Carrega Bronze
dados_bronze = ler_bronze()

# Transforma para Silver
dados_silver = transformar_silver(dados_bronze)

print("-" * 50)
print("RESUMO")
print("-" * 50)
print(f"Bronze : {len(dados_bronze)}")
print(f"Silver : {len(dados_silver)}")

# Exibe o primeiro veículo tratado estruturado linha por linha
print("\nPrimeiro registro Silver")
print("-" * 50)
pprint(dados_silver[0], sort_dicts=False)

# Isola o primeiro carro em uma variável para validar
registro = dados_silver[0]

print("\n===== CAMPOS GERADOS =====")
# Lista todos os novos campos criados
campos = [
    "latitude",
    "longitude",
    "parcelas",
    "porcentagem_entrada",
    "coeficiente",
    "valor_parcela",
    "valor_entrada",
    "nome_veiculo",
    "qtd_caracteristicas",
    "qtd_promocoes",
    "idade_veiculo",
    "idade_fabricacao",
    "desconto",
    "economia_reais",
    "percentual_desconto",
    "abaixo_preco_0km",
    "faixa_preco",
    "faixa_desconto",
    "km_por_ano",
    "categoria_km",
    "regiao"
]

for campo in campos:
    print(f"{campo:25} -> {registro[campo]}")
print("============ FIM ============")

print("\n===== AMOSTRA DE VEÍCULOS (POSIÇÕES ESPECÍFICAS) =====\n")
print(f"{'POSIÇÃO':<8} | {'MARCA':<10} | {'MODELO':<12} | {'PREÇO':<13} | {'FAIXA PREÇO':<15} | {'CATEG KM':<8} | REGIAO")
print("-" * 85)
# Amostras aleatórias do estoque
for i in [0, 100, 500, 1000, 3000]:
    v = dados_silver[i]
    print(
        f"{i:8} | "
        f"{v['marca']:<10} | "
        f"{v['modelo']:<12} | "
        f"R$ {v['preco']:<10} | "
        f"{v['faixa_preco']:<15} | "
        f"{v['categoria_km']:<8} | "
        f"{v['regiao']}"
    )

print()
print("===== FIM =====\n")

# Contagem de quantos veículos falharam nas regras de validação (ficaram nulos)
print("Latitude nula:",
      sum(v["latitude"] is None for v in dados_silver))

print("Preço nulo:",
      sum(v["preco"] is None for v in dados_silver))

print("Região nula:",
      sum(v["regiao"] is None for v in dados_silver))

print("Percentual desconto nulo:",
      sum(v["percentual_desconto"] is None for v in dados_silver))

# Cria uma lista apenas com as chaves de identificação dos anúncios
ids = [v["id"] for v in dados_silver]

# Valida a integridade do banco de dados checando se existem anúncios duplicados no lote
print("\nIDs únicos:", len(set(ids)))
print("Duplicados:", len(ids) - len(set(ids)))

# Agrupa e conta o estoque por categorias comerciais para gerar relatórios de negócios
print(Counter(v["faixa_preco"] for v in dados_silver))
print(Counter(v["categoria_km"] for v in dados_silver))
print(Counter(v["faixa_desconto"] for v in dados_silver))