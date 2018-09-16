<<<<<<< HEAD:Clustering/Mixed_Numeric_Categorical_Data_Clustering/README.md
### How do we apply k-means clustering algorithm for mixed numeric and categorical data?
-------------
The standard k-means algorithm isn't directly applicable to categorical data, for various reasons. The sample space for categorical data is discrete and a Euclidean distance function on that space is not.
Categorical data is a problem for most algorithms in machine learning. Suppose, for example, you have some categorical variable called __"color"__ that could take on the values red, blue, or yellow. If we simply encode these numerically as 1,2, and 3 respectively, our algorithm will think that red __(1)__ is closer to blue __(2)__ than it is to yellow __(3)__. We need to use a representation that lets the computer understand that these things are all equally different. One simple way is to use what's called a one-hot representation. Rather than having one variable like "color" that can take on three values, we separate it into three variables. These would be "color-red," "color-blue," and "color-yellow," which all can only take on the value 1 or 0. This approach however, increases the dimensionality of the space, but now use of any clustering algorithm is possible. 


You should not use k-means clustering on a dataset containing mixed datatypes. Rather, there are several clustering algorithms that can appropriately handle mixed datatypes.


Here we will use the [k-prototypes algorithm](https://github.com/nicodv/kmodes#id4) that combines [k-modes](https://link-springer-com.stanford.idm.oclc.org/article/10.1007/s00357-001-0004-3) and [k-means](https://en.wikipedia.org/wiki/K-means_clustering) and demonstrate its usage for clustering mixed numerical and categorical data.

=======
### How do we apply k-means clustering algorithm for mixed numeric and categorical data?
-------------
The standard k-means algorithm isn't directly applicable to categorical data, for various reasons. The main reason is that the sample space for categorical data is discrete and a Euclidean distance function on that space is not.
Having categorical data is pretty common and sometimes a challenge in most of algorithms in machine learning. Suppose, for example, we have some categorical variable called __"car model"__ that could take on the values BMW, Honda, or Toyota. If we simply encode these variables numerically as 1,2, and 3 respectively, our algorithm will think that BMW __(1)__ is closer to Honda __(2)__ than it is to Toyota __(3)__. However, we need to use a representation that lets the computer understand that these things are all equally different. One simple way is to use what's called a _one-hot_ representation. Rather than having one variable like __"car type"__ that can take on three values, we separate it into three variables. These would be "cartype-BMW," "cartype-Honda," and "cartype-Toyota," which all can only take on the value 1 or 0. This approach however, increases the dimensionality of the space, but now use of any clustering algorithm is possible. 


We should not use k-means clustering on a dataset containing mixed datatypes. Rather, there are several clustering algorithms that can appropriately handle mixed datatypes.


Here we will use the k-prototypes algorithm that combines [k-modes](https://link-springer-com.stanford.idm.oclc.org/article/10.1007/s00357-001-0004-3) and [k-means](https://en.wikipedia.org/wiki/K-means_clustering) and demonstrate its usage for clustering mixed numerical and categorical data.

>>>>>>> 2dbff4d2457e3fdb57df4f08adcafa86d1ae0b78:Python/Clustering/Mixed_Numeric_Categorical_Data_Clustering/README.md
