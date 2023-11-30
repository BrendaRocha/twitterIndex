import json
import os
import time
from BSBI import Indice_BSBI

class Indice_de_fechas(Indice_BSBI):
    def __init__(self, salida, temporal, documentos, blocksize):
        super().__init__(salida, temporal, documentos, blocksize)
        self._fecha_a_fechaID = {}

        self.generar_docID()
        self.indexar()

    def indexar(self):
        n = 0
        lista_de_bloques = []

        for bloque in self.parse_next_block():
            bloque_invertido = self.invertir_bloque(bloque)
            lista_de_bloques.append(self.guardar_bloque_invertido(bloque_invertido, n))
            n += 1
        start = time.process_time()
        self.intercalar_bloques(lista_de_bloques, self._fecha_a_fechaID)
        end = time.process_time()
        print("Intercalar bloques de fechas ==> Tiempo transcurrido: ", end-start)

        self.guardar_dict_fechas()
        self.guardar_dict_docs()
    
    def guardar_dict_fechas(self):
        super().guardar_index_dict("dict_dates.json", self._fecha_a_fechaID)

    def parse_next_block(self):
        blocksize = self._blocksize
        dateID = 0
        bloque = []
        for doc in self.docs_list:
            try:
                with open(doc, "r", encoding="utf-8") as file_corpus:
                    dict_tweet = json.load(file_corpus)
                    for id, data in dict_tweet.items():
                        blocksize -= len(data['texto'].encode('utf-8'))
                        date = self.limpiar_fechas(data['fecha'])
                        if date not in self._fecha_a_fechaID:
                            self._fecha_a_fechaID[date] = dateID
                            dateID += 1
                        bloque.append((self._fecha_a_fechaID[date],(self._doc_a_docID[doc], id)))

                        if blocksize <= 0:
                            yield bloque
                            blocksize = self._blocksize
                            bloque = []
                    yield bloque
            except Exception as e:
                print(e)

    def limpiar_fechas(self, tweet):
        fecha = tweet[:4] +'-'+ tweet[5:7] +'-'+ tweet[8:10] +' '+ tweet[11:13] +':'+ tweet[14:16]
        return fecha

