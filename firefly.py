from math import exp
import numpy as np


class Firefly(object):
    """
    Firefly Algorithm
    """

    def __init__(self, X, number_outlet):

        self.X = X
        self.gamma = 0.95
        self.number_outlet = number_outlet

    def fitness_fcs(self, x):
        """
            Fleet Capacity Score (FCS)
        """
        k, x0 = 15, 0.5
        return 1/(1 + exp(-k*(x-x0)))
        
    def fitness_odws(self, x):
        """
            Outlet Delivery Window Score (ODWS)
        """
        return x^3*(self.number_outlet - 
                        (x*(self.number_outlet-1)/100))

    def fitness_fdws(self, x):
        """
            Fleet Delivery Window Score (FDWS)
        """
        k, x0 = -10, 0.5
        return 1/(1 + exp(-k*(x-x0)))

    def fitness_oas(self, x):
        """
            Outlet Accessibility Score (OAS)
        """
        return x^3


    def fly(self):

        --bersambung--