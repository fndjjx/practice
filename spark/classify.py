from pyspark import SparkConf,SparkContext
from pyspark.mllib.regression import LabeledPoint 
import numpy as np

from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.tree import DecisionTree



def readdata():
    data = sc.textFile("ml-100k/u.user")
    user_fields = data.map(lambda x:x.split("|"))
    
    age = user_fields.map(lambda x:float(x[1]))
    print age.collect()
    print age.distinct().collect()
    agearray = np.array(age.collect())
    print np.mean(agearray)

def generate_data():
    feature_pool = [["rainy","cloudy","sunny"],["sad","soso","happy"],["lack","enough","most"]]
    sample = []
    for i in range(100):
        each_sample = []
        each_sample_feature = []
        count = 0
        for j in range(len(feature_pool)):
            r = np.random.uniform(0,1)
            if r>0 and r<0.33:
                s = 0
            elif 0.33<r<0.66:
                s = 1
            else:
                s = 2
            each_sample_feature.append(feature_pool[j][s])
            count += s
        each_sample.append(each_sample_feature)
        if count>3:
            each_sample.append("yes")
        else:
            each_sample.append("no")
        sample.append(each_sample)
    return sample


def classify(sc, sample):
    def ff(x):
        newsample = []
        nl = ["rainy","sad","lack"]
        ml = ["cloudy","soso","enough"]
        pl = ["sunny","happy","most"]
        for i in x:
            if i in nl:
                newsample.append(0)
            elif i in ml:
                newsample.append(1)
            elif i in pl:
                newsample.append(2)
        return newsample

    f = lambda x:1 if x=="yes" else 0
    traindata = sc.parallelize(sample).map(lambda x:(ff(x[0]),f(x[1]))) 
    traindata = traindata.map(lambda x:LabeledPoint(x[1],x[0]))
    testdata = traindata.first()
    print testdata

    ######
#    print "logistic"
#    lrModel = LogisticRegressionWithSGD.train(traindata, 10)
#    prediction = lrModel.predict(testdata.features)
#    print prediction
    

    #####
#    print "svm"
#    svmModel = SVMWithSGD.train(traindata, 10)
#    prediction = svmModel.predict(testdata.features)
#    print prediction
#
#
#    ####
#    print "naive bayes"
#    nbModel = NaiveBayes.train(traindata)
#    prediction = nbModel.predict(testdata.features)
#    print prediction
#
#
#    ####
    print "decesion tree"
    detreeModel = DecisionTree.trainClassifier(traindata, 2, {})
    prediction = detreeModel.predict(testdata.features)
    print prediction


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("myapp")
    sc = SparkContext(conf=conf)
    sample = generate_data()
    classify(sc,sample)
