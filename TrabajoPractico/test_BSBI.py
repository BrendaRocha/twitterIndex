import json
from BSBI import Indice_BSBI

indice = Indice_BSBI("output_words/test_bsbi", "temp_words/test_bsbi", 'TrabajoPractico/docs/corpus_B.json', 1000000)

def test_constructor():
    assert indice.documentos == 'TrabajoPractico/docs/corpus_B.json'
    assert indice.salida == 'output_words/test_bsbi'
    assert indice._blocksize == 1000000
    assert indice._temp == 'temp_words/test_bsbi'

def test_generar_docID():
    indice.generar_docID()
    assert len(indice._doc_a_docID) == 1

def test_invertir_bloque():
    #bloque = [(termID,(docID, id))]
    bloque = [('111',(1,'15789654')),('222',(1,'2548424'))]
    bloque_invertido = indice.invertir_bloque(bloque)
    assert bloque_invertido == {'111': {(1, '15789654')}, '222': {(1, '2548424')}}

def test_guardar_bloque():
    bloque = {'0': {(0, '15789654')}, '1': {(0, '2548424')}}
    archivo_salida = indice.guardar_bloque_invertido(bloque,5)
    assert archivo_salida == 'temp_words/test_bsbi\\b5.json'

def test_guardar_diccionario_de_docs():
    indice.guardar_dict_docs()
    with open('output_words/test_bsbi\\dict_docs.json') as dict_docs:
        docs_guardados = json.load(dict_docs)
    assert indice._doc_a_docID == docs_guardados

def test_guardar_diccionario_indexado():
    dict_aux = {"nuev": 0, "cas": 1, "queretar": 2, "salud": 3}
    indice.guardar_index_dict('dict_terms.json', dict_aux)
    with open('output_words/test_bsbi\\dict_terms.json') as dict_terms:
        diccionario_de_terms = json.load(dict_terms)
    assert dict_aux == diccionario_de_terms

def test_intercalar_bloques():
    dict_aux = {"nuev": 0, "cas": 1}
    indice.intercalar_bloques(['temp_words/test_bsbi\\b5.json'], dict_aux)
    with open('output_words/test_bsbi\\postings.json') as postings:
        dict_postings = json.load(postings)
    assert dict_postings ==  {'0': {'0': ['15789654']}, '1': {'0': ['2548424']}}

