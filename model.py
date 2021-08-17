from flask import session
from dataclasses import field, dataclass
from typing import List, Dict, Optional
from gensim.models.word2vec import Word2Vec
from uuid import uuid4


@dataclass
class SearchQuery:
    positive: List[str] = field(default_factory=list)
    negative: List[str] = field(default_factory=list)

    def is_empty(self):
        return len(self.positive) == 0 and len(self.negative) == 0


@dataclass
class SimilarNovel:
    title: str
    score: float


novel2vec: Word2Vec = Word2Vec.load(
    'novel2vec_skipgram_gensim4_100dim.model')


class Novel2VecWrapper:
    def __init__(self) -> None:
        self.sq: SearchQuery = SearchQuery()
        self.unknown_titles: List[str] = []

    def set_search_query(self, sq: SearchQuery) -> None:
        self.sq = sq
        self.unknown_titles = []
        for title in self.sq.positive+self.sq.negative:
            if not title in novel2vec.wv:
                self.unknown_titles.append(title)

    def any_unknown_titles(self) -> bool:
        return bool(self.unknown_titles)

    def get_unknown_titles(self) -> List[str]:
        return self.unknown_titles

    def get_similar_novels(self) -> List[SimilarNovel]:
        if self.any_unknown_titles() or self.sq.is_empty():
            return []
        model_result: List = novel2vec.wv.most_similar(
            positive=self.sq.positive,
            negative=self.sq.negative,
            topn=20
        )
        similar_novels: List[SimilarNovel] = []
        for title, score in model_result:
            similar_novel = SimilarNovel(title, score)
            similar_novels.append(similar_novel)
        return similar_novels


class SessionManager:
    HOST_SID_KEY: str = 'sid'

    def __init__(self):
        self.sid2data: Dict[str, str] = {}

    def has_session(self) -> bool:
        return (SessionManager.HOST_SID_KEY in session)\
            and (session[SessionManager.HOST_SID_KEY] in self.sid2data)

    def create_session(self) -> None:
        sid: str = str(uuid4())
        self.sid2data[sid] = Novel2VecWrapper()
        session[SessionManager.HOST_SID_KEY] = sid

    def get_session_data(self) -> Optional[Novel2VecWrapper]:
        if self.has_session():
            sid: str = session[SessionManager.HOST_SID_KEY]
            data: Novel2VecWrapper = self.sid2data[sid]
            return data
        return None

    def delete_session(self) -> None:
        if self.has_session():
            sid: str = session[SessionManager.HOST_SID_KEY]
            self.sid2data.pop(sid)
            session.pop(SessionManager.HOST_SID_KEY)


session_manager = SessionManager()
