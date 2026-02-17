# preprocess_data.py

import pandas as pd
import numpy as np


def load_data(path):
    df = pd.read_csv(path)
    print("Dataset Loaded")
    return df


def clean_data(df):

    print("Cleaning started...")

    # Remove missing IDs
    df.dropna(subset=["User's ID", "ProdID"], inplace=True)

    # Convert IDs to numeric
    df["User's ID"] = pd.to_numeric(df["User's ID"], errors='coerce')
    df["ProdID"] = pd.to_numeric(df["ProdID"], errors='coerce')

    # Drop invalid rows again
    df.dropna(subset=["User's ID", "ProdID"], inplace=True)

    # Convert to integer
    df["User's ID"] = df["User's ID"].astype("int64")
    df["ProdID"] = df["ProdID"].astype("int64")

    # Fill text columns
    text_cols = ["Category", "Brand", "Description", "Tags"]
    for col in text_cols:
        df[col] = df[col].fillna("")

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    print("Cleaning completed ✅")
    return df


def create_user_item_matrix(df):

    matrix = df.pivot_table(
        index="User's ID",
        columns="ProdID",
        values="Rating"
    )

    print("User-Item Matrix Created")
    print("Shape:", matrix.shape)

    return matrix


if __name__ == "__main__":

    data = load_data("clean_data.csv")

    cleaned = clean_data(data)

    user_item_matrix = create_user_item_matrix(cleaned)

    cleaned.to_csv("cleaned_data.csv", index=False)

    print("Saved cleaned_data.csv")
