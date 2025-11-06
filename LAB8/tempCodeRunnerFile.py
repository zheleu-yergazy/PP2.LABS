import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Mini Paint")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    radius = 10
    mode = "draw"
    start_pos = None
    last_pos = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)
                    mode = "draw"
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                    mode = "draw"
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                    mode = "draw"
                elif event.key == pygame.K_e:
                    mode = "erase"
                elif event.key == pygame.K_c:
                    mode = "circle"
                elif event.key == pygame.K_w:
                    mode = "rect"
                elif event.key == pygame.K_SPACE:
                    screen.fill((0, 0, 0))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    radius = max(1, radius - 1)
                elif event.button == 3:
                    radius = min(50, radius + 1)
                elif event.button == 2:
                    start_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if start_pos:
                    end_pos = event.pos
                    if mode == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0],
                                                       end_pos[1] - start_pos[1]))
                        pygame.draw.rect(screen, color, rect, 3)
                    elif mode == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx ** 2 + dy ** 2) ** 0.5)
                        pygame.draw.circle(screen, color, start_pos, r, 3)
                    start_pos = None
                last_pos = None  # сбрасываем после отпускания

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and mode in ("draw", "erase"):
                    color_draw = (0, 0, 0) if mode == "erase" else color
                    if last_pos:
                        pygame.draw.line(screen, color_draw, last_pos, event.pos, radius * 2)
                    pygame.draw.circle(screen, color_draw, event.pos, radius)
                    last_pos = event.pos
                else:
                    last_pos = None

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
