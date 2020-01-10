from lmp_reader import get_lmp
import cvxpy as cp
import numpy as np


# constants
H = 24  # number of hours per day
eta_chg = 0.95  # charging efficiency
eta_dsg = 0.95  # discharging efficiency
E_min = 0.1  # minimal energy coefficient
E_max = 0.95

def OptimalBatteryDispatch(P, E, debug=False):
    pi_energy = get_lmp(5, 200, debug)
    pi_energy.reshape(1, H)
    # define decision variables
    P_chg = cp.Variable(H)
    P_dsg = cp.Variable(H)
    E_soc = cp.Variable(H+1)
    gamma = cp.Variable(H, boolean=True)

    # objective functions
    objective = cp.Minimize(pi_energy * (P_chg - P_dsg))

    # constraints
    constraints = []
    constraints += [E_min * E <= E_soc, E_soc <= E_max * E]
    constraints += [0 <= P_chg, P_chg <= P]
    constraints += [0 <= P_dsg, P_dsg <= P]
    constraints += [E_soc[0] == E_soc[-1]]

    for i in range(H):
        constraints += [0 * gamma[i] <= P_chg[i]]
        constraints += [P_chg[i] <= P * gamma[i]]
        constraints += [0 * (1 - gamma[i]) <= P_dsg[i]]
        constraints += [P_dsg[i] <= (1 - gamma[i]) * P]
        constraints += [E_soc[i+1] == E_soc[i] + eta_chg * P_chg[i] - P_dsg[i] / eta_dsg]

    # form the problem and solve.
    prob = cp.Problem(objective, constraints)
    print('start solving the problem')
    prob.solve(verbose=False)

    result_power = np.round(P_chg.value - P_dsg.value, 2)

    result_energy = np.round(E_soc[:-1].value, 2)
    if debug:
        print('\n')
        print('the objective value is: %.2f' % prob.objective.value)
        print('\n')
        print('the charging/discharging decisions are: ')
        print(gamma.value)
        print('\n')
        print('the charging power results are: ')
        print(result_power)
        print('\n')
        print('the energy stored are: ')
        print(result_energy)



if __name__ == "__main__":
    P = 25  # battery power rating, kW
    E = 100  # battery energy rating, kWh
    OptimalBatteryDispatch(P, E, True)
