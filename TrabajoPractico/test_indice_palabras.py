import unittest
import json
from test import support
from BSBI import Indice_BSBI
from Indice_de_palabras import Indice_de_palabras
  


  
indicee=Indice_de_palabras("indice_x/output", "indice_x/temp","TrabajoPractico/docs/corpus_B.json", 1000000)

def test_lematizar_palabra():
    t = indicee.lemmatizar("inglaterra")

    assert t =="inglaterr"

def test_lematizar_strip():
    t = indicee.lemmatizar("inglatérrá")

    assert t == "inglaterr"

def test_lematizar_strip2():
    t = indicee.lemmatizar("¿inglatérrá????!!!!!!!?????¡¡¡¿¿¿¿¿")

    assert t == "inglaterr"

def test_limpiar_hashtag():
    t = indicee.sacar_links_y_emojis("sintomas de resfrio covid #covid-19")

    assert t == ['sintomas','de','resfrio','covid']

def test_limpiar_menciones():
    t = indicee.sacar_links_y_emojis("sintomas de resfrio covid @laNacion")

    assert t == ['sintomas','de','resfrio','covid']

def test_limpiar_links():
    t = indicee.sacar_links_y_emojis("sintomas de resfrio covid https://www.clarin.com/sociedad/vacunados-dosis-sintomas-resfrio-probabilidad-covid_0_KJgOMgORD.html")

    assert t ==['sintomas','de','resfrio','covid']

def test_limpiar_y_lematizar():
    palabra_fast_and_dirty = "sintomas? de résfrio covid #covid-19 @clarin https://www.clarin.com/sociedad/vacunados-dosis-sintomas-resfrio-probabilidad-covid_0_KJgOMgORD.html"

    t=indicee.sacar_links_y_emojis(palabra_fast_and_dirty)
    palabras_lematizadas=[]
    for palabra in t:
        palabras_lematizadas.append(indicee.lemmatizar(palabra))
    assert palabras_lematizadas == ['sintom', 'de', 'resfri', 'cov']

def test_indexar(): 
    indice = Indice_de_palabras("testPalabras/output_test", "testpalabras/test_temp","TrabajoPractico/testpalabras/test_docs/corpus_test.json", 1000000)
    with open("testpalabras/output_test/dict_terms.json", "r", encoding="utf-8") as corpus:
        dict_test=json.load(corpus)
        
    assert dict_test== {"excelent": 0, "usted": 1, "sab": 2}

def test_indexar2(): 
    indice = Indice_de_palabras("testPalabras/output_test", "testPalabras/test_temp","TrabajoPractico/testpalabras/test_docs/corpus_test2.json", 1000000)
    with open("testpalabras/output_test/dict_terms.json", "r", encoding="utf-8") as corpus:
        dict_test=json.load(corpus)
        
    assert dict_test== {"la": 0, "voz": 1, "kids": 2, "peque\u00f1": 3, "emocion": 4, "entren": 5, "tras": 6, "cont": 7, "cant": 8, "padr": 9, "fallec": 10, "covid-19": 11, "127": 12, "nuev": 13, "cas": 14, "queretar": 15, "salud": 16, "estatal": 17, "mi": 18, "abuel": 19, "hombr": 20, "fuert": 21, "san": 22, "75": 23, "a\u00f1os": 24, "le": 25, "aplic": 26, "dos": 27, "dosis": 28, "ahor": 29, "presion": 30, "alta": 31, "problem": 32, "corazon": 33, "demasi": 34, "efect": 35, "secundari": 36, "se": 37, "pens": 38, "verd": 39, "aturd": 40, "silenci": 41, "hay": 42, "tap": 43, "enan": 44, "indecent": 45, "escuel": 46, "superior": 47, "informat": 48, "celebr": 49, "sant": 50, "tecl": 51, "jorn": 52, "empres": 53, "form": 54, "presencial": 55, "es": 56, "cuidat": 57, "gir": 58, "program": 59, "cuid": 60, "public": 61, "pues": 62, "todav": 63, "segu": 64, "pandemi": 65, "aparec": 66, "variant": 67, "inglaterr": 68, "piens": 69, "va": 70, "vari": 71, "mes": 72, "situacion": 73, "dificil": 74, "tod": 75}

def test_indexar3(): 
    indice = Indice_de_palabras("testPalabras/output_test", "testPalabras/test_temp","TrabajoPractico/testpalabras/test_docs/corpus_test3.json", 1000000)
    with open("testpalabras/output_test/dict_terms.json", "r", encoding="utf-8") as corpus:
        dict_test=json.load(corpus)
        
    assert dict_test== {"esa": 0, "vacun": 1, "dio": 2, "feo": 3, "al": 4, "horn": 5, "eeuu": 6, "expert": 7, "recomend": 8, "fda": 9, "pfiz": 10, "ni\u00f1": 11, "11": 12, "a\u00f1os": 13, "rusi": 14, "registr": 15, "1.106": 16, "fallec": 17, "covid-19": 18, "nuev": 19, "maxim": 20, "diari": 21, "buen": 22, "si": 23, "muer": 24, "which": 25, "is": 26, "unlikely": 27, "gan": 28, "igual": 29, "situacion": 30, "lind": 31, "xdi": 32, "hac": 33, "cas": 34, "que": 35, "bol": 36, "no": 37, "aca": 38, "llev": 39, "tres": 40, "mism": 41, "por": 42, "fin": 43, "encontr": 44, "cov": 45, "tap": 46, "car": 47, "satrap": 48, "ya": 49, "contamin": 50, "visual": 51, "oposicion": 52, "san": 53, "lazar": 54, "reclam": 55, "secretari": 56, "salud": 57, "jorg": 58, "alcoc": 59, "286": 60, "mil": 61, "muert": 62, "regal": 63, "lap": 64, "ahor": 65, "unas": 66, "mascarill": 67, "tecnolog": 68, "pued": 69, "funcion": 70, "tradicional": 71}
