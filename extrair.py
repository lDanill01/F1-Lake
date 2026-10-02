#%% Importando Bibliotecas
import pandas as pd
import fastf1

# Configurando Visualizacao
pd.set_option('display.max_columns', None)

#%%

class CollectResults:
  
  def __init__(self, years=[2021, 2022, 2023], modes=["R", "S"]):
    self.years = years
    self.modes = modes
    
  def get_data(self, year, gp, mode)->pd.DataFrame:
      try:
        session = fastf1.get_session(year, gp, mode)
        
      except ValueError as err:
        return pd.DataFrame()
        
      session._load_drivers_results()
      return session.results
  
  def save_data(self, df, year, gp, mode):
    df.to_parquet(f'data/{year}_{gp:02}_{mode}.parquet')
    
  def process(self, year, gp, mode):
    df = self.get_data(year, gp, mode)
    if df.empty:
      return False
    
    self.save_data(df,year, gp, mode)
    return True
  
  def process_year_mode(self, year, mode):
    for i in range(1,50):
      if  not self.process(year, i, mode):
        break
    
#%%
collect = CollectResults([2021, 2022], ['R'])
collect.process_year_mode(2021,'R')    


# %%
