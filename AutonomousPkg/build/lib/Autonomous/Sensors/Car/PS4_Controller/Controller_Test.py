from PS4_Controller import PS4_Controller
import pygame

screen_x = 640
screen_y = 640

controller = PS4_Controller()
screen = pygame.display.set_mode((screen_x, screen_y))

left_x = screen_x/2
left_y = screen_y/2
right_x = left_x
right_y = left_y

left_rect = pygame.rect.Rect(left_x-20, left_y, 20, 20)
right_rect = pygame.rect.Rect(right_x+20, right_y, 20, 20)
left_clr = pygame.Color(0, 255, 0)
right_clr = pygame.Color(255,0,0)

def main():
    global screen, controller, left_x, right_x, left_y, right_y

    pygame.init()
    screen.fill(pygame.Color(255, 255, 255))
    pygame.draw.rect(screen, left_clr, left_rect)
    pygame.draw.rect(screen, right_clr, right_rect)
    while True:
        screen.fill(pygame.Color(255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        left_x += controller.Left_Stick_X
        left_y += controller.Left_Stick_Y

        left_rect.x = left_x
        left_rect.y = left_y

        right_x += controller.Right_Stick_X
        right_y += controller.Right_Stick_Y
        right_rect.x = right_x
        right_rect.y = right_y

        print(controller.Left_Stick_X, controller.Left_Stick_Y, controller.Right_Stick_X, controller.Right_Stick_Y)

        pygame.draw.rect(screen, left_clr, left_rect)
        pygame.draw.rect(screen, right_clr, right_rect)
        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")