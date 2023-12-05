import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import numpy as np
import random

def habilitarWidgets():
    entryorigen.config(state=tk.NORMAL)
    entrydestino.config(state=tk.NORMAL)
    botonFlujo.config(state=tk.NORMAL)

def getElementos():
    elemento=entryElement.get()
    n = int(elemento)
    if(n<5 or n>15):
        entryElement.delete(0, 'end')
    else:
        entryElement.configure(state="disabled")
        global componentes
        componentes=n
        botonElement.config(state=tk.DISABLED)
        botonAleatorio.config(state=tk.ACTIVE)
        botonManual.config(state=tk.ACTIVE)
        habilitarWidgets()

global eleccion
eleccion=''

def eleccionManual():
    for i in range(componentes):
        fila_Entries=[]
        for j in range(componentes):
            entryMatriz=tk.Entry(frameMatriz,width=5, fg="black", font=("Arial",10,'bold'))
            entryMatriz.grid(row=i,column=j)
            entryMatriz.insert(tk.END,0)
            fila_Entries.append(entryMatriz)
        matrizwidgets.append(fila_Entries)
    eleccion='M'
    

def eleccionAleatoria():
    matriz = np.zeros([componentes, componentes])
    if len(matrizwidgets)==0:
        for i in range(componentes):
            fila_Entries=[]
            for j in range(componentes):
                if(i==j):
                    element=0
                else:
                    element=random.randint(0, 100)
                matriz[i][j]=element
                entryMatriz=tk.Entry(frameMatriz,width=5, fg="black", font=("Arial",10,'bold'))
                entryMatriz.grid(row=i,column=j)
                entryMatriz.bind('')
                entryMatriz.insert(tk.END,str(element))
                fila_Entries.append(entryMatriz)
            matrizwidgets.append(fila_Entries)
    else:
        for i in range(componentes):
            for j in range(componentes):
                if(i==j):
                    element=0
                else:
                    element=random.randint(0,100)
                matriz[i][j]=element
                matrizwidgets[i][j].delete(0,tk.END)
                matrizwidgets[i][j].insert(0,element)
    eleccion='A'

def clickFlujoBoton():
    if(entrydestino.get()!="" and entryorigen.get()!=""):
        elementoorigen=entryorigen.get()
        norigen = int(elementoorigen)
        elementodestino=entrydestino.get()
        ndestino=int(elementodestino)
        matrizfinal=np.zeros([componentes,componentes])
        for i in range(componentes):
            for j in range(componentes):
                valor=int(matrizwidgets[i][j].get())
                if(valor<0 or valor>100):
                    matrizfinal[i][j]=0
                matrizfinal[i][j]=valor
        print(matrizfinal)
        grafo=crear_grafo_desde_matriz(matrizfinal)
        flujomaximo=encontrar_flujo_maximo(grafo,norigen,ndestino)
        print(f"Flujo Maximo",flujomaximo)
        flmax=str(flujomaximo)
        mostrar_grafo(grafo,flmax) 

def crear_grafo_desde_matriz(matriz):
    G = nx.DiGraph()
    n = len(matriz)
    for i in range(n):
        G.add_node(i)
        for j in range(n):
            if i != j and matriz[i][j] > 0:  # Evitar arcos de vuelta
                G.add_edge(i, j, capacity=matriz[i][j])
    return G

def encontrar_flujo_maximo(grafo, fuente, destino):
    from networkx.algorithms.flow import shortest_augmenting_path
    flujo_maximo, flujo = nx.maximum_flow(grafo, fuente, destino,flow_func=shortest_augmenting_path)
    return flujo_maximo

def mostrar_grafo(G,flujomaximo):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Nueva Ventana")
    nueva_ventana.geometry("1015x575")
    nueva_ventana.config(bg="grey11")
    frame_nuevo=tk.Frame(master=nueva_ventana)
    frame_nuevo.pack(side=tk.LEFT)
    fig, ax = plt.subplots() 
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold', font_color='black')
    edge_labels = {(u, v): d['capacity'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3)
    canvas = FigureCanvasTkAgg(fig, master=nueva_ventana)
    canvas.get_tk_widget().pack()
    toolbar=NavigationToolbar2Tk(canvas,pack_toolbar=False)
    toolbar.update()
    toolbar.pack()
    canvas.draw()
    plt.title("Flujo maximo: "+ flujomaximo)



def reiniciar():
    global matrizwidgets
    for fila in matrizwidgets:
     for entrada in fila:
       entrada.grid_remove()
    matrizwidgets = []
    entryElement.delete(0,tk.END)
    entryElement.config(state=tk.NORMAL)
    botonElement.config(state=tk.ACTIVE)
    botonManual.config(state=tk.DISABLED)
    botonAleatorio.config(state=tk.DISABLED)
    entryorigen.delete(0,tk.END)
    entrydestino.delete(0,tk.END)
    entryorigen.config(state="disabled")
    entrydestino.config(state="disabled")
    botonFlujo.config(state=tk.DISABLED)




window=tk.Tk()
window.title("Red de Flujos | Flujo Maximo")
window.geometry("1015x575")
window.resizable(height=False,width=False)
window.config(bg="grey11")
label=tk.Label(window,text="Red de Flujos | Flujo Maximo",foreground="purple3",bg="grey11",font=("Cascadia Code",20))
label.pack()
frame=tk.Frame(master=window)
frame.config(bg="grey13")
frame.pack(pady=15,padx=68,fill="both",expand=True)
frameLabel=tk.Frame(master=frame)
frameLabel.pack()
label = tk.Label(master=frameLabel, text="Tamaño de la Matriz:", font=("Cascadia Code",20), bg="grey13", fg="white")
label.grid(row=1, column=1)

global matrizwidgets
matrizwidgets=[]

frameEntryBoton=tk.Frame(master=frame,bg="grey13")
frameEntryBoton.pack()
entryElement = tk.Entry(master=frameEntryBoton)
entryElement.grid(row=0, column=0, padx=10, pady=20)
botonElement = tk.Button(master=frameEntryBoton, text="OK",command=getElementos)
botonElement.grid(row=0, column=1, padx=10,pady=20)
botonreiniciar=tk.Button(master=frameEntryBoton, text="Reiniciar",command=reiniciar)
botonreiniciar.grid(row=0, column=2, padx=10,pady=20)
frameLabelGn=tk.Frame(master=frame,bg="grey13")
frameLabelGn.pack()
labelGeneracion=tk.Label(master=frameLabelGn,text="Seleccione la opcion que desee:", font=("Cascadia Code",12), bg="grey13", fg="white")
labelGeneracion.grid(row=0,column=1,padx=10,pady=5)

global matriz
matriz = np.zeros([5, 5])

frameManualAleatorio=tk.Frame(master=frame,bg="grey13")
frameManualAleatorio.pack()
frameMatriz=tk.Frame(master=frame,bg="grey13")
frameMatriz.pack(side=tk.LEFT,padx=(30,0))
botonManual = tk.Button(master=frameManualAleatorio, text="Manualmente",command=eleccionManual,state=tk.DISABLED)
botonManual.grid(row=2, column=0, padx=10, pady=(10, 15))
botonAleatorio = tk.Button(master=frameManualAleatorio, text="Aleatorio",command=eleccionAleatoria,state=tk.DISABLED)
botonAleatorio.grid(row=2, column=3, padx=10, pady=(10, 15))
frameBotonFlujo=tk.Frame(master=frame,bg="grey13")
frameBotonFlujo.pack(side=tk.RIGHT,padx=(0,10))
labelorigen=tk.Label(master=frameBotonFlujo,text="Origen:",bg="#007FFF")
labelorigen.pack(pady=5)
entryorigen=tk.Entry(master=frameBotonFlujo,width=10,state="disabled")
entryorigen.pack(pady=5)
labeldestino=tk.Label(master=frameBotonFlujo,text="Destino:",bg="darkgoldenrod1")
labeldestino.pack(pady=5)
entrydestino=tk.Entry(master=frameBotonFlujo,width=10,state="disabled")
entrydestino.pack(pady=5)
botonFlujo=tk.Button(master=frameBotonFlujo,text="Flujo Maximo",height=5,command=clickFlujoBoton,state="disabled")
botonFlujo.pack(side=tk.RIGHT,pady=5,padx=30)

window.mainloop()