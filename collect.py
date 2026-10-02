"""Coleta os resultados das corridas de F1 (1980-2026) usando FastF1.

Os resultados de cada corrida sao salvos em data/{ano}_{round:02}_{modo}.parquet.
Rodar o script de novo baixa apenas o que ainda nao existe (retomavel).
"""

from pathlib import Path

import fastf1

# --------------------------------------------------------------- Configuracao
START_YEAR = 1980
END_YEAR = 2026
MODES = ["R"]  # R = corrida. Para incluir Sprints (2021+) use ["R", "S"].

DATA_DIR = Path("data")
CACHE_DIR = Path("cache")


# ------------------------------------------------------------------ Coleta
def result_path(year, round_number, mode):
    """Caminho padrao de um arquivo de resultados."""
    return DATA_DIR / f"{year}_{round_number:02}_{mode}.parquet"


def get_results(year, round_number, mode):
    """Busca os resultados de uma sessao. Retorna None em caso de falha."""
    try:
        session = fastf1.get_session(year, round_number, mode)
        session._load_drivers_results()
        return session.results
    except Exception as error:
        print(f"    ! {year} R{round_number:02} {mode}: {error}")
        return None


def save_results(df, year, round_number, mode):
    """Grava os resultados em parquet."""
    path = result_path(year, round_number, mode)

    # Anos antigos vem indexados por DriverNumber, que colide com a coluna de
    # mesmo nome ao salvar. O indice e redundante, entao descartamos.
    df = df.reset_index(drop=True)

    df.to_parquet(path)
    return path


def collect_round(year, round_number, mode, event_name):
    """Coleta uma sessao. Pula se o arquivo ja existe. Retorna True se salvou."""
    path = result_path(year, round_number, mode)

    if path.exists():
        print(f"  = {year} R{round_number:02} {mode} ja existe, pulando")
        return False

    df = get_results(year, round_number, mode)
    if df is None or df.empty:
        return False

    save_results(df, year, round_number, mode)
    print(f"  + {year} R{round_number:02} {mode} ({event_name}) salvo")
    return True


def collect_year(year):
    """Coleta todas as corridas de um ano, usando o calendario oficial."""
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    print(f"\n=== {year}: {len(schedule)} eventos ===")

    for _, event in schedule.iterrows():
        round_number = int(event["RoundNumber"])
        for mode in MODES:
            collect_round(year, round_number, mode, event["EventName"])


# --------------------------------------------------------------------- Main
def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))

    for year in range(START_YEAR, END_YEAR + 1):
        try:
            collect_year(year)
        except Exception as error:
            print(f"  x ano {year} falhou por completo: {error}")


if __name__ == "__main__":
    main()
