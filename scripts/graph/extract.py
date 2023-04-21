import pandas as pd


def extract_micro_csv(ident, kvs_type, csv_name):
    df = pd.read_csv(csv_name)
    lines = df[
        (df["IDENT"] == ident) & (df["ARGS"].str.startswith(f"{kvs_type}:read_single"))
    ]
    read_single = {
        "x": lines["ARGS"].str.split(":", expand=True)[2],
        "y": lines["MEDIAN"],
        "y_err": [lines["MEDIAN"] - lines["P25"], lines["P95"] - lines["MEDIAN"]],
        "x_label": "Array size",
        "y_label": "Median",
        "title": f"Median over size for {ident} Data",
    }
    lines = df[
        (df["IDENT"] == ident)
        & (df["ARGS"].str.startswith(f"{kvs_type}:update_single"))
    ]
    update_single = {
        "x": lines["ARGS"].str.split(":", expand=True)[2],
        "y": lines["MEDIAN"],
        "y_err": [lines["MEDIAN"] - lines["P25"], lines["P95"] - lines["MEDIAN"]],
        "x_label": "Array size",
        "y_label": "Median",
        "title": f"Median over size for {ident} Data",
    }
    return read_single, update_single


def extract_list_traversal_csv(ident, kvs_type, csv_name):
    df = pd.read_csv(csv_name)
    lines = df[(df["IDENT"] == ident) & (df["ARGS"].str.startswith(f"{kvs_type}"))]
    data = {
        "x": lines["ARGS"].str.split(":", expand=True)[1],
        "y": lines["MEDIAN"],
        "y_err": [lines["MEDIAN"] - lines["P25"], lines["P95"] - lines["MEDIAN"]],
        "x_label": "Depth",
        "y_label": "Median",
        "title": f"Median over size for {ident} Data",
    }
    return data
