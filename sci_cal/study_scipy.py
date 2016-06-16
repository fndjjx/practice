
import numpy as np
from scipy.integrate import odeint
from scipy.integrate import quad
from scipy import optimize as op
from scipy import interpolate as ip




##### differential equation############################################################################

def deriv(y,t):    
    a = -2.0
    b = -0.1
    return np.array([ y[1], a*y[0]+b*y[1] ])

deriv = lambda y,t:np.array([ y[1], -2*y[0]-0.1*y[1] ])
time = np.linspace(0.0,50.0,1000)
yinit = np.array([0.0005,0.2])    
y = odeint(deriv,yinit,time)
########################################################################################################


######linear equations####################################################################################
##### 3x0+2x1=9 2x0+x1=8

a = [[3,2],[2,1]]
b = [9,8]

r= np.linalg.solve(a,b)
###########################################################################################################


#####liner###################################################################################################

f = lambda p,x:x.dot(p)
x1 = np.linspace(0,10,100)
x2 = np.linspace(10,100,100)
x=zip(x1,x2)
x=np.array(map(lambda x:np.array(x),x))
p=np.array([10,70])
real_y = f(p,x)
noise_y = [i+np.random.randn(1)[0] for i in real_y]

err = lambda p,x,y:0.5*(f(p,x)-y)**2
y0=[1,1]
r=op.leastsq(err,y0,args=(x,noise_y))
##################################################################################################################


#####min constrain##############################################################################################
f = lambda x:-(2*x[0]*x[1]+2*x[0]-x[0]**2-2*x[1]**2)
x0 = [-1,1]
r=op.minimize(f,x0,method='SLSQP')
#print r
cons = ({'type': 'eq',  'fun': lambda x: np.array([x[0]**3 - x[1]])},{'type': 'ineq', 'fun': lambda x: np.array([x[1] - 1])})
r=op.minimize(f,x0,constraints=cons,method='SLSQP')


f = lambda x:x**2-2*x+1
x0=0
cons=({'type':'ineq','fun':lambda x:x-5})
r=op.minimize(f,x0,constraints=cons,method='SLSQP')




f=lambda w:0.00015*w[0]*w[0]+0.00025*w[1]*w[1]+0.0001*w[2]*w[2]+0.0001*w[0]*w[1]-0.00014*w[0]*w[2]-0.00006*w[1]*w[2]
cons=({'type':'eq','fun':lambda w:np.array(1-w[0]-w[1]-w[2])},{'type':'ineq','fun':lambda w:np.array(0.11*w[0]+0.15*w[1]+0.08*w[2]-0.11)},{'type':'ineq','fun':lambda w:np.array(0.25-w[2])})
#cons=({'type':'eq','fun':lambda w:np.array(1-w[0]-w[1]-w[2])},{'type':'eq','fun':lambda w:np.array(0.11*w[0]+0.15*w[1]+0.08*w[2]-0.11)})
w0=[0,0,0]
r=op.minimize(f,w0,constraints=cons,method='SLSQP',options={'ftol': 1e-10,'disp': True})
e=lambda w:np.array(0.11*w[0]+0.15*w[1]+0.08*w[2])
print r

#####################################################################################################################


###nonlinere equation################################################################################################
f=lambda x:[5*x[1]+3,4*x[0]**2-2*np.sin(x[1]*x[2]),x[1]*x[2]-1.5]
r=op.fsolve(f,[1,1,1])
#print r
###############################################################################################################



########spline####################################################################################################
x=np.linspace(1,10,5)
y=5*x

xnew=np.linspace(1,10,20)
ynew=ip.spline(x,y,xnew,order=3)
#print ynew
###################################################################################################################




###integarate
f=lambda x:x**2-1
r=quad(f,-1,1)
print r





##### global optimize
f = lambda x:np.sin(x[0])+0.05*x[0]**2+np.sin(x[1])+0.05*x[1]**2
x0_range = (-10,10.1,0.1)
x1_range = (-10,10.1,0.1)
r = op.brute(f,(x0_range,x1_range))
print r
