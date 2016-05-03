import math



class Gas:
    def __init__(self, name):
        self.temp = 300
        self.k = 1.38064852e-23
        self.m = 4.002602/6.02214129e26
        self.X = 1.63
        self.korr = 5.7
        self.saug = 1320
        self.label = 'Helium' 
        self.radius = 2.5e-5
    
    def dichte(self, string, gasart):
        gas = gasart()
        #erstmal den String auseinanderkriegen
        druck, temperatur, edruck = string.strip().split(",")
        druck = float(druck)
        temperatur = float(temperatur)
        edruck = float(edruck)
        X = gas.X
        m = gas.m
        k = self.k
        r = self.r
        saug = gas.saug
        korr = gas.korr 
        vgas = math.sqrt(((2*X*k*temperatur)/((X-1)*m)))
        dichte = (1e-5*4*korr*druck*saug)/(3.141*k*r*temperatur*vgas)
        dichte = eformat(dichte, 2, 2)
        return (dichte)

    def eformat(f, prec, exp_digits):
        s = "%.*e"%(prec, f)
        mantissa, exp = s.split('e')
        # add 1 to digits as 1 is taken by sign +/-
        return "%se%+0*d"%(mantissa, exp_digits+1, int(exp))



class Wasserstoff(Gas):
    def __init__(self):
        super().__init__('Wasserstoff')
        self.m = 2.016/6.02214129e26
        self.X = 1.4054
        self.korr = 2.4
        self.saug = 1100
        self.label = 'Wasserstoff'

class Helium(Gas):
     def __init__(self):
        super().__init__('Helium')
        self.m = 4.002602/6.02214129e26
        self.X = 1.63
        self.korr = 5.7
        self.saug = 1320
        self.label = 'Helium'

class Neon(Gas):
     def __init__(self):
        super().__init__('Neon')
        self.m= 20.179/6.02214129e26
        self.X= 1.6669
        self.korr = 3.8
        self.saug = 1000
        self.label = 'Neon'

class Argon(Gas):
     def __init__(self):
        super().__init__('Argon')
        self.m = 39.948/6.02214129e26
        self.X = 1.6696
        self.korr = 0.8
        self.saug = 1000
        self.label = 'Argon'

class Krypton(Gas):
     def __init__(self):
        super().__init__('Krypton')
        self.m = 83.798/6.02214129e26
        self.X =  1.6722
        self.korr = 0.5
        self.saug = 850
        self.label = 'Krypton'

class Xenon(Gas):
     def __init__(self):
        super().__init__('Xenon')
        self.m = 131.293/6.02214129e26
        self.X = 1.6773
        self.korr = 0.4
        self.saug = 850
        self.label = 'Xenon'

class Stickstoff(Gas):
     def __init__(self):
        super().__init__('Stickstoff')
        self.m = 28.0134/6.02214129e26
        self.X = 1.4013
        self.korr = 1
        self.saug = 1320
        self.label = 'Stickstoff'

