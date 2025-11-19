
# (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 8
    color = (0, 0, 255)
    tool = "qalam"
    start_pos = None
    last_pos = None
    drawing = False

    font = pygame.font.SysFont("vardana", 24)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    tool = "qalam"; color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    tool = "qalam"; color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    tool = "qalam"; color = (0, 0, 255)
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_w:
                    tool = "rect"
                elif event.key == pygame.K_SPACE:
                    screen.fill((0, 0, 0))
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    radius = max(1, radius - 1)
                elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    radius = min(50, radius + 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if tool in ("qalam", "eraser"):
                        drawing = True
                        last_pos = event.pos
                    else:
                        start_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos
                    if tool == "rect":
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(screen, color, rect, max(1, radius//2))
                    elif tool == "circle":
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx*dx + dy*dy)**0.5)
                        pygame.draw.circle(screen, color, start_pos, r, max(1, radius//2))
                drawing = False
                start_pos = None
                last_pos = None

        if drawing and tool in ("qalam", "eraser"):
            pos = pygame.mouse.get_pos()
            if tool == "qalam":
                draw_color = color
            else:
                draw_color = (0, 0, 0)

        if last_pos:
            pygame.draw.circle(screen, draw_color, pos, radius)
            last_pos = pos

        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 640, 25))
        text = font.render(f"Tool: {tool}  |  Color: {color}  |  Size: {radius}", True, (255, 255, 255))
        screen.blit(text, (10, 5))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
