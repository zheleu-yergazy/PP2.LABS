import os
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((580, 300))
pygame.display.set_caption("My Music Player")
font = pygame.font.SysFont("Arial", 26, bold=True)
music_folder = "mus_folder"
playlist = [os.path.join(music_folder, t) for t in os.listdir(music_folder) if t.endswith(".mp3")]

current = 0
volume = 0.5
paused = False

mixer.music.set_volume(volume)
bg = (40, 0, 60)
btn = (130, 0, 180)
btn_hov = (200, 0, 250)
Txt = (255, 220, 255)

buttons = {"play": pygame.Rect(100, 220, 80, 40),"stop": pygame.Rect(200, 220, 80, 40),"prev": pygame.Rect(300, 220, 80, 40),"next": pygame.Rect(400, 220, 80, 40)}

def play_music():
    global paused
    mixer.music.load(playlist[current])
    mixer.music.play()
    paused = False

def text(txt, pos):
    img = font.render(txt, True, Txt)
    screen.blit(img, pos)

def draw(status):
    screen.fill(bg)
    text("MEME-MUSIC", (200, 30))
    text(f"Трек: {os.path.basename(playlist[current])}", (50, 80))
    text(f"Громкость: {int(volume * 100)}%", (50, 120))
    text(status, (50, 160))

    for name, rect in buttons.items():
        color = btn_hov if rect.collidepoint(pygame.mouse.get_pos()) else btn
        pygame.draw.rect(screen, color, rect)
        text(name.capitalize(), (rect.x + 10, rect.y + 8))

    pygame.display.flip()


play_music()
status = "Играет"


while True:
    draw(status)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if buttons["play"].collidepoint(e.pos):
                if paused:
                    mixer.music.unpause()
                    paused = False
                    status = "Продолжает"
                elif mixer.music.get_busy():
                    mixer.music.pause()
                    paused = True
                    status = "Пауза"
                else:
                    play_music()
                    status = "Играет"

            elif buttons["stop"].collidepoint(e.pos):
                mixer.music.stop()
                status = "Остановлено"

            elif buttons["next"].collidepoint(e.pos):
                current = (current + 1) % len(playlist)
                play_music()
                status = "Следующий трек"

            elif buttons["prev"].collidepoint(e.pos):
                current = (current - 1) % len(playlist)
                play_music()
                status = "Предыдущий трек"

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False
            elif e.key == pygame.K_UP:
                volume = min(1.0, volume + 0.1)
                mixer.music.set_volume(volume)
            elif e.key == pygame.K_DOWN: 
                volume = max(0.0, volume - 0.1)
                mixer.music.set_volume(volume)
            elif e.key == pygame.K_RIGHT:
                current = (current + 1) % len(playlist)
                play_music()
                status = "Следующий трек"
            elif e.key == pygame.K_LEFT:
                current = (current - 1) % len(playlist)
                play_music()
                status = "Предыдущий трек"
            elif e.key == pygame.K_p:
                if paused:
                    mixer.music.unpause()
                    paused = False
                    status = "Продолжает"
                elif mixer.music.get_busy():
                    mixer.music.pause()
                    paused = True
                    status = "Пауза"
                else:
                    play_music()
                    status = "Играет"
            elif e.key == pygame.K_s:
                mixer.music.stop()
                status = "Остановлено"

