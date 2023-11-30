import json
import os
import re

class Indice_BSBI(object):
    def __init__(self, salida, temporal, documentos, blocksize):
        self.documentos = documentos
        self.salida = salida
        self._blocksize = blocksize
        self._temp = temporal
        
    def generar_docID(self):
            doc_a_docID = {}
            docID_to_doc = {}
            docs_list = re.findall(r'(?<=Practico\/)\S*', self.documentos)

            for i in range(len(docs_list)):
                doc_a_docID[docs_list[i]] = str(i)
            self.docs_list = docs_list
            self._doc_a_docID = doc_a_docID

    def invertir_bloque(self, bloque):
        bloque_invertido = {}
        bloque_ordenado = sorted(bloque, key=lambda tuple: (tuple[0], tuple[1]))
        for par in bloque_ordenado:
            posting = bloque_invertido.setdefault(par[0], set())
            posting.add(par[1])
        return bloque_invertido

    def guardar_bloque_invertido(self, bloque, numero_bloque):
        archivo_de_salida = "b"+str(numero_bloque)+".json"
        archivo_de_salida = os.path.join(self._temp, archivo_de_salida)
        for clave in bloque:
            bloque[clave] = list(bloque[clave])
        with open(archivo_de_salida, "w") as contenedor:
            json.dump(bloque, contenedor)
        return archivo_de_salida

    def guardar_dict_docs(self):
        self._doc_a_docID = { doc_id : doc for doc, doc_id in self._doc_a_docID.items()}
        path = os.path.join(self.salida, "dict_docs.json")
        with open(path, "w") as contenedor:
            json.dump(self._doc_a_docID, contenedor)
    
    def guardar_index_dict(self, dict_path, dict):
        path = os.path.join(self.salida, dict_path)
        with open(path, "w") as container:
            json.dump(dict, container)

    def intercalar_bloques(self, archivos_temp, archivos_ID):
        lista_term_ID=[str(i) for i in range(len(archivos_ID))]
        posting = os.path.join(self.salida,"postings.json")
        lista_de_bloques=[]
        dict_postings = {}

        open_files = [open(f, "r") for f in archivos_temp]
        for data in open_files:
            data.seek(0)
            lista_de_bloques.append(json.load(data))
        
        with open(posting,"w") as output:
            for termID in lista_term_ID:
                dict_docID_tweetID = {}
                for bloque in lista_de_bloques:
                    try:
                        for lista in bloque[termID]:
                            if lista[0] not in dict_docID_tweetID.keys():
                                dict_docID_tweetID[lista[0]] = []
                            dict_docID_tweetID[lista[0]].append(lista[1])
                    except:
                        pass
                dict_postings.update({termID : dict_docID_tweetID})
            output.write(json.dumps(dict_postings, indent=2))