import pygame
from traffic import Point

def drawTraffic(screen, traffic):
    for driver in traffic.drivers:
        drawCar(screen, driver.car)
    for segment in traffic.trafficNetwork.segments:
        if segment.trafficLight is not None:
            drawTrafficLight(screen, segment.end + Point(50, 0), segment.trafficLight)

def drawCar(screen, car):
    pygame.draw.circle(screen, (0, 0, 255), (int(car.pos.x), int(car.pos.y)), 10)

def drawTrafficLight(screen, pos, trafficLight):
    if trafficLight.isRed:
        pygame.draw.circle(screen, (255, 0, 0), (int(pos.x), int(pos.y)), 10)
    else:
        pygame.draw.circle(screen, (0, 255, 0), (int(pos.x), int(pos.y)), 10)
