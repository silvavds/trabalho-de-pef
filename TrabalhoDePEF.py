import tkinter as tk

forceList = []
beamList = []
loadList = []

root = tk.Tk()
root.title("Trabalho de PEF")

structureFrame = tk.LabelFrame(root,text="Estrutura",labelanchor="n")
elementManipulationFrame = tk.LabelFrame(root,text="Cargas e barras",padx=130,pady=200,labelanchor="n")
diagramFrame = tk.LabelFrame(root,text="Diagramas de N,V e M",labelanchor="n")

diagram = tk.Canvas(structureFrame,width=800,height=800)
diagram.create_line(0,400,800,400,width=5, arrow=tk.LAST)
diagram.create_line(400,0,400,800,width=5, arrow=tk.FIRST)

diagram.grid(row=0,column=0)

def alreadyInList(List, Element):
    for x in List:
        if x == Element: 
            return True
    return False

def showForces():
    for i in range(len(forceList)):
        Label =tk.Label(elementManipulationFrame,text=str(forceList[i]))
        Label.grid(row=i,column=4)
        
def addForce(entryOne, entryTwo, entryThree, entryFour):
    global forceList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),float(entryThree.get()),float(entryFour.get())]
    if (alreadyInList(forceList,values)== False): 
        forceList.append(values)
        diagram.create_line(400+values[0],400-values[1],400+values[0]+values[2],400-values[3]-values[1],activewidth=3,fill="blue",width=2,arrow=tk.LAST)
        root.update()
        
def addBeam(entryOne, entryTwo, entryThree, entryFour):
    global beamList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),float(entryThree.get()),float(entryFour.get())]
    if (alreadyInList(beamList,values)== False): 
        beamList.append(values)
        diagram.create_line(400+values[0],400-values[1],400+values[2],400-values[3],activewidth=4,fill="red",width=2)
        root.update()
    
def transladar(values):
    D = values[4]
    x_1 = values[0]
    y_1 = values[1]
    Hip = (x_1**2+y_1**2)**(1/2)
    
    x_2 = y_1*D/Hip
    y_2 = x_1*D/Hip
    return [x_1,y_1,x_2,y_2]
    
    
def addLoad(entryOne, entryTwo, entryThree, entryFour,entryFive):
    global loadList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),float(entryThree.get()),float(entryFour.get()),float(entryFive.get())]
    if (alreadyInList(loadList,values)== False): 
        loadList.append(values)
        diagram.create_line(400+values[0],400-values[1],400+values[2],400-values[3],activewidth=4,fill="green",width=2)
        newValues = transladar(values)
        diagram.create_line(400+newValues[0],400-newValues[1],400+newValues[2],400+newValues[3],activewidth=4,fill="green",width=2)
        root.update()


def concentratedForceWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações da Força")
    tk.Label(top,text="Insira as especificações da Força").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Aplicação X",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Aplicação Y",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Intensidade na direção X",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Intensidade na direção Y",labelanchor="n",padx=50,pady=20)
    
    entryOne = tk.Entry(frameOne)
    entryTwo = tk.Entry(frameTwo)
    entryThree = tk.Entry(frameThree)
    entryFour = tk.Entry(frameFour)
    
    insertButton = tk.Button(top,text="Adicionar força",padx=200,pady=20,command=lambda: addForce(entryOne,entryTwo,entryThree,entryFour))
    
    frameOne.grid(row=1,column=0)
    frameTwo.grid(row=1,column=1)
    frameThree.grid(row=2,column=0)
    frameFour.grid(row=2,column=1)


    entryOne.grid(row=1,column=0)
    entryTwo.grid(row=1,column=0)
    entryThree.grid(row=1,column=0)
    entryFour.grid(row=1,column=0)
    
    entryOne.insert(0,"0")
    entryTwo.insert(0,"0")
    entryThree.insert(0,"0")
    entryFour.insert(0,"0")
    
    insertButton.grid(row=3,column=0,columnspan=2)

def loadWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações da Carga Distribuida")
    tk.Label(top,text="Insira as especificações da Carga Distribuida").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Início X",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Início Y",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Coordenada de Fim X",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Coordenada de Fim Y",labelanchor="n",padx=50,pady=20)
    frameFive = tk.LabelFrame(top, text="Valor (Constante)",labelanchor="n",padx=200,pady=20)
    
    entryOne = tk.Entry(frameOne)
    entryTwo = tk.Entry(frameTwo)
    entryThree = tk.Entry(frameThree)
    entryFour = tk.Entry(frameFour)
    entryFive = tk.Entry(frameFive)
    
    insertButton = tk.Button(top,text="Adicionar Carga",padx=200,pady=20,command=lambda: addLoad(entryOne,entryTwo,entryThree,entryFour,entryFive))
    
    frameOne.grid(row=1,column=0)
    frameTwo.grid(row=1,column=1)
    frameThree.grid(row=2,column=0)
    frameFour.grid(row=2,column=1)
    frameFive.grid(row=3,column=0,columnspan=2)

    entryOne.grid(row=1,column=0)
    entryTwo.grid(row=1,column=0)
    entryThree.grid(row=1,column=0)
    entryFour.grid(row=1,column=0)
    entryFive.grid(row=1,column=0)
    
    entryOne.insert(0,"0")
    entryTwo.insert(0,"0")
    entryThree.insert(0,"0")
    entryFour.insert(0,"0")
    entryFive.insert(0,"0")
    
    insertButton.grid(row=4,column=0,columnspan=2)
    
    
def beamWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações da Barra")
    tk.Label(top,text="Insira as especificações da Barra").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Início X",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Início Y",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Coordenada de Fim X",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Coordenada de Fim Y",labelanchor="n",padx=50,pady=20)
    
    entryOne = tk.Entry(frameOne)
    entryTwo = tk.Entry(frameTwo)
    entryThree = tk.Entry(frameThree)
    entryFour = tk.Entry(frameFour)
    
    insertButton = tk.Button(top,text="Adicionar barra",padx=200,pady=20,command=lambda: addBeam(entryOne,entryTwo,entryThree,entryFour))
    
    frameOne.grid(row=1,column=0)
    frameTwo.grid(row=1,column=1)
    frameThree.grid(row=2,column=0)
    frameFour.grid(row=2,column=1)


    entryOne.grid(row=1,column=0)
    entryTwo.grid(row=1,column=0)
    entryThree.grid(row=1,column=0)
    entryFour.grid(row=1,column=0)
    
    entryOne.insert(0,"0")
    entryTwo.insert(0,"0")
    entryThree.insert(0,"0")
    entryFour.insert(0,"0")
    
    insertButton.grid(row=3,column=0,columnspan=2)
    
    
def Clicked2():
    pass

newForceButton = tk.Button(elementManipulationFrame,text="Criar nova Força",padx=50,pady=10,command=concentratedForceWindow,bg="#ef000f")
showForceButton = tk.Button(elementManipulationFrame,text="Mostrar Forças",padx=50,pady=10,command=Clicked2,bg="#ef000f")

newLoadButton = tk.Button(elementManipulationFrame,text="Criar nova Carga",padx=50,pady=10,command=loadWindow,bg="#ef000f")
showLoadButton = tk.Button(elementManipulationFrame,text="Mostrar Cargas",padx=50,pady=10,command=Clicked2,bg="#ef000f")

newBeamButton = tk.Button(elementManipulationFrame,text="Criar Barra",padx=50,pady=10,command=beamWindow,bg="#ef000f")
showBeamButton = tk.Button(elementManipulationFrame,text="Mostrar Barras",padx=50,pady=10,command=Clicked2,bg="#ef000f")


structureFrame.grid(row=0,column=0,rowspan=2)
elementManipulationFrame.grid(row=0,column=1)
diagramFrame.grid(row=1,column=1)


newForceButton.grid(row=0,column=0)
showForceButton.grid(row=0,column=1)
newLoadButton.grid(row=1,column=0)
showLoadButton.grid(row=1,column=1)
newBeamButton.grid(row=2,column=0)
showBeamButton.grid(row=2,column=1)

root.mainloop()