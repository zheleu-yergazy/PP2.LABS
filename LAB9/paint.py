import pygame, math

def draw_menu(screen, shape, color, mouse_pos):
    
    qalam = pygame.draw.rect(screen, 'white', (272,24,30,28))
    if shape == "brush":
        pygame.draw.rect(screen, 'green', (268,21,38,57), 3)
    elif qalam.collidepoint(mouse_pos):
        pygame.draw.rect(screen, 'green', (268,21,38,57), 2)

    shapes = [
        ("eraser", pygame.draw.rect(screen, (0,0,0), (200, 57, 15, 15), 2)),
        ("circle", pygame.draw.circle(screen, (100,100,100), (337, 40), 10, 2)),
        ("square", pygame.draw.rect(screen, (100,100,100), (329,53,17,17),2)),
        ("right_triangle", pygame.draw.polygon(screen, (100,100,100), [(410,45),(430,45),(430,30)],2)),
        ("equilateral_triangle", pygame.draw.polygon(screen, (100,100,100), [(420,52),(410,68),(430,68)],2)),
        ("rhombus", pygame.draw.polygon(screen, (100,100,100), [(370,40),(380,30),(390,40),(380,50)],2)),
        ("rectangle", pygame.draw.rect(screen, (100,100,100), (368,55,25,15),2))]

    for sname, rect in shapes:
        if shape == sname:
            pygame.draw.rect(screen, 'green', rect.inflate(8,8), 2)
        elif rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'lightgreen', rect.inflate(8,8), 2)

    colors_list = [
        ((255,0,0), pygame.draw.rect(screen, (255,0,0), (709,24,15,15))),
        ((0,0,255), pygame.draw.rect(screen, (0,0,255), (689,24,15,15))),
        ((0,255,0), pygame.draw.rect(screen, (0,255,0), (689,43,15,15))),
        ((255,255,0), pygame.draw.rect(screen, (255,255,0), (669,24,15,15))),
        ((0,0,0), pygame.draw.rect(screen, (0,0,0), (650,24,15,15))),
        ((0,255,255), pygame.draw.rect(screen, (0,255,255), (669,43,15,15))),
        ((255,0,255), pygame.draw.rect(screen, (255,0,255), (709,43,15,15))),
        ((255,255,255), pygame.draw.rect(screen, (255,255,255), (650,43,15,15)))
    ]

    for col, rect in colors_list:
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'lightgreen', rect.inflate(4,4), 2)

    pygame.draw.rect(screen, color, (578,25,26,26))
    return shapes, colors_list, [qalam]

def draw_shape(surface, color, start, end, shape):
    x1,y1 = start
    x2,y2 = end
    w,h = x2-x1, y2-y1

    if shape == "rectangle":
        pygame.draw.rect(surface, color, pygame.Rect(x1,y1,w,h), 2)
    elif shape == "square":
        side = min(abs(w),abs(h))
        pygame.draw.rect(surface, color, pygame.Rect(x1,y1,side*(1 if w>0 else -1), side*(1 if h>0 else -1)), 2)
    elif shape == "circle":
        radius = int(math.sqrt(w**2 + h**2))
        pygame.draw.circle(surface, color, start, radius, 2)
    elif shape == "right_triangle":
        pygame.draw.polygon(surface, color, [(x1,y2),(x2,y2),(x2,y1)], 2)
    elif shape == "equilateral_triangle":
        pygame.draw.polygon(surface, color, [(x1+w//2,y1),(x1,y1+abs(h)),(x1+w,y1+abs(h))],2)
    elif shape == "rhombus":
        cx,cy = (x1+x2)//2, (y1+y2)//2
        pygame.draw.polygon(surface, color, [(cx,y1),(x2,cy),(cx,y2),(x1,cy)],2)

def draw_painting(screen, painting):
    for color, start, end, tool, radius in painting:
        if tool in ["brush", "eraser"]:
            pygame.draw.circle(screen, color if tool=="brush" else (255,255,255), start, radius)
        else:
            draw_shape(screen, color, start, end, tool)

def main():
    pygame.init()
    WIDTH, HEIGHT = 850,620
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    bg = pygame.image.load('bgpaint.jpeg')
    bg = pygame.transform.smoothscale(bg, (WIDTH,HEIGHT))
    marker = pygame.image.load('marker.jpg')
    marker = pygame.transform.smoothscale(marker, (29,30))
    eraser_img = pygame.image.load('eraser.png')
    eraser_img = pygame.transform.smoothscale(eraser_img, (20,20))

    area_top = 120
    painting = []
    shape = "circle"
    active_color = (255,255,255)
    drawing = False
    start_pos = None
    radius = 15  
    
    while True:
        clock.tick(120)
        screen.blit(bg,(0,0))
        pygame.draw.rect(screen,'white',(317,26,123,50))
        pygame.draw.rect(screen,'gray',(317,26,123,50),1)

        mouse = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and mouse[1] > area_top:
            if shape in ["brush", "eraser"]:
                painting.append((active_color, mouse, None, shape, radius))

        draw_painting(screen, painting)
        shapes_list, colors_list, qalams = draw_menu(screen, shape, active_color, mouse)
        if drawing and start_pos and mouse[1] > area_top and start_pos[1] > area_top:
            temp = screen.copy()
            draw_shape(temp, active_color, start_pos, mouse, shape)
            screen.blit(temp,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    painting.clear()
                elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    radius = min(radius + 1, 50)  
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    radius = max(radius - 1, 1)   
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_menu = False
                for q in qalams:
                    if q.collidepoint(event.pos):
                        shape = "brush"; clicked_menu = True
                for sname, rect in shapes_list:
                    if rect.collidepoint(event.pos):
                        shape = sname; clicked_menu = True
                for col, rect in colors_list:
                    if rect.collidepoint(event.pos):
                        active_color = col; clicked_menu = True
                if not clicked_menu and event.pos[1] > area_top:
                    drawing = True
                    start_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos and event.pos[1] > area_top:
                    painting.append((active_color, start_pos, event.pos, shape, radius))
                drawing = False
                start_pos = None
        
        font = pygame.font.SysFont('Verdana',10)
        size = font.render(f"{radius}",True,(50, 50, 50))
        screen.blit(size,(538,75))
        screen.blit(marker,(273,25))
        screen.blit(eraser_img,(198,55))
        pygame.display.update()
main()
