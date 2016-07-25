import numpy as np

def generate_data_for_logistic(n):
    x1 = np.random.uniform(0,10,n)
    y1 = np.random.randn(n)+5
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
            t.append(0)

    return s,t

def generate_data_for_linear_regression(n):
    x = np.linspace(0,10,n)
    xx = []
    yy = []
    for i in x:
        xx.append([i])
    y = 2*x+np.random.randn(1)
    for i in y:
        yy.append(i)
    return xx,yy

def sigmoid(x):
    return 1/(1+np.exp(-x))

class linear_regression():
    def __init__(self, sample, target):
        self.theta = [0.0]*len(sample[0])
        self.sample = sample
        self.target = target

    def grad_descend(self, step, n):
        for j in range(n):
            tmp = [0.0]*len(self.sample[0])
            for i in range(len(self.sample)):
                xi = self.sample[i]
                yi = self.target[i]
                h_theta = np.dot(np.array(self.theta).reshape(1,len(self.theta)),np.array(xi).reshape(len(xi),1))
                tmp += (yi-h_theta)*xi
            print "error"
            print tmp
            print self.theta
            self.theta = self.theta + step*tmp
            print self.theta
            self.theta = self.theta[0]

    def get_result(self, testdata):
        return np.dot(np.array(self.theta).reshape(1,len(self.theta)),np.array(testdata).reshape(len(testdata),1))

class logistic_regression():
    def __init__(self, sample, target):
        self.theta = [0.0]*len(sample[0])
        self.sample = sample
        self.target = target

    def grad_descend(self, step, n):
        for j in range(n):
            tmp = [0.0]*len(self.sample[0])
            for i in range(len(self.sample)):
                xi = self.sample[i]
                yi = self.target[i]
                h_theta = sigmoid(np.dot(np.array(self.theta).reshape(1,len(self.theta)),np.array(xi).reshape(len(xi),1)))
                tmp += (yi-h_theta)*xi
            self.theta = self.theta + step*tmp
            self.theta = self.theta[0]

    def get_result(self, testdata):
        return sigmoid(np.dot(np.array(self.theta).reshape(1,len(self.theta)),np.array(testdata).reshape(len(testdata),1)))

if __name__=="__main__":
    s,t = generate_data_for_linear_regression(1000)
    #s,t = generate_data_for_logistic(100)
    print s
    print t
   
    #my_cc = logistic_regression(s,t)
    my_cc = linear_regression(s,t)
    my_cc.grad_descend(0.000005,10)
    #print my_cc.get_result([1.0120506642272276, 3.9636142132154073])
    #print my_cc.get_result([5.6188620524020401, 1.6759698608676632])
    print my_cc.get_result([1.02])
    
