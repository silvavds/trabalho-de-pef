from operator import concat, pos
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
    tipo = None
    tamanhoBarra = 0
    
    def __init__(this, tamanhoBarra, points=100, tipo='fixo-movel'):
        this.tamanhoBarra = tamanhoBarra
        this.posicoes = np.linspace(0,tamanhoBarra,points)
        this.tipo = tipo
    
    def setTipo(this, tipo):
        this.tipo = tipo

    def addForca(this, posicao, valor):
        if posicao>this.tamanhoBarra or posicao<0:
            raise ValueError('Forca fora da barra')

        if posicao==0:
            posicao+=2/len(this.posicoes)
        if posicao==this.tamanhoBarra:
            posicao-=20/len(this.posicoes)

        updated = False
        for i in this.forcas:
            if i['posicao']==posicao:
                i['valor']+=valor
                updated = True

        if not updated:
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
        reacoes = this.reacoesApoio()
        for k in list(reacoes.keys()):
            if k=='Rva':
                concentradas.append({
                    'posicao': 0,
                    'valor': reacoes['Rva']
                })
            if k=='Rvb':
                concentradas.append({
                    'posicao': this.tamanhoBarra,
                    'valor': reacoes['Rvb']
                })
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
        reacoes = this.reacoesApoio()
        if 'Rma' in list(reacoes.keys()):
            moms.append({
                'posicao': 0,
                'valor': reacoes['Rma']
            })
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

    def getN(this):
        return np.zeros(len(this.posicoes))

    def getV(this, carga=None, cargaConcentradaPosicoes=None):
        if carga==None:
            carga, cargaConcentradaPosicoes = this.getCarga()
        pos = this.posicoes
        vetorCortante = np.zeros(len(pos))
        currentCortante = 0
        if cargaConcentradaPosicoes[0] != 0:
            currentCortante+= cargaConcentradaPosicoes[0]
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
        currentMomento += momentosConcentrados[0]
        for i in range(1, len(pos)):
            currentMomento += (0.5*(pos[i]-pos[i-1])*(cortantes[i-1]+cortantes[i]))
            currentMomento += momentosConcentrados[i]
            vetorMomento[i] = currentMomento
        return vetorMomento

    def reacoesApoio(this):
        if this.tipo == 'fixo-movel':
            somatorio = 0
            forc = copy.deepcopy(this.forcas)
            for c in this.cargasDistribuidas:
                nova = {
                    'posicao': (c['fim']+c['comeco'])/2,
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
        if this.tipo=='engaste':
            forc = copy.deepcopy(this.forcas)
            for c in this.cargasDistribuidas:
                nova = {
                    'posicao': (c['fim']+c['comeco'])/2,
                    'valor': (c['fim']-c['comeco'])*c['valor']
                }
                forc.append(nova)
            mom = copy.deepcopy(this.momentos)
            forcHor = copy.deepcopy(this.forcasHorizontais)
            reacaoVertical = 0
            reacaoHorizontal = 0
            reacaoMomento = 0
            for f in forcHor:
                reacaoHorizontal-=f
            for f in forc:
                reacaoVertical-=f['valor']
            for m in mom:
                reacaoMomento-=m['valor']
            for f in forc:
                reacaoMomento-=f['valor']*f['posicao']
            return {
                'Rha': reacaoHorizontal,
                'Rva': reacaoVertical,
                'Rma': reacaoMomento
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
    
    def plotNormal(this, normal=None):
        if normal==None:
            normal = this.getN()
        plt.figure()
        plt.plot(this.posicoes, normal, color='red')
        plt.fill_between(this.posicoes,normal, color='red', alpha=0.30)
        plt.xlabel('Posição (m)')
        plt.ylabel('Normal (N)')
        plt.title('Plot de normal em função da posição')
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