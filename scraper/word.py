from typing import List, Optional


class Word(object):
    """
    Describes a word on Thesaurus.com uniquely identified by it's slug/URL.
    """
    def __init__(self, entry: str, inflections: Optional[List[str]] = None, variants: Optional[List['WordVariant']] = None,
                 pronunciation: Optional['Pronunciation'] = None, examples: Optional[List['ExampleSentence']] = None):
        self.entry = entry
        self.inflections = inflections or []
        self.variants = variants or []
        self.pronunciation = pronunciation
        self.examples = examples or []

    @classmethod
    def from_raw(cls, data: dict) -> 'Word':
        pass

    def __repr__(self) -> str:
        pass


class WordVariant(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_raw(cls, data: dict) -> 'WordVariant':
        pass

    def __repr__(self) -> str:
        pass


class Pronunciation(object):
    def __init__(self, term: str, definition: str, pos: str, synonyms: List[str], antonyms: List[str], informal: Optional[int],
                 vulgar: int, note: Optional[str], id: int) -> None:
        pass

    @classmethod
    def from_raw(cls, data: dict) -> 'Pronunciation':
        pass

    def __repr__(self) -> str:
        pass

class ExampleSentence(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def from_raw(cls, data: dict) -> 'ExampleSentence':
        pass

    def __repr__(self) -> str:
        pass
