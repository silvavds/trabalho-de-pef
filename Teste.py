from Solver1D import Solver1D
from matplotlib import pyplot as plt

solver = Solver1D(10,10000)
#solver.addForca(7,-5)
#solver.addForca(3,10)
#solver.addCargaDistribuida(1,3,5)
solver.addCargaDistribuida(0,2,3)
solver.addCargaDistribuida(3,5,5)
solver.addForca(7,10)
solver.plotCarga()
solver.plotCortante()
solver.plotMomentos()
#solver.addForca(3,2)
solver.addMomento(8,50)

print(solver.reacoesApoio())