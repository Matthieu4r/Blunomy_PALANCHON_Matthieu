import numpy as np
import matplotlib.pyplot as plt
import data_processing
import cluster_plane
from scipy import vectorize
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression

# i = 0 : 'easy' / i = 1 : 'medium'
# i = 2 : 'hard' / i = 3 : 'extrahard'

# CHOOSE THE LEVEL BY COMMENT/ UNCOMMENT

espace = data_processing.data_processing(r"C:\Users\Matthieu\Documents\GitHub\Blunomy_PALANCHON_Matthieu\files\lidar_cable_points_easy.parquet")
# espace = data_processing("C:\files\lidar_cable_points_medium.parquet")
# espace = data_processing("C:\files\lidar_cable_points_hard.parquet")
# espace = data_processing("C:\files\lidar_cable_points_extrahard.parquet")

epsilon = [0.7,0.3,0.7,0.7,0.5]
distance = [0.7,0.2,0.3,0.3,0.4]

# we implement the orthogonal projections on the affine approximation for a straight line y = a*x + b
def p_x(x0,y0, a, b):
    return (a*y0 - a*b - b*x0)/(a**2 -b )

def p_y(x0,y0, a, b):
    return a*(a*y0 - a*b - b*x0)/(a**2 -b ) + b

def proj_x(tab):
    return tab[0]

# if bool == True, we plot the figures
def plot_2D(espace,i, bool):
    parameters = []

    coef = []
    # we make the clustering
        
    e = epsilon[i]
    d = distance[i]
    cluster= cluster_plane.figure_clustering_plane(espace, i, False)

    for k in range (len(cluster)):
        clust = cluster[k]
        # we make the linear regression in the plane 'xy'. We assume that the plane is vertical.
        x = np.array([clust[i][0] for i in range (len(clust))]).reshape((len(clust),1))
        y = np.array([clust[i][1] for i in range (len(clust))])
        reg = LinearRegression().fit(x, y)
        
        # we print the score of the linear regression
        
        print('Score = ' + str(reg.score(x,y)) + ' . The approximation by a vertical plane is relevant.')

        a = reg.coef_[0]

        b=reg.intercept_

        coef.append([a,b])

        # we make the projection
        intermediaire = np.array([[p_x(x[i], y[i], a, b), p_y(x[i], y[i], a, b) ] for i in range(len(x))])
        tx = np.array([intermediaire[i][0] for i in range(len(intermediaire))])
        ty = np.array([intermediaire[i][1] for i in range(len(intermediaire))])

        # we pass to the coordinates of the plane
        # we merge x and y into a single coordinate starting from 0
        x_max = max(tx)
        y_min = min (ty)

        tabx=np.array([0. for i in range(len(intermediaire))])
        for i in range (len(intermediaire)):
            tabx[i] = np.sqrt((ty[i] - y_min)**2 + (tx[i] -x_max)**2)
    
        # we define the model function
        def f(x,x0,y0,c):
            return y0 + c*((np.exp((x-x0)/c)+ np.exp(-(x-x0)/c))*0.5 - 1)
        # we vectorize the function
        f_vect = vectorize(f)
        tabz =np.array([clust[i][2] for i in range (len(clust))])
        params, params_cov = curve_fit(f_vect,tabx,tabz,p0=np.array([1.,1.,1.]))

        if (bool):
            # we scatter the projected points
            plt.scatter(tabx,tabz)

            # we plot the catenary function
            tab_int = np.array([[tabx[i], f(tabx[i],params[0],params[1],params[2])] for i in range (len(tabx))])
            tab_int = sorted(tab_int, key =proj_x)
            list_x = np.array([tab_int[i][0] for i in range (len(tab_int))])
            list_z = np.array([tab_int[i][1] for i in range (len(tab_int))])
            plt.plot(list_x, list_z, 'r')
            plt.show()
        parameters.append([params[0], params[1], params[2]])

    return parameters, coef, cluster

plot_2D(espace, 0, True)
# plot_2D(espace, 1, True)
# plot_2D(espace, 2, True)
# plot_2D(espace, 3, True)


