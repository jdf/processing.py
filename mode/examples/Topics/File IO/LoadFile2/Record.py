class Record(object):
    def __init__(self, pieces):
        self.name = pieces[0]
        self.mpg = pieces[1]
        self.cylinders = int(pieces[2])
        self.displacement = float(pieces[3])
        self.horsepower = pieces[4]
        self.weight = float(pieces[5])
        self.acceleration = float(pieces[6])
        self.year = int(pieces[7])
        self.origin = float(pieces[8])
