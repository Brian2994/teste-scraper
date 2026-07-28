import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

def obter_texto(locator):
    try:
        return locator.inner_text()
    except:
        return None

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

    print("\nCarregando todos os anúncios...")
    quantidade_anterior = 0
    while True:            
        cards = page.locator(".car")
        quantidade_atual = cards.count()            
        print(f"Veículos carregados: {quantidade_atual}")

        if quantidade_atual == quantidade_anterior:
            print("\nTodos os anúncios foram carregados!")
            break

        quantidade_anterior = quantidade_atual

        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(2000)

    # cards = page.locator(".car")

    # print(f"Foram encontrados {cards.count()} anúncios.")

    # veiculos = []

    # # extrair tudo do primeiro carro
    # for i in range(cards.count()):
    #     carro = cards.nth(i)
    #     print(f"\nProcessando veículo {i+1}/{cards.count()}")

    #     titulo = obter_texto(carro.locator(".info__title"))
    #     versao = obter_texto(carro.locator(".info__subtitle"))
    #     dados = obter_texto(carro.locator(".add__info"))

    #     ano, quilometragem, cidade = [
    #         item.strip()
    #         for item in dados.split("•")
    #     ]

    #     preco_antigo = obter_texto(carro.locator(".price-24"))
    #     preco_atual = obter_texto(carro.locator(".price-30"))
    #     imagem = carro.locator(".vehicle-img").get_attribute("src")
    #     link = carro.locator("a").get_attribute("href")
    #     url_completo = BASE_URL + link

    #     print("Título:", titulo)
    #     print("Versão:", versao)
    #     print("Dados:", dados)
    #     print("Ano:", ano)
    #     print("KM:", quilometragem)
    #     print("Cidade:", cidade)
    #     print("Preço antigo:", preco_antigo)
    #     print("Preço atual:", preco_atual)
    #     print("Imagem:", imagem)
    #     print("Link:", url_completo)

    #     veiculo = {
    #     "titulo": titulo,
    #     "versao": versao,
    #     "ano": ano,
    #     "quilometragem": quilometragem,
    #     "cidade": cidade,
    #     "preco_antigo": preco_antigo,
    #     "preco_atual": preco_atual,
    #     "imagem": imagem,
    #     "url": url_completo
    #     }

    #     veiculos.append(veiculo)
    #     print(f"✓ {titulo}")

    # print("\n=================================")
    # print(f"Total coletado: {len(veiculos)}")
    # print("\nPrimeiro veículo:")
    # print(veiculos[0])

    input("\nPressione ENTER para fechar...")

    browser.close()

print("Navegador encerrado.")