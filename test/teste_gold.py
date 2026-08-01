from src.silver.silver import ler_bronze, transformar_silver
from src.gold.gold import criar_dataframe, resumo_geral, tabela_marcas, tabela_regioes, tabela_estados, tabela_categorias, tabela_faixa_preco, tabela_modelos, tabela_combustivel, tabela_transmissao, tabela_descontos, tabela_categoria_km, tabela_ano_modelo, tabela_lojas, tabela_cor, tabela_marca_categoria, salvar_tabelas_gold

# Carrega Bronze
dados_bronze = ler_bronze()

# Transforma para Silver
dados_silver = transformar_silver(dados_bronze)

df = criar_dataframe(dados_silver)

print("-" * 80)
print("DATAFRAME GOLD")
print("-" * 80)

print(df.head(10))

print("\nQuantidade de linhas:", len(df))
print("Quantidade de colunas:", len(df.columns))
print()

df.info()

# Conta quantos registros possuem alguma imagem dentro da lista de incentivos
total_img_incentivos = sum(
    len(v.get("incentivos") or []) > 0 
    and (v.get("incentivos")[0].get("img") is not None)
    for v in dados_silver
)

print("\n===== CONFIRMAÇÃO RÁPIDA DE IMAGENS =====")
print(f"Imagens principais (Camada Silver)        : {df['img'].notna().sum()}")
print(f"Imagens escondidas dentro de Incentivos   : {total_img_incentivos}")
print(f"Soma total de qualquer imagem disponível  : {df['img'].notna().sum() + total_img_incentivos}")

# Filtra apenas as linhas do DataFrame onde a imagem principal está em branco
anuncios_sem_img = df[df["img"].isna()]

print("\n" + "=" * 60)
print(f"ANÚNCIOS SEM IMAGEM PRINCIPAL: {len(anuncios_sem_img)} VEÍCULOS")
print("=" * 60)

# Exibe as informações essenciais dos 10 primeiros veículos sem imagem para análise
print(anuncios_sem_img[["id", "marca", "modelo", "loja", "combustivel", "fonte"]].head(10))

# Filtra os veículos que não possuem a imagem principal
print("\n" + "=" * 60)
print("AUDITORIA DETALHADA: PRIMEIRO VEÍCULO SEM FOTO REAL")
print("=" * 60)

if not anuncios_sem_img.empty:
    # Captura a linha (.iloc) dos anúncios que estão sem imagem
    primeiro_sem_foto = anuncios_sem_img.iloc[0] # inidice 0

    # Verifica se a palavra 'Ar condicionado' está na lista de características do carro
    lista_caracteristicas = primeiro_sem_foto.get("caracteristicas") or []
    tem_ar = "Sim" if "Ar condicionado" in lista_caracteristicas else "Não"
    
    # Extrai os dados necessários para montar a URL dinâmica no padrão do site
    categoria = primeiro_sem_foto.get("categoria", "Hatch")
    marca = primeiro_sem_foto.get("marca", "Renault")
    modelo = primeiro_sem_foto.get("modelo", "Kwid")
    id_veiculo = primeiro_sem_foto.get("id")

    # Monta o link oficial de detalhes exatamente no novo padrão informado
    link_anuncio = f"https://www.seminovosmovida.com.br/veiculo/detalhe/{categoria}/{marca}/{modelo}/{id_veiculo}"
    
    # Imprime a ficha técnica completa solicitada de forma limpa e organizada
    print(f"ID              : {primeiro_sem_foto['id']}")
    print(f"MARCA           : {primeiro_sem_foto['marca']}")
    print(f"MODELO          : {primeiro_sem_foto['modelo']}")
    print(f"VERSAO          : {primeiro_sem_foto['versao']}")
    print(f"LOJA            : {primeiro_sem_foto['loja']}")
    print(f"PREÇO           : R$ {primeiro_sem_foto['preco']}")
    print(f"KM              : {primeiro_sem_foto['quilometragem']:,}".replace(",", "."))
    print(f"ANO             : {primeiro_sem_foto['ano_modelo']}")
    print(f"COMBUSTÍVEL     : {primeiro_sem_foto['combustivel']}")
    print(f"COR             : {primeiro_sem_foto['cor']}")
    print(f"CÂMBIO          : {primeiro_sem_foto['transmissao']}")
    print(f"PORTAS          : {primeiro_sem_foto['portas']}")
    print(f"AR-CONDICIONADO : {tem_ar}")
    print(f"LINK DO ANÚNCIO : {link_anuncio}")
    print(f"FONTE           : {primeiro_sem_foto['fonte']}")
else:
    print("Nenhum veículo sem imagem foi encontrado neste lote!")

print("\nRESUMO GERAL - KPIS")
print("-" * 50)

# RESUMO GERAL
df_resumo = resumo_geral(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - RESUMO GERAL KPIS")
print("=" * 80)

print(df_resumo)


# RESUMO TABELA MARCAS
df_marcas = tabela_marcas(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - MARCAS")
print("=" * 80)

print(df_marcas)

# RESUMO TABELA REGIOES
df_regioes = tabela_regioes(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - REGIOES")
print("=" * 80)

print(df_regioes)

# RESUMO TABELA ESTADOS
df_estados = tabela_estados(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - ESTADOS")
print("=" * 80)

print(df_estados)

# RESUMO TABELA CATEGORIAS
df_categorias = tabela_categorias(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - CATEGORIAS")
print("=" * 80)

print(df_categorias)

# RESUMO TABELA FAIXA DE PREÇO
df_faixa_preco = tabela_faixa_preco(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - FAIXA DE PREÇO")
print("=" * 80)

print(df_faixa_preco)

# RESUMO TABELA MODELOS
df_modelos = tabela_modelos(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - MODELOS")
print("=" * 80)

print(df_modelos)

# RESUMO TABELA COMBUSTÍVEL
df_combustivel = tabela_combustivel(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - COMBUSTÍVEL")
print("=" * 80)

print(df_combustivel)

# RESUMO TABELA TRANSMISSÃO
df_transmissao = tabela_transmissao(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - TRANSMISSÃO")
print("=" * 80)

print(df_transmissao)

# RESUMO TABELA DESCONTOS
df_descontos = tabela_descontos(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - DESCONTOS")
print("=" * 80)

print(df_descontos)

# RESUMO TABELA CATEGORIA KM
df_categoria_km = tabela_categoria_km(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - CATEGORIA DE KM")
print("=" * 80)

print(df_categoria_km)

# RESUMO TABELA ANO MODELO
df_ano_modelo = tabela_ano_modelo(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - ANO MODELO")
print("=" * 80)

print(df_ano_modelo)

# RESUMO TABELA LOJAS
df_lojas = tabela_lojas(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - LOJAS")
print("=" * 80)

print(df_lojas)

# RESUMO TABELA COR
df_cor = tabela_cor(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - CORES")
print("=" * 80)

print(df_cor)

# RESUMO TABELA MARCA x CATEGORIA
df_marca_categoria = tabela_marca_categoria(df)

print("\n")
print("=" * 80)
print("TABELA ANALÍTICA - MARCA x CATEGORIA")
print("=" * 80)

print(df_marca_categoria)

# SALVA TABELAS
print("\n")
print("=" * 80)
print("SALVANDO TABELAS GOLD")
print("=" * 80)

# DataFrame principal
salvar_tabelas_gold(
    df,
    "fato_veiculos",
)

salvar_tabelas_gold(
    df_resumo,
    "kpi_resumo_geral",
)

# Tabelas analíticas
salvar_tabelas_gold(
    df_marcas,
    "dim_marcas",
)

salvar_tabelas_gold(
    df_regioes,
    "dim_regioes",
)

salvar_tabelas_gold(
    df_estados,
    "dim_estados",
)

salvar_tabelas_gold(
    df_categorias,
    "dim_categorias",
)

salvar_tabelas_gold(
    df_faixa_preco,
    "dim_faixa_preco",
)

salvar_tabelas_gold(
    df_modelos,
    "dim_modelos",
)

salvar_tabelas_gold(
    df_combustivel,
    "dim_combustivel",
)

salvar_tabelas_gold(
    df_transmissao,
    "dim_transmissao",
)

salvar_tabelas_gold(
    df_descontos,
    "dim_faixa_desconto",
)

salvar_tabelas_gold(
    df_categoria_km,
    "dim_categoria_km",
)

salvar_tabelas_gold(
    df_ano_modelo,
    "dim_ano_modelo",
)

salvar_tabelas_gold(
    df_lojas,
    "dim_lojas",
)

salvar_tabelas_gold(
    df_cor,
    "dim_cor",
)

salvar_tabelas_gold(
    df_marca_categoria,
    "dim_marca_categoria",
)

print("\nPipeline Gold finalizada com sucesso!")