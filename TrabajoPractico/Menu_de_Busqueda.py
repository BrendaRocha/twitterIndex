import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.constants import END
from Indice_de_palabras import Indice_de_palabras
from Indice_de_fechas import Indice_de_fechas
from Menu_operaciones import Menu_de_operaciones

class Aplicacion:
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.resizable(False,False)
        self.ventana1.title("Panchitos Team App")
        #self.ventana1.iconbitmap("Twitter.ico")
        self.labelframe1=ttk.LabelFrame(self.ventana1, text="Búsqueda")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.ingresar_corpus()
        self.labelframe2=ttk.LabelFrame(self.ventana1, text="Operaciones")        
        self.labelframe2.grid(column=0, row=1, padx=5, pady=10)        
        self.operaciones()
        self.ventana1.mainloop()

    def ingresar_corpus(self):
        self.label1=ttk.Label(self.labelframe1, text="Nombre del corpus:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.entry1=ttk.Entry(self.labelframe1, width=38)
        self.entry1.grid(column=1, row=0, padx=4, pady=4)
        self.boton1=ttk.Button(self.labelframe1, text="Examinar",command=self.examinar)
        self.boton1.grid(column=1, row=2, padx=5, pady=2)
        self.boton2=ttk.Button(self.labelframe1, text="Ingresar",command=self.cargar_docs)
        self.boton2.grid(column=1, row=2, padx=5, pady=2, sticky='E')

    def operaciones(self):
        self.boton3=ttk.Button(self.labelframe2, text="Búsqueda por palabras", command=self.buscar_palabra)
        self.boton3.grid(column=0, row=0, padx=4, pady=4)
        self.boton4=ttk.Button(self.labelframe2, text="Búsqueda por fechas",command=self.buscar_fecha)
        self.boton4.grid(column=1, row=0, padx=4, pady=4)

    def buscar_palabra(self):
        self.ventana1.destroy()
        self.ventana2=tk.Tk()
        self.ventana2.resizable(False,False)
        self.ventana2.title("Panchitos Team App")
        #self.ventana2.iconbitmap("Twitter.ico")
        
        self.labelframe2=ttk.LabelFrame(self.ventana2,text="Opciones")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10) 

        self.label1=ttk.Label(self.labelframe2, text="Ingrese la Palabra:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.entry_palabra=ttk.Entry(self.labelframe2, width=43)
        self.entry_palabra.grid(column=1, row=0, padx=4, pady=4)
        self.entry_palabra.config(foreground='grey')
        self.entry_palabra.insert(0, "(palabra AND/OR palabra) AND/OR palabra")
        self.entry_palabra.bind("<FocusIn>", lambda event: self.escribir_focus_in(self.entry_palabra))

        self.label2=ttk.Label(self.labelframe2, text="Ingrese palabras NOT:")
        self.label2.grid(column=0, row=3, padx=4, pady=4)
        self.entry_negadas=ttk.Entry(self.labelframe2, width=43)
        self.entry_negadas.grid(column=1, row=3, padx=4, pady=4)
        self.entry_negadas.config(foreground='grey')
        self.entry_negadas.insert(0, "palabra palabra palabra")
        self.entry_negadas.bind("<FocusIn>", lambda event: self.escribir_focus_in(self.entry_negadas))

        self.label3=ttk.Label(self.labelframe2, text="Ingrese cantidad:")
        self.label3.grid(column=0, row=4, padx=4, pady=4)
        self.entry_cantidad_palabra=ttk.Entry(self.labelframe2, width=21)
        self.entry_cantidad_palabra.insert(END, '10')
        self.entry_cantidad_palabra.grid(column=1, row=4, padx=4, pady=4, sticky='W')

        
        self.boton4=ttk.Button(self.labelframe2, text="Aceptar",command=self.aceptar_palabras)
        self.boton4.grid(column=1, row=5, padx=4, pady=4,sticky='E')

        self.boton5=ttk.Button(self.labelframe2, text="Volver",command=self.volver)
        self.boton5.grid(column=0, row=5, padx=4, pady=4,sticky='W')

        self.ventana2.mainloop()


    def buscar_fecha(self):
        self.ventana1.destroy()
        self.ventana2=tk.Tk()
        self.ventana2.resizable(False,False)
        self.ventana2.title("Panchitos Team App")
        #self.ventana2.iconbitmap("Twitter.ico")
        self.labelframe2=ttk.LabelFrame(self.ventana2,text="Ingrese la Fecha")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)

        self.label1=ttk.Label(self.labelframe2, text="Desde:")
        self.label1.grid(column=0, row=1, padx=4, pady=4,sticky= "W")
        self.entry_desde=ttk.Entry(self.labelframe2, width=21)
        self.entry_desde.grid(column=1, row=1, padx=4, pady=4)
        self.entry_desde.config(foreground='grey')
        self.entry_desde.insert(0, "AAAA-MM-DD HH:MM")
        self.entry_desde.bind("<FocusIn>", lambda event: self.escribir_focus_in(self.entry_desde))

        self.label2=ttk.Label(self.labelframe2, text="Hasta:")
        self.label2.grid(column=0, row=2, padx=4, pady=4,sticky="W")
        self.entry_hasta=ttk.Entry(self.labelframe2, width=21)
        self.entry_hasta.grid(column=1, row=2, padx=4, pady=4)
        self.entry_hasta.config(foreground='grey')
        self.entry_hasta.insert(0, "AAAA-MM-DD HH:MM")
        self.entry_hasta.bind("<FocusIn>", lambda event: self.escribir_focus_in(self.entry_hasta))


        self.label3=ttk.Label(self.labelframe2, text="Cantidad de tweets:")
        self.label3.grid(column=0, row=4, padx=4, pady=4)
        self.entry_cantidad_tweets=ttk.Entry(self.labelframe2, width=21)
        self.entry_cantidad_tweets.insert(END, '10')
        self.entry_cantidad_tweets.grid(column=1, row=4, padx=4, pady=4)

        self.boton5=ttk.Button(self.labelframe2, text="Volver",command=self.volver)
        self.boton5.grid(column=0, row=6, padx=4, pady=4,sticky='W')
        
        self.boton4=ttk.Button(self.labelframe2, text="Aceptar",command=self.aceptar_fechas)
        self.boton4.grid(column=1, row=6, padx=4, pady=4,sticky='E')
        self.ventana2.mainloop()
        
    def aceptar_fechas(self):
        d=self.entry_desde.get()
        h=self.entry_hasta.get()
        if(self.entry_cantidad_tweets.get()==""):
            cantidad="0"
        else:
            cantidad=self.entry_cantidad_tweets.get()
        fecha_operator=Menu_de_operaciones()
        try:
            fecha_operator.aceptar_fechas(d,h,cantidad)
        except ValueError:
            messagebox.showerror('Error', 'Formato de fecha inválido')
            
    
    def aceptar_palabras(self):
        entrada = self.entry_palabra.get()
        cantidad = self.entry_cantidad_palabra.get()
        negadas = self.entry_negadas.get()
        palabra_operator=Menu_de_operaciones()
        try:
            palabra_operator.aceptar_palabras(entrada,negadas,cantidad)
        except KeyError:
            messagebox.showerror('Error', 'No se encontro la palabra')
        except SyntaxError:
            messagebox.showerror('Error', 'Formato inválido')
            
    def volver(self):
        self.ventana2.destroy()
        self.__init__()
    
    def escribir_focus_in(self, entry):
        entry.delete(0,tk.END)
        entry.config(foreground='black')

    def examinar(self):
        self.path=fd.askopenfilenames(initialdir = "Escritorio",title = "Seleccione archivo",filetypes = (("JSON File (.json)","*.json"),("todos los archivos","*.*")))
        if self.path!='':
            self.entry1.insert(0,self.path)

    def cargar_docs(self):
        try:
            self.path = ' '.join(self.path)
            indice_de_fechas = Indice_de_fechas("output_dates", "temp_dates", self.path, 100000000)
            indice_de_palabras = Indice_de_palabras("output_words", "temp_words", self.path, 100000000)
        except AttributeError:
            self.entry1.delete(0,END)
            messagebox.showerror('Error', 'Path inválido.')
            
aplicacion1=Aplicacion()