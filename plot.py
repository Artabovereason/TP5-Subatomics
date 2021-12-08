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
'''
    E                    : Energy data from experiment.
    br                   : Branching Ratio.
    delta                : Number of counts under a peak.
    incertitude_delta    : Incertitude on the number of counts under a peak.
    error_bar_y          : The calculated plus and minus error on each values of the effiency.
    ar                   : Residual activity.
    delta_minus          : Number of counts under a peak plus the error on the number.
    delta_maxim          : Number of counts under a peak minus the error on the number.
    x                    : Array of the energies.
    y                    : Array of the efficiency for each value of energies.
    y_min                : Array of the effiency values with the minus error.
    y_max                : Array of the effiency values with the plus error.
    to_plot              : Array used for the plotting.
    poly_fit_test        : Polynomial fitting of order 4 on the y array.
    poly_fit_test_min    : Polynomial fitting of order 4 on the y_min array.
    poly_fit_test_max    : Polynomial fitting of order 4 on the y_max array.
    function_plot_theory : Efficiency from the fitting on the GENIE software.
    function_plot        : Efficiency from the fitting on the experimental data.
'''

def f(delta, ar, br): #efficiency
    return delta/(ar*br*300)
def A(t, T):          #activity
    return 43100*np.exp(-np.log(2)*t/T)

E                 = [121.8 , 244.8  , 344.3, 778.9  , 1112   , 1407.7  ]
br                = [0.2858, 0.07583, 0.265, 0.12942, 0.13644, 0.21005 ]
delta             = [10384 , 1879   , 4741 , 1122   , 767    ,    1006 ]
incertitude_delta = [1.29  ,    2.91, 1.66 ,    4.73,    4.10,    3.36 ]
error_bar_y       = [4.943856818053838e-05,
                    7.6059318927023745e-06,
                    3.132606815876588e-05 ,
                    4.325400451855594e-05 ,
                    2.4311470540763422e-05,
                    1.6974159991409014e-05]
ar                = []
delta_minus       = []
delta_maxim       = []
x                 = []
y                 = []
y_min             = []
y_max             = []
to_plot           = np.linspace(min(E),max(E),2000)

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

'''
    activity_from_efficiency_cesium : allows us to compute the residual activity cesium from the efficiency.
'''
def activity_from_efficiency_cesium(delta, eps, br):
    return delta/(eps*np.exp(-np.log(2)*6.008/30.08)*br*300)

def activity_from_efficiency_cobalt(delta, eps, br):
    return delta/(eps*np.exp(-np.log(2)*6.049/(2.62e6))*br*300)


print('—————————————————————-—————————————————————')
print('Residual activity from Cesium using our fit = '  +str(activity_from_efficiency_cesium(88335, 0.001023   ,0.8521))) #red curve
print('Meaning an error of '+str(round(abs(100*(387946.0172042941-497000)/497000),2))+'%')
print('Residual activity from Cesium using GENIE fit = '+str(activity_from_efficiency_cesium(88335, 0.00086346 ,0.8521))) #bue curve
print('Meaning an error of '+str(round(abs(100*(459626.1269775009-497000)/497000),2))+'%')
print('—————————————————————-—————————————————————')

print(' ')

print('—————————————————————-—————————————————————')
print('Residual activity from Cobalt using our fit = '  +str(activity_from_efficiency_cobalt(27036, 0.0005418, 0.9990)*0.9990+activity_from_efficiency_cobalt(24367, 0.0004684, 0.9988)*0.9988) ) #red curve
print('Meaning an error of '+str(round(abs(100*(activity_from_efficiency_cobalt(27036, 0.0005418, 0.9990)*0.9990+activity_from_efficiency_cobalt(24367, 0.0004684, 0.9988)*0.9988-395000)/395000),2))+'%')
print('Residual activity from Cobalt using GENIE fit = '+str(activity_from_efficiency_cobalt(27036, 0.0004883, 0.9990)*0.9990+activity_from_efficiency_cobalt(24367, 0.0004295, 0.9988)*0.9988)) #bue curve
print('Meaning an error of '+str(round(abs(100*(activity_from_efficiency_cobalt(27036, 0.0004883, 0.9990)*0.9990+activity_from_efficiency_cobalt(24367, 0.0004295, 0.9988)*0.9988-395000)/395000),2))+'%')
print('—————————————————————-—————————————————————')
