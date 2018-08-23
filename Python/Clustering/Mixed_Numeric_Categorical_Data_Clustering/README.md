## How do we apply k-means clustering algorithm for mixed data-numeric and categorical?
-------------
-------------
The standard k-means algorithm isn't directly applicable to categorical data, for various reasons. The sample space for categorical data is discrete and a Euclidean distance function on that space is not.
Categorical data is a problem for most algorithms in machine learning. Suppose, for example, you have some categorical variable called "color" that could take on the values red, blue, or yellow. If we simply encode these numerically as 1,2, and 3 respectively, our algorithm will think that red (1) is closer to blue (2) than it is to yellow (3). We need to use a representation that lets the computer understand that these things are all equally different. One simple way is to use what's called a one-hot representation. Rather than having one variable like "color" that can take on three values, we separate it into three variables. These would be "color-red," "color-blue," and "color-yellow," which all can only take on the value 1 or 0. This approach however, increases the dimensionality of the space, but now use of any clustering algorithm is possible. 

You should not use k-means clustering on a dataset containing mixed datatypes. Rather, there are several clustering algorithms that can appropriately handle mixed datatypes. Some possibilities include:
1. __Partitioning-based algorithms__: k-Prototypes
2. __Hierarchical algorithms__: ROCK, Agglomerative single, average, and complete linkage
3. __Density-based algorithms__: HIERDENC, MULIC, CLIQUE
4. __Model-based algorithms__: SVM clustering, Self-organizing maps

Here we will use the [k-prototypes algorithm](https://github.com/nicodv/kmodes#id4) that combines [k-modes](https://link-springer-com.stanford.idm.oclc.org/article/10.1007/s00357-001-0004-3) and [k-means](https://en.wikipedia.org/wiki/K-means_clustering) and demonstrate its usage for clustering mixed numerical and categorical data.

