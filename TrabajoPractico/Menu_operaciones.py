import json
import re
import string
import tkinter as tk
from tkinter import Listbox, Scrollbar, Tk, ttk
from tkinter import filedialog as fd
from tkinter.constants import BOTH, END, LEFT, RADIOBUTTON, RIGHT, X, Y
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

class Menu_de_operaciones:
    def __init__(self):
        self._stop_words = frozenset(stopwords.words('spanish'))
        self._stemmer = SnowballStemmer('spanish', ignore_stopwords=False)

    def aceptar_fechas(self,d,h,cantidad):
        with open ("output_dates/dict_dates.json","r",encoding="UTF-8") as dict_dates,\
            open ("output_dates/postings.json","r",encoding="UTF-8") as posting,\
            open ("output_dates/dict_docs.json","r",encoding="UTF-8") as dict_docs:
            self.dict_da= json.load(dict_dates)
            self.post= json.load(posting)
            self.dict_doc=json.load(dict_docs)

        desde= self.pasaje_fecha_a_numero(d)
        hasta= self.pasaje_fecha_a_numero(h)

        self.lista_completa = []
        for c,v in self.dict_da.items():
            clave= self.pasaje_fecha_a_numero(c)
            if clave >=desde and clave<=hasta:
                self.obtener_id(str(v))
        self.ventana_nueva_fechas(self.lista_completa,cantidad)

    def obtener_id(self,valor):
        dict_apariciones=self.post[valor]

        for doc_id,list_tweets in dict_apariciones.items():
            with open (str(self.dict_doc[str(doc_id)]),"r",encoding="UTF-8") as corpus:
                self.corpus=json.load(corpus)
                for id in list_tweets:
                    self.lista_completa.append(id)
            
    def pasaje_fecha_a_numero(self,palabras):
        suma=""
        lista = re.split(r'[\W]', palabras)
        for num in lista:
            suma+=num
        return int(suma)
    

    def ventana_nueva_fechas(self, list_tweets, cantidad_de_tweets_pedidos):
            self.ventana1 = Tk()
            self.ventana1.geometry('600x680')
            self.ventana1.resizable(False,False)
            self.ventana1.iconbitmap("Twitter.ico")
            self.labelframe1=ttk.LabelFrame(self.ventana1, text="Búsqueda")        
            self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
            scrollbar = Scrollbar(self.labelframe1)
            scrollbar.pack( side = RIGHT, fill = Y )

            mylist = Listbox(self.labelframe1, yscrollcommand = scrollbar.set, width=95, height=40)
            cantidad_de_tweets = int(cantidad_de_tweets_pedidos)
            if(len(list_tweets)<cantidad_de_tweets-1):
                cantidad_de_tweets = len(list_tweets)-1
            
            for id_tweet in list_tweets[0:int(cantidad_de_tweets_pedidos)]:
                tweet = ("@{} => {}".format(self.corpus[id_tweet]["cuenta"], self.corpus[id_tweet]["texto"]))
                largo = len(tweet.encode('utf-8'))
                mylist.insert(END,'---------------------------------------------------------------------------------------------------------------')
                aux = 0
                for x in range(0,largo//100):
                    mylist.insert(END,tweet[aux:aux+100])
                    aux=aux+100
                mylist.insert(END,tweet[aux:])
            mylist.insert(END,'---------------------------------------------------------------------------------------------------------------')

            mylist.pack( side = LEFT, fill = BOTH )
            scrollbar.config( command = mylist.yview )

            self.ventana1.mainloop()
    
    def aceptar_palabras(self,entrada,negadas,cantidad):
        with open ("output_words/dict_terms.json","r",encoding="UTF-8") as dict_terms,\
            open ("output_words/postings.json","r",encoding="UTF-8") as posting,\
            open ("output_words/dict_docs.json","r",encoding="UTF-8") as dict_docs:
            self.dict_term= json.load(dict_terms)
            self.post= json.load(posting)
            self.dict_doc=json.load(dict_docs)

        lista_dicts_conjuntos = self.conjuntos_id_tweets(entrada)
    
        operacion_final= self.crear_operacion(entrada,negadas)

        self.lista_completa_de_tuplas = []
        contador= 0
        for tweet in operacion_final:
            encontrado = False
            for dict in lista_dicts_conjuntos:
                for c,v in dict.items():
                    if(encontrado == False):
                        for id in v:
                            if (int(id) == tweet) & (contador< int(cantidad)):
                                contador+=1
                                with open(self.dict_doc[c],"r",encoding="UTF-8") as corpus:
                                    self.corpus = json.load(corpus)
                                    self.lista_completa_de_tuplas.append((self.corpus[id]["cuenta"], self.corpus[id]["texto"]))
                                encontrado = True
            
        self.ventana_nueva_palabras(self.lista_completa_de_tuplas)
        
    def ventana_nueva_palabras(self, lista_de_tuplas):
        
        self.ventana2 = Tk()
        self.ventana2.geometry('600x680')
        self.ventana2.resizable(False,False)
        self.ventana2.iconbitmap("Twitter.ico")
        self.labelframe2=ttk.LabelFrame(self.ventana2, text="Búsqueda")        
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        scrollbar = Scrollbar(self.labelframe2)
        scrollbar.pack( side = RIGHT, fill = Y )

        mylist2 = Listbox(self.labelframe2, yscrollcommand = scrollbar.set, width=95, height=40)

        for par in lista_de_tuplas:
            linea = ("@{} => {}".format(par[0], par[1]))
            largo = len(linea.encode('utf-8'))
            mylist2.insert(END,'---------------------------------------------------------------------------------------------------------------')
            aux = 0
            for x in range(0,largo//100):
                mylist2.insert(END,linea[aux:aux+100])
                aux=aux+100
            mylist2.insert(END,linea[aux:])
        mylist2.insert(END,'-------------------------------------------------------------------------------------------------------------------')    
        
        mylist2.pack( side = LEFT, fill = BOTH )
        scrollbar.config( command = mylist2.yview )

        self.ventana2.mainloop()

    def conjuntos_id_tweets(self,entrada):
        lista_lematizadas = [self.lematizar(palabra) for palabra in re.split("[A-Z\s]+", entrada)]
    
        lista_dicts = []
        for palabra in lista_lematizadas:
            dict_doc_sets = {}
            id = self.dict_term[palabra]
            dict_doc_tweet = self.post[str(id)]
            for c,v in dict_doc_tweet.items():
                conjunto = set()
                for id_tweet in v:
                    conjunto.add(id_tweet)
                    dict_doc_sets[c] = conjunto
            lista_dicts.append(dict_doc_sets)
        print(lista_dicts)
        return lista_dicts

    def conjunto_id_negadas(self,negadas):
        lista_negadas_lematizadas = [self.lematizar(palabra) for palabra in negadas.split(' ')]
        print(lista_negadas_lematizadas)
        conjunto_id_negadas = set()
        for palabra in lista_negadas_lematizadas:
            id = self.dict_term[palabra]
            for c,v in self.post[str(id)].items():
                for id_tweets in v:
                    conjunto_id_negadas.add(int(id_tweets))
        return conjunto_id_negadas
        
    def crear_operacion(self,entrada,negadas):
        simbolos = ['(',')','A','N','D','O','R',' ']
        operacion_final = ''
        numero_de_palabra = 0
        posicion=0
        entrada+=" "
        lista_dicts_conjuntos = self.conjuntos_id_tweets(entrada)

        while posicion < len(entrada):
            if entrada[posicion] not in simbolos:
                operacion_final+="{"
                for c,v in lista_dicts_conjuntos[numero_de_palabra].items():
                    for id_tweet in v:
                        operacion_final+= id_tweet
                        operacion_final+=","
                operacion_final= operacion_final[:-1]
                operacion_final+="}"
                numero_de_palabra+=1
                booleano_posicion=True
                while booleano_posicion:
                    posicion+=1
                    if(entrada[posicion]) in simbolos:
                        booleano_posicion=False
            else:
                operacion_final+=entrada[posicion]
                posicion+=1

        operacion_final=operacion_final.replace("AND", "&")
        operacion_final=operacion_final.replace("OR", "|")
        operacion_final=eval(operacion_final)
        operacion_final=operacion_final-self.conjunto_id_negadas(negadas)
        return operacion_final    

    def lematizar(self, palabra):
        palabra = palabra.strip(string.punctuation + "|" + "'" + "´" + "-" + "»" + "\x97" + "¿" + "¡" +\
                                "\u201c" + "\u25b6" + "\u201d" + "\u2014" + "\u2018" + "\u2019" + "\u00bf")

        palabra_lematizada = self._stemmer.stem(palabra)
        return palabra_lematizada
