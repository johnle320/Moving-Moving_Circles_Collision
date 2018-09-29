from random import randint
from random import uniform
from Particle import Particle
import math
import pygame


class ParticleManager(object):

    def __init__(self):
        self.particles_list = []

    def generate_particles(self, num):

        for n in range(num):
            x = uniform(400, 600)
            y = uniform(200, 400)
            radius = randint(40, 50)
            speed = uniform(0, 1)
            angle = uniform(0, 2 * math.pi)
            p = Particle((x, y), radius, (2, angle), 4)
            self.particles_list.append(p)

        return self.particles_list

    def size(self):
        return len(self.particles_list)

    def pop(self):
        self.particles_list.pop()

    def get(self, index):
        return self.particles_list[index]

    def add(self, p):
        if type(p) is not Particle:
            raise TypeError('Not an instance of Particle class.')

        self.particles_list.append(p)

    def find_selected_particle(self, mouse_position):
        mouseX, mouseY = mouse_position

        for p in self.particles_list:
            d = math.hypot(p.x - mouseX, p.y - mouseY)
            if d <= p.radius:
                return p

        return None # if no selected particle, return NONE

    @staticmethod
    def collision_check(p1, p2):
        if ParticleManager.box_collision(p1, p2):  # fast check

            # thorough check: moderately cost computer resource
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            d_sq = pow(dx, 2) + pow(dy, 2)

            if d_sq <= pow(p1.radius + p2.radius, 2):  # avoid using square root to speed up
                print('bang')

        return False

    @staticmethod
    def collision_prediction(p1, p2, screen, sandwich, motion_analyze):
        # Decarte velocity of p1:
        (v1x, v1y) = (p1.speed * math.cos(p1.angle), p1.speed * math.sin(p1.angle))
        # Decarte velocity of p2:
        (v2x, v2y) = (p2.speed * math.cos(p2.angle), p2.speed * math.sin(p2.angle))

        # Relative velocity of p1 to p2:
        (v1x, v1y) = (v1x - v2x, v1y - v2y)
        if sandwich:
            # Draw it
            pygame.draw.lines(screen, [50, 255, 50], False,
                              [(p1.x, p1.y), (p1.x + pow(10, 2) * v1x, p1.y + pow(10, 2) * v1y), 2])

        # square magnitude of v1:
        v1_mag_sq = v1x * v1x + v1y * v1y



        # calculate the normal vector of the moving line of p1
        (n1x, n1y) = (v1y, -v1x)
        # square magnitude of n1:
        n1_mag_sq = v1_mag_sq

        # vector p1p2 (pointing from p1 to p2)
        (p1p2_x, p1p2_y) = (p2.x - p1.x, p2.y - p1.y)

        # check if p1 is coming toward p2:
        toward_ea_other = (v1x * p1p2_x + v1y * p1p2_y) > 0

        if not (n1x == 0 and n1y == 0) and toward_ea_other and not v1_mag_sq == 0:
            # magnitude of v1 We calculate vector u1 here so to save
            # the computer's resources.
            v1_mag = math.sqrt(v1_mag_sq)
            # Directional unit vector in the moving direction of p1.
            (u1x, u1y) = (x / v1_mag for x in (v1x, v1y))

            if sandwich:

                # Draw connecting lines between 2 circles
                pygame.draw.lines(screen, [255, 255, 255], False, [(p1.x, p1.y), (p2.x, p2.y)], 1)

                # Draw projecting line of the relative velocity
                (uN1x, uN1y) = (u1y, -u1x)
                (k1x, k1y) = (p1.x + uN1x * p1.radius, p1.y + uN1y * p1.radius)
                pygame.draw.lines(screen, [50, 255, 50], False,
                                  [(k1x, k1y), (k1x + pow(10, 3) * v1x, k1y + pow(10, 3) * v1y), 2])
                (t1x, t1y) = (p1.x - uN1x * p1.radius, p1.y - uN1y * p1.radius)
                pygame.draw.lines(screen, [50, 255, 50], False,
                                  [(t1x, t1y), (t1x + pow(10, 3) * v1x, t1y + pow(10, 3) * v1y), 2])

            # find the closest point of p1 to p2:
            # 1. find proj(p1p2) onto n1:
            scale3 = (p1p2_x * n1x + p1p2_y * n1y) / n1_mag_sq
            (p1p2N_x, p1p2N_y) = (n1x * scale3, n1y * scale3)
            # 2. find the position of p1 when it is closest to p2. Let it be "colliding position of p1": cp1
            (cp1_x, cp1_y) = (p2.x - p1p2N_x, p2.y - p1p2N_y)

            # closest square distance that the 2 particles can be
            closest_d_sq = pow(p1p2N_x, 2) + pow(p1p2N_y, 2)
            # minimum distance between the 2 particles to avoid colliding
            min_d = p1.radius + p2.radius

            # output the results
            if closest_d_sq < pow(min_d, 2): # then they are gonna hit
                # 3. find the collision position of p1

                scale4 = math.sqrt(pow(p1.radius + p2.radius, 2) - closest_d_sq)
                (p1_touch_x, p1_touch_y) = (cp1_x - u1x * scale4, cp1_y - u1y * scale4)

                (p1p2_touch_x, p1p2_touch_y) = (p2.x - p1_touch_x, p2.y - p1_touch_y)

                ratio = p1.radius / (p1.radius + p2.radius)
                (cld_p_x, cld_p_y) = (p1p2_touch_x * ratio + p1_touch_x, p1p2_touch_y * ratio + p1_touch_y)

                if sandwich:
                    # draw the position of p1 at collision
                    pygame.draw.circle(screen, [255, 255, 255], (int(p1_touch_x), int(p1_touch_y)), 4, 0)

                # draw the collision point
                pygame.draw.circle(screen, [randint(0, 255), 100, 100], (int(cld_p_x), int(cld_p_y)), 4, 0)

                if sandwich:
                    # draw as if p1 is at the collision point
                    p = Particle((p1_touch_x, p1_touch_y), p1.radius, (0, 0), p1.thickness)
                    p.display(screen)
                if motion_analyze:
                    print("gonna hit")
                return True
            else:
                if motion_analyze:
                    print("path is clear")
                return False
        elif not toward_ea_other:
            if motion_analyze:
                print("Further away")
            return False
        else: # p1 is not moving
            if motion_analyze:
                print("not moving")
            return False

    @staticmethod
    def box_collision(p1, p2):
        a1 = p1.radius * 2
        a2 = p2.radius * 2
        return abs(p1.x - p2.x) <= a1 + a2 and abs(p1.y - p2.y) <= a1 + a2
