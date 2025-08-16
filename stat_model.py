# Log-transform y to handle large multiplicative differences
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


filling = "75%"


# regression
def model(x, a, b):
    return np.exp(-a*x**b)


def model_log(x, a, b):
    return np.log(model(x, a, b))


# Data (on remplace les 0.0 par 1e-8 < 1/n_window pour qu'ils tirent la regression vers le bas (si on laisse 0, vu qu'on est en log, le point sera en -infini -> erreur)
y_data_25prc = [0.936603235497742, 0.06066875845554843, 0.002469178930520004,
                0.00011432854212054039, 6.51037531519744e-05, 7.939482091704195e-06,
                3.652161762183929e-05, 3.1757928366816777e-06, 1e-8, 7.939482091704195e-06,
                1.5878964183408389e-06, 3.1757928366816777e-06, 4.763689255022516e-06,
                9.527378510045032e-06, 1e-8, 4.763689255022516e-06]
y_data_25prc = [0.9822229219921605, 0.017422977875196453, 0.0003335875103315505, 1.7107051811874385e-05, 1.504786964933395e-06, 3.167972557754516e-07, 1e-8, 1e-8, 1e-8, 1e-8, 1e-8, 1e-8, 1e-8, 7.91993139438629e-08]

y_data_half = [0.9995740464654931, 0.00040598452495364356, 1.695285706864196e-05, 2.132107790841474e-06, 8.840446937635379e-07]
y_data_half = [0.9989051714873096, 0.0010594667304565483, 3.5361782233824585e-05]

y_data_75prc = [0.9926222422782544, 0.0070631132555965875, 0.00024151374075464957,
                4.4962919747090535e-05, 1.6891086180337106e-05, 4.942562149360006e-06,
                2.73520429624777e-06, 1.1996510071262149e-06, 1.1036789265561177e-06,
                6.238185237056317e-07, 2.39930201425243e-07, 9.597208057009719e-08,
                9.597208057009719e-08, 2.39930201425243e-07]
y_data_75prc = [0.9905819238313743, 0.009019935992380584, 0.0003028878862792267, 5.4608113844385304e-05,
                2.1737676249127014e-05, 9.453249936154573e-06, 4.510687786794568e-06, 1.7274974502617495e-06,
                1.4395812085514578e-06, 4.318743625654374e-07,  9.597208057009719e-08, 1e-8,
                4.7986e-8, 1e-8,  4.7986e-8]

if filling == "25%":
    y_data = y_data_25prc
elif filling == "half":
    y_data = y_data_half
elif filling == "75%":
    y_data = y_data_75prc
else:
    raise ValueError(f"Error in the filling name {filling}")


x_data = [i for i in range(len(y_data))]

# Fit the non-linear model
y_log = np.log(y_data)
params, covariance = curve_fit(model_log, x_data, y_log, p0=[1,1])

a_hat, b_hat = params

print(f"Fitted parameters: a={a_hat:.3f}, b={b_hat:.3f}")

# Plot results
model_list = [1]
x_reg = 0
x_reg_list = [0]
while model_list[-1] > 8.68 * 1e-10:
    x_reg += 1
    model_list.append(model(x_reg, a_hat, b_hat))
    x_reg_list.append(x_reg)


# plot
fig, ax = plt.subplots(figsize=(10, 6))
plt.scatter(x_data, y_data, label="Data")
plt.plot(x_reg_list, model_list, color='red', label="Fitted curve")
ax.set_xlabel('Number of events in one bin')
ax.set_ylabel('Probability of occurrence')
ax.set_title('Regression of the maximum number of events in a bin for one month, for 25% filling of LS')
ax.grid(True)
plt.legend()
plt.yscale('log')
plt.show()
