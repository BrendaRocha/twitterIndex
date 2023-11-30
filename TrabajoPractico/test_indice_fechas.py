import unittest
import json
from BSBI import Indice_BSBI
from Indice_de_fechas import Indice_de_fechas



indice = Indice_de_fechas("indice_x/output", "indice_x/temp","TrabajoPractico/docs/corpus_B.json", 100000000)


def test_limpiar_fechas_correctas():
    fecha_limpia = indice.limpiar_fechas("2021-10-29T20:38:57.000Z")
    assert fecha_limpia == '2021-10-29 20:38'

def test_limpiar_fechas_con_barras():
    fecha_limpia = indice.limpiar_fechas("2021/10/29 20:38")
    assert fecha_limpia == '2021-10-29 20:38'


def test_limpiar_fechas_con_varias_letras():
    fecha_limpia = indice.limpiar_fechas("2021t10t29 20:38")
    assert fecha_limpia == '2021-10-29 20:38'

def test_limpiar_fechas_con_formato_incorrecto_da_error():
    fecha_limpia = indice.limpiar_fechas("2021tt10tt29 20:38")
    assert fecha_limpia != '2021-10-29 20:38'

def test_guardar_dict_fechas_exitosamente():
    indice.guardar_dict_fechas()

def test_indexar_fechas(): 
    indice = Indice_de_fechas("test_fechas/output_test", "test_fechas/test_temp","TrabajoPractico/test_fechas/test_docs/corpus_test_fechas.json", 1000000)
    with open("test_fechas/output_test/dict_dates.json", "r", encoding="utf-8") as corpus:
        dict_test=json.load(corpus)
        
    assert dict_test== {"2021-10-20 01:55": 0}

def test_guadar_fechas_dict_docs(): 
    indice = Indice_de_fechas("test_fechas/output_test", "test_fechas/test_temp","TrabajoPractico/test_fechas/test_docs/corpus_test_fechas.json", 1000000)
    with open("test_fechas/output_test/dict_docs.json", "r", encoding="utf-8") as corpus:
        dict_test=json.load(corpus)
        
    assert dict_test== {"0": "test_fechas/test_docs/corpus_test_fechas.json"}


def test_guardar_posting_de_fechas():
    indice = Indice_de_fechas("test_fechas/output_test", "test_fechas/test_temp","TrabajoPractico/test_fechas/test_docs/corpus_test_fechas.json", 1000000)
    with open("test_fechas/output_test/postings.json", "r", encoding="utf-8") as corpus:
        posting=json.load(corpus)
        
    assert posting == {"0": {"0": ["1450641904907993091"]}}





    






