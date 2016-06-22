from pyspark import SparkConf,SparkContext
from pyspark.mllib.regression import LabeledPoint
import numpy as np

from pyspark.mllib.regression import LinearRegressionWithSGD
from pyspark.mllib.tree import DecisionTree

def generate_data(n):
    x = np.linspace(0,10,n)
    xx = []
    for i in x:
        xx.append([i])
    y = 2*x+np.random.randn(1)
    sample = zip(xx,y)
    return sample


def regression(sc, sample):

    traindata = sc.parallelize(sample)
    traindata = traindata.map(lambda x:LabeledPoint(x[1],x[0]))
    testdata = [8.2]
    #####
#    linear_model = LinearRegressionWithSGD.train(traindata,iterations=10)
#    prediction = linear_model.predict(testdata)
#    print prediction


    #####
    decision_model = DecisionTree.trainRegressor(traindata,{})
    prediction = decision_model.predict(testdata)
    print prediction


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("myapp")
    sc = SparkContext(conf=conf)
    sample = generate_data(20)
    print sample
    regression(sc,sample)
