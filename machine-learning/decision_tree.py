import numpy as np
import MySQLdb as md


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
    print sample
    return sample


class node():

    def __init__(self, cur, tablename, nodeid, conditions, val, rc='NULL', fc='NULL'):
        self.nodeid = nodeid
        self.tablename = tablename
        self.cur = cur
        self.conditions = conditions
        self.val = val
        self.rc = rc
        self.fc = fc
        self.create_node_db()

    def create_node_db(self):
        cmd = 'insert into {} (nodeid, conditions, val, rc, fc) values ({}, "{}", "{}", "{}", "{}")'.format(self.tablename, self.nodeid, str(self.conditions), str(self.val), str(self.rc), str(self.fc))
        print cmd
        cur.execute(cmd)

def entropy(data):
    data = np.array(data)
    target_list = list(data[:,-1])
    target_set = set(target_list)
    e = []
    for i in target_set:
        count = 0
        for j in target_list:
            if i == j:
                count += 1
        p = count/float(len(target_list))
        e.append(-p*np.log2(p))
    return sum(e)

def divide(data, col, value):
    data = np.array(data)
    feature_list = list(data[:,0])
    set1 = []
    set2 = []
    for i in range(len(feature_list)):
        if isinstance(feature_list[i][col],float):
            if feature_list[i][col]<value:
                set1.append(data[i])
            else:
                set2.append(data[i])
        else:
            if feature_list[i][col]==value:
                set1.append(data[i])
            else:
                set2.append(data[i])

    return set1,set2

def unique_feature(data):
    data = np.array(data)
    feature_list = list(data[:,0])
    feature_list = np.array(feature_list)
    unique_feature = []
    for i in range(len(feature_list[0])):
        each_feature_choice = feature_list[:,i]
        unique_feature.append((i,list(set(list(each_feature_choice)))))
    return unique_feature

def unique_result(data):
    data = np.array(data)
    result = list(data[:,1])
    return list(set(result))


def build_tree(cur, tablename, sample, nodeid = '0'):
    ent = entropy(sample)
    unique = unique_feature(sample)
    best_gain = 0
    criteria = []
    lc = []
    rc = []
         
    for i in unique:
        col = i[0]
        for v in i[1]:
            set1,set2 = divide(sample, col, v)
            if len(set1)>0 and len(set2)>0:
                p = float(len(set1))/len(sample)
                gain = ent - p*entropy(set1) - (1-p)*entropy(set2)
                if gain>best_gain:
                    best_gain = gain
                    criteria = [col, v]
                    lc = set1
                    rc = set2
    if best_gain>0:
        current_node = node(cur, tablename, nodeid, criteria[0], criteria[1], nodeid+'1', nodeid+'2')
        build_tree(cur,tablename,lc,nodeid+'1')
        build_tree(cur,tablename,rc,nodeid+'2')
    else:
        current_node = node(cur, tablename, nodeid, "NULL", "NULL", unique_result(sample)[0], unique_result(sample)[0])
        
        
def get_result(cur, tablename, testdata):
    cur.execute('select val from {} where nodeid=0'.format(tablename))
    val =  cur.fetchone()[0]
    nodeid = "0"
    while val!="NULL":
        cur.execute('select conditions from {} where nodeid={}'.format(tablename,nodeid))
        condition =  int(cur.fetchone()[0])
        cur.execute('select val from {} where nodeid={}'.format(tablename,nodeid))
        val =  cur.fetchone()[0]
        if testdata[condition]==val:
            nodeid = nodeid+"1" 
        else:
            nodeid = nodeid+"2" 
        cur.execute('select val from {} where nodeid={}'.format(tablename,nodeid))
        val =  cur.fetchone()[0]
    cur.execute('select rc from {} where nodeid={}'.format(tablename,nodeid))
    result =  cur.fetchone()[0]
    return result

    
    
                

if __name__ == "__main__":

    con = md.connect(db='test',user='root',passwd='root') 
    cur = con.cursor()
    cur.execute('drop table testnode')
    cur.execute('create table testnode (nodeid varchar(20), conditions varchar(20), val varchar(20), rc varchar(20), fc varchar(20))')
    sample = generate_data()
    build_tree(cur,'testnode',sample)
    con.commit()
    print get_result(cur,'testnode',['cloudy','happy','enough'])
    cur.close()
    con.close()
