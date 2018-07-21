
class HammingDistance(object):

    def __init__(self, xi, xj):
        self.xi = xi
        self.xj = xj

    def hamming_sum(self):

        '''
        computes the distance using Python's built-in sum() 
        and zip() functions, and uses a generator expression 
        for nice, clear, Pythonic code.
        '''
        if len(self.xi) != len(self.xj):
            raise ValueError()
        return sum(c0 != c1 for (c0, c1) in zip(self.xi, self.xj))

    def hamming_loop(self):

        '''
        computes the distance using a non-Pythonic for loop 
        over the indices into the string arguments.
        '''
        if len(self.xi) != len(self.xj):
            raise ValueError()
        count = 0
        for i in range(len(self.xi)):
            count += (self.xi[i] != self.xj[i])
        return count