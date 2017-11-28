import math

DT = 0.01

class Car:
    def __init__(self):
        self.currentSegment = None
        self.posOnSegment = 0
        self.vel = 1
        
    @property
    def pos(self):
        return self.currentSegment.getPosition(self.posOnSegment)

    def handle(self):
        self.integrate()

    def integrate(self):
        self.posOnSegment += DT * self.vel
        # self.vel += DT * self.acceleration

class Driver:
    def __init__(self, car, segments):
        self.car = car
        self.segments = segments
        self.car.currentSegment = self.getNextSegment()

    def getNextSegment(self):
        nextSegment = self.segments[0]
        self.segments = self.segments[1:]
        return nextSegment

    def checkIfEndOfSegmentReached(self):
        if self.car.posOnSegment > self.car.currentSegment.length:
            self.car.posOnSegment -= self.car.currentSegment.length
            self.car.currentSegment = self.getNextSegment()

    def handle(self):
        self.checkIfEndOfSegmentReached()

class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = end.distance(start)
        self.successors = []

    def addSuccessor(self, segment):
        self.successors.append(segment)

    def getPosition(self, posOnSegment):
        return self.start + (self.end - self.start) * posOnSegment / self.length

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, b):
        return Point(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Point(self.x - b.x, self.y - b.y)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return "{} {}".format(self.x, self.y)
    
    def distance(self, b):
        return math.sqrt((self.x - b.x) ** 2 + (self.y - b.y) ** 2)

class TrafficNetwork:
    def __init__(self, segments):
        self.segments = segments

class Traffic:
    def __init__(self, trafficNetwork, drivers):
        self.trafficNetwork = trafficNetwork
        self.drivers = drivers

    def handle(self):
        for driver in self.drivers:
            driver.handle()
            driver.car.handle()

    @staticmethod
    def getSimpleTraffic():
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(1, 1)

        a = Segment(p1, p2)
        b = Segment(p2, p3)

        a.addSuccessor(b)

        network = TrafficNetwork([a, b])
        car = Car()
        driver = Driver(car, network.segments)
        return Traffic([a, b], [driver])

traffic = Traffic.getSimpleTraffic()
for i in range(300):
    traffic.handle()
