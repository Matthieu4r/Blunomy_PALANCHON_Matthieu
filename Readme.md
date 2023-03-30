You may have to change the path of the files to make sure it works.

. The 'data_processing.py' file is responsible for retrieving point data.

. I decided to implement a clustering algorithm suitable for close lines. For this, the algorithm works in several steps:

First step, initialization: I put the first element in a cluster. Then I look at all the points close to less than epsilon of this point: I add them to the cluster. I put the unselected points in 'not_taken' to work with them later. I put the selected points in a pile.

Second step: for each element of the stack, I add in the cluster all the points of not_taken close to less than epsilon and I update the stack.

3rd step: I do a linear regression on the points of the considered cluster. I then add to the cluster the points at less distance from the line obtained.

4th step: I empty the stack like step 2 (empty_stack function)

5th step: I repeat steps 3 and 4 until convergence (no element is added). (prox_line function)

Step 6: I take an item from not_taken, put it in a new cluster, and start over.

I continue until not_taken is empty.

.The 'cluster_plane.py' file performs the clustering of the dataset in the plan and displays the clusters.

. catenary_2D does the clustering on the data, giving as input an integer i corresponding to the file: 1 = easy, 2 = medium, 3 = hard, 4 = extrahard.

I made the linear regression in the plane 'xy'. I assumed that the plane is vertical.

If on input bool = True, then the function returns the comparison between the catenary points and the catenary model.

It does not wor very well for medium due to the proximoity of the points.

. The 'catenary_3D.py' file resumes the results of clustering and displays in 3 dimensions the points and the model chain.