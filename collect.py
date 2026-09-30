#%% 
import fastf1
import pandas as pd
from pathlib import Path

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
        

# %%
