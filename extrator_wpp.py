import pandas as pd
import re

# Ler o conteúdo do arquivo fornecido
with open('dados/links.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Regex corrigido para pegar /d/danfeNFCe e danfeNFCe
link_pattern = re.compile(r'https?://nfe\.sefaz\.go\.gov\.br/nfeweb/sites/nfce/(?:d/)?danfeNFCe\?p=([0-9]+)')

# Lista para armazenar os IDs
ids = []

# Extrair IDs
for line in lines:
    match = link_pattern.search(line)
    if match:
        nota_id = match.group(1)
        ids.append({'id': nota_id})

# Converter em DataFrame
df_ids = pd.DataFrame(ids)

# Salvar CSV
df_ids.to_csv('dados/ids_extraidos.csv', index=False)

print(f"IDs extraídos: {len(df_ids)}")
