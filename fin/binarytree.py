import numpy as np


class tree():
    def __init__(self, steps, s0, up_pro, down_pro, xp, r):
        self.steps = steps
        self.s0 = s0
        self.up_pro = up_pro
        self.down_pro = down_pro
        self.xp = xp
        self.r = r
        self.sto_tree = np.zeros([self.steps,self.steps])
        self.sec_tree = np.zeros([self.steps,self.steps])
        self.build_sto_tree()
        self.p = (r-down_pro)/(up_pro-down_pro)
        self.build_sec_tree()

    def build_sto_tree(self):
        for step in range(self.steps):
            for offset in range(step+1):
                if step == 0:  
                   # print "enter 1"
                    p = self.s0
                elif offset<step:
                   # print "enter 2"
                    p = self.sto_tree[step-1][offset]*self.up_pro
                else:
                   # print "enter 3"
                    p = self.sto_tree[step-1][offset-1]*self.down_pro
                self.sto_tree[step][offset] = p

    def build_sec_tree(self):
        for step in range(self.steps-1,-1,-1):
            for offset in range(step+1):
                if step == self.steps-1:
                    sp = max(self.sto_tree[step][offset]-self.xp,0)
                else:
                    sp = (self.p*self.sec_tree[step+1][offset]+(1-self.p)*self.sec_tree[step+1][offset+1])/self.r
                self.sec_tree[step][offset] = sp

    def get_tree(self, tree_select):
        if tree_select == 1:
            return self.sto_tree
        elif tree_select == 2:
            return self.sec_tree
        else:
            return self.sto_tree, self.sec_tree
    

            
        

if __name__=="__main__":
    mytree = tree(2,35,1.10517,0.904837,35,1.024)
    st,spt = mytree.get_tree(3)
    print st.T
    print spt.T
        
