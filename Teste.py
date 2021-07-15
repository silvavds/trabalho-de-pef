from Solver1D import Solver1D
from matplotlib import pyplot as plt

solver = Solver1D(10,10000,tipo='fixo-movel')
solver.addCargaDistribuida(1.5,2.5,5)
solver.addCargaDistribuida(4,6,8)
solver.addCargaDistribuida(6,8,10)
solver.addForcaHorizontal(50)

solver.addForca(2,10)
solver.addForca(4,-10)
solver.addMomento(7,10)

print(solver.reacoesApoio())
solver.plotCarga()
solver.plotNormal()
solver.plotCortante()
solver.plotMomentos()
solver.setTipo('engaste')
solver.plotCarga()
solver.plotNormal()
solver.plotCortante()
solver.plotMomentos()
#solver.addForca(3,2)
#solver.addMomento(8,50)