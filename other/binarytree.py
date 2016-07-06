class node():
    def __init__(self, v, lc=None, rc=None, f=None):
        self.lc = lc
        self.rc = rc
        self.v = v
        self.f = f

class binarytree():
    def __init__(self,l):
        self.l = l
        self.num_node = 0
        self.root = None
    def build_tree(self):
        for i in self.l:
            new_node = node(i)
            if self.num_node == 0:
                self.root = new_node
            else: 
                self.insert(new_node,self.root)
            self.num_node += 1
    def insert(self, new_node, current_node):
        if new_node.v<current_node.v:
            if current_node.lc == None:
                current_node.lc = new_node
                new_node.f = current_node
            else:
                self.insert(new_node,current_node.lc)
        else:
            if current_node.rc == None:
                current_node.rc = new_node
                new_node.f = current_node
            else:
                self.insert(new_node,current_node.rc)
    def preorder(self, current_node=None):
        if current_node == None:
            current_node = self.root
        print current_node.v
        if current_node.lc != None:
            self.preorder(current_node.lc) 
        if current_node.rc != None:
            self.preorder(current_node.rc) 
    def midorder(self, current_node=None):
        if current_node == None:
            current_node = self.root
        if current_node.lc != None:
            self.midorder(current_node.lc)
        print current_node.v
        if current_node.rc != None:
            self.midorder(current_node.rc)
    def postorder(self, current_node=None):
        if current_node == None:
            current_node = self.root
        if current_node.lc != None:
            self.postorder(current_node.lc)
        if current_node.rc != None:
            self.postorder(current_node.rc)
        print current_node.v
    def search(self,v,current_node=None):
        if current_node == None:
            current_node = self.root
        if v==current_node.v:
            found = current_node
        elif v<current_node.v and current_node.lc!=None:
            found = self.search(v,current_node.lc)
        elif v>current_node.v and current_node.rc!=None:
            found = self.search(v,current_node.rc)
        return found
    def findmax(self,current_node=None):
        if current_node == None:
            current_node = self.root
        if current_node.rc!=None:
            max_value = self.findmax(current_node.rc)
        else:
            max_value = current_node.v
        return max_value
    def findmin(self,current_node=None):
        if current_node == None:
            current_node = self.root
        if current_node.lc!=None:
            min_value = self.findmin(current_node.lc)
        else:
            min_value = current_node.v
        return min_value
    def delete(self,node):
        if node.lc==None and node.rc==None:
            if node.v>node.f.v:
                node.f.rc = None
            else:
                node.f.lc = None
            node.f = None
        elif node.lc!=None:
            lcmax_v = self.findmax(node.lc)
            lcmax_node = self.search(lcmax_v)
            node.v = lcmax_node.v
            self.delete(lcmax_node)
        elif node.rc!=None:
            lcmin_v = self.findmin(node.rc)
            lcmin_node = self.search(lcmin_v)
            node.v = lcmin_node.v
            self.delete(lcmin_node)
            
            
            
        
            
        

            
if __name__=="__main__":
    l = [3,2,4,1,5,6]
    t = binarytree(l)
    t.build_tree()
    print t.num_node
    t.midorder() 
    print t.search(2)
    print t.findmax()
    t.delete(t.search(3))
    t.midorder()
