import numpy as np
import matplotlib.pyplot as plt 

# Define the infos of the rod 

h = 258                                                                 # heat diffusivity
length = 100                                                            #length of the rode
nodes = 30                                                              # imagine a discrete rod
time = 10  
dx = length / nodes                                                     #smaller dt, better precision
dy = length / nodes
dt = min(dx**2 / (4*h), dy**2 / (4*h))                                  # formula from stability analysis of FDS
t_nodes = int(time / dt)                                                #initialoze rod

u = np.zeros((nodes, nodes)) + 20                                         #assuming that the rod is initially at 20 degrees
# Defining the first and the last element (Dirichlet b.c)
u[0, :] = 100
u[-1, :] = 100

# Visualization
 
fig, axis = plt.subplots()
pcm = axis.pcolormesh(u, cmap=plt.cm.jet, vmin = 0, vmax=100)           # u because we are dealing with a 1D rod 
plt.colorbar(pcm, ax=axis)

#Simulation 

counter = 0

while counter < time :                                                  #using while loop so the iterations over every node increase till we reach the simulation 
    w = u.copy()                                                        # making a seperate copy of the iteration 
    for i in range(1, nodes-1):
        for j in range(1, nodes-1):                                     # compute differential scheme at each node

            dd_ux = (w[i-1, j] - 2 * w[i,j] + w[i+1,j]) / dx ** 2       #explicit finite difference scheme
            dd_uy = (w[i, j-1] - 2 * w[i,j] + w[i,j+1]) / dx ** 2  
            u[i,j] = dt * h * (dd_ux + dd_uy) + w[i,j]                  #explicit finite difference scheme

    counter += dt
    print("t: {:.3f} [s], Average temperature: {:.2f} Celcius".format(counter, np.average(u)))
    
    # update u after each iteration
    pcm.set_array(u)
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)


plt.show()