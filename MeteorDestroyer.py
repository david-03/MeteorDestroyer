import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constant variables
WIN_WIDTH = 1200
WIN_HEIGHT = 900
DELAY = 3000
SPACING = 64
EXPLOSION = 500
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("Agency FB", 30)

# Initialize window object
win = 0


def get_angle(meteor_x_speed, meteor_y_speed, speed):
    # Angle
    if meteor_x_speed == 0:
        if meteor_y_speed < 0:
            return 90
        else:
            return -90
    elif meteor_y_speed == 0:
        if meteor_x_speed < 0:
            return 180
        else:
            return 0
    else:
        # Calculate angle based on arc cos
        angle = math.acos(meteor_x_speed / speed)
        # If the meteor goes downwards (positive y speed), then the angle is negative (Cartesian coordinate system)
        if meteor_y_speed > 0:
            angle = -angle
        # Convert radians to degrees
        angle = angle / math.pi * 180
        return angle


# Check if asteroids are too close
def check(mouse_x, mouse_y, asteroids):
    if mouse_x < 0 or mouse_y < 0 or mouse_x > WIN_WIDTH - 0 or mouse_y > WIN_HEIGHT - 0:
        return False
    for i in range(SPACING):
        for j in range(SPACING):
            # If mouse position is too close to existing asteroid, return False and don't create new asteroid
            if (mouse_x - i, mouse_y - j) in asteroids.values():
                return False
    return True


def main():
    global win

    # Background music
    pygame.mixer.music.load("data\\background.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    # Load high score
    try:
        try:
            high_score_file = open("data\\HighScore.txt", "r")
            high_score = int(high_score_file.read())
        except ValueError:
            high_score = 0
    except FileNotFoundError:
        high_score = 0

    # Initializing local variables
    score = 0
    max_asteroid = 5
    frames = 0
    explode_time = -1
    speed = 0
    meteor_x_speed = 0
    meteor_y_speed = 0
    meteor_x = WIN_WIDTH // 2
    meteor_y = WIN_HEIGHT // 2
    star_x = 0
    star_y = 0
    paused = (-1, -1)
    asteroids = {}
    click = False
    playing = True
    start = True

    # Load useful images
    asteroid = pygame.transform.scale(pygame.image.load("data\\asteroid.png"), (SPACING, SPACING))
    meteor_img = pygame.image.load("data\\meteor.png")
    meteor_flipped_img = pygame.image.load("data\\meteor_flipped.png")
    explosion = pygame.transform.scale(pygame.image.load("data\\explosion.png"), (2 * SPACING, 2 * SPACING))
    star = pygame.image.load("data\\star.png")
    right_star = pygame.transform.rotate(star, 5)
    left_star = pygame.transform.rotate(star, -5)

    # Load sounds
    placing_sound = pygame.mixer.Sound("data\\place.wav")
    placing_sound.set_volume(0.9)
    removing_sound = pygame.mixer.Sound("data\\remove.wav")
    removing_sound.set_volume(1.0)
    explosion_sound = pygame.mixer.Sound("data\\explosion.wav")
    explosion_sound.set_volume(0.3)
    losing_sound = pygame.mixer.Sound("data\\lose.wav")
    losing_sound.set_volume(1.0)
    star_sound = pygame.mixer.Sound("data\\star.wav")
    star_sound.set_volume(1.0)

    # Rotate images based on angle
    angle = get_angle(meteor_x_speed, meteor_y_speed, speed)
    meteor = pygame.transform.rotate(meteor_img, 45 + angle)
    meteor_flipped = pygame.transform.rotate(meteor_flipped_img, 45 + angle)

    # Fit background to window size
    background = pygame.image.load("data\\space.png")
    adjusted_background = pygame.transform.scale(background, (WIN_WIDTH, WIN_HEIGHT))

    # Generate star location

    # Create clock to regulate frames per second
    my_clock = pygame.time.Clock()

    # Game loop
    game = True
    while game:
        # Frames per second
        my_clock.tick(60)
        frames += 1
        # Re-draw background every frame
        win.blit(adjusted_background, (0, 0))

        # Message displays if player has not started yet
        if start:
            start_msg = FONT.render("TO START, PRESS 'S'", True, WHITE)
            win.blit(start_msg, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 60))

        for event in pygame.event.get():
            # Quit (end game loop)
            if event.type == pygame.QUIT:
                # Main function returns False (this ends the function)
                return False
            # Check if user clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            # Check if user released click
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False
            # Check if user restarts
            if event.type == pygame.KEYDOWN:
                # Fullscreen when F11 is pressed
                if event.key == pygame.K_F11 and win.get_flags() != -2147483648:
                    w, h = win.get_size()
                    win = pygame.display.set_mode((w, h), pygame.FULLSCREEN)

                # Escape -> resize window out of fullscreen
                if event.key == pygame.K_ESCAPE and win.get_flags() == -2147483648:
                    w, h = win.get_size()
                    win = pygame.display.set_mode((w, h))

                # If player wants to restart
                if event.key == pygame.K_r and not playing:
                    # Call main function (recursive function)
                    main()
                    # If the new main function ends, end this main function as well
                    return False
                # Check if player is ready to start
                elif event.key == pygame.K_s and start:
                    # Set speed
                    speed = 15
                    # Random sign (positive or negative)
                    sign = random.choice([-1, 1])
                    # Random horizontal speed
                    meteor_x_speed = random.randint(-speed, speed)
                    # Vertical speed calculated from speed vector and horizontal speed
                    meteor_y_speed = round(sign * (math.sqrt(speed * speed - meteor_x_speed * meteor_x_speed)))
                    # Rotate images based on angle
                    angle = get_angle(meteor_x_speed, meteor_y_speed, speed)
                    meteor = pygame.transform.rotate(meteor_img, 45 + angle)
                    meteor_flipped = pygame.transform.rotate(meteor_flipped_img, 45 + angle)
                    # Generate star location
                    star_x = random.randint(WIN_WIDTH // 3, 2 * WIN_WIDTH // 3)
                    star_y = random.randint(WIN_HEIGHT // 3, 2 * WIN_HEIGHT // 3)

                    start = False

        # Display number of asteroids left
        num_left = FONT.render("ASTEROIDS LEFT : " + str(round(max_asteroid) - len(asteroids)), True, WHITE)
        win.blit(num_left, (WIN_WIDTH - 200, 10))
        # Display score
        score_text = FONT.render("SCORE : " + str(score), True, WHITE)
        win.blit(score_text, (10, 10))

        # Create an asteroid and insert its time and position in the asteroids dictionary
        if click and len(asteroids) < round(max_asteroid) and not start:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # If mouse not too close to existing asteroid, create a new one
            if check(mouse_x, mouse_y, asteroids):
                # Stop other sounds before playing new sound
                pygame.mixer.Sound.stop(placing_sound)
                placing_sound.play()
                # Insert asteroid in dictionary
                asteroids[pygame.time.get_ticks()] = (mouse_x - SPACING // 2, mouse_y - SPACING // 2)

        # Create masks for the meteor, the asteroid and the star
        meteor_mask = pygame.mask.from_surface(meteor)
        asteroid_mask = pygame.mask.from_surface(asteroid)
        star_mask = pygame.mask.from_surface(star)

        # Check if the meteor collides with the star
        star_offset = (meteor_x - star_x + 15, meteor_y - star_y + 15)
        star_collide = meteor_mask.overlap(star_mask, star_offset)
        if star_collide:
            pygame.mixer.Sound.stop(star_sound)
            star_sound.play()
            star_x = random.randint(WIN_WIDTH // 3, 2 * WIN_WIDTH // 3)
            star_y = random.randint(WIN_HEIGHT // 3, 2 * WIN_HEIGHT // 3)
            score += 200

        # Empty list of dead asteroids
        popped = []
        # Iterate through the asteroids dictionary
        for (time, (x, y)) in asteroids.items():

            # Create a rectangle around meteor image
            meteor_rect = pygame.Rect((meteor_x, meteor_y), meteor.get_size())
            # Get the center of the rectangle, which is also the center of the meteor
            (mx, my) = meteor_rect.center
            # Calculate the offset between each asteroid's center and the meteor
            offset_x = mx - (x + SPACING // 2)
            offset_y = my - (y + SPACING // 2)
            # Check if the two masks overlap based on their offset
            collide = meteor_mask.overlap(asteroid_mask, (offset_x, offset_y))

            if playing and not start:  # If playing and not start (xD can't be any clearer than that,
                # if you need comments to explain this shite then you should go and get help)

                # Check if there is collision between the meteor and an asteroid
                if collide and paused == (-1, -1):
                    # Play explosion sound
                    explosion_sound.play()
                    # Increase score by 50
                    score += 50
                    # The maximum number of asteroids increases every four collisions
                    max_asteroid += 0.25
                    # The speed increases every two collisions
                    if max_asteroid % 0.5 == 0:
                        speed += 1
                    # Paused variable used to determine where to draw explosion
                    # and to set a timer before the next collision can happen
                    # (otherwise the meteor would hit the same asteroid or nearby ones multiple times)
                    paused = (x, y)
                    # Set a timer for the explosion duration
                    explode_time = pygame.time.get_ticks()
                    # If the asteroid is not already dead, kill it
                    if time not in popped:
                        popped.append(time)

                    # Set new x speed for the meteor
                    # 50% of the time, it only interchanges x speed and y speed
                    # other 50% of the time, it changes the speed randomly
                    meteor_x_speed = -meteor_y_speed + random.randint(0, 1) * random.randint(0, speed -
                                                                                             abs(meteor_y_speed))
                    # Calculate y speed based on x speed and total speed
                    meteor_y_speed = round(math.sqrt(speed * speed - meteor_x_speed * meteor_x_speed))
                    # Set the sign so that the meteor will bounce towards the center if it's near the edges
                    if meteor_x < WIN_WIDTH // 3:
                        meteor_x_speed = abs(meteor_x_speed)
                    elif meteor_x >= 2 * WIN_WIDTH // 3:
                        meteor_x_speed = -abs(meteor_x_speed)
                    if meteor_y < WIN_HEIGHT // 3:
                        meteor_y_speed = abs(meteor_y_speed)
                    elif meteor_y >= 2 * WIN_HEIGHT // 3:
                        meteor_y_speed = -abs(meteor_y_speed)

                    # Rotate images based on new angle
                    angle = get_angle(meteor_x_speed, meteor_y_speed, speed)
                    meteor = pygame.transform.rotate(meteor_img, 45 + angle)
                    meteor_flipped = pygame.transform.rotate(meteor_flipped_img, 45 + angle)

            # Draw each asteroid if it hasn't exceeded the time limit
            if pygame.time.get_ticks() - time < DELAY and time not in popped:
                win.blit(asteroid, (x, y))
            else:
                if time not in popped:
                    popped.append(time)

        # If the asteroid's dead, it is popped from the dictionary
        for time in popped:
            # Stopping other sounds before playing new sound
            pygame.mixer.Sound.stop(removing_sound)
            removing_sound.play()
            # Remove asteroid from dictionary
            asteroids.pop(time)

        # If there is collision, draw image of explosion at the correct place
        if paused != (-1, -1):
            x, y = paused
            win.blit(explosion, (x - SPACING // 2, y - SPACING // 2))

        # Animation (image changes four times per second)
        if not start and playing:
            if frames >= 30:
                frames = 0
            if frames < 15:
                win.blit(meteor, (meteor_x, meteor_y))
                win.blit(right_star, (star_x, star_y))
            else:
                win.blit(meteor_flipped, (meteor_x, meteor_y))
                win.blit(left_star, (star_x, star_y))

        # The collision detection system pauses for 500 ms, after that it resets
        if pygame.time.get_ticks() - explode_time >= EXPLOSION:
            paused = (-1, -1)

        # Apply position change every 5 frames
        if frames % 5 == 0:
            meteor_x += meteor_x_speed
            meteor_y += meteor_y_speed

        # Check if dead
        if meteor_x < -meteor.get_width() or meteor_y < -meteor.get_height() \
                or meteor_x > WIN_WIDTH or meteor_y > WIN_HEIGHT:
            # Fade out background music
            pygame.mixer.music.fadeout(500)
            # Play losing sound effect
            if playing:
                losing_sound.play()
                playing = False
            # Update high score
            if score > int(high_score):
                high_score = score
                with open("data\\HighScore.txt", "w") as high_score_file:
                    high_score_file.write(str(score))
            # Display high score
            lost = FONT.render("HIGH SCORE : " + str(high_score), True, WHITE)
            win.blit(lost, (WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2 - 50))
            # Display restart message
            restart = FONT.render("TO RESTART, PRESS 'R'", True, WHITE)
            win.blit(restart, (WIN_WIDTH // 2 - 120, WIN_HEIGHT - 50))

        # Update display
        pygame.display.flip()


if __name__ == '__main__':
    try:
        # Create window
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("MeteorDestroyer")
        icon = pygame.image.load('data\\meteor.png')
        pygame.display.set_icon(icon)
        # Call main function
        main()

    except pygame.error:
        pass

    pygame.quit()
