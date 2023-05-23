import time
from datetime import date, datetime, timedelta
import billboard
import pandas as pd


def scrape(last_date, max_date):
    # Começa a calcular o tempo utilizado
    start_time = time.time()
    curr_date = last_date
    chart_entries = []
    while curr_date >= max_date:
        nc = billboard.ChartData("hot-100", curr_date)

        for track in nc:
            # Tratamento para designar o principal artista
            artist_list = track.artist.split(" ")
            main_artist = artist_list[0]
            if len(artist_list) > 1:
                # Só pegar até o 3 nome para não ficar muito grande
                for name in artist_list[1:]:
                    if (
                        name.lower() not in ("featuring", "&", "and")
                        and "(" not in name
                    ):
                        main_artist += " " + name
                    else:
                        break
            chart_entries.append(
                {
                    "name": track.title,
                    "artist": main_artist,
                    "rank": track.rank,
                    "weeks": track.weeks,
                }
            )
        # Decrementa uma semana a cada iteração
        curr_date -= timedelta(days=7)

    # Termina de calcular o tempo gasto
    time_diff = time.time() - start_time
    print(f"Scrapping time: {time_diff:.2f}s")
    return chart_entries


def main():
    last_date = date.fromisoformat("2022-01-01")
    max_date = date.fromisoformat("2021-12-01")
    chart_entries = scrape(last_date, max_date)
    # print(chart_entries)
    entries = pd.DataFrame(chart_entries)
    # print(entries)
    entries.to_csv("billboard_db2.csv", index=False)


if __name__ == "__main__":
    main()
