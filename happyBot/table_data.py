import pandas

def read_table():
    df = pandas.read_csv("table.csv")
    return df

def write_csv(df):
    df.to_csv("table.csv",index=False)
