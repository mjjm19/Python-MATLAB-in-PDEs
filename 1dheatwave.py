import numpy as np
import matplotlib.pyplot as plt 

# Define the basics of the rod 

h = 258                                                                   # heat diffusivity
length = 100                                                              #length of the rode
nodes = 30                                                                # imagine a discrete rod
time = 10  
dx = length / nodes                                                       #smaller dt, better precision
dt = 0.5 * dx**2 / h                                                      # formula from stability analysis of FDS
t_nodes = int(time / dt)                                                  #initialize rod

u = np.zeros(nodes) + 20                                                  #assuming that the rod is initially at 20 degrees

# Defining the first and the last element (Dirichlet b.c)
u[0] = 100
u[-1] = 100

# Visualization
 
fig, axis = plt.subplots()
pcm = axis.pcolormesh([u], cmap=plt.cm.jet, vmin = 0, vmax=100)             # u because we are dealing with a 1D rod 
plt.colorbar(pcm, ax=axis)
axis.set_ylim([-2,3])
#Simulation 

counter = 0

while counter < time :                                                        #using while loop so the iterations over every node increase till we reach the simulation 
    w = u.copy()   # making a seperate copy of the iteration 
    for i in range(1, nodes-1):                                               # compute differential scheme at each node
        u[i] = dt * h * (w[i+1]- 2 * w[i] + w[i-1]) / dx ** 2 + w[i]          #explicit finite difference scheme

    counter += dt
    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))
    
    # update u after each iteration
    pcm.set_array([u])
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)


plt.show()
