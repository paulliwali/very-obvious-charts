import os

import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns
from gender_guesser.detector import Detector

from constants import COLORS, DATA_RAW_DIR, KAGGLE_DATA_DIR, REPORT_DIR

if __name__ == "__main__":
    plt.style.use("Solarize_Light2")
    sns.set_palette(COLORS)

    nba_player_df = pl.read_csv(
        os.path.join(
            DATA_RAW_DIR, KAGGLE_DATA_DIR, "nba-players-2023", "player_stats.csv"
        )
    )
    nba_player_df = nba_player_df.with_columns(
        pl.col("PName").str.split(" ").list.get(0).alias("first_name")
    )
    gender_detector = Detector()

    nba_player_df = nba_player_df.with_columns(
        pl.col("first_name")
        .map_elements(lambda x: gender_detector.get_gender(x))
        .alias("gender")
    )

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    sns.histplot(x=nba_player_df["gender"], ax=ax)
    fig.suptitle("Nba Player's gender guessed based on first name")
    ax.tick_params(axis="x", labelrotation=30)
    ax.set_ylabel("Number of Players")
    ax.set_xlabel("Gender guessed")

    fig.tight_layout()
    fig.savefig(os.path.join(REPORT_DIR, "nba-player-gender-guess.png"))
