import pygame
################################################################################################################################################
# 1. Initialize pygame
pygame.init()

################################################################################################################################################
# 2. Create the screen
WIDTH, HEIGHT = 900, 600 # Width and height of the screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping n Pong!")

FPS = 60 # Frames per second

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50) # Font for the score
WINNING_SCORE = 10

################################################################################################################################################
# 3. Create the paddles
class Paddle:
    COLOR = WHITE
    VEL = 5 # Velocity of the paddle

    '''
    This is the constructor of the class
    the constructor is called when an object is created from the class
    x: x position of the paddle
    y: y position of the paddle
    width: width of the paddle
    height: height of the paddle
    '''
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    '''
    This draw function is used to draw the paddle on the screen
    self: refers to the object that is calling the function
    win: refers to the window on which the paddle is drawn
    '''
    def draw(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    '''
    This function is used to move the paddle up or down
    Small note: the y axis is inverted in pygame
    self: refers to the object that is calling the function
    up: refers to the direction in which the paddle is moved. True means up, False means down
    '''
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    '''
    This reset function is used to reset the paddle to its original position
    '''
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

################################################################################################################################################
# 4. Create the ball
class Ball:
    MAX_VEL = 6 # Maximum velocity of the ball
    COLOR = WHITE

    '''
    This is the constructor of the class
    the constructor is called when an object is created from the class
    x: x position of the ball
    y: y position of the ball
    radius: radius of the ball
    '''
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    '''
    This draw function is used to draw the ball on the screen
    win: refers to the window on which the ball is drawn
    '''
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    '''
    Move is used to move the ball
    '''
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


    '''
    This reset function is used to reset the ball to its original position
    '''
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
################################################################################################################################################
# 5. This function is used to draw the screen, paddles and ball
'''
win: refers to the window on which the ball is drawn
paddles: refers to the list of paddles
ball: refers to the ball
left_score: refers to the score of the left paddle
right_score: refers to the score of the right paddle
'''
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE) # Render the text for the left score
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE) # Render the text for the right score
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20)) # Blit the text on the screen. Bilt is used to draw text on the screen
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20)) # Blit the text on the screen. 

    for paddle in paddles: #For loop making sure that both paddles are drawn
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20): # Draw the lines in the middle
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

################################################################################################################################################
# 6. Function to handle the collision of the ball with the paddles and the walls
'''
ball: refers to the ball
left_paddle: refers to the left paddle
right_paddle: refers to the right paddle
'''
def handle_collision(ball, left_paddle, right_paddle):
    '''
    These conditions are used to check if the ball has collided with the walls
    if it has collided with the walls, the y velocity is reversed
    else if it has collided with the paddles, the x velocity is reversed
    '''
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height: # Check if the ball has collided with the left paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:   # Check if the ball has collided with the left paddle
                ball.x_vel *= -1 # if so, reverse the x velocity

                middle_y = left_paddle.y + left_paddle.height / 2 # Get the middle of the paddle
                difference_in_y = middle_y - ball.y # Get the difference between the middle of the paddle and the ball
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL # Get the reduction factor
                y_vel = difference_in_y / reduction_factor # Get the y velocity
                ball.y_vel = -1 * y_vel # Set the y velocity

    else: # Same as above but for the right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

################################################################################################################################################
# 7. Function to handle the movement of the paddles

'''
This function is used to handle the movement of the paddles
The basic idea is that if the user presses the up or down key, the paddle moves up or down respectively
keys: refers to the keys pressed by the user
left_paddle: refers to the left paddle
right_paddle: refers to the right paddle
'''
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

################################################################################################################################################
# 8. Function to handle the scoring and the main function of the game
def main():
    run = True
    clock = pygame.time.Clock() # Clock object to keep track of the FPS

    '''
    The paddles and the ball are initialized
    Making sure that the paddles are at the correct position and the ball is in the middle of the screen
    '''
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Variables to keep track of the scores. Default value is 0
    left_score = 0 
    right_score = 0

    while run:
        clock.tick(FPS) # Set the FPS
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) # Draw the screen

        # For loop to check if the user has quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed() # Get the keys pressed by the user
        handle_paddle_movement(keys, left_paddle, right_paddle) # Handle the movement of the paddles

        ball.move() # Move the ball
        handle_collision(ball, left_paddle, right_paddle) # Handle the collision of the ball with the paddles and the walls

        # Check if the ball has gone out of the screen
        # if it has, increase the score of the player who has not lost the ball
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        won = False # Variable to check if the game has been won by any player
        '''
        If the score of any player is greater than or equal to the winning score, the game is won
        The text to be displayed is set accordingly
        '''
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        '''
        If the game has been won, the text is displayed on the screen
        The game is paused for 5 seconds and then the game is reset
        '''
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE) # Render the text
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                            2, HEIGHT//2 - text.get_height()//2)) # Display the text
            pygame.display.update() # Update the display
            pygame.time.delay(5000) # Pause the game for 5 seconds
            ball.reset() # Reset the ball
            left_paddle.reset() # Reset the left paddle
            right_paddle.reset() # Reset the right paddle
            left_score = 0  # Reset the left score
            right_score = 0 # Reset the right score

    pygame.quit()


if __name__ == '__main__':
    main()
