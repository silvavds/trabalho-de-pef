class Funcoes:
    
    forcas = []
    
    def __init__(this):
        pass

    def addForca(this, posicao, valor):
        this.forcas.append({
            'posicao': posicao,
            'valor': valor
        })
    
    def getCortante(this, x):
        resultado = None
        if hasattr(x, "__len__"):
            resultado = []
            for p in x:
                resultadoTemp = 0
                for i in this.forcas:
                    if p>=i['posicao']:
                        resultadoTemp+=i['valor']
                resultado.append(resultadoTemp)
        else: 
            resultado = 0
            for i in this.forcas:
                if x>=i['posicao']:
                    resultado+=i['valor']
        return resultado
    
    def integrar(this, x,y):
        integral = 0
        vetorIntegral = [0]
        for i in range(0,len(x)-1):
            integral+= (0.5*(x[i+1]-x[i])*(y[i]+y[i+1]))
            vetorIntegral.append(integral)
        return integral, vetorIntegral

    def getMomento(this, x, cortantes):
        integral, vetorIntegral = this.integrar(x,cortantes)
        return vetorIntegral