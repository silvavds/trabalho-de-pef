# Import packages
#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, TextBox
import matplotlib.gridspec as gridspec
import numpy as np

plt.style.use('seaborn')

# Fermi-Dirac Distribution
def cortante(x, posicao, forca) -> float:
    resultados = []
    for i in x:
        if i<posicao:
            resultados.append(0)
        else:
            resultados.append(forca)
    return resultados

def cortanteResultante(primeira, segunda):
    resultados = []
    for i in range(0,len(primeira)):
        resultados.append(primeira[i]+segunda[i])
    return resultados

# Temperature values
posicoes = np.linspace(0, 10, 100)

fig = plt.figure(figsize=(6, 4.5))

# Create main axis
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.2, top=0.65)

#quantasCortantes = int(input('Quantas cortantes? '))
# Create axes for sliders
gs = gridspec.GridSpec(2,2)
gs.update(left=0.3, right=0.77, bottom=0.85, top=0.98, hspace=0.1)
axes = [fig.add_subplot(gs[i,j]) for i,j in [[0,0],[0,1],[1,0],[1,1]]]

s_Cortante = TextBox(ax = axes[0], label='Posição 1', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca = TextBox(ax = axes[1], label='Força 0', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Cortante2 = TextBox(ax = axes[2], label='Posição 1', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca2 = TextBox(ax=axes[3], label='Força 1', initial='5', color='.95', hovercolor='1', label_pad=0.01)


# Plot default data
x = np.linspace(0, 10, 100)
Ef_0 = 5
T_0 = 10
y = cortante(x, Ef_0, T_0)
f_d, = ax.plot(x, y, linewidth=2.5)

# Update values

def update(val):
    p1 = float(s_Cortante.text)
    f1 = float(s_Forca.text)
    parte1 = cortante(x, p1, f1)
    p2 = float(s_Cortante2.text)
    f2 = float(s_Forca2.text)
    parte2 = cortante(x, p2, f2)
    f_d.set_data(x, cortanteResultante(parte1,parte2))
    fig.canvas.draw_idle()

s_Cortante.on_submit(update)
s_Forca.on_submit(update)
s_Cortante2.on_submit(update)
s_Forca2.on_submit(update)
    
# Set axis labels
ax.set_xlabel('Posição (m)')
ax.set_ylabel('Força')

plt.show() 
