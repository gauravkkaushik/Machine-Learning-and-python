from sqlite3 import connect
import pandas as pd
from pathlib import Path

cwd = Path(__file__).parent
db = cwd / 'romeo_and_juliet.db'

def query(function):

    def wrapper(*args, **kwargs):
        conn = connect(db)
        sql = function(*args, **kwargs)
        return pd.read_sql(sql, conn)

    return wrapper

def remove_punctuation(function):

    def wrapper(*args, **kwargs):
        import string

        df = function(*args, **kwargs)
        df['word'] = df.word.apply(
            lambda x: x.translate(
                str.maketrans('', '',
                string.punctuation)
                )
            )

        df = df.groupby('word').sum().reset_index()

        return df
    
    return wrapper

def remove_stopwords(function):

    def wrapper(*args, **kwargs):
        from src.stopwords import stopwords

        df = function(*args, **kwargs)
        return df[~df.word.isin(stopwords)]
    
    return wrapper
