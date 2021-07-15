import numpy as np
import copy
from matplotlib import pyplot as plt
plt.style.use('seaborn')
class Solver1D:
    def __init__(self):
        pass

    forcas = []
    forcasHorizontais = []
    cargasDistribuidas = []
    momentos = []
    posicoes = None
    tamanhoBarra = 0
    
    def __init__(this, tamanhoBarra, points=100):
        this.tamanhoBarra = tamanhoBarra
        this.posicoes = np.linspace(0,tamanhoBarra,points)

    def addForca(this, posicao, valor):
        if posicao>this.tamanhoBarra or posicao<0:
            raise ValueError('Forca fora da barra')
        this.forcas.append({
            'posicao': posicao,
            'valor': valor
        })

    def addForcaHorizontal(this, valor):
        this.forcasHorizontais.append(valor)
    
    def addCargaDistribuida(this, comeco, fim, valor):
        if comeco < 0 or fim > this.tamanhoBarra:
            raise ValueError('Forca fora da barra')
        this.cargasDistribuidas.append({
            'comeco': comeco,
            'fim': fim,
            'valor': valor
        })

    def addMomento(this, posicao, valor):
        if posicao>this.tamanhoBarra or posicao<0:
            raise ValueError('Momento fora da barra')
        this.momentos.append({
            'posicao': posicao,
            'valor': valor
        })
    
    def getCarga(this):
        concentradas = copy.deepcopy(this.forcas)
        distribuidas = copy.deepcopy(this.cargasDistribuidas)
        pos = this.posicoes
        for f in concentradas:
            f['aplicada'] = False
        carga = np.zeros(len(this.posicoes))
        cargaConcentradaPosicoes = np.zeros(len(this.posicoes))
        for i in range(0,len(carga)):
            for f in concentradas:
                if pos[i]>=f['posicao'] and f['aplicada']==False:
                    f['aplicada'] = True
                    carga[i] += f['valor']
                    cargaConcentradaPosicoes[i] = f['valor']
            for d in distribuidas:
                if pos[i]>=d['comeco'] and pos[i]<=d['fim']:
                    carga[i] += d['valor']
        return carga, cargaConcentradaPosicoes
    
    def getMomentos(this):
        moms = copy.deepcopy(this.momentos)
        pos = this.posicoes
        for f in moms:
            f['aplicado'] = False
        cargaMomento = np.zeros(len(this.posicoes))
        for i in range(0,len(cargaMomento)):
            for f in moms:
                if pos[i]>=f['posicao'] and f['aplicado']==False:
                    f['aplicado'] = True
                    cargaMomento[i] += f['valor']
        return cargaMomento

    def getV(this, carga=None, cargaConcentradaPosicoes=None):
        if carga==None:
            carga, cargaConcentradaPosicoes = this.getCarga()
        pos = this.posicoes
        vetorCortante = np.zeros(len(pos))
        currentCortante = 0
        for i in range(1, len(pos)):
            if cargaConcentradaPosicoes[i] != 0:
                currentCortante+= cargaConcentradaPosicoes[i]
            else:
                currentCortante += (0.5*(pos[i]-pos[i-1])*(carga[i-1]+carga[i]))
            vetorCortante[i] = currentCortante
        return -vetorCortante
    
    def getM(this, cortantes=None):
        if cortantes is None:
            cortantes = this.getV()
        pos = this.posicoes
        vetorMomento = np.zeros(len(pos))
        currentMomento = 0
        momentosConcentrados = this.getMomentos()
        for i in range(1, len(pos)):
            currentMomento += (0.5*(pos[i]-pos[i-1])*(cortantes[i-1]+cortantes[i]))
            currentMomento += momentosConcentrados[i]
            vetorMomento[i] = currentMomento
        return vetorMomento

    def reacoesApoio(this):
        somatorio = 0
        forc = copy.deepcopy(this.forcas)
        for c in this.cargasDistribuidas:
            nova = {
                'posicao': (c['fim']-c['comeco'])/2,
                'valor': (c['fim']-c['comeco'])*c['valor']
            }
            forc.append(nova)
        for i in forc:
            somatorio+=i['posicao']*i['valor']
        momentoResultante = 0
        for i in this.momentos:
            momentoResultante+=i['valor']
        Rvb = (-somatorio-momentoResultante)/this.tamanhoBarra
        somaSimples = 0
        for i in forc:
            somaSimples+=i['valor']
        Rva = -Rvb-somaSimples
        Rha = 0
        for a in this.forcasHorizontais:
            Rha -= a
        return {
            'Rva': Rva,
            'Rha': Rha,
            'Rvb': Rvb
        }
    
    def plotCarga(this, carga=None):
        if carga==None:
            carga = this.getCarga()[0]
        plt.figure()
        plt.plot(this.posicoes, carga)
        plt.fill_between(this.posicoes,carga, alpha=0.30)
        plt.xlabel('Posição (m)')
        plt.ylabel('Carga (N)')
        plt.title('Plot de carga em função da posição')
        plt.show()
    
    def plotCortante(this, cortante=None):
        if cortante==None:
            cortante = this.getV()
        plt.figure()
        plt.plot(this.posicoes, cortante, color='green')
        plt.fill_between(this.posicoes,cortante, color='green', alpha=0.30)
        plt.xlabel('Posição (m)')
        plt.ylabel('Cortante (N)')
        plt.title('Plot de cortante em função da posição')
        plt.show()

    def plotMomentos(this, momentos=None):
        if momentos==None:
            momentos = this.getM()
        plt.figure()
        plt.plot(this.posicoes, momentos, color='orange')
        plt.fill_between(this.posicoes,momentos, color='orange', alpha=0.30)
        plt.xlabel('Posição (m)')
        plt.ylabel('Momento (N.m)')
        plt.title('Plot de momento em função da posição')
        plt.show()