import pygame
from random import randint
import math


class Particle(object):
    gravity_switch = True
    gravity = (math.pi / 2, 0.5)
    elastic = 0.7

    def __init__(self, position, radius, velocity, thickness):
        self.x, self.y = position
        self.radius = radius
        self.mass_density = 100
        self.mass = 4 / 3 * math.pi * math.pow(self.radius, 3) * self.mass_density
        self.color = (randint(50, 255), randint(50, 255), randint(50, 255))
        self.oldColor = self.color
        self.thickness = thickness

        self.speed, self.angle = velocity
        self.drag = 0.9999

    def display(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)
        dx = math.cos(self.angle) * self.speed  # vx * t
        dy = math.sin(self.angle) * self.speed
        # pygame.draw.lines(screen, self.color, False, [(self.x, self.y), (self.x + pow(10, 3) * dx, self.y + pow(10, 3) * dy)], 2)

    def move(self, screen):
        # air friction
        self.speed *= self.drag

        if self.speed < 0.2 and screen.get_height() - (self.y + self.radius) < 0.4:
            # make the balls stop more naturally
            self.speed *= 0.05
            self.y = screen.get_height() - self.radius
        else:
            # gravity effect
            if Particle.gravity_switch:
                self.angle, self.speed = self.add_vector((self.angle, self.speed), Particle.gravity)

            # update position
            dx = math.cos(self.angle) * self.speed  # vx * t
            dy = math.sin(self.angle) * self.speed  # vy * t

            self.x += dx  # x = x0 + vx * t
            self.y += dy  # y = y0 + vy * t

    def drag_move_params_update(self, screen, mouse_pos):

        mouseX, mouseY = mouse_pos

        if mouseX > screen.get_width():
            self.x = screen.get_width() - self.radius
            self.speed = 0
        else:
            dx = mouseX - self.x
            dy = mouseY - self.y
            self.speed = math.hypot(dx, dy) * 0.5
            self.angle = math.atan2(dy, dx)

    def bounce(self, screen):
        width = screen.get_width()
        height = screen.get_height()

        # right boundary check
        d1 = self.x - (width - self.radius)
        if d1 >= 0: # the ball has crossed the right wall a distance d1
            self.x = (width - self.radius) - d1   # reflect x
            self.angle = math.pi - self.angle   # reflect the angle
            self.speed *= Particle.elastic     # elastic lost

        # left boundary check
        d2 = self.radius - self.x
        if d2 >= 0:  # the ball has crossed the left wall a distance d2
            self.x = d2 + self.radius   # reflect x
            self.angle = math.pi - self.angle # reflect the angle
            self.speed *= Particle.elastic # elastic lost

        # top boundary check
        a1 = self.radius - self.y
        if a1 >= 0: # the ball has crossed the ceiling a distance a1
            self.y = a1 + self.radius
            self.angle = - self.angle
            self.speed *= Particle.elastic

        # bottom boundary check
        a2 = self.y + self.radius - height
        if a2 >= 0: # the ball has sink down below the floor a distance a2
            self.y = height - self.radius - a2
            self.angle = - self.angle
            self.speed *= Particle.elastic

    def add_vector(self, vector1, vector2):
        a1 = vector1[0]
        sp1 = vector1[1]
        x1 = sp1 * math.cos(a1)
        y1 = sp1 * math.sin(a1)

        a2 = vector2[0]
        sp2 = vector2[1]
        x2 = sp2 * math.cos(a2)
        y2 = sp2 * math.sin(a2)

        sum_x = x1 + x2
        sum_y = y1 + y2
        sum_angle = math.atan2(sum_y , sum_x)
        # sum_mag = math.sqrt(math.pow(sum_x, 2) + math.pow(sum_y, 2))
        sum_mag = math.hypot(sum_x, sum_y)

        return sum_angle, sum_mag





