import math
import random
import itertools
import bisect

DT = 5
MAXVEL = 1
SAFETY_DISTANCE = 50

class Car:
    def __init__(self):
        self.currentSegment = None
        self.posCurrentSegment = 0
        self.vel = MAXVEL
        
    @property
    def pos(self):
        return self.currentSegment.getPosition(self.posCurrentSegment)

    def handle(self):
        self.integrate()

    def integrate(self):
        self.posCurrentSegment += DT * self.vel
        # self.vel += DT * self.acceleration

    def willReachNextFrame(self, posCurrentSegment):
        return posCurrentSegment - self.posCurrentSegment < DT * MAXVEL

class Driver:
    def __init__(self, car, segments):
        self.car = car
        self.segments = segments
        self.currentSegment = self.getNextSegment()
        self.shouldBeDeleted = False

    def getNextSegment(self):
        if len(self.segments) == 0:
            return None
        nextSegment = self.segments[0]
        self.segments = self.segments[1:]
        return nextSegment

    # def getNextTrafficLight(self):
    #     for segment in self.segments:
    #         if segment.trafficLight is not None:
    #             return segment.trafficLight
    #     return None
    
    def getNextCar(self):
        result = self.getNextCarWithDistance()
        if result is None:
            return result
        return result[0]

    def getDistanceToNextCar(self):
        result = self.getNextCarWithDistance()
        if result is None:
            return result
        return result[1]

    def getNextCarWithDistance(self):
        distance = 0
        if self.currentSegment is None:
            return
        for (i, segment) in enumerate([self.currentSegment] + self.segments):
            if segment == self.currentSegment:
                carList = segment.cars[segment.cars.index(self.car)+1:]
                distance += segment.length - self.car.posCurrentSegment
            else:
                carList = segment.cars
                distance += segment.length
            if len(carList) > 0:
                nextCar = carList[0]
                distance -= segment.length - nextCar.posCurrentSegment
                return (nextCar, distance)
        return None

    def drive(self):
        if self.tooCloseToNextCar() or self.tooCloseToRedLight():
            self.car.vel = 0
        else:
            self.car.vel = MAXVEL
        
    def tooCloseToNextCar(self):
        distance = self.getDistanceToNextCar()
        if distance is None:
            return False
        return self.car.willReachNextFrame(self.car.posCurrentSegment + distance - SAFETY_DISTANCE)

    def tooCloseToRedLight(self):
        if self.currentSegment.trafficLight is not None:
            if self.currentSegment.trafficLight.isRed:
                return self.car.willReachNextFrame(self.currentSegment.length)

    @property
    def currentSegment(self):
        return self.car.currentSegment

    @currentSegment.setter
    def currentSegment(self, value):
        self.car.currentSegment = value

    def checkIfEndOfSegmentReached(self):
        if self.car.posCurrentSegment > self.currentSegment.length:
            self.car.posCurrentSegment -= self.currentSegment.length
            self.currentSegment = self.getNextSegment()
            if self.currentSegment is None:
                self.shouldBeDeleted = True

    def handle(self):
        self.drive()
        self.checkIfEndOfSegmentReached()

class TrafficLight:
    def __init__(self, times):
        self.cycleTime = sum(times)
        self.times = list(itertools.accumulate(times))
        self.updateState(0)

    def updateState(self, time):
        timeInCycle = time % self.cycleTime
        self.currentState = bisect.bisect(self.times, timeInCycle)

    @property
    def isRed(self):
        return self.currentState % 2

class Segment:
    def __init__(self, start, end, trafficLight=None):
        self.start = start
        self.end = end
        self.length = end.distance(start)
        self.successors = []
        self.trafficLight = trafficLight

    def addSuccessor(self, segment):
        self.successors.append(segment)

    def getPosition(self, posCurrentSegment):
        return self.start + (self.end - self.start) * posCurrentSegment / self.length

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
        if len(segments) == 2:
            raise ValueError

    def findPath(self, startSegment):
        if startSegment.successors == []:
            return [startSegment]
        nextSegment = startSegment.successors[0]
        return [startSegment] + self.findPath(nextSegment)

class Traffic:
    def __init__(self, trafficNetwork, drivers):
        self.trafficNetwork = trafficNetwork
        self.drivers = drivers
        self.time = 0
        self.updateSegmentCarLists()

    def handle(self):
        self.time += DT
        for segment in self.trafficNetwork.segments:
            if segment.trafficLight is not None:
                segment.trafficLight.updateState(self.time)
        for driver in self.drivers:
            driver.handle()
            driver.car.handle()
            self.removeDriversThatShouldBeDeleted()
        if random.random() < 0.03:
            self.addDriver()
        self.updateSegmentCarLists()

    def removeDriversThatShouldBeDeleted(self):
        driversThatShouldBeDeleted = [driver for driver in self.drivers if driver.shouldBeDeleted]
        for d in driversThatShouldBeDeleted:
            self.drivers.remove(d)

    def updateSegmentCarLists(self):
        for segment in self.trafficNetwork.segments:
            segment.cars = []
            for driver in self.drivers:
                if driver.car.currentSegment == segment:
                    segment.cars.append(driver.car)
            segment.cars.sort(key = lambda x : x.posCurrentSegment)

    @staticmethod
    def getSimpleTraffic():
        p1 = Point(0, 100)
        p2 = Point(500, 100)
        p3 = Point(500, 600)

        a = Segment(p1, p2, TrafficLight([150, 150]))
        b = Segment(p2, p3)

        a.addSuccessor(b)

        network = TrafficNetwork([a, b])
        return Traffic(network, [])

    @staticmethod
    def getSimpleTraffic2():
        s1 = Point(100, 100)
        s2 = Point(900, 100)
        p1 = Point(550, 500)
        p2 = Point(650, 500)
        p3 = Point(600, 600)
        p4 = Point(600, 800)

        a1 = Segment(s1, p1, TrafficLight([1300, 1900]))
        a2 = Segment(s2, p2, TrafficLight([0, 1700, 1300, 200]))
        b1 = Segment(p1, p3)
        b2 = Segment(p2, p3)
        c = Segment(p3, p4, TrafficLight([500, 1500]))

        a1.addSuccessor(b1)
        a2.addSuccessor(b2)
        b1.addSuccessor(c)
        b2.addSuccessor(c)

        network = TrafficNetwork([a1, a2, b1, b2, c])
        return Traffic(network, [])

    def __repr__(self):
        return "{}".format(self.drivers[0].car.pos)

    def addDriver(self):
        car = Car()
        if random.random() < 0.5:
            start = self.trafficNetwork.segments[0]
        else:
            start = self.trafficNetwork.segments[1]
        path = self.trafficNetwork.findPath(start)
        self.drivers.append(Driver(car, path))

# _traffic = Traffic.getSimpleTraffic2()
# for i in range(30):
#     _traffic.handle()
