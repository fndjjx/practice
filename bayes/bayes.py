
class pmf():

    def __init__(self, choice = None):
        self.values = {}
        if choice:
            for i in choice:
                self.set_prob(i,1.0/len(choice))

    def set_prob(self, name, prob):
        self.values[name] = prob 


    def show_prob(self, name):
        return self.values[name]

    def normalize(self):
        total = 0
        for i in self.values:
            total += self.values[i]

        for i in self.values:
            self.values[i] = self.values[i]/float(total)

    def multiply(self, name, prob):
        self.values[name] = self.values[name]*prob

    def update_by_data(self, data):
        for i in self.values:
            self.multiply(i, self.likehood(i,data))
        self.normalize()

    def likehood(self):
        pass


def basic_test():
    mypp = pmf()
    mypp.set_prob("red", 5)
    mypp.set_prob("black", 5)
    mypp.normalize()
    mypp.multiply("black",0.75)

    print mypp.show_prob("black")
    mypp = pmf(["red","black"])

    print mypp.show_prob("red")

        
 
def cookie_test():
    mix = {"bowl1":{"vanilla":0.75,"choclate":0.25},"bowl2":{"vanilla":0.5,"choclate":0.5}}
    class cookie(pmf):
        def likehood(self, hypo, taste):
            return mix[hypo][taste]

    mypp = cookie(["bowl1","bowl2"])
    mypp.normalize()
    mypp.update_by_data("vanilla")
    mypp.update_by_data("vanilla")
    mypp.update_by_data("vanilla")
    mypp.update_by_data("choclate")
    print mypp.show_prob("bowl1")
    
    
def mm_test():
    mix94 = {"zong":0.3,"huang":0.2,"hong":0.2,"lv":0.1,"cheng":0.1,"huanghe":0.1}
    mix96 = {"zong":0.13,"huang":0.14,"hong":0.13,"lv":0.2,"cheng":0.16,"lan":0.24}
    choice = {"choice1":{"first":mix94,"second":mix96},"choice2":{"first":mix96,"second":mix94}}

    class mm(pmf):
        def likehood(self, hypo, data):
            return choice[hypo]["first"][data[0]]*choice[hypo]["second"][data[1]]

    mymm = mm(["choice1","choice2"])
    mymm.normalize()
    mymm.update_by_data(["huang","lv"])
    print mymm.show_prob("choice1")


def monty_test():
    class monty(pmf):
        def likehood(self, hypo, data):
            if hypo == "a":
                return 0.5
            elif hypo == "b":
                return 0
            else:
                return 1

    mymonty = monty(["a","b","c"])
    print mymonty.show_prob("a")
            
            


def dice_test():
    class dice(pmf):
        def likehood(self, hypo, data):
            if data>hypo:
                return 0
            else:
                return 1.0/hypo

    mydice=dice([4,6,8,12,20])
    for i in mydice.values:
        print mydice.show_prob(i)

    mydice.update_by_data(6)
    for i in mydice.values:
        print "{} {}".format(i,mydice.show_prob(i))


def train_test():
    class train(pmf):
        def likehood(self, hypo, data):
            if hypo < data:
               return 0
            else:
               return 1.0/hypo
        def percentage(self, target_percent):
            current_percent = 0
            s = sorted(self.values.iteritems(), key = lambda x:x[0])
            for i in s:
                current_percent = current_percent + i[1]
                if current_percent >= target_percent:
                    return i[0]

    mytrain = train(range(1,1001))
    mytrain.update_by_data(60)
    total = 0
    for i in mytrain.values:
        total+=mytrain.values[i]*i
    print total
    print mytrain.percentage(0.05)
    print mytrain.percentage(0.95)


def coin_test():
    class coin(pmf):
        def likehood(self, hypo, data):
            if data == "z":
                return hypo/100.0
            elif data == "f":
                return 1-hypo/100.0
        def percentage(self, target_percent):
            current_percent = 0
            s = sorted(self.values.iteritems(), key = lambda x:x[0])
            for i in s:
                current_percent = current_percent + i[1]
                if current_percent >= target_percent:
                    return i[0]
          
            

    mycoin = coin(range(1,101))
    print mycoin.values
    for i in range(10000):
        mycoin.update_by_data("z")
        mycoin.update_by_data("f")
    print mycoin.values
    print mycoin.percentage(0.05)
    print mycoin.percentage(0.95)
    


if __name__=="__main__":
    coin_test()

    

    
  
