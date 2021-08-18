from flask import session
from dataclasses import field, dataclass
from typing import List, Dict, Optional
from gensim.models.word2vec import Word2Vec
import json

@dataclass
class SimilarNovel:
    title: str
    score: float


novel2vec: Word2Vec = Word2Vec.load(
    'novel2vec_skipgram_gensim4_100dim.model')


class Novel2VecWrapper:
    def to_json(self) -> str:
        return json.dumps({
            'positivie_titles':self.positive_titles,
            'negative_titles':self.negative_titles,
            'unknown_titles': self.unknown_titles
        })

    @staticmethod
    def from_json(json_text: str):
        instance: Novel2VecWrapper = Novel2VecWrapper()
        try:
            obj = json.loads(json_text)
            instance.positive_titles = obj['positivie_titles']
            instance.negative_titles = obj['negative_titles']
            instance.unknown_titles = obj['unknown_titles']
        except:
            pass
        return instance

    def __init__(self) -> None:
        self.positive_titles: List[str] = []
        self.negative_titles:List[str]=[]
        self.unknown_titles: List[str] = []

    def set_search_query(self, positive_titles:List[str],negative_titles:List[str] ) -> None:
        self.positive_titles=positive_titles
        self.negative_titles=negative_titles
        self.unknown_titles = []
        for title in self.positive_titles+self.negative_titles:
            if not title in novel2vec.wv:
                self.unknown_titles.append(title)

    def any_unknown_titles(self) -> bool:
        return bool(self.unknown_titles)

    def get_unknown_titles(self) -> List[str]:
        return self.unknown_titles
    
    def is_search_query_empty(self)->bool:
        return not(bool(self.positive_titles) or bool(self.negative_titles))

    def get_similar_novels(self) -> List[SimilarNovel]:
        if self.any_unknown_titles() or self.is_search_query_empty():
            return []
        model_result: List = novel2vec.wv.most_similar(
            positive=self.positive_titles,
            negative=self.negative_titles,
            topn=20
        )
        similar_novels: List[SimilarNovel] = []
        for title, score in model_result:
            similar_novel = SimilarNovel(title, score)
            similar_novels.append(similar_novel)
        return similar_novels


class SessionManager:
    HOST_DATA_KEY: str = 'session_data_json_text'

    def __init__(self):
        pass

    def has_session(self) -> bool:
        return SessionManager.HOST_DATA_KEY in session

    def create_session(self) -> None:
        data: Novel2VecWrapper = Novel2VecWrapper()
        self.set_session_data(data)

    def get_session_data(self) -> Optional[Novel2VecWrapper]:
        if self.has_session():
            json_text: str = session[SessionManager.HOST_DATA_KEY]
            data: Novel2VecWrapper = Novel2VecWrapper.from_json(json_text)
            return data
        return None

    def set_session_data(self, data: Novel2VecWrapper) -> None:
        session[SessionManager.HOST_DATA_KEY] = data.to_json()

    def delete_session(self) -> None:
        if self.has_session():
            session.pop(SessionManager.HOST_DATA_KEY)


session_manager = SessionManager()
