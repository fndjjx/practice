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
    print sample
    print target
    return sample, target

def sigmoid(x):
    return 1/(1+np.exp(-x))


def dtanh(x):
    return 1-x**2

class neural_network_classifier():
    def __init__(self, dbname, sample, target):
        self.con = self.create_db(dbname)
        self.sample = sample
        self.target = target
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
            self.update_weight('hidden_to_output_weight',hiddenid,each_target,0.1)
 
    def forward(self, each_sample, targets):
        def activate_hidden(each_sample, targets):
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

        def get_weight_list(each_sample, targets):
            self.input_node = each_sample
            self.hidden_node = activate_hidden(each_sample, targets)
            self.output_node = targets
            
            self.input_o = np.array([1.0]*len(self.input_node))
            self.hidden_o = np.array([1.0]*len(self.hidden_node))
            self.output_o = np.array([1.0]*len(self.output_node))


            self.wih = np.array([[self.get_weight('input_to_hidden_weight',i,j) for i in self.input_node] for j in self.hidden_node])
            self.who = np.array([[self.get_weight('hidden_to_output_weight',i,j) for i in self.hidden_node] for j in targets])


        get_weight_list(each_sample, targets)
        self.hidden_o = sigmoid(np.dot(self.wih, self.input_o))
        self.output_o = sigmoid(np.dot(self.who, self.hidden_o))
        return self.output_o

    def bp(self, targets, step=1):
        output_error = np.array(targets)-self.output_o
        output_delta = dtanh(self.output_o) * output_error
        whochange = step* np.dot(output_delta.reshape(len(output_delta),1),self.hidden_o.reshape(1,len(self.hidden_o)))
        self.who = self.who-whochange

        tmp =  np.mat(self.who).I * output_delta.reshape(len(output_delta),1)
        tmp1 = []
        for i in tmp:
            tmp1.append(float(i[0]))
        hidden_error = np.array(tmp1)- self.hidden_o
        hidden_delta = dtanh(self.hidden_o)*hidden_error
        wihchange = step*np.dot(hidden_delta.reshape(len(hidden_delta),1),self.input_o.reshape(1,len(self.input_o)))
        self.wih = self.wih - wihchange

        
        

    def train_nn(self):
        all_targets = list(set(self.target))
        for i in range(len(self.sample)):
            each_sample = self.sample[i]
            each_target = self.target[i]
            self.generate_hidden(each_sample, each_target)
            self.forward(each_sample, all_targets)
            sign_target = []
            for i in all_targets:
                if i == each_target:
                    sign_target.append(1)
                else:
                    sign_target.append(0)
            print sign_target
            self.bp(sign_target)
            self.update_db()

    def update_db(self):
        for i in range(len(self.hidden_node)):
            for j in range(len(self.input_node)):
                self.update_weight('input_to_hidden_weight',self.input_node[j],self.hidden_node[i],self.wih[i,j])

        for i in range(len(self.output_node)):
            for j in range(len(self.hidden_node)):
                self.update_weight('hidden_to_output_weight',self.hidden_node[j],self.output_node[i],self.who[i,j])

    def predict(self, testdata):
        all_targets = list(set(self.target))
        return self.forward(testdata,all_targets)

        
    
        
        
        
        
if __name__=="__main__":
    sample, target = generate_data()
    my_nn = neural_network_classifier('test', sample, target)
    #my_nn.update_weight('hidden_to_output_weight','1','2','10')
    #my_nn.update_weight('input_to_hidden_weight','1','2','10')
    #my_nn.generate_hidden(['cloudy','happy','enough'],['yes'])
    #print my_nn.get_weight('hidden_to_output_weight','cloudy_happy_enough','yes')
    #print my_nn.get_weight('hidden_to_output_weight','cloudy_happy_enough','no')
    my_nn.train_nn()
    print my_nn.predict(["cloudy","soso","enough"])


