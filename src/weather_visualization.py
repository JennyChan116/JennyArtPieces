import sys
import math
import random
import pygame
sys.path.append(".")
from data.sample_weather_data import weather_data

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artistic Weather Visualization")
font = pygame.font.Font(None, 32)

def temp_to_color(temp):
    t = max(25, min(35, temp))
    ratio = (t - 25) / 10
    r = int(50 + 205 * ratio)
    g = int(100 + 80 * (1 - ratio))
    b = int(220 - 180 * ratio)
    return (r, g, b)

def draw_particles(day, frame):
    temp = (day["temp_min"] + day["temp_max"]) / 2
    humidity = (day["humidity_min"] + day["humidity_max"]) / 2
    wind = day["wind_speed"]
    desc = day["description"]
    count = int(120 + humidity * 1.2)
    cx = WIDTH // 2
    cy = HEIGHT // 2
    dot_radius = 220 + 30 * wind
    flicker = ("骤雨" in desc or "雷暴" in desc)
    for i in range(count):
        angle = 2 * math.pi * i / count + frame * (0.01 + wind * 0.008)
        base_r = dot_radius * (0.7 + 0.3 * random.random())
        x = int(cx + base_r * math.cos(angle) + random.uniform(-8, 8))
        y = int(cy + base_r * math.sin(angle) + random.uniform(-8, 8))
        color = temp_to_color(temp + random.uniform(-2, 2))
        alpha = int(60 + humidity * 1.2 + random.uniform(0, 40))
        size = 4 if not flicker else 7 if (frame // 8) % 2 == 0 else 4
        surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color + (alpha,), (size, size), size)
        screen.blit(surf, (x, y))

def draw_text(day):
    date_text = font.render(day["date"], True, (30,30,30))
    desc_text = font.render(day["description"], True, (60,60,60))
    screen.blit(date_text, (40, 40))
    screen.blit(desc_text, (40, 80))

def draw_background():
    # Artistic radial gradient background
    bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for r in range(0, WIDTH//2, 8):
        alpha = max(0, 120 - r//3)
        color = (180 + r//20, 200 - r//10, 255 - r//8, alpha)
        pygame.draw.circle(bg, color, (WIDTH//2, HEIGHT//2), r)
    screen.blit(bg, (0,0))

def main():
    clock = pygame.time.Clock()
    frame = 0
    day_idx = 0
    running = True
    auto_switch_interval = 180  # 约3秒
    last_switch = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((245, 245, 255))
        draw_background()
        draw_particles(weather_data[day_idx], frame)
        draw_text(weather_data[day_idx])
        pygame.display.flip()
        frame += 1
        # 自动切换日期
        if frame - last_switch > auto_switch_interval:
            day_idx = (day_idx + 1) % len(weather_data)
            last_switch = frame
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
