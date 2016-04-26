import numpy as np
import MySQLdb as md


def generate_data():
    feature_pool = [["rainy","cloudy","sunny"],["sad","soso","happy"],["lack","enough","most"]]
    sample = []
    target = []
    for i in range(10):
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
        if count>3:
            target.append("yes")
        else:
            target.append("no")
        sample.append(each_sample_feature)
    return sample, target

def sigmoid(x):
    return 1/(1+np.exp(-x))

def tanh(x):
    print x
    return 0.5*(np.log((1+x)/(1-x)))

def dtanh(x):
    return 1/(1.0-x**2)

def dsigmoid(x):
    return np.exp(-x)/((1+np.exp(-x))**2)

class neural_network_classifier():
    def __init__(self, dbname):
        self.con = self.create_db(dbname)
        self.input_node = []
        self.hidden_node = []
        self.output_node = []
        self.input_o = []
        self.hidden_o = []
        self.output_o = []
        self.wih = []
        self.who = []


    def create_db(self, dbname):
        con = md.connect(db=dbname,user="root",passwd="root")
        cur = con.cursor()
        cur.execute("drop table input_to_hidden_weight")
        cur.execute("drop table hidden_to_output_weight")
        cur.execute("drop table hidden")
        cur.execute("create table input_to_hidden_weight (fromid varchar(20), toid varchar(20), weight float)")
        cur.execute("create table hidden_to_output_weight (fromid varchar(20), toid varchar(20), weight float)")
        cur.execute("create table hidden (hiddenid varchar(30))")
        con.commit()
        return con


    def update_weight(self, table, fromid, toid, weight):
        cur = self.con.cursor()
        cur.execute('select weight from {} where (fromid = "{}" and toid = "{}")'.format(table, fromid, toid))
        result = cur.fetchone()
        if result == None:
            cmd = "insert into {} (fromid, toid, weight) values ('{}', '{}', '{}')".format(table, fromid, toid, weight)
        else:
            cmd = "update {} set weight = '{}' where (fromid = '{}' and toid = '{}')".format(table, weight, fromid, toid)
        cur.execute(cmd)
        self.con.commit()


    def get_weight(self, table, fromid, toid):
        cur = self.con.cursor()
        cmd = "select weight from {} where (fromid = '{}' and toid = '{}')".format(table, fromid, toid)
        cur.execute(cmd)
        result = cur.fetchone()
        if result == None:
            result = 0
        else: 
            result = result[0]
        return float(result)

    def generate_hidden(self, each_sample, each_target):
        hiddenid = '_'.join(each_sample)
        cur = self.con.cursor()
        cmd = 'select hiddenid from hidden where hiddenid="{}"'.format(hiddenid)
        cur.execute(cmd)
        result = cur.fetchone()
        if result == None:
            cmd = 'insert into hidden (hiddenid) values ("{}")'.format(hiddenid)
            cur.execute(cmd)
            for i in each_sample:
                self.update_weight('input_to_hidden_weight',i,hiddenid,1/float(len(each_sample)))
            for j in each_target:
                self.update_weight('hidden_to_output_weight',hiddenid,j,0.1)

    def activate_hidden(self, each_sample, targets):
        cur = self.con.cursor()
        hidden_actived = []
        for i in each_sample:
            cmd = "select toid from input_to_hidden_weight where fromid='{}'".format(i)
            cur.execute(cmd)
            result = cur.fetchall()
            for j in result:
                hidden_actived.append(j[0])
        for i in targets:
            cmd = "select fromid from hidden_to_output_weight where toid='{}'".format(i)
            cur.execute(cmd)
            result = cur.fetchall()
            for j in result:
                hidden_actived.append(j[0])
        hidden_actived = list(set(hidden_actived))
        return hidden_actived


    def get_weight_list(self, each_sample, targets):
        self.input_node = each_sample
        self.hidden_node = self.activate_hidden(each_sample, targets)
        self.output_node = targets

        self.input_o = np.array([1.0]*len(self.input_node))
        self.hidden_o = np.array([1.0]*len(self.hidden_node))
        self.output_o = np.array([1.0]*len(self.output_node))

        print self.input_node
        print self.hidden_node
        print self.output_node

        self.wih = np.array([[self.get_weight('input_to_hidden_weight',j,i) for i in self.hidden_node] for j in self.input_node])
        self.who = np.array([[self.get_weight('hidden_to_output_weight',j,i) for i in targets] for j in self.hidden_node])

 
    def forward(self):

        self.hidden_o = np.tanh(np.dot(self.input_o.reshape(1,len(self.input_o)), self.wih))[0]
        #self.hidden_o = sigmoid(np.dot(self.input_o.reshape(1,len(self.input_o)), self.wih))[0]
        self.output_o = np.tanh(np.dot(self.hidden_o.reshape(1,len(self.hidden_o)), self.who))[0]
        #self.output_o = sigmoid(np.dot(self.hidden_o.reshape(1,len(self.hidden_o)), self.who))[0]
        print self.input_o
        print self.hidden_o
        print self.output_o
        return self.output_o

    def bp(self, targets, step=0.5):
        #output error
      
        output_error = np.array(targets)-self.output_o
        
        output_delta = dtanh(self.output_o) * output_error
        #output_delta = dsigmoid(self.output_o) * output_error

        #hidden error
        
        hidden_error =  np.dot(self.who , output_delta.reshape(len(output_delta),1))
        hidden_delta = dtanh(self.hidden_o)*hidden_error
        #hidden_delta = dsigmoid(self.hidden_o)*hidden_error
        hidden_delta = hidden_delta[0]


        whochange = step* np.dot(self.hidden_o.reshape(len(self.hidden_o),1),output_delta.reshape(1,len(output_delta)))
        self.who = self.who+whochange

        wihchange = step*np.dot(self.input_o.reshape(len(self.input_o),1),hidden_delta.reshape(1,len(hidden_delta)))
        self.wih = self.wih+ wihchange

        
        

    def train_nn(self, sample, target, select):
        self.generate_hidden(sample, target)
        self.get_weight_list(sample, target)
        self.forward()
        targets = [0.0]*len(target)
        targets[target.index(select)]=1.0
        self.bp(targets)
        self.update_db()

    def update_db(self):
        for i in range(len(self.input_node)):
            for j in range(len(self.hidden_node)):
                self.update_weight('input_to_hidden_weight',self.input_node[i],self.hidden_node[j],self.wih[i][j])

        for i in range(len(self.hidden_node)):
            for j in range(len(self.output_node)):
                self.update_weight('hidden_to_output_weight',self.hidden_node[i],self.output_node[j],self.who[i][j])

    def get_result(self, sample, target):
        self.get_weight_list(sample,target)
        return self.forward()

        
    
        
        
        
        
if __name__=="__main__":
    sample, target = generate_data()
    my_nn = neural_network_classifier('test')
    #my_nn.update_weight('hidden_to_output_weight','1','2','10')
    #my_nn.update_weight('input_to_hidden_weight','1','2','10')
    alltarget = list(set(target))
    for i in range(len(sample)):
        es = sample[i]
        et = target[i]
        
        my_nn.generate_hidden(es,alltarget)
        my_nn.get_weight_list(es,alltarget)
        my_nn.train_nn(es,alltarget,et)
    #print my_nn.get_result(["cloudy","soso","enough"],alltarget)
    print my_nn.get_result(["sunny","sad","lack"],alltarget)
    #print my_nn.forward()
#    print my_nn.predict(["sunny","happy","more"])


