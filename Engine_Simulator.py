import pygame
from random import uniform
import math

from Particle import Particle
from ParticlesManager import ParticleManager
from DashPoint import Point

pygame.init()

[width, height] = [800, 700]
screen = pygame.display.set_mode((width, height))

background_color = [0, 0, 0]
screen.fill(background_color)

# change the caption name of the window
pygame.display.set_caption('Physics Simulation')
# Redraw the window
pygame.display.flip()

# Create an instance of Particles_Management.
# A particles_manager hold responsible to generates and manage a list of particles_manager
particles_manager = ParticleManager()

# generate a group of particles
particles_manager.generate_particles(0)
r1 = 80
p1 = Particle((r1 + 5, r1 + 5), r1, (1, math.pi / 3), 2)
r2 = 110
p2 = Particle((width - r2 - 5, height - r2 - 5), r2, (2, math.pi / 3 - math.pi), 2)
particles_manager.add(p1)
particles_manager.add(p2)


# generate the clock for the game.
# later inside the loop we call <clock.tick(number). The bigger the number, the faster the game.
# Question: can we put it outside?
clock = pygame.time.Clock()

selected_particle = None

# WHAT-IT-DOES: 1-check the state of game, 2- check user interaction with the game (mouse clicks)
# 3- calculate and update particles' motions, 4- reflect that on the screen.
running = True  # Condition for the game engine.
while running:  # Game loop

    # Erase the screen:
    # Intuitively, it would be more intuitive to one's thought to only clear the screen after
    # the calculation is done.
    # Bu to save time, I think we should erase the screen at the beginning of the loop
    # so that the screen would be cleared and make ready to be redrawn again once the
    # calculation of game state is done.
    screen.fill(background_color)

    # Get the position of the mouse when it is within the window.
    (mouseX, mouseY) = pygame.mouse.get_pos()

    # WHAT-IT-DOES: loop through all the event in the event-queue returned from pygame.event.get()
    # REASON: to check 1-if the game is quit, 2- if the mouse is clicked on any particle
    for event in pygame.event.get():

        # if the mouse has clicked the "x" sign of the game window.
        # Then pygame.QUIT would be inserted in the event-queue
        if event.type == pygame.QUIT:
            running = False # stop the game loop

        # Check if the mouse is clicked and HOLD anywhere inside the game window
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Then check if the mouse click any particle by asking the particles_manager, given her
            # the mouse-clicked-coordinate. Particles_manger would return the particle selected by the mouse
            # if there's any OR return NONE otherwise.
            # Note: we save the selected particle to "selected_particle" variable declared outside the loop
            # so that in the next clause checking if the mouse has released yet, we would know whether there is
            # a particle is currently hold by the mouse.
            selected_particle = particles_manager.find_selected_particle((mouseX, mouseY))

            # if there is an particle selected
            if selected_particle:
                # highlight the ball:
                selected_particle.color = [255, 255, 255]

        # Check if the mouse releases its click to free the selected particle
        # by checking if the MOUSEBUTTONUP is in the event-queue. Note that we look for
        # the MOUSEBUTTONUP only after looking for MOUSEBUTTONDOWN
        elif event.type == pygame.MOUSEBUTTONUP:

            # if there is a particle being selected
            if selected_particle:
                # 1. unhighlight the particle
                selected_particle.color = selected_particle.oldColor
                # 2. then free the particle
                selected_particle = None

    # putting this clause outside the loop save many steps.
    # because there is only one particle selected at a time.
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        # change speed and angle of the particle so its center would follow wherever the mouse goes
        selected_particle.drag_move_params_update(screen, (mouseX, mouseY))

    # a line connecting 2 circles.
    # Point.draw_dashed_line(screen, [255, 255, 255], (p1.x, p1.y), (p2.x, p2.y), 1, 10 )

    p1.move(screen)
    p2.move(screen)
    p1.bounce(screen)
    p2.bounce(screen)

    # plot the closest position of p1 to p2 in case of collision.
    ParticleManager.collision_prediction(p1, p2, screen, True, False)

    p1.display(screen)
    p2.display(screen)

    # redraw all the particles with their new position:
    # for (i, p) in enumerate(particles_manager.particles_list):
    #     # given the screen, calculate p new position.
    #     p.move(screen)
    #
    #     for p2 in particles_manager.particles_list[i + 1:]:
    #
    #     p.bounce(screen)  # check and reflect if p is bouncing off the frame.
    #     p.display(screen) # display the particle on the screen

    pygame.display.update()
    clock.tick(20)

