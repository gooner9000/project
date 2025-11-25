import pygame
import numpy as np
import os

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1100, 800
N_PARTICLES = 500
N_TYPES = 4
R_MAX = 80
R_BOND_FORM = 15
R_BOND_LEN = 20
FRICTION = 0.80
DT = 0.4
FORCE_FACTOR = 0.3
SPRING_K = 0.1
SAVE_FILE = "saved_rules.npy"

# UI Constants
UI_START_X = 50
UI_START_Y = 70
CELL_WIDTH = 60
CELL_HEIGHT = 30

COLOR_DEFS = [
    {"name": "RED", "rgb": (255, 50, 50)},
    {"name": "GREEN", "rgb": (50, 255, 50)},
    {"name": "BLUE", "rgb": (50, 50, 255)},
    {"name": "YELLO", "rgb": (255, 255, 50)},
    {"name": "CYAN", "rgb": (50, 255, 255)},
    {"name": "MAGEN", "rgb": (255, 50, 255)},
]
N_TYPES = min(N_TYPES, len(COLOR_DEFS))


def respawn_particles():
    positions = np.random.rand(N_PARTICLES, 2) * [WIDTH, HEIGHT]
    velocities = np.zeros((N_PARTICLES, 2))
    types = np.random.randint(0, N_TYPES, N_PARTICLES)
    bonds = []
    bond_counts = np.zeros(N_PARTICLES, dtype=int)
    return positions, velocities, types, bonds, bond_counts


def generate_random_rules():
    return np.random.uniform(-0.5, 0.5, (N_TYPES, N_TYPES))


def generate_zero_rules():
    return np.zeros((N_TYPES, N_TYPES))


def save_rules(rules):
    try:
        np.save(SAVE_FILE, rules)
        return "Rules Saved!"
    except Exception as e:
        return f"Error: {e}"


def load_rules():
    if os.path.exists(SAVE_FILE):
        try:
            rules = np.load(SAVE_FILE)
            # Ensure shape matches (in case you changed N_TYPES)
            if rules.shape == (N_TYPES, N_TYPES):
                return rules, "Rules Loaded!"
            else:
                return None, "Save file mismatch!"
        except:
            return None, "Corrupt Save File"
    return None, "No Save Found!"


def update_physics(positions, velocities, types, rules, bonds, bond_counts, max_bonds):
    # 1. Standard Particle Forces
    x = positions[:, 0:1]
    y = positions[:, 1:2]
    dx = x.T - x
    dy = y.T - y

    dx = np.where(dx > WIDTH / 2, dx - WIDTH, dx)
    dx = np.where(dx < -WIDTH / 2, dx + WIDTH, dx)
    dy = np.where(dy > HEIGHT / 2, dy - HEIGHT, dy)
    dy = np.where(dy < -HEIGHT / 2, dy + HEIGHT, dy)

    r2 = dx ** 2 + dy ** 2
    r2 = np.maximum(r2, 0.01)
    r = np.sqrt(r2)

    mask = (r > 0) & (r < R_MAX)
    f_magnitude = np.zeros((N_PARTICLES, N_PARTICLES))
    f_magnitude[mask] = (1 - r[mask] / R_MAX)

    type_matrix_i = np.tile(types, (N_PARTICLES, 1)).T
    type_matrix_j = np.tile(types, (N_PARTICLES, 1))
    interactions = rules[type_matrix_i, type_matrix_j]
    f_magnitude *= interactions * FORCE_FACTOR

    vx_change = np.sum((dx / r) * f_magnitude, axis=1)
    vy_change = np.sum((dy / r) * f_magnitude, axis=1)

    velocities[:, 0] += vx_change * DT
    velocities[:, 1] += vy_change * DT

    # 2. Bond Physics
    if len(bonds) > 0:
        for idx, (p1, p2) in enumerate(bonds):
            bx = positions[p2, 0] - positions[p1, 0]
            by = positions[p2, 1] - positions[p1, 1]

            if bx > WIDTH / 2:
                bx -= WIDTH
            elif bx < -WIDTH / 2:
                bx += WIDTH
            if by > HEIGHT / 2:
                by -= HEIGHT
            elif by < -HEIGHT / 2:
                by += HEIGHT

            dist = np.sqrt(bx * bx + by * by)
            if dist < 0.1: dist = 0.1

            force = (dist - R_BOND_LEN) * SPRING_K
            fx = (bx / dist) * force
            fy = (by / dist) * force

            velocities[p1, 0] += fx * DT
            velocities[p1, 1] += fy * DT
            velocities[p2, 0] -= fx * DT
            velocities[p2, 1] -= fy * DT

    # 3. Form New Bonds
    close_mask = (r > 0.1) & (r < R_BOND_FORM)
    potential_pairs = np.argwhere(close_mask)
    np.random.shuffle(potential_pairs)

    checks = 0
    for i, j in potential_pairs:
        if checks > 50: break
        if i >= j: continue

        if bond_counts[i] >= max_bonds or bond_counts[j] >= max_bonds:
            continue

        force_i_j = rules[types[i]][types[j]]
        force_j_i = rules[types[j]][types[i]]

        if force_i_j > 0.5 or force_j_i > 0.5:
            already_bonded = False
            for b1, b2 in bonds:
                if (b1 == i and b2 == j) or (b1 == j and b2 == i):
                    already_bonded = True
                    break

            if not already_bonded:
                bonds.append((i, j))
                bond_counts[i] += 1
                bond_counts[j] += 1
                checks += 1

    velocities *= FRICTION
    positions += velocities * DT
    positions[:, 0] %= WIDTH
    positions[:, 1] %= HEIGHT

    return positions, velocities, bonds, bond_counts


def draw_ui(screen, rules, font, steps_per_frame, paused, max_bonds, message, msg_timer):
    panel_h = UI_START_Y + (N_TYPES * CELL_HEIGHT) + 40
    panel_w = UI_START_X + 80 + (N_TYPES * CELL_WIDTH) + 20

    s = pygame.Surface((panel_w + 30, panel_h))
    s.set_alpha(220)
    s.fill((30, 30, 30))
    screen.blit(s, (0, 0))

    target_text = font.render("TARGET (ATTRACTS)", True, (150, 150, 150))
    screen.blit(target_text, (UI_START_X + 80, UI_START_Y - 45))

    actor_text = font.render("ACTOR", True, (150, 150, 150))
    actor_text = pygame.transform.rotate(actor_text, 90)
    screen.blit(actor_text, (10, UI_START_Y))

    # Bond UI
    bond_y = panel_h - 25
    bond_text = font.render(f"MAX BONDS: {max_bonds} (UP/DOWN)", True, (255, 200, 50))
    screen.blit(bond_text, (UI_START_X, bond_y))

    # Header
    status_text = "PAUSED" if paused else f"SPEED: {steps_per_frame}x"
    header_col = (255, 100, 100) if paused else (100, 255, 100)
    status = font.render(status_text, True, header_col)
    screen.blit(status, (20, 10))

    controls = font.render("S: Save | L: Load | C: Clear | R: Respawn", True, (180, 180, 180))
    screen.blit(controls, (150, 10))

    # Grid
    for j in range(N_TYPES):
        col_x = UI_START_X + 80 + j * CELL_WIDTH
        name = font.render(COLOR_DEFS[j]["name"][:3], True, COLOR_DEFS[j]["rgb"])
        screen.blit(name, (col_x + 10, UI_START_Y - 20))

    for i in range(N_TYPES):
        row_y = UI_START_Y + i * CELL_HEIGHT
        name = font.render(COLOR_DEFS[i]["name"], True, COLOR_DEFS[i]["rgb"])
        screen.blit(name, (UI_START_X, row_y + 5))

        for j in range(N_TYPES):
            col_x = UI_START_X + 80 + j * CELL_WIDTH
            val = rules[i][j]
            c_val = int(abs(val) * 255)
            if val > 0:
                bg_col = (0, c_val // 2 + 20, 0)
                txt_col = (150, 255, 150)
            else:
                bg_col = (c_val // 2 + 20, 0, 0)
                txt_col = (255, 150, 150)

            if val > 0.5:
                pygame.draw.rect(screen, (255, 255, 255), (col_x, row_y, CELL_WIDTH - 2, CELL_HEIGHT - 2), 1)

            pygame.draw.rect(screen, bg_col, (col_x + 1, row_y + 1, CELL_WIDTH - 4, CELL_HEIGHT - 4))
            val_str = f"{val:+.1f}"
            txt = font.render(val_str, True, txt_col)
            screen.blit(txt, (col_x + 10, row_y + 5))

    # --- MESSAGE OVERLAY ---
    if msg_timer > 0:
        msg_s = font.render(message, True, (255, 255, 255))
        # Draw a black box behind text for contrast
        bg_rect = msg_s.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        bg_rect.inflate_ip(20, 10)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)
        screen.blit(msg_s, msg_s.get_rect(center=(WIDTH // 2, HEIGHT - 50)))


def handle_mouse_click(pos, rules, button):
    mx, my = pos
    grid_x = UI_START_X + 80
    grid_y = UI_START_Y
    if mx < grid_x or my < grid_y: return rules
    col = (mx - grid_x) // CELL_WIDTH
    row = (my - grid_y) // CELL_HEIGHT
    if 0 <= row < N_TYPES and 0 <= col < N_TYPES:
        change = 0.1 if button == 1 else -0.1
        rules[row][col] = np.clip(rules[row][col] + change, -1.0, 1.0)
    return rules


def main():
    pygame.init()
    font = pygame.font.SysFont("consolas", 14, bold=True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Life - Save/Load Enabled")
    clock = pygame.time.Clock()

    positions, velocities, types, bonds, bond_counts = respawn_particles()
    rules = generate_zero_rules()

    paused = False
    steps_per_frame = 1
    max_bonds = 2

    # Message Logic
    message = ""
    msg_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    positions, velocities, types, bonds, bond_counts = respawn_particles()
                    message = "Particles Respawned"
                    msg_timer = 120  # Frames

                elif event.key == pygame.K_RETURN:
                    rules = generate_random_rules()
                    positions, velocities, types, bonds, bond_counts = respawn_particles()
                    message = "Random Rules Generated"
                    msg_timer = 120

                elif event.key == pygame.K_c:
                    rules = generate_zero_rules()
                    positions, velocities, types, bonds, bond_counts = respawn_particles()
                    message = "Rules Cleared (Zero)"
                    msg_timer = 120

                # --- SAVE / LOAD ---
                elif event.key == pygame.K_s:
                    message = save_rules(rules)
                    msg_timer = 120

                elif event.key == pygame.K_l:
                    loaded_rules, msg = load_rules()
                    message = msg
                    msg_timer = 120
                    if loaded_rules is not None:
                        rules = loaded_rules
                        # Optionally respawn to see the rules fresh
                        # positions, velocities, types, bonds, bond_counts = respawn_particles()

                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    steps_per_frame = min(steps_per_frame + 1, 10)
                elif event.key == pygame.K_LEFT:
                    steps_per_frame = max(steps_per_frame - 1, 1)
                elif event.key == pygame.K_UP:
                    max_bonds += 1
                elif event.key == pygame.K_DOWN:
                    max_bonds = max(0, max_bonds - 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                rules = handle_mouse_click(event.pos, rules, event.button)

        if not paused:
            for _ in range(steps_per_frame):
                positions, velocities, bonds, bond_counts = update_physics(
                    positions, velocities, types, rules, bonds, bond_counts, max_bonds
                )

        screen.fill((20, 20, 20))

        # Draw Bonds
        for p1, p2 in bonds:
            x1, y1 = positions[p1]
            x2, y2 = positions[p2]
            if abs(x1 - x2) < WIDTH / 2 and abs(y1 - y2) < HEIGHT / 2:
                pygame.draw.line(screen, (100, 100, 100), (x1, y1), (x2, y2), 1)

        # Draw Particles
        for i in range(N_PARTICLES):
            x, y = int(positions[i, 0]), int(positions[i, 1])
            color = COLOR_DEFS[types[i]]["rgb"]
            if bond_counts[i] > 0:
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
            pygame.draw.circle(screen, color, (x, y), 3)

        # Decrement message timer
        if msg_timer > 0:
            msg_timer -= 1

        draw_ui(screen, rules, font, steps_per_frame, paused, max_bonds, message, msg_timer)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()