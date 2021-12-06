import numpy             as np
import matplotlib.pyplot as plt
import seaborn           as sns
sns.set(rc={'axes.facecolor':'whitesmoke'})



def f(delta, ar, br): #efficiency
    return delta/(ar*br*300)
def A(t, T): #activity
    return 43100*np.exp(-np.log(2)*t/T)

E    = [121.8, 244.8, 344.3, 443.8, 778.9, 1112, 1407.7] #energy
ar   = [ ] #activity
br   = [0.2858, 0.007583, 0.265, 0.0280, 0.12942, 0.13644, 0.21005 ] #proportion
delta= [10384 , 1879    , 4741 , 524   , 1122   , 767    ,    1006 ] #nombre de coups

incertitude_delta = [1.29,2.91,1.66,8.57,4.73,4.10,3.36]

delta_minus = []
delta_maxim = []
for i in range(len(E)):
        delta_minus.append(delta[i]*(100-incertitude_delta[i])/100)
        delta_maxim.append(delta[i]*(100+incertitude_delta[i])/100)




for i in range(len(E)):
    ar.append(A(6.044, 13.5))

x = []
y = []
y_min=[]
y_max=[]
for i in range(len(E)):
    if i==1:
        pass
    else:
        x.append(E[i])
        y.append(f(delta[i], ar[i], br[i]))
        y_min.append(f(delta_minus[i], ar[i], br[i]))
        y_max.append(f(delta_maxim[i], ar[i], br[i]))

'''
4.943856818053838e-05
3.132606815876588e-05
0.0001691717323819182
4.325400451855594e-05
2.4311470540763422e-05
1.6974159991409014e-05
'''
error_bar_y = [4.943856818053838e-05,
3.132606815876588e-05,
0.0001691717323819182,
4.325400451855594e-05,
2.4311470540763422e-05,
1.6974159991409014e-05]


poly_fit_test = np.polyfit(x,y,deg=2)

poly_fit_test_min = np.polyfit(x,y_min,deg=2)
poly_fit_test_max = np.polyfit(x,y_max,deg=2)



to_plot = np.linspace(min(E),max(E),2000)

def function_plot_theory(x):
    #return -7.315*10+4.405*10*np.log(x)-1.045*np.log(x)**2+1.074*np.log(x)**3-4.127*0.01*np.log(x)**4
    return -7.315*10+4.405*10*x-1.045*x**2+1.074*x**3-4.127*0.01*x**4

def function_plot(x):
    return  poly_fit_test[2]+poly_fit_test[1]*x+poly_fit_test[0]*x**2

#fig, axs = plt.subplots(1)
plt.title('Efficiency of the detector')
for i in range(0, len(E)):
    if i==1:
        pass
    else:
        plt.scatter(E[i],f(delta[i], ar[i], br[i]),color='blue',marker='.')

#plt.ylim(0,0.004)
plt.plot(to_plot,function_plot(to_plot),color='red')

plt.errorbar(x,y,yerr=error_bar_y,fmt='o',color = 'orange',
            ecolor = 'lightgreen', elinewidth = 5, capsize=10,label='Efficiency with errorbars')

plt.plot(to_plot,[poly_fit_test_min[2]+poly_fit_test_min[1]*i+poly_fit_test_min[0]*i**2 for i in to_plot],color='red',linestyle='--')
plt.plot(to_plot,[poly_fit_test_max[2]+poly_fit_test_max[1]*i+poly_fit_test_max[0]*i**2 for i in to_plot],color='red',linestyle='--')
plt.fill_between(to_plot,[poly_fit_test_min[2]+poly_fit_test_min[1]*i+poly_fit_test_min[0]*i**2 for i in to_plot],[poly_fit_test_max[2]+poly_fit_test_max[1]*i+poly_fit_test_max[0]*i**2 for i in to_plot],color='red',alpha=0.2)
#plt.grid()
#plt.yscale('log')
plt.xlabel('$E$')
plt.ylabel('$\epsilon$')
plt.legend()

print(poly_fit_test_min[2]+poly_fit_test_min[1]*661.7+poly_fit_test_min[0]*661.7**2)
print(poly_fit_test[2]+poly_fit_test[1]*661.7+poly_fit_test[0]*661.7**2)
print(poly_fit_test_max[2]+poly_fit_test_max[1]*661.7+poly_fit_test_max[0]*661.7**2)


plt.savefig('graphe5.png',dpi=300)
plt.show()
