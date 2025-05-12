import pandas as pd
from scraper import scraper_function

# Carregar CSV com links e IDs
df_links = pd.read_csv('dados/ids_extraidos.csv')

# Iterar sobre os IDs (chaves de acesso)
n = len(df_links)
for i, chave in enumerate(df_links['id']):
    print(f"{i+1}/{n} - Processando chave: {chave}")
    try:
        produtos = scraper_function(chave)
    except Exception as e:
        print(f"Erro ao processar chave {chave}: {e}")
        produtos = None

    if produtos is None:
        print(f"Nota {chave} já processada ou erro.")
    elif produtos == []:
        print(f"Nenhum produto encontrado para {chave}.")
    else:
        print(f"{len(produtos)} produtos adicionados para a chave {chave}.")

print("Processamento finalizado.")
