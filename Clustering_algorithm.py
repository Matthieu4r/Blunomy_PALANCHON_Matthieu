from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# this algorithm adds the points which are outside of already build clusters and 
# close to the to the line constructed by linear regression on the current cluster to less than distance
def prox_line(espace,not_taken, clust, distance, stack):
    #We make a lienar regression of the current point in the cluster
    changed = False
    x = np.array([clust[i][0] for i in range (len(clust))]).reshape((len(clust),1))
    y = np.array([clust[i][1] for i in range (len(clust))])
    reg = LinearRegression().fit(x, y)
    a = reg.coef_[0]
    b = reg.intercept_
    
    
    # we add the point close to the straight line
    count = 0
    for i in range(len(not_taken)):
        i = i - count
        x = espace[not_taken[i]][0]
        y = espace[not_taken[i]][1]
        if (np.abs(y - a*x-b)< distance):
            clust.append(espace[not_taken[i]])
            stack.append(not_taken[i])
            not_taken.remove(not_taken[i])
            count = count + 1
            changed = True
    # changed tells if points have been added in the cluster by the function
    return not_taken, clust, stack, changed

# this algorithm makes it possible to test the elements
# added to the cluster to find the points close to less than epsilon
def empty_stack(espace, not_taken, clust, epsilon, stack):
    while (len(stack) > 0):
        point = stack.pop()
        count = 0
        for i in range(len(not_taken)):
            i = i - count 
            if (dist(espace[point], espace[not_taken[i]]) < epsilon):
                clust.append(espace[not_taken[i]])
                stack.append(not_taken[i])
                not_taken.remove(not_taken[i])
                count = count + 1
    return not_taken, clust, stack


# We need a fonction which calculates the distance between two points
def dist(x,y):
    return np.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)

# We can now implement the clustering algorithm
def clusters(espace, epsilon, distance):
    #1st step : initialization
    clusters = []
    not_taken = []
    # clust is the current cluster
    clust = []
    clust.append(espace[0])
    stack = [0]
    #stack contains the point added to the cluster whose neighborhood has not yet been checked
    # we add the points close to the initialization point to less than epsilon
    for i in range(len(espace)):
        if (dist(espace[0], espace[i]) < epsilon):
            clust.append(espace[i])
            stack.append(i)
        else:
            not_taken.append(i)
    stack.remove(0)

    changed = True
    #while there is changes in the clusters (ie while points are added in the cluster), the stack is emptied
    # and we search for points close to the linear regression of the cluster
    while (changed):
        not_taken, clust, stack = empty_stack(espace, not_taken, clust, epsilon, stack)
        not_taken, clust, stack, changed = prox_line(espace,not_taken, clust, distance, stack)
    
    clusters.append(clust)

    # we make the same thing for the rest of the points, which leads to several clusters
    while (len(not_taken) > 0):
        clust=[]
        first = not_taken[0]
        clust.append(espace[first])
        point = first
        stack = [first]
        
        not_taken, clust, stack = empty_stack(espace, not_taken, clust, epsilon, stack)
                
        not_taken, clust, stack,changed = prox_line(espace,not_taken, clust, distance, stack)
        changed = True
    
        while (changed):
            not_taken, clust, stack = empty_stack(espace, not_taken, clust, epsilon, stack)
            not_taken, clust, stack, changed = prox_line(espace,not_taken, clust, distance, stack)

        clusters.append(clust)
    
    return clusters
