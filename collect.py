#%% 
import fastf1
import pandas as pd
from pathlib import Path


#%%

class CollectResults:
        
        def __init__(self, years=[2021, 2022, 2023], modes=['R', 'S']):
                self.years = years
                self.modes = modes
        
        def get_data(self, year, gp, mode) ->pd.DataFrame:
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
                
                self.save_data(df, year, gp, mode)
                return True
        
        def process_year_modes(self, year):
                for i in range(1,50):
                    for mode in self.modes:
                        if not self.process(year, i, mode) and mode == 'R':
                                return
                        
        def process_years(self):
                for year in self.years:
                        self.process_year_modes(year)
                        
#%%

collect = CollectResults([2021, 2022, 2023], ['R', 'S'])
collect.process_years()


#%% Carregando as corridas

data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

for year in range(1990, 2027):
        schedule = fastf1.get_event_schedule(year, include_testing=False)

        for _, event in schedule.iterrows():
                round_number = int(event["RoundNumber"])
                try:
                        session = fastf1.get_session(year, round_number, "R")
                        session._load_drivers_results()
                        print(f"Results for {year} round {round_number} ({event['EventName']}):")
                        print(session.results)

                        session.results.to_parquet(
                                data_dir / f"results_{year}_{round_number}.parquet"
                        )
                except Exception as error:
                        print(
                                f"Could not collect {year} round {round_number} "
                                f"({event['EventName']}): {error}"
                        )
