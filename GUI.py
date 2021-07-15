import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Solver1D import Solver1D


forceList = []
beamList = []
loadList = []
reactionList = []
momentumList = []
resultantes = []

solver = ''

root = tk.Tk()
root.title("Trabalho de PEF")

fig = Figure(figsize=(5.5,4), dpi=100)
fig.add_subplot(111)

structureFrame = tk.LabelFrame(root,text="Estrutura",labelanchor="n")
elementManipulationFrame = tk.LabelFrame(root,text="Cargas e barras",padx=100,pady=10,labelanchor="n")
diagramFrame = tk.LabelFrame(root,text="Diagramas de esforços solicitantes",padx=10,pady=10,labelanchor="n")


canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
canvas.draw()
canvas.get_tk_widget().grid(row=0,column=0,columnspan=3)


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

def addMomentum(entryOne,entryTwo,entryThree):
    global momentumList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),float(entryThree.get())]
    x = values[0]
    y = values[1]
    z = values[2]
    if (alreadyInList( momentumList,values)== False): 
        momentumList.append(values)
        diagram.create_oval(400+x-10,400-y+10,400+x+10,400-y-10)
        if(z <0): diagram.create_line(400+x-0.01+3,400-y-4*np.sqrt(10/2),400+x+0.01+3,400-y-4*np.sqrt(10/2),arrow=tk.LAST)
        elif(z>0): diagram.create_line(400+x-0.01-3,400-y-4*np.sqrt(10/2),400+x+0.01-3,400-y-4*np.sqrt(10/2),arrow=tk.FIRST)
        root.update()
        
def addBeam(entryOne, entryTwo, entryThree, entryFour):
    global beamList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),float(entryThree.get()),float(entryFour.get())]
    if (alreadyInList(beamList,values)== False): 
        beamList.append(values)
        diagram.create_line(400+values[0],400-values[1],400+values[2],400-values[3],activewidth=4,fill="blue",width=2)
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
    if (alreadyInList(loadList,values)== False and values[4] != 0): 
        loadList.append(values)
        a = values[0]
        b = -values[1]
        c = +values[2]
        d =-values[3]

        if( c-a != 0):
            e = a
            g = c
            f= -40+b
            h= -40+d
            diagram.create_line(400+a,400+b,400+c,400+d,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+a,400+b, 400+e,400+f,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+c,400+d, 400+g,400+h,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+e,400+f, 400+g,400+h,activewidth=4,fill="blue",width=2)
            
            i =0
            if(values[4] >0):
                arrow = tk.LAST
            elif (values[4] < 0):
                arrow = tk.FIRST
                
                
            while i <= abs(c-a):
                diagram.create_line(400+a+i,400+b, 400+e+i,400+f,activewidth=3,fill="blue",width=1,arrow=arrow)
                i += 20
       
        elif(c-a == 0):
            f= b
            h= d
            e= 40+a
            g= 40+c
            diagram.create_line(400+a,400+b,400+c,400+d,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+a,400+b, 400+e,400+f,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+c,400+d, 400+g,400+h,activewidth=4,fill="blue",width=2)
            diagram.create_line(400+e,400+f, 400+g,400+h,activewidth=4,fill="blue",width=2)
            i =0
            if(values[4] >0):
                arrow = tk.LAST
            elif (values[4] < 0):
                arrow = tk.FIRST
                
            while i <= abs(d-b):
                diagram.create_line(400+c,400+d+i, 400+g,400+h+i,activewidth=3,fill="blue",width=1,arrow=arrow)
                i += abs(d-b)/4
            

        root.update()

def desenhaApoio(x,y):
    global diagram
    diagram.create_polygon([400+x,400-y,400+x-20,400-y+20,400+x+20,400-y+20])
    diagram.create_oval(400+x-5,400-y+5, 400+x+5,400-y-5)
    diagram.create_oval(400+x-20,400-y+20, 400+x-5,400-y+30)
    diagram.create_oval(400+x+5,400-y+20, 400+x+20,400-y+30)
    root.update()
    
    
def desenhaArticulacao(x,y):
    global diagram
    diagram.create_polygon([400+x,400-y,400+x-20,400-y+20,400+x+20,400-y+20])
    diagram.create_oval(400+x-5,400-y+5, 400+x+5,400-y-5)
    diagram.create_line(400+x-20,400-y+25, 400+x+20,400-y+25)
    
    
def desenhaEngaste(x,y):
    global diagram
    diagram.create_line(400+x-20,400-y, 400+x+20,400-y)
    i = -20
    while(i <= 20):
        diagram.create_line(400+x+i,400-y, 400+x+i,400-y+10)
        i +=4
        
        
def desenhaEngasteVert(x,y):
    global diagram
    diagram.create_line(400+x,400-y-20, 400+x,400-y+20)
    i = -20
    while(i <= 20):
        diagram.create_line(400+x,400-y+i, 400+x-10,400-y+i)
        i +=4

    
def addReaction(entryOne,entryTwo,reactionType):
    global reactionList
    global diagram
    values = [float(entryOne.get()),float(entryTwo.get()),reactionType]
    if(alreadyInList(reactionList,values) == False and len(reactionList) < 2):
        reactionList.append(values)
        if(reactionType=='AS'): desenhaApoio(values[0],values[1])
        elif(reactionType=='AD'): desenhaArticulacao(values[0],values[1])
        elif(reactionType=='ENH'): desenhaEngaste(values[0],values[1])
        elif(reactionType=='ENV'): desenhaEngasteVert(values[0],values[1])
        

def concentratedForceWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações da Força")
    tk.Label(top,text="Insira as especificações da Força").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Aplicação X (m)",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Aplicação Y (m)",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Intensidade na direção X (N)",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Intensidade na direção Y (N)",labelanchor="n",padx=50,pady=20)
    
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
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Início X (m)",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Início Y (m)",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Coordenada de Fim X (m)",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Coordenada de Fim Y (m)",labelanchor="n",padx=50,pady=20)
    frameFive = tk.LabelFrame(top, text="Intensidade (N/m)",labelanchor="n",padx=200,pady=20)
    
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
    

def momentumWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações do Momento")
    tk.Label(top,text="Insira as especificações do Momento").grid(row=0,column=0,columnspan=3)
    
    frameOne = tk.LabelFrame(top,text="Coordenada X (m)",labelanchor="n",padx=25,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada Y (m)",labelanchor="n",padx=25,pady=20)
    frameThree = tk.LabelFrame(top,text="Intensidade na direção Z (Nm)",labelanchor="n",padx=25,pady=20)

    entryOne = tk.Entry(frameOne)
    entryTwo = tk.Entry(frameTwo)
    entryThree = tk.Entry(frameThree)

    insertButton = tk.Button(top,text="Adicionar Momento",padx=100,pady=20,command=lambda: addMomentum(entryOne,entryTwo,entryThree))
    
    frameOne.grid(row=1,column=0)
    frameTwo.grid(row=1,column=1)
    frameThree.grid(row=1,column=2)


    entryOne.grid(row=0,column=0)
    entryTwo.grid(row=0,column=0)
    entryThree.grid(row=0,column=0)

    entryOne.insert(0,"0")
    entryTwo.insert(0,"0")
    entryThree.insert(0,"0")
    
    insertButton.grid(row=3,column=0,columnspan=3)
        
    

def beamWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações da Barra")
    tk.Label(top,text="Insira as especificações da Barra").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada de Início X (m)",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada de Início Y (m)",labelanchor="n",padx=50,pady=20)
    frameThree = tk.LabelFrame(top,text="Coordenada de Fim X (m)",labelanchor="n",padx=50,pady=20)
    frameFour = tk.LabelFrame(top,text="Coordenada de Fim Y (m)",labelanchor="n",padx=50,pady=20)
    
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

def reactionWindow():
    top = tk.Toplevel()
    top.title("Insira as especificações do Vinculo")
    tk.Label(top,text="Insira as especificações do Vinculo").grid(row=0,column=0,columnspan=4)
    
    frameOne = tk.LabelFrame(top,text="Coordenada X (m)",labelanchor="n",padx=50,pady=20)
    frameTwo = tk.LabelFrame(top,text="Coordenada Y (m)",labelanchor="n",padx=50,pady=20)
    
    entryOne = tk.Entry(frameOne)
    entryTwo = tk.Entry(frameTwo)
    
    apoioSimplesButton = tk.Button(top,text="Adicionar Apoio Simples",padx=60,pady=20,command=lambda: addReaction(entryOne,entryTwo,"AS"))
    apoioDuploButton = tk.Button(top,text="Adicionar Articulação",padx=60,pady=20,command=lambda: addReaction(entryOne,entryTwo,"AD"))
    engasteButton = tk.Button(top,text="Adicionar Engastamento Horizontal",padx=50,pady=20,command=lambda: addReaction(entryOne,entryTwo,"ENH"))
    engasteButtonV = tk.Button(top,text="Adicionar Engastamento Vertical",padx=50,pady=20,command=lambda: addReaction(entryOne,entryTwo,"ENV"))
    
    
    
    frameOne.grid(row=2,column=0)
    frameTwo.grid(row=2,column=1)


    entryOne.grid(row=1,column=0)
    entryTwo.grid(row=1,column=0)
    
    entryOne.insert(0,"0")
    entryTwo.insert(0,"0")
    
    apoioSimplesButton.grid(row=3,column=0)
    apoioDuploButton.grid(row=3,column=1)
    engasteButton.grid(row=4,column=0)
    engasteButtonV.grid(row=4,column=1)
    
    
def diagramaN():
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot([0,(len(solver.getPosicoes())-1)/100],[0,0])
    ax.set_xlabel('Posição (m)')
    ax.set_ylabel('Normal (N)')
    ax.set_title('Plot de normal em função da posição')
    canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,columnspan=3)
    diagramFrame.update()

def diagramaV():
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot(solver.getPosicoes(),solver.getV())
    ax.fill_between(solver.getPosicoes(),solver.getV(),alpha=0.30)
    ax.set_xlabel('Posição (m)')
    ax.set_ylabel('Cortante (N)')
    ax.set_title('Plot de cortante em função da posição')
    canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,columnspan=3)
    diagramFrame.update()

def diagramaM():
    fig.clf()
    ax = fig.add_subplot(111)
    ax.plot(solver.getPosicoes(),solver.getM())
    ax.fill_between(solver.getPosicoes(),solver.getM(),alpha=0.30)
    ax.set_xlabel('Posição (m)')
    ax.set_ylabel('Momento (N.m)')
    ax.set_title('Plot de momento em função da posição')
    canvas = FigureCanvasTkAgg(fig, master=diagramFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,column=0,columnspan=3)
    diagramFrame.update()


def resetAll():
    global forceList
    global beamList
    global loadList
    global reactionList
    global momentumList
    forceList = []
    beamList = []
    loadList = []
    reactionList = []
    momentumList = []
    diagram.delete("all")
    diagram.create_line(0,400,800,400,width=5, arrow=tk.LAST)
    diagram.create_line(400,0,400,800,width=5, arrow=tk.FIRST)

    
    
def solveAndShow():
    global forceList
    global beamList
    global loadList
    global reactionList
    global momentumList
    global solver
    
    flag = ''
    if(len(reactionList)==2):
        if(beamList[0][0] != beamList[0][2]):
            flag = 'H'
            solver = Solver1D(abs(beamList[0][0]-beamList[0][2]),int(100*int(pointsEntry.get())),'fixo-movel')
        else:
            flag = 'V'
            solver = Solver1D(abs(beamList[0][1]-beamList[0][3]),int(100*int(pointsEntry.get())),'fixo-movel')
        
        for x in forceList:
            if flag =='H':
                solver.addForca(x[0]-beamList[0][0], x[3])
            else:
                solver.addForca(x[1]-beamList[0][1], x[2])
                
        for x in loadList:
            if flag =='H':
                solver.addCargaDistribuida(x[0]-beamList[0][0],x[2]-beamList[0][0], x[4])
            else:
                solver.addCargaDistribuida(x[1]-beamList[0][1],x[3]-beamList[0][1], x[4])
        
        for x in momentumList:
            if flag =='H':
                solver.addMomento(x[0]-beamList[0][0], x[2])
            else:
                solver.addMomento(x[1]-beamList[0][1], x[2])
        myStr = "Reação Vertical na articulação em ("+str(reactionList[0][0])+",  "+ str(reactionList[0][1])+"): "+str(solver.reacoesApoio()['Rva'])+"N\n"
        myStr += "Reação Hoizontal na articulação em ("+str(reactionList[0][0])+",  "+ str(reactionList[0][1])+"): "+str(solver.reacoesApoio()['Rha'])+"N\n"
        myStr += "Reação Vertical no apoio em ("+str(reactionList[1][0])+",  "+ str(reactionList[1][1])+"): "+str(solver.reacoesApoio()['Rvb'])+"N\n"
        tk.Label(elementManipulationFrame,text=myStr).grid(row=10,column=0,columnspan=2)
        diagramaN()
    elif(len(reactionList)==1):
        if(beamList[0][0] != beamList[0][2]):
            flag = 'H'
            solver = Solver1D(abs(beamList[0][0]-beamList[0][2]),int(100*int(pointsEntry.get())),'engaste')
        else:
            flag = 'V'
            solver = Solver1D(abs(beamList[0][1]-beamList[0][3]),int(100*int(pointsEntry.get())),'engaste')
        
        for x in forceList:
            if flag =='H':
                solver.addForca(x[0]-beamList[0][0], x[3])
            else:
                solver.addForca(x[1]-beamList[0][1], x[2])
                
        for x in loadList:
            if flag =='H':
                solver.addCargaDistribuida(x[0]-beamList[0][0],x[2]-beamList[0][0], x[4])
            else:
                solver.addCargaDistribuida(x[1]-beamList[0][1],x[3]-beamList[0][1], x[4])
        
        for x in momentumList:
            if flag =='H':
                solver.addMomento(x[0]-beamList[0][0], x[2])
            else:
                solver.addMomento(x[1]-beamList[0][1], x[2])
        myStr = "Reação Vertical no Engaste em ("+str(reactionList[0][0])+",  "+ str(reactionList[0][1])+"): "+str(solver.reacoesApoio()['Rva'])+"N\n"
        myStr += "Reação Hoizontal no Engaste em ("+str(reactionList[0][0])+",  "+ str(reactionList[0][1])+"): "+str(solver.reacoesApoio()['Rha'])+"N\n"
        myStr += "Reação de momento no Engaste em ("+str(reactionList[0][0])+",  "+ str(reactionList[0][1])+"): "+str(solver.reacoesApoio()['Rma'])+"Nm\n"
        tk.Label(elementManipulationFrame,text=myStr).grid(row=10,column=0,columnspan=2)
        diagramaN()

newForceButton = tk.Button(elementManipulationFrame,text="Adicionar Força",height=2,width=23,command=concentratedForceWindow )
newLoadButton = tk.Button(elementManipulationFrame,text="Adicionar Carga",height=2,width=23,command=loadWindow )
newMomentumButton = tk.Button(elementManipulationFrame,text="Adicionar Momento",height=2,width=23,command=momentumWindow )
newBeamButton = tk.Button(elementManipulationFrame,text="Adicionar Barra",height=2,width=23,command=beamWindow )
newReactionButton = tk.Button(elementManipulationFrame, text= "Adicionar Vinculo", height=2,width=23,command=reactionWindow )
resetButton = tk.Button(elementManipulationFrame, text ="Resetar Valores",height=2,width=23, command=resetAll )
solveButton = tk.Button(elementManipulationFrame, text="Calcular Reações e Diagramas",height=2,width=23, command=solveAndShow)
pointFrame =  tk.LabelFrame(elementManipulationFrame,text="Pontos por unidade",labelanchor="n")
pointsEntry = tk.Entry(pointFrame)

normalButton = tk.Button(diagramFrame, text = "Diagrama N",height=2,width=10,command=diagramaN)
verticalButton = tk.Button(diagramFrame, text = "Diagrama V",height=2,width=10,command=diagramaV)
momentumButton =  tk.Button(diagramFrame, text = "Diagrama M",height=2,width=10,command=diagramaM)

structureFrame.grid(row=0,column=0,rowspan=2,padx=1,pady=1)
elementManipulationFrame.grid(row=0,column=1,padx=1,pady=1)
diagramFrame.grid(row=1,column=1,padx=1,pady=1)

newForceButton.grid(row=0,column=0)
newLoadButton.grid(row=0,column=1)
newMomentumButton.grid(row=1,column=0)
newBeamButton.grid(row=1,column=1)
newReactionButton.grid(row=2,column=0)
resetButton.grid(row=2,column=1)
solveButton.grid(row=3,column=0)
pointFrame.grid(row=3,column=1)
pointsEntry.grid(row=0,column=0)
pointsEntry.insert(0,"100")

normalButton.grid(row=1,column=0)
verticalButton.grid(row=1,column=1)
momentumButton.grid(row=1,column=2)

root.mainloop()

#%%
p