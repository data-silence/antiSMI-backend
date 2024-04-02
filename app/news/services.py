from datetime import datetime
import pandas as pd
import json
import requests
from io import StringIO
import datetime as dt
from sklearn.cluster import AgglomerativeClustering
from dataclasses import dataclass, field
from collections import Counter
import numpy as np
from numpy.linalg import norm
from app.news.embs_exps import make_single_embs

api_url = "http://127.0.0.1:8000"
default_day = dt.date(year=2014, month=2, day=22)
default_categories = ['society', 'economy', 'technology', 'entertainment', 'science', 'sports']


def get_time_period(start_date: datetime.date = datetime.now(),
                    end_date: datetime.date = None) -> tuple:  # + timedelta(hours=3)
    if end_date is None:
        end_date = start_date

    start = datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=00, minute=00)
    end = datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=23, minute=59)
    one_day = dt.timedelta(days=1)

    if start_date == datetime.today():
        if start_date.hour in range(0, 10):
            start = start.replace(hour=20, minute=56) - one_day
            end = end.replace(hour=22, minute=55) - one_day
        if start_date.hour in range(10, 14):
            start = start.replace(hour=22, minute=56) - one_day
            end = end.replace(hour=8, minute=55)
        if start_date.hour in range(14, 18):
            start = start.replace(hour=8, minute=56)
            end = end.replace(hour=12, minute=55)
        if start_date.hour in range(18, 22):
            start = start.replace(hour=12, minute=56)
            end = end.replace(hour=16, minute=55)
        if start_date.hour in range(22, 24):
            start = start.replace(hour=16, minute=56)
            end = end.replace(hour=20, minute=55)

    return start, end


def get_date_df_from_handler(date: dt.date) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}/news/tm/{str(date)}"
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


def get_clusters_columns(date: dt.date) -> pd.DataFrame:
    df = get_date_df_from_handler(date)

    if len(df) > 1:  # кластеризацию возможно сделать только если количество новостей более одной
        model = AgglomerativeClustering(n_clusters=None, metric='cosine', linkage='complete',
                                        distance_threshold=0.3)
        labels = model.fit_predict(list(df.embedding))
        df.loc[:, 'label'] = labels

    elif len(df) == 1:  # если новость одна - присваиваем ей лейбл = -1
        df.loc[:, 'label'] = -1
    # чтобы избежать отнесения одной новости по разным категориям, присвоим одному лейблу наиболее частую категорию,
    trans = df.groupby(by=['label'])['category'].agg(pd.Series.mode)
    df['new'] = df.label.apply(lambda x: trans.iloc[x])
    # Оставляем только одно значение, если мода выдаёт несколько значений в np.ndarray
    df.loc[:, 'new'] = df.new.apply(lambda x: x[0] if isinstance(x, np.ndarray) else x)

    # Удаляем вспомогательные столбцы и сортируем
    df.drop(columns='category', inplace=True)
    df.rename(columns={'new': 'category'}, inplace=True)
    df.sort_values(by=['category', 'label'], ascending=True, inplace=True)

    return df


def filter_df(df: pd.DataFrame, amount: int = 3, categories: list = ['society', 'technology', 'sport']) -> pd.DataFrame:
    df = df.loc[df['category'].isin(categories)]
    final_labels = []
    for category in categories:
        most_tuple = Counter(list(df.label[df.category == category])).most_common(amount)
        most_labels = [el[0] for el in most_tuple]
        final_labels.extend(most_labels)
    return df[df.label.isin(final_labels)]


def cos_simularity(a, b):
    cos_sim = np.dot(a, b) / (norm(a) * norm(b))
    return cos_sim


def find_sim_news(df: pd.DataFrame, q_emb: list[float]):
    df.loc[:, 'sim'] = df['embedding'].apply(lambda x: cos_simularity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result


@dataclass
class NewsService:
    date: dt.date = default_day
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.categories = default_categories
        self.date_df = get_clusters_columns(date=self.date)
        self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def set_news_amount(self, news_amount: int):
        self.news_amount = news_amount
        self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def set_categories(self, categories: list[str]):
        self.categories = categories
        self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def set_date_df(self, date: dt.date):
        self.date = date
        self.date_df = get_clusters_columns(date=self.date)
        self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def get_source_links(self, title: str):
        cluster = self.most_df.label[self.most_df.title == title].iloc[0]

        links_set = set()
        links = self.most_df['links'][self.most_df.label == cluster].tolist()
        urls = self.most_df['url'][self.most_df.label == cluster].tolist()
        for group in links:
            group = group.split(',')
            links_set.update(group)
        links_set.update(urls)
        return ' '.join(list(links_set))

    def leave_me_alone(self) -> pd.DataFrame:
        unique_labels = set(self.most_df.label.tolist())
        url_final_list = []
        for label in unique_labels:
            avg_emb = np.array(list(self.most_df.embedding[self.most_df.label == label])).mean(axis=0)
            best_url = find_sim_news(self.most_df, avg_emb).url.index[0]
            url_final_list.append(best_url)
        final_df = self.most_df[self.most_df.index.isin(url_final_list)].drop(columns=['sim', 'embedding', 'label'])
        final_df.links = final_df.title.apply(lambda x: self.get_source_links(x))
        return final_df


def get_today_emb():
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}/news/asmi/today/brief"
    response = requests.get(handler_url).json()
    # print(response)
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    df['embedding'] = df['news'].apply(lambda x: make_single_embs(x))
    emb_news_dict = df.to_dict(orient='records')
    return emb_news_dict


if __name__ == "__main__":
    pass
    # df = get_today_emb()
    # print(df.head())
    # print(get_time_period())
    # print(dt.datetime.now() - start)
