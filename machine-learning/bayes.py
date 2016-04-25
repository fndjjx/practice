import numpy as np

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

def bayes_classifier(sample, testdata):
    def calc_cat_count(sample):
        target_list = list(np.array(sample)[:,1])
        target_set = set(target_list)
        cat_count = {}
        for i in target_set:
            s = 0
            for j in target_list:
                if j == i:
                    s+=1
            cat_count[i] = float(s)

        return cat_count
 
    def calc_feature_count(sample):
        feature_list = list(np.array(sample)[:,0])
        target_list = list(np.array(sample)[:,1])
        target_set = set(target_list)
        feature_set = set(reduce(lambda x,y:np.hstack((x,y)),list(np.array(sample)[:,0])))
         
        feature_count = {}
        for i in feature_set:
            feature_count[i] = {}
            for k in target_set:
                feature_count[i][k] = 0
            for j in range(len(feature_list)):
                if i in feature_list[j]:
                    feature_count[i][target_list[j]] += 1 
                     
        print feature_count
        return feature_count

    def predict(cat_count, feature_count, testdata):
        cat_pro = {}
        s = 0
        for k,v in cat_count.iteritems():
            s += v
        for k,v in cat_count.items():
            cat_pro[k] = float(v)/s

        print cat_pro
        testdata_cat_pro = {}
        for k in cat_pro.keys():
            pfc = 1
            for j in testdata:
                pfc *= feature_count[j][k]/cat_count[k]
            testdata_cat_pro[k] = pfc*cat_pro[k]

        return testdata_cat_pro

    def uniform(data):
        pro = {}
        s = 0
        for k,v in data.iteritems():
            s += v
        for k,v in data.items():
            pro[k] = float(v)/s

        return pro
                

      
    cat_count = calc_cat_count(sample)
    print cat_count
    feature_count = calc_feature_count(sample)
    print feature_count
    result =  predict(cat_count, feature_count, testdata)
    return uniform(result)
                

if __name__=="__main__":

    data = generate_data()
    print data
    print bayes_classifier(data,["sunny","happy","enough"])
            

            
    
