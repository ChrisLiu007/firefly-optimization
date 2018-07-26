from math import exp
import numpy as np
import pandas as pd
import time

individu = np.array([
    [ 4, 12,  4,  5,  2,  8,  4,  4,  4, 13,  4,  2,  2,  7,  2, 11, 3, 15,  2,  3,  4,  9,  1,  6,  2,  1,  1, 14,  4, 10],
    [ 3, 15,  1, 14,  1,  9,  2,  4,  1,  5,  4, 11,  3, 10,  2,  1, 1,  3,  4,  8,  3,  6,  1, 13,  1,  7,  3, 12,  3,  2],
    [ 1, 11,  4,  4,  1,  6,  4,  7,  3, 12,  4, 10,  2, 14,  3,  1, 1, 13,  2, 15,  3,  9,  4,  8,  3,  5,  1,  2,  4,  3],
    [ 2, 14,  3, 13,  4, 10,  1,  3,  1,  8,  2, 11,  4,  7,  2,  1, 4,  9,  3,  5,  4, 15,  3, 12,  4,  4,  1,  6,  1,  2],
    [ 3,  9,  3, 13,  2,  3,  3,  1,  4,  6,  1, 11,  3,  8,  4, 10, 3, 14,  1,  5,  3,  2,  3, 12,  3, 15,  3,  7,  3,  4],
    [ 4,  2,  1,  8,  3, 15,  4,  6,  3,  3,  4, 10,  1, 11,  1,  7, 3, 12,  4,  4,  4,  1,  2, 14,  1,  9,  3, 13,  3,  5],
    [ 2,  1,  4,  6,  2,  4,  1,  3,  1,  7,  2,  8,  4,  5,  2, 12, 4, 15,  4, 10,  2, 14,  4,  2,  1, 13,  2, 11,  1,  9],
    [ 4,  3,  1,  8,  2,  1,  3, 15,  3, 12,  1,  2,  1, 10,  1,  4, 3, 13,  2, 14,  4,  5,  1,  7,  3, 11,  2,  6,  1,  9],
    [ 4, 15,  4, 10,  3,  7,  2, 11,  2,  9,  2,  1,  1,  4,  2,  8, 2, 14,  2,  3,  2, 12,  3,  6,  4, 13,  4,  5,  4,  2]
    ])

data_outlet = pd.read_csv("data_outlet.csv")
"""data_outlet
"Nama Outlet | Latitude | Longitude | Open Time | Close Time | Accessibility | Demand"
"""

class Firefly(object):
    """
    Firefly Algorithm
    """

    def __init__(self, individu, data_outlet):

        self.X = individu
        self.gamma = 0.95
        self.number_outlet = len(data_outlet)
        self.data_outlet = data_outlet
        self.fitness_outlet = get_fitness_outlet() 

        # fleet
        self.fleet_dict = {"Truck":1, "Van":2, "Triseda":3, "Motor":4}
        self.fleet_capacity = [30, 15, 7, 3]

    def get_x_fcs(self, xi):
        # variable x untuk fcs setiap anggota individu (total demand/fleet capacity)
        # berbentuk float

        total_demand, total_capacity = 0, 0
        for i in range(len(xi)):
            if i % 2 == 0:
                total_capacity = total_capacity + self.fleet_capacity[xi[i]]
            else:
                total_demand = total_demand + self.data_outlet["Demand"][xi[i]]
        return total_demand/total_capacity

    def get_x_oas(self, xi):
        # variable x untuk oas setiap anggota individu match(accessibily <> fleet)
        # berbentuk float

        self.data_outlet.replace({"accessibility":self.fleet_dict})
        list_access = list(self.data_outlet["accessibility"])
        
        is_match = 0
        for i in range(len(xi)):
            if i % 2 != 0:
                if list_access[x[i + 1]] ==  x[i]:
                    is_match = is_match + 1
        return is_match/(len(xi)/2)

    def get_x_odws(self, xi):
        return None

    def get_x_fdws(self, xi):
        return None

    def fitness_fcs(self, xi):
        """
            Fleet Capacity Score (FCS)
        """
        x = get_x_oas(xi)
        k, x0 = 15, 0.5
        
        return [1/(1 + exp(-k*(i-x0))) for i in x]
        
    def fitness_odws(self, xi):
        """
            Outlet Delivery Window Score (ODWS)
        """
        x = get_x_odws(xi)

        return [i^3*(self.number_outlet - 
                        (i*(self.number_outlet-1)/100)
                    ) for i in x]

    def fitness_fdws(self, xi):
        """
            Fleet Delivery Window Score (FDWS)
        """
        x = get_x_fdws(xi)
        k, x0 = -10, 0.5

        return [1/(1 + exp(-k*(i-x0))) for i in x]

    def fitness_oas(self, xi):
        """
            Outlet Accessibility Score (OAS)
        """
        x = get_x_oas(xi)
        return [i^3 for i in x]

    def get_fitness(self, xi):
        # Total fitness

        f1 = fitness_fcs(xi)
        f2 = fitness_fdws(xi)
        f3 = fitness_oas(xi)
        f4 = fitness_odws(xi)

        return [f1[i] + f2[i] + f3[i] + f4[i] for i in range(len(f1))]
    
    def hamming_distance(self, xi, xj):
        # Hamming Distance
        if len(xi) != len(xj):
            raise ValueError("Panjang kedua cluster tidak sama!")
        count = 0
        for i in range(len(xi)):
            count += (xi[i] != xj[i])
        return count
    
    def random(self, r_ij):
        # Random number antara 2 dan r_ij
        return np.random.randint(low=2, r_ij*self.gamma, size=1)

    def fly(self):
        
        I = [get_fitness(xi) for xi in self.X]

        # Maximal 600 detik untuk running
        max_time = 600 
        start_time = time.time()
        while (time.time() - start_time) < max_time:
            for i in range(len(self.X)):
                for j in range(len(self.X)):
                    if i != j:
                        if I[i] < I[j]:
                            r_ij = hamming_distance(x[i], x[j])
                            n = random(r_ij)


            

            


