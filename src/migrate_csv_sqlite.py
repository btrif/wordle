#  Created by btrif Trif on 09-03-2023 , 11:59 AM.
import os
import sqlite3

import pandas as pd

from database import DB_URL
from models import WordleModel, OxfordEnglishModel


def read_CSV_into_pandas():
    # Step 1: Load data CSV file
    with open("../data/english Dictionary.csv", 'r') as csv_file:
        df = pd.read_csv(csv_file)

        # Step 2 : Data clean-up
        df.columns = df.columns.str.strip()

        # Uncapitalize words :
        df['word'] = df['word'].str.lower()

        columns = ["word", "part_of_speech", "definition"]
        df.columns = columns

        print(df)
    return df


def read_and_process_text_file_into_pandas():
    with open('../data/5-letter-words.txt') as text_file:
        words = text_file.read().split('\n')
        # print(words)

        # data_frame = pd.read_csv(text_file, header=None)
        # data_frame = pd.DataFrame(zip(range(1, len(words) + 1), words))
        data_frame = pd.DataFrame(words, columns=["word"])

        # data_frame.insert(1, 'New_ID', range(1, 1 + len(data_frame)))
        print(data_frame)
    return data_frame


if __name__ == '__main__':
    print(os.getcwd())

    text_dataframe = read_and_process_text_file_into_pandas()

    csv_dataframe = read_CSV_into_pandas()

    if os.path.isfile(DB_URL):
        raise Exception("\033[91m  Database table already exists")

    # Step 3 : Create a connection to a SQLite database
    db_conn = sqlite3.connect(DB_URL)

    with db_conn:
        # Step 4 : Load data to SQLite3
        text_dataframe.to_sql(
            name="wordle",
            schema="dbo",
            con=db_conn,
            index_label='id'
            )

        csv_dataframe.to_sql(
                name="oxford_english",
                schema="dbo",
                con=db_conn,
                index_label='id'
                )
