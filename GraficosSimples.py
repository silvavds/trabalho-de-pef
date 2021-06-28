# Import packages
#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
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
ax_Cortante = fig.add_axes([0.3, 0.70, 0.4, 0.05])
ax_Cortante.spines['top'].set_visible(True)
ax_Cortante.spines['right'].set_visible(True)

ax_Forca = fig.add_axes([0.3, 0.77, 0.4, 0.05])
ax_Forca.spines['top'].set_visible(True)
ax_Forca.spines['right'].set_visible(True)

ax_Cortante2 = fig.add_axes([0.3, 0.84, 0.4, 0.05])
ax_Cortante2.spines['top'].set_visible(True)
ax_Cortante2.spines['right'].set_visible(True)

ax_Forca2 = fig.add_axes([0.3, 0.91, 0.4, 0.05])
ax_Forca2.spines['top'].set_visible(True)
ax_Forca2.spines['right'].set_visible(True)

# Create sliders

s_Cortante = Slider(ax=ax_Cortante, label=f'Posição {0}', valmin=0, valmax=10.0, valinit=5.0, valfmt=' %1.1f m', facecolor='#cc7000')
s_Forca = Slider(ax=ax_Forca, label=f'Força {0}', valmin=1, valmax=5, valinit=5, valfmt=' %i N', facecolor='#cc7000')
s_Cortante2 = Slider(ax=ax_Cortante2, label=f'Posição {1}', valmin=0, valmax=10.0, valinit=5.0, valfmt=' %1.1f m', facecolor='#cc7000')
s_Forca2 = Slider(ax=ax_Forca2, label=f'Força {1}', valmin=1, valmax=5, valinit=5, valfmt=' %i N', facecolor='#cc7000')


# Plot default data
x = np.linspace(0, 10, 100)
Ef_0 = 5
T_0 = 10
y = cortante(x, Ef_0, T_0)
f_d, = ax.plot(x, y, linewidth=2.5)

# Update values
def update(val):
    p1 = s_Cortante.val
    f1 = s_Forca.val
    parte1 = cortante(x, p1, f1)
    p2 = s_Cortante2.val
    f2 = s_Forca2.val
    parte2 = cortante(x, p2, f2)
    f_d.set_data(x, cortanteResultante(parte1,parte2))
    fig.canvas.draw_idle()

s_Cortante.on_changed(update)
s_Forca.on_changed(update)
s_Cortante2.on_changed(update)
s_Forca2.on_changed(update)
    
# Set axis labels
ax.set_xlabel('Posição (m)')
ax.set_ylabel('Força')

plt.show()