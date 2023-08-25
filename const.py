from string import punctuation


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = (
    'a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
    'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu',
    'ya', 'je', 'i', 'ji', 'g'
)
PROBLEM_SYMBOLS = punctuation.replace('.', ' ')
TRANS = {}

for cyrillic, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = translation
    TRANS[ord(cyrillic.upper())] = translation.upper()

for symbol in PROBLEM_SYMBOLS:
    TRANS[ord(symbol)] = "_"
