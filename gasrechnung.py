import math


class Gas:
    K = 1.38064852e-23
    RADIUS = 2.5e-5

    def __init__(self, label):
        self.temp = 0
        self.X = 0
        self.korr = 0
        self.saug = 0
        self.m = 0
        self.label = label

    def rechne_dichte_aus(self, message):
        # erstmal den String auseinanderkriegen
        druck, temperatur, edruck = message.strip().split(",")
        druck = float(druck)
        temperatur = float(temperatur)
        edruck = float(edruck)
        vgas = math.sqrt(((2 * self.X * Gas.K * temperatur) / ((self.X - 1) * self.m)))
        dichte = (1e-5 * 4 * self.korr * druck * self.saug) / (3.141 * Gas.K * Gas.RADIUS * temperatur * vgas)
        return dichte, temperatur


class Wasserstoff(Gas):
    def __init__(self):
        super().__init__('Wasserstoff')
        self.m = 2.016 / 6.02214129e26
        self.X = 1.4054
        self.korr = 2.4
        self.saug = 1100

class Deuterium(Gas):
    def __init__(self):
        super().__init__('Deuterium')
        self.m = 4.0282/ 6.02214129e26
        self.X = 1.3981
        self.korr = 2.4
        self.saug = 1100

class Helium(Gas):
    def __init__(self):
        super().__init__('Helium')
        self.m = 4.002602 / 6.02214129e26
        self.X = 1.63
        self.korr = 5.7
        self.saug = 1320


class Neon(Gas):
    def __init__(self):
        super().__init__('Neon')
        self.m = 20.179 / 6.02214129e26
        self.X = 1.6669
        self.korr = 3.8
        self.saug = 1000


class Argon(Gas):
    def __init__(self):
        super().__init__('Argon')
        self.m = 39.948 / 6.02214129e26
        self.X = 1.6696
        self.korr = 0.8
        self.saug = 1000


class Krypton(Gas):
    def __init__(self):
        super().__init__('Krypton')
        self.m = 83.798 / 6.02214129e26
        self.X = 1.6722
        self.korr = 0.5
        self.saug = 850


class Xenon(Gas):
    def __init__(self):
        super().__init__('Xenon')
        self.m = 131.293 / 6.02214129e26
        self.X = 1.6773
        self.korr = 0.4
        self.saug = 850


class Stickstoff(Gas):
    def __init__(self):
        super().__init__('Stickstoff')
        self.m = 28.0134 / 6.02214129e26
        self.X = 1.4013
        self.korr = 1
        self.saug = 1320
