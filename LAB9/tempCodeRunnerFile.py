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

