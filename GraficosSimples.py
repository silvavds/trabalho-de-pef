# Import packages
#%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, TextBox
import matplotlib.gridspec as gridspec
import numpy as np
from Funcoes import Funcoes

plt.style.use('seaborn')

# Temperature values
posicoes = np.linspace(0, 10, 100)

fig = plt.figure(figsize=(6, 4.5))
figCortante = plt.figure(figsize=(6, 4.5))
figMomento = plt.figure(figsize=(6, 4.5))

# Create main axis
ax = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.2, top=0.65)
axCortante = figCortante.add_subplot(111)
axCortante.set_xlabel('Posição (m)')
axCortante.set_ylabel('Cortante (N)')
axMomento = figMomento.add_subplot(111)
axMomento.set_xlabel('Posição (m)')
axMomento.set_ylabel('Momento (N.m)')
#figMomento.subplots_adjust(bottom=0.2, top=0.65)

#quantasForcas = int(input('Quantas forças? (1 <= F <= 4): '))
# Create axes for sliders
gs = gridspec.GridSpec(4,2)
gs.update(left=0.3, right=0.77, bottom=0.85, top=0.98, hspace=0.1)
#axes = [fig.add_subplot(gs[i,j]) for i,j in [[0,0],[0,1],[1,0],[1,1]]]
axes = [fig.add_subplot(gs[i,j]) for i,j in [[0,0],[0,1],[1,0],[1,1],[2,0],[2,1],[3,0],[3,1]]]

s_Cortante = TextBox(ax = axes[0], label='Posição 0', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca = TextBox(ax = axes[1], label='Força 0', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Cortante2 = TextBox(ax = axes[2], label='Posição 1', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca2 = TextBox(ax=axes[3], label='Força 1', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Cortante3 = TextBox(ax = axes[4], label='Posição 2', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca3 = TextBox(ax=axes[5], label='Força 2', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Cortante4 = TextBox(ax = axes[6], label='Posição 3', initial='5', color='.95', hovercolor='1', label_pad=0.01)
s_Forca4 = TextBox(ax=axes[7], label='Força 3', initial='5', color='.95', hovercolor='1', label_pad=0.01)


ClasseDeForcas = Funcoes()
ClasseDeForcas.addForca(posicao=5, valor=5)
ClasseDeForcas.addForca(posicao=5, valor=5)
ClasseDeForcas.addForca(posicao=5, valor=5)
ClasseDeForcas.addForca(posicao=5, valor=5)

# Plot default data
x = np.linspace(0, 10, 100)
y = ClasseDeForcas.getCortante(x)
y2 = ClasseDeForcas.getMomento(x,y)
f_d, = ax.plot(x, np.zeros(len(x)), linewidth=2.5, color='black')
global f_q1, fq_2
f_q1 = ax.quiver([5], [0], [0], [2], angles='xy', scale_units='xy', scale=1)
f_q2 = ax.quiver([5], [0], [0], [2], angles='xy', scale_units='xy', scale=1)
ax.set_ylim([-5,5])

f_c, = axCortante.plot(x,y,linewidth=2.5)
f_e, = axMomento.plot(x, y2, linewidth=2.5)

# Update values

def update(val):
    global f_q1, f_q2
    p1 = float(s_Cortante.text)
    f1 = float(s_Forca.text)
    #parte1 = cortante(x, p1, f1)
    p2 = float(s_Cortante2.text)
    f2 = float(s_Forca2.text)
    #parte2 = cortante(x, p2, f2)
    #ClasseDeForcas = Funcoes()
    ClasseDeForcas.forcas = []
    ClasseDeForcas.addForca(p1,f1)
    ClasseDeForcas.addForca(p2,f2)

    f_q1.set_UVC(U=0, V=0)
    f_q1 = ax.quiver([p1], [0], [0], [2], angles='xy', scale_units='xy', scale=1)
    f_q2.set_UVC(U=0, V=0)
    f_q2 = ax.quiver([p2], [0], [0], [2], angles='xy', scale_units='xy', scale=1)

    resultante = ClasseDeForcas.getCortante(x)
    f_d.set_data(x, np.zeros(len(x)))
    f_c.set_data(x, resultante)
    f_e.set_data(x, ClasseDeForcas.getMomento(x, resultante))
    fig.canvas.draw_idle()
    figCortante.canvas.draw_idle()
    figMomento.canvas.draw_idle()
    
    ax.relim()
    ax.autoscale_view()
    ax.set_ylim([-5,5])
    
    axCortante.relim()
    axCortante.autoscale_view()

    axMomento.relim()
    axMomento.autoscale_view()

s_Cortante.on_submit(update)
s_Forca.on_submit(update)
s_Cortante2.on_submit(update)
s_Forca2.on_submit(update)
    
# Set axis labels
ax.set_xlabel('Posição (m)')
#ax.set_ylabel('Força (N)')

plt.show() 
