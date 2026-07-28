import os
from dotenv import load_dotenv
import requests

load_dotenv()

URL = os.getenv("URL")
tamanhos_para_testar = [50, 100, 200, 500, 1000]

print("🚀 Iniciando teste de limite da API...")

for tamanho in tamanhos_para_testar:
    payload = {
        "from": "0",
        "size": tamanho,
        "localizacao": {"latitude": None, "longitude": None, "uf": None}
    }
    
    try:
        r = requests.post(URL, json=payload, timeout=10)
        
        if r.status_code == 200:
            dados = r.json().get("data", [])
            print(f"🟢 size={tamanho}: Funcionou! Retornou {len(dados)} carros.")
            
            if tamanho > 20 and len(dados) == 20:
                print("⚠️ A API ignorou o tamanho e fixou o padrão de 20 carros.")
                break
        else:
            print(f"🔴 size={tamanho}: Falhou com status {r.status_code}.")
            break
            
    except Exception as e:
        print(f"💥 size={tamanho}: Erro na conexão ({e}).")
        break

print("\n🏁 Teste finalizado!")
