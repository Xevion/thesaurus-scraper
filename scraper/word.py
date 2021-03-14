from collections import namedtuple
from typing import Dict, List, Optional, Set

Inflection = namedtuple('Inflection', ['display', 'slug'])
SimilarWord = namedtuple('SimilarWord', ['term', 'similarity', 'vulgar', 'informal', 'targetTerm', 'targetSlug'])


class Word(object):
    """
    Describes a word on Thesaurus.com uniquely identified by it's slug/URL.
    """

    def __init__(self, entry: str, inflections: Optional[List[Inflection]] = None, variants: Optional[List['WordVariant']] = None,
                 pronunciation: Optional['Pronunciation'] = None, examples: Optional[List['ExampleSentence']] = None):
        self.entry = entry
        self.inflections = inflections or []
        self.variants = variants or []
        self.pronunciation = pronunciation
        self.examples = examples or []

    def get_urls(self) -> Set[str]:
        urls = set()
        for variant in self.variants:
            for word in variant.antonyms + variant.synonyms:
                urls.add(f'https://www.thesaurus.com/browse/{word.targetSlug}')
        return urls

    @classmethod
    def from_raw(cls, data: dict) -> 'Word':
        """
        Creates a Word instance from raw data extracted from Thesaurus.com

        :param data: A parsed Python dictionary.
        :return: A Word instance.
        """
        api = data['tunaApiData']
        inflections = [Inflection(inflection['displayForm'], inflection['slug']) for inflection in api['inflections']]
        variants = [WordVariant.from_raw(api['entry'], variant_raw) for variant_raw in api['posTabs']]
        pronunciation = Pronunciation.from_raw(api['pronunciation']) if (api.get('pronunciation') is not None) else None
        examples = [ExampleSentence.from_raw(example_raw) for example_raw in api['exampleSentences']]

        return Word(
                entry=api['entry'],
                inflections=inflections,
                variants=variants,
                pronunciation=pronunciation,
                examples=examples
        )

    def __repr__(self) -> str:
        # Count the number of antonyms and synonyms
        s = a = 0
        for variant in self.variants:
            s += len(variant.synonyms)
            a += len(variant.antonyms)

        return f'Word("{self.entry}", {len(self.variants)} variant{"s" if len(self.variants) != 1 else ""}, {s} syn{"s" if s != 1 else ""}' \
               f', {a} ant{"s" if a != 1 else ""})'


class WordVariant(object):
    def __init__(self, term: str, definition: str, pos: str, synonyms: List[SimilarWord], antonyms: List[SimilarWord],
                 informal: Optional[int],
                 vulgar: int, note: Optional[str], ref_id: int) -> None:
        self.term = term
        self.definition = definition
        self.pos = pos
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.informal = informal
        self.vulgar = vulgar
        self.note = note
        self.id = ref_id

    @staticmethod
    def basic_word(raw: dict) -> SimilarWord:
        return SimilarWord(term=raw['term'],
                           similarity=int(raw['similarity']),
                           vulgar=raw['isVulgar'],
                           informal=raw['isInformal'],
                           targetSlug=raw['targetSlug'],
                           targetTerm=raw['targetTerm'])

    @classmethod
    def from_raw(cls, term: str, data: dict) -> 'WordVariant':
        return WordVariant(
                term=term,
                definition=data['definition'],
                pos=data['pos'],
                synonyms=[WordVariant.basic_word(syn) for syn in data['synonyms']],
                antonyms=[WordVariant.basic_word(ant) for ant in data['antonyms']],
                informal=int(data['isInformal']) if data['isInformal'] else None,
                vulgar=int(data['isVulgar']),
                note=data['note'],
                ref_id=int(data['thesRid']) if 'thesRid' in data.keys() else None
        )

    def __repr__(self) -> str:
        return f'WordVariant({self.term}, {self.pos}, {self.definition}, [{len(self.synonyms)}/{len(self.antonyms)}])'


class Pronunciation(object):
    def __init__(self, audio: Optional[Dict[str, str]], ipa: Optional[str], spelling: Optional[str]) -> None:
        self.audio = audio
        self.ipa = ipa
        self.spelling = spelling

    @classmethod
    def from_raw(cls, data: dict) -> 'Pronunciation':
        return Pronunciation(
                audio=data['audio'] if 'audio' in data.keys() else None,
                ipa=data['ipa'] if 'ipa' in data.keys() else None,
                spelling=data['spell'] if 'spell' in data.keys() else None
        )

    def __repr__(self) -> str:
        return f'Pronunciation({len(self.audio.keys())} audio sources, {self.ipa}, {self.spelling})'


class ExampleSentence(object):
    def __init__(self, id: int, sentence: str, source: Dict[str, str], profanity: int) -> None:
        self.id = id
        self.sentence = sentence
        self.source = source
        self.profanity = profanity

    @classmethod
    def from_raw(cls, data: dict) -> 'ExampleSentence':
        return ExampleSentence(
                id=data['id'],
                sentence=data['sentence'],
                source=data['source'],
                profanity=data['profanity']
        )

    def __repr__(self) -> str:
        return f'ExampleSentence({self.id}, "{self.sentence[:15]}{"..." if len(self.sentence) >= 15 else ""}")'
