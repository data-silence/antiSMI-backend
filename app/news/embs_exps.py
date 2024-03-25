from sqlalchemy import create_engine, text
import datetime as dt
from loguru import logger

import pandas as pd

import torch
from transformers import AutoTokenizer, AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")
model = AutoModel.from_pretrained("cointegrated/LaBSE-en-ru").to(device)

DB_USER = 'maxlethal'
DB_NAME = 'timemachine'
DB_PASS = "00Goelro00!"
DB_HOST = "38.242.140.206:5432"

timemachine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}', pool_pre_ping=True)


def make_single_embs(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].tolist()


def search_answer(query):
    answer = text(f"""select
        resume, date
    from news
    where url in
    (SELECT news_url FROM embs ORDER BY embedding <-> '{query}
    ' LIMIT 5)
    order by date""")
    with timemachine.begin() as conn:
        test_df = pd.read_sql_query(answer, conn)
    return test_df


def make_batch_embs(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings.tolist()


def start_making_embs():
    finish_date = dt.date(2023, 12, 31)
    current_date = dt.date(2023, 9, 19)
    delta = dt.timedelta(days=1)

    while current_date < finish_date:
        with timemachine.begin() as conn:
            query = text(f"""SELECT url, news from news where date::date = '{current_date}'""")
            test_df = pd.read_sql_query(query, conn).rename(columns={'url': 'news_url'})
            log_info = {current_date: len(test_df)}
            try:
                embs = make_batch_embs(test_df.news.tolist())
                test_df['embedding'] = embs
                test_df.drop(columns='news', inplace=True)
                test_df.to_sql(name='embs', con=conn, if_exists='append', index=False)
                logger.info(log_info)
            except Exception as e:
                logger.error(log_info)
        current_date += delta


date_tuple = ([dt.date(2023, 9, 19)],
              [dt.date(2023, 9, 20)],
              [dt.date(2023, 9, 21)],
              [dt.date(2023, 9, 22)],
              [dt.date(2023, 9, 25)],
              [dt.date(2023, 9, 26)],
              [dt.date(2023, 9, 27)],
              [dt.date(2023, 9, 28)],
              [dt.date(2023, 9, 29)],
              [dt.date(2023, 10, 3)],
              [dt.date(2023, 10, 4)],
              [dt.date(2023, 10, 5)],
              [dt.date(2023, 10, 6)],
              [dt.date(2023, 10, 9)],
              [dt.date(2023, 10, 10)],
              [dt.date(2023, 10, 11)],
              [dt.date(2023, 10, 12)],
              [dt.date(2023, 10, 13)],
              [dt.date(2023, 10, 16)],
              [dt.date(2023, 10, 17)],
              [dt.date(2023, 10, 18)],
              [dt.date(2023, 10, 19)],
              [dt.date(2023, 10, 20)],
              [dt.date(2023, 10, 23)],
              [dt.date(2023, 10, 24)],
              [dt.date(2023, 10, 25)],
              [dt.date(2023, 10, 26)],
              [dt.date(2023, 10, 27)],
              [dt.date(2023, 10, 30)],
              [dt.date(2023, 10, 31)],
              [dt.date(2023, 11, 1)],
              [dt.date(2023, 11, 2)],
              [dt.date(2023, 11, 3)],
              [dt.date(2023, 11, 7)],
              [dt.date(2023, 11, 8)],
              [dt.date(2023, 11, 9)],
              [dt.date(2023, 11, 10)],
              [dt.date(2023, 11, 13)],
              [dt.date(2023, 11, 14)],
              [dt.date(2023, 11, 15)],
              [dt.date(2023, 11, 16)],
              [dt.date(2023, 11, 17)],
              [dt.date(2023, 11, 20)],
              [dt.date(2023, 11, 21)],
              [dt.date(2023, 11, 22)],
              [dt.date(2023, 11, 23)],
              [dt.date(2023, 11, 24)],
              [dt.date(2023, 11, 27)],
              [dt.date(2023, 11, 28)],
              [dt.date(2023, 11, 29)],
              [dt.date(2023, 11, 30)],
              [dt.date(2023, 12, 1)],
              [dt.date(2023, 12, 4)],
              [dt.date(2023, 12, 5)],
              [dt.date(2023, 12, 6)],
              [dt.date(2023, 12, 7)],
              [dt.date(2023, 12, 8)],
              [dt.date(2023, 12, 11)],
              [dt.date(2023, 12, 12)],
              [dt.date(2023, 12, 13)],
              [dt.date(2023, 12, 14)],
              [dt.date(2023, 12, 15)],
              [dt.date(2023, 12, 18)],
              [dt.date(2023, 12, 19)],
              [dt.date(2023, 12, 20)],
              [dt.date(2023, 12, 21)],
              [dt.date(2023, 12, 22)],
              [dt.date(2023, 12, 25)],
              [dt.date(2023, 12, 26)],
              [dt.date(2023, 12, 27)],
              [dt.date(2023, 12, 28)],
              [dt.date(2023, 12, 29)],)


def finish_making_embs():
    with timemachine.begin() as conn:
        for current_date in date_tuple:
            query = text(f"""SELECT url, news from news where date::date = '{current_date[0]}'""")
            test_df = pd.read_sql_query(query, conn).rename(columns={'url': 'news_url'})
            log_info = {current_date[0]: len(test_df)}
            embs1 = make_batch_embs(test_df.news.iloc[:500].tolist())
            embs2 = make_batch_embs(test_df.news.iloc[500:].tolist())
            embs = embs1 + embs2
            test_df['embedding'] = embs
            test_df.drop(columns='news', inplace=True)
            test_df.to_sql(name='embs', con=conn, if_exists='append', index=False)

            logger.info(log_info)


if __name__ == '__main__':
    # start_making_embs()
    # finish_making_embs()
    # query = make_single_embs('Перспективы обслуживания внешнего долга РФ')
    # print(search_answer(query))
    print(make_single_embs('А я иду шагаю по Москве'))