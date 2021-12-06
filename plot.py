import numpy             as np
import matplotlib.pyplot as plt
import seaborn           as sns
sns.set(rc={'axes.facecolor':'whitesmoke'})

'''
Error bar for y :
4.943856818053838e-05
7.6059318927023745e-06
3.132606815876588e-05
0.0001691717323819182
4.325400451855594e-05
2.4311470540763422e-05
1.6974159991409014e-05
'''

def f(delta, ar, br): #efficiency
    return delta/(ar*br*300)
def A(t, T):          #activity
    return 43100*np.exp(-np.log(2)*t/T)

E                 = [121.8 , 244.8  , 344.3, 778.9  , 1112   , 1407.7  ] #energy
br                = [0.2858, 0.07583, 0.265, 0.12942, 0.13644, 0.21005 ] #proportion
delta             = [10384 , 1879   , 4741 , 1122   , 767    ,    1006 ] #count number
incertitude_delta = [1.29  ,    2.91, 1.66 ,    4.73,    4.10,    3.36 ] #% of error on delta
error_bar_y       = [4.943856818053838e-05,
                    7.6059318927023745e-06,
                    3.132606815876588e-05 ,
                    4.325400451855594e-05 ,
                    2.4311470540763422e-05,
                    1.6974159991409014e-05]
ar                = []                                                  #activity
delta_minus       = []
delta_maxim       = []
x                 = []
y                 = []
y_min             = []
y_max             = []
to_plot           = np.linspace(min(E),max(E),2000) #used for the plotted fit

for i in range(len(E)):
    ar         .append(A(6.044, 13.5))
    delta_minus.append(delta[i]*(100-incertitude_delta[i])/100)
    delta_maxim.append(delta[i]*(100+incertitude_delta[i])/100)
    x          .append(E[i])
    y          .append(f(delta[i], ar[i], br[i]))
    y_min      .append(f(delta_minus[i], ar[i], br[i]))
    y_max      .append(f(delta_maxim[i], ar[i], br[i]))

poly_fit_test     = np.polyfit(x,y    ,deg=4)
poly_fit_test_min = np.polyfit(x,y_min,deg=4)
poly_fit_test_max = np.polyfit(x,y_max,deg=4)

def function_plot_theory(x):
    return -7.315*10+4.405*10*x-1.045*10*x**2+1.074*x**3-4.127*0.01*x**4

def function_plot(x):
    return  poly_fit_test[4]+poly_fit_test[3]*x+poly_fit_test[2]*x**2+poly_fit_test[1]*x**3+poly_fit_test[0]*x**4



for i in range(0, len(E)):
    plt.scatter(E[i],f(delta[i], ar[i], br[i]),color='blue',marker='.')

plt.plot(to_plot,function_plot(to_plot)                                                                                                                      ,color='red'                  ,label='fit'            )
plt.plot(to_plot,[np.exp(function_plot_theory(np.log(i))) for i in to_plot]                                                                                  ,color='blue'                 ,label='theory'         )
plt.plot(to_plot,[poly_fit_test_min[4]+poly_fit_test_min[3]*i+poly_fit_test_min[2]*i**2+poly_fit_test_min[1]*i**3+poly_fit_test_min[0]*i**4 for i in to_plot],color='purple',linestyle='--',label='fit lower-error')
plt.plot(to_plot,[poly_fit_test_max[4]+poly_fit_test_max[3]*i+poly_fit_test_max[2]*i**2+poly_fit_test_max[1]*i**3+poly_fit_test_max[0]*i**4 for i in to_plot],color='green' ,linestyle='--',label='fit upper-error')
plt.errorbar(x,y,yerr=error_bar_y,fmt='o',color = 'orange',ecolor = 'lightgreen', elinewidth = 5, capsize=10,label='Efficiency with errorbars')

plt.title('Efficiency of the detector')
plt.xlabel('$E$ in keV')
plt.ylabel('$\epsilon$')
plt.legend()
print('—————————————————————-—————————————————————')
print('efficiency ymin = '+str(poly_fit_test_min[4]+poly_fit_test_min[3]*661.7+poly_fit_test_min[2]*661.7**2+poly_fit_test_min[1]*661.7**3+poly_fit_test_min[0]*661.7**4))
print('efficiency ymid = '+str(function_plot(661.7)))
print('efficiency ymax = '+str(poly_fit_test_max[4]+poly_fit_test_max[3]*661.7+poly_fit_test_max[2]*661.7**2+poly_fit_test_max[1]*661.7**3+poly_fit_test_max[0]*661.7**4))
print('efficiency theo = '+str(np.exp(function_plot_theory( np.log(661.7)))))
print('—————————————————————-—————————————————————')

plt.savefig('graphe5.png',dpi=300)
#plt.show()
