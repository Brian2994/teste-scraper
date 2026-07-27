import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Carrega as variáveis do arquivo .env
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
SEARCH_URL = os.getenv("SEARCH_URL")

with sync_playwright() as p:
    print("Iniciando Playwright...")

    # Abrindo o navegador
    browser = p.chromium.launch(headless=False)    
    # Nova aba
    page = browser.new_page()

    # Acessando o site
    print(f"Acessando: {SEARCH_URL}")
    page.goto(SEARCH_URL)

    # wait_for_timeout() espera um tempo fixo, mesmo que a página já tenha carregado.
    # wait_for_selector() espera apenas até que os anúncios existam na página.
    page.wait_for_selector(".car")
    
    print("Página carregada!")

    cards = page.locator(".car")

    print(f"Foram encontrados {cards.count()} anúncios.")

    # extrair tudo do primeiro carro
    primeiro_carro = cards.nth(0)
    titulo = primeiro_carro.locator(".info__title").inner_text()
    versao = primeiro_carro.locator(".info__subtitle").inner_text()
    dados = primeiro_carro.locator(".add__info").inner_text()

    ano, quilometragem, cidade = [
        item.strip()
        for item in dados.split("•")
    ]

    preco_antigo = primeiro_carro.locator(".price-24").inner_text()
    preco_atual = primeiro_carro.locator(".price-30").inner_text()
    imagem = primeiro_carro.locator(".vehicle-img").get_attribute("src")
    link = primeiro_carro.locator("a").get_attribute("href")
    url_completo = BASE_URL + link

    print("Título:", titulo)
    print("Versão:", versao)
    print("Dados:", dados)
    print("Ano:", ano)
    print("KM:", quilometragem)
    print("Cidade:", cidade)
    print("Preço antigo:", preco_antigo)
    print("Preço atual:", preco_atual)
    print("Imagem:", imagem)
    print("Link:", url_completo)

    input("\nPressione ENTER para fechar...")

    browser.close()

print("Navegador encerrado.")