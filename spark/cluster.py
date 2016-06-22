from pyspark import SparkConf,SparkContext
from pyspark.mllib.regression import LabeledPoint
import numpy as np


from pyspark.mllib.clustering import KMeans
from pyspark.mllib.clustering import GaussianMixture


def generate_data(n):
    sample = []
    for i in range(n):
        x = np.random.randn(n)+5*i
        y = np.random.randn(n)+5*i
        sample.extend(zip(x,y))
    return sample


def cluster(sc,sample):
    sample = sc.parallelize(sample)
    testdata = sc.parallelize([5,5])

    ######
#    kmeansmodel = KMeans.train(sample,3)

#    print kmeansmodel.centers
#    print kmeansmodel.predict([5,5])



    gmmmodel = GaussianMixture.train(sample,3,maxIterations=10)

#    print gmmmodel.weights
    print gmmmodel.predict(testdata)



if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("myapp")
    sc = SparkContext(conf=conf)
    sample = generate_data(3)
    cluster(sc,sample)

