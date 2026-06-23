import pygame
import math
import statistics
import random
import pyautogui

# ----------------------------
# Settings
# ----------------------------
WIDTH, HEIGHT = 1000, 700
TARGET_RADIUS = 11
CLICK_RADIUS = 2
NUM_CLICKS = 35

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Accuracy & Precision Test")

font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

target = (WIDTH // 2, HEIGHT // 2)
clicks = []

screen_width, screen_height = pyautogui.size()


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


running = True

while running:
    screen.fill((245, 245, 245))

    # Draw target
    pygame.draw.circle(screen, (255, 0, 0), target, TARGET_RADIUS)
    pygame.draw.circle(screen, (0, 0, 0), target, TARGET_RADIUS + 2, 1)

    # Draw clicks
    for c in clicks:
        pygame.draw.circle(screen, (0, 100, 255), c, CLICK_RADIUS)

    txt = font.render(
        f"Click the target ({len(clicks)}/{NUM_CLICKS})",
        True,
        (0, 0, 0),
    )
    screen.blit(txt, (20, 20))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(clicks) < NUM_CLICKS:
                clicks.append(event.pos)
                # Generate random X and Y coordinates within screen boundaries
                random_x = random.randint(0, screen_width - 1)
                random_y = random.randint(0, screen_height - 1)

                # Move the cursor to the random location
                pyautogui.moveTo(random_x, random_y)

    if len(clicks) == NUM_CLICKS:
        running = False

    clock.tick(120)

pygame.quit()

# ----------------------------
# Calculations
# ----------------------------

xs = [p[0] for p in clicks]
ys = [p[1] for p in clicks]

mean_x = statistics.mean(xs)
mean_y = statistics.mean(ys)
mean_point = (mean_x, mean_y)

# Accuracy
accuracy_error = distance(mean_point, target)

# Precision (RMS spread)
precision = math.sqrt(
    sum(
        (x - mean_x) ** 2 + (y - mean_y) ** 2
        for x, y in clicks
    ) / len(clicks)
)

# Radial errors
errors = [distance(c, target) for c in clicks]

mean_radial_error = statistics.mean(errors)
max_error = max(errors)

# CEP50 and CEP95
sorted_errors = sorted(errors)

cep50 = sorted_errors[int(0.50 * len(sorted_errors))]
cep95 = sorted_errors[min(int(0.95 * len(sorted_errors)), len(sorted_errors)-1)]

# ----------------------------
# Results
# ----------------------------

print("\n========== RESULTS ==========")
print(f"Target            : {target}")
print(f"Average Click     : ({mean_x:.2f}, {mean_y:.2f})")
print(f"Accuracy Error    : {accuracy_error:.2f} px")
print(f"Precision (RMS)   : {precision:.2f} px")
print(f"Mean Radial Error : {mean_radial_error:.2f} px")
print(f"CEP50             : {cep50:.2f} px")
print(f"CEP95             : {cep95:.2f} px")
print(f"Maximum Error     : {max_error:.2f} px")
print("=============================\n")
