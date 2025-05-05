from abc import ABC, abstractmethod

class IFormat(ABC):
    pass

class ArticleFormat(ABC):
    pass

class IEEEFormat(IFormat):
    pass

class SpringerNatureFormat(IFormat):
    pass
