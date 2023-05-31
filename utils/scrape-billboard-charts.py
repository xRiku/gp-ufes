import time
from datetime import date, datetime, timedelta
import billboard
import pandas as pd


def scrape(last_date, max_date, output_file_name):
    curr_date = last_date
    max_chart_date = billboard.ChartData("hot-100", max_date).date
    while (
        curr_chart_date := (chart := billboard.ChartData("hot-100", curr_date)).date
    ) >= max_chart_date:
        allow_header = True if curr_date == last_date else False
        chart_entries = []
        # Itera sobre as músicas da semana
        for track in chart:
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
                    "date": chart.date,
                }
            )
        entries = pd.DataFrame(chart_entries)
        entries.to_csv(output_file_name, mode="a", index=False, header=allow_header)
        if curr_chart_date == max_chart_date:
            return
        # Decrementa uma semana a cada iteração
        curr_date -= timedelta(days=7)


def main():
    output_file_name = "billboard_db_definitive.csv"
    last_date = date.fromisoformat("2022-01-01")
    max_date = date.fromisoformat("1958-08-03")
    scrape(last_date, max_date, output_file_name)


if __name__ == "__main__":
    main()
