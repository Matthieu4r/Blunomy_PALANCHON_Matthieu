import catenary_2D
import numpy as np
import data_processing
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d 
import catenary_2D
from scipy.optimize import curve_fit
from scipy import vectorize
from sklearn.linear_model import LinearRegression
# CHOOSE THE LEVEL BY COMMENT/ UNCOMMENT


espace = data_processing.data_processing(r"C:\Users\Matthieu\Documents\GitHub\Blunomy_PALANCHON_Matthieu\files\lidar_cable_points_easy.parquet")
# espace = data_processing("C:\files\lidar_cable_points_medium.parquet")
# espace = data_processing("C:\files\lidar_cable_points_hard.parquet")
# espace = data_processing("C:\files\lidar_cable_points_extrahard.parquet")

def f(x,x0,y0,c):
    return y0 + c*((np.exp((x-x0)/c)+ np.exp(-(x-x0)/c))*0.5 - 1)


def plot_3D(espace, i):
    parameters, coef, cluster= catenary_2D.plot_2D(espace, i, False)
    for k in range (len(cluster)):
        fig = plt.figure()
        x0, y0, c = parameters[k]
        a, b = coef[k]
        clust = cluster[k]
        ax = fig.add_subplot(projection='3d')
        # we make the linear regression in the plane 'xy'. We assume that the plane is vertical.
        x = np.array([clust[i][0] for i in range (len(clust))])
        y = np.array([clust[i][1] for i in range (len(clust))])
        z = np.array([clust[i][2] for i in range (len(clust))])
        
        ax.scatter(x, y, z, label='data')
        #we pass to the coordinates of the plane
        intermediaire = np.array([[catenary_2D.p_x(x[i], y[i], a, b), catenary_2D.p_y(x[i], y[i], a, b) ] for i in range(len(x))])
        tx = np.array([intermediaire[i][0] for i in range(len(intermediaire))])
        ty = np.array([intermediaire[i][1] for i in range(len(intermediaire))])
        x_max = max(tx)
        y_min = min (ty)

        tabx=np.array([0. for i in range(len(intermediaire))])
        for i in range (len(intermediaire)):
            tabx[i] = np.sqrt((ty[i] - y_min)**2 + (tx[i] -x_max)**2)

        f_vect = np.vectorize(f)
        params, paramcov = curve_fit(f_vect,tabx,z,p0=np.array([1.,1.,1.]))
        x0, y0, c = params
        tz = np.array([f(x, x0, y0, c) for x in tabx])
        t = np.array([[tx[i], ty[i], tz[i]] for i in range(len(tz))])
        t = sorted(t, key =catenary_2D.proj_x)
    
        tx = np.array([t[i][0] for i in range(len(intermediaire))])
        ty = np.array([t[i][1] for i in range(len(intermediaire))])
        tz = np.array([t[i][2] for i in range(len(intermediaire))])
        ax.plot(tx, ty, tz, label='model', color =  'r', linewidth=4) 
        plt.show()
        




plot_3D(espace, 0)
# plot_3D(espace, 1)
# plot_3D(espace, 2)
# plot_3D(espace, 3)