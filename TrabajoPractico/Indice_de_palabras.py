from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import string
import re
import time
import json
import os
from BSBI import Indice_BSBI

class Indice_de_palabras(Indice_BSBI):
    def __init__(self, salida, temporal, documentos, blocksize, language='spanish'):
        super().__init__(salida, temporal, documentos,blocksize)
        self._stop_words = frozenset(stopwords.words(language))
        self._stemmer = SnowballStemmer(language, ignore_stopwords=False)
        self._term_to_termID = {}

        self.generar_docID()
        self.indexar()


    def lemmatizar(self, palabra):
        palabra = palabra.strip(string.punctuation + "|" + "'" + "´" + "-" + "»" + "\x97" + "¿" + "¡" +\
                                "\u201c" + "\u25b6" + "\u201d" + "\u2014" + "\u2018" + "\u2019" + "\u00bf")

        lemmatized_word = self._stemmer.stem(palabra)
        return lemmatized_word

    def indexar(self):
        n = 0
        lista_de_bloques = []

        for bloque in self.parse_next_block():
            bloque_invertido = self.invertir_bloque(bloque)
            lista_de_bloques.append(self.guardar_bloque_invertido(bloque_invertido, n))
            n += 1
        start = time.process_time()
        self.intercalar_bloques(lista_de_bloques, self._term_to_termID)
        end = time.process_time()
        print("Intercalar bloques de palabras ==> Tiempo transcurrido: ", end-start)

        self.guardar_dict_terms()
        self.guardar_dict_docs()

    def parse_next_block(self):
        blocksize = self._blocksize
        termID = 0
        bloque = []
        for doc in self.docs_list:
            try:
                with open(doc, "r", encoding="utf-8") as corpus:
                    dict_tweet = json.load(corpus)
                    for id, data in dict_tweet.items():

                        blocksize -= len(data['texto'].encode('utf-8'))
                        tweet = self.sacar_links_y_emojis(data['texto'])
                        for palabra in tweet:
                            
                            if palabra not in self._stop_words and len(palabra) > 1:
                                palabra = self.lemmatizar(palabra)
                                if palabra not in self._term_to_termID:
                                    self._term_to_termID[palabra] = termID
                                    termID += 1
                                bloque.append((self._term_to_termID[palabra],(self._doc_a_docID[doc], id )))

                        if blocksize <= 0:
                            yield bloque
                            blocksize = self._blocksize
                            bloque = []
                    yield bloque
            except Exception as e:
                print(e)

    def sacar_links_y_emojis(self, tweet):
        regex_link = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        regex_emoji = '[\u2620-\U0001fa7a]|[\U000e0067-\U000e007f]|[\U000e0062\U000e0065]\
                        |[\U0001fa7a-\U0001fac0]+|[\u200d]+|[\U0001f4bc]+'
        regex_mention = '@[a-zA-Z0-9-]*|#[a-zA-Z0-9À-ÿ\u00f1\u00d1$-_@.&+]*'

        links = set(re.findall(regex_link, tweet))
        emojis = set(re.findall(regex_emoji, tweet))
        menciones = set(re.findall(regex_mention, tweet))
        set_de_caracteres = links.union(emojis.union(menciones))

        for caracter in set_de_caracteres:
            tweet = tweet.replace(caracter, ' ')

        return(tweet.split())

    def guardar_dict_terms(self):
        super().guardar_index_dict("dict_terms.json", self._term_to_termID)