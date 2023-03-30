import numpy as np
import matplotlib.pyplot as plt
import data_processing
import Clustering_algorithm
# i = 0 : 'easy' / i = 1 : 'medium'
# i = 2 : 'hard' / i = 3 : 'extrahard'

# CHOOSE THE LEVEL BY COMMENT/ UNCOMMENT

espace = data_processing.data_processing(r"C:\Users\Matthieu\Documents\GitHub\Blunomy_PALANCHON_Matthieu\files\lidar_cable_points_easy.parquet")
# espace = data_processing("C:\files\lidar_cable_points_medium.parquet")
# espace = data_processing("C:\files\lidar_cable_points_hard.parquet")
# espace = data_processing("C:\files\lidar_cable_points_extrahard.parquet")

epsilon = [0.7,0.3,0.7,0.7,0.5]
distance = [0.7,0.2,0.3,0.3,0.4]

def figure_clustering_plane(espace, i, bool):
    e = epsilon[i]
    d = distance[i]
    cluster= Clustering_algorithm.clusters(espace, e,d)
    
    if (i == 3):
        cluste= Clustering_algorithm.clusters(espace, e, d)
        clust = cluste[1]
        cluster = Clustering_algorithm.clusters(clust, epsilon[4], distance[4])
        cluster.append(cluste[0])

    if (bool):
        for k in range (len(cluster)):
            clust = cluster[k]
            tabx = np.array([clust[i][0] for i in range (len(clust))])
            taby = np.array([clust[i][1] for i in range (len(clust))])
            plt.scatter(tabx,taby)
        plt.show()

    return cluster


figure_clustering_plane(espace, 0, True)
# figure_clustering_plane(espace, 1, True)
# figure_clustering_plane(espace, 2, True)
# figure_clustering_plane(espace, 3, True)