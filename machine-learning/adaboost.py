import sklearn
from sklearn.linear_model import LogisticRegression
import numpy as np
from linear_regression import logistic_regression

def generate_data(n):
    x1 = np.random.uniform(0,10,n)
    y1 = np.random.randn(n)+0.3
    s1 = zip(x1,y1)
    x2 = np.random.uniform(0,10,n)
    y2 = np.random.randn(n)
    s2 = zip(x2,y2)
    s = s1+s2
    t = []
    for i in s:
        if i in s1:
            t.append(1)
        else:
            t.append(-1)

    return s,t

def weak_clf(sample,target):
    clf = logistic_regression(sample,target)
    clf.grad_descend(0.02,10)
    result = []
    for i in range(len(sample)):
        result.append(clf.get_result(sample[i]))
    print result
    count = 0
    for i in range(len(target)):
        if target[i]==result[i]:
            count+=1
    return count/float(len(target))

def strong_clf(sample,target,k):
    mya = adaboost(sample,target,k)
    mya.build_adaboost()
    result = []
    for i in range(len(sample)):
        if mya.predict(sample[i])>0:
            result.append(1)
        else:
            result.append(-1)
    count = 0
    for i in range(len(target)):
        if target[i]==result[i]:
            count+=1
    return count/float(len(target))

class adaboost():
    def __init__(self, sample, target, k):
        self.sample = sample
        self.target = target
        self.sample_weight = [1.0/len(self.sample)]*len(self.sample)
        self.clf = []
        self.alpha = []
        self.k = k


    def weak_model(self, sample,target):
        clf = LogisticRegression()
        clf.fit(sample,target)
        return clf


    def weak_model_predict_error(self, clf, sample, target, weight):
        count = 0
        result = [] 
        for i in range(len(sample)):
            predict = clf.predict(sample[i])[0] 
            result.append(predict)
            if predict != target[i]:
                count += 1*weight[i]
        return count,result

    def normalize(self, data):
        return map(lambda x:x/float(sum(data)), data)

    def build_adaboost(self):
        for i in range(self.k):
            clf = self.weak_model(self.sample,self.target,self.sample_weight)
            clf_error,predict_result = self.weak_model_predict_error(clf,self.sample,self.target,self.sample_weight)
            print clf_error
            if clf_error==0:
                break
            alpha = 0.5*np.log((1-clf_error)/clf_error)
            self.clf.append(clf)
            self.alpha.append(alpha)
            for i in range(len(predict_result)):
                if predict_result[i]==self.target[i]:
                    self.sample_weight[i]=self.sample_weight[i]*np.exp(-alpha)
                else:
                    self.sample_weight[i]=self.sample_weight[i]*np.exp(alpha)
            print self.sample_weight
            self.sample_weight = self.normalize(self.sample_weight)


    def predict(self,testdata):
        single_predict_result = []
        for i in range(len(self.clf)):
            single_predict_result.append(self.clf[i].predict(testdata)[0])
        return np.sum(np.array(single_predict_result)*np.array(self.alpha))

        
           
            
if __name__=="__main__":
    sample,target = generate_data(10)
    print "weak"
    print weak_clf(sample,target)
    print strong_clf(sample,target,3)










            
