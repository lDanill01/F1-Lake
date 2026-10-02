#%% Importando Bibliotecas
import pandas as pd
import fastf1

# Configurando Visualizacao
pd.set_option('display.max_columns', None)

#%%

for i in range(1,50):
    
  print(f'Coletando o GP{i}...')
    
  # Define a sessao de busca
  session = fastf1.get_session(2021, i, 'R')
  session._load_drivers_results()

  #Exibe e salva os dados obtidos
  session.results
  session.results.to_parquet(f'data/2021_{i:02}_R.parquet')
  print(session.results)
# %%
