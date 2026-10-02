"""maimai-petpet — bản pygame. Chạm/click để vuốt ve, tap nhanh để combo, 50 combo = nổ."""
import glob
import math
import os
import re
import sys

import pygame

from petpet_core import Petpet, combo_color, combo_text_size_sp

BASE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  # hỗ trợ PyInstaller
ASSETS = os.path.join(BASE, "assets")
BG = (28, 28, 34)
FPS = 60


def load(path, alpha=True):
    img = pygame.image.load(path)
    return img.convert_alpha() if alpha else img.convert()


def explosion_files():
    files = sorted(glob.glob(os.path.join(ASSETS, "explosion", "frame_*_delay_*.png")))
    delays = [int(re.search(r"delay_(\d+)", os.path.basename(f)).group(1)) for f in files]
    return files, delays


def fit(surf, box_w, box_h):
    w, h = surf.get_size()
    k = min(box_w / float(w), box_h / float(h))
    size = (max(1, int(w * k)), max(1, int(h * k)))
    return pygame.transform.smoothscale(surf, size)


def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 520), pygame.RESIZABLE)
    pygame.display.set_caption("maimai-petpet")
    clock = pygame.time.Clock()

    idle_src = load(os.path.join(ASSETS, "idle.png"), alpha=False)
    pygame.display.set_icon(pygame.transform.smoothscale(idle_src, (32, 32)))
    pet_src = [load(os.path.join(ASSETS, "pet", "frame%d.png" % i)) for i in range(5)]
    exp_paths, exp_delays = explosion_files()
    exp_src = [load(p, alpha=False) for p in exp_paths]

    pet = Petpet(exp_delays)
    cache = {}
    fonts = {}

    def scaled(kind, idx, src, bw, bh):
        key = (kind, idx, bw, bh)
        if key not in cache:
            if len(cache) > 400:
                cache.clear()
            cache[key] = fit(src, bw, bh)
        return cache[key]

    def font(px):
        if px not in fonts:
            f = pygame.font.Font(None, px)
            f.set_bold(True)
            fonts[px] = f
        return fonts[px]

    running = True
    while running:
        now = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_SPACE:
                    pet.tap(now)
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                pet.tap(now)
            elif e.type == pygame.VIDEORESIZE:
                cache.clear()
        pet.update(now)

        W, H = screen.get_size()
        unit = min(W, H) / 260.0            # ~1dp
        pad = int(4 * unit)
        bw, bh = W - 2 * pad, H - 2 * pad

        screen.fill(BG)
        if pet.mode == "explosion":
            img = scaled("exp", pet.index, exp_src[pet.index], bw, bh)
        else:
            img = scaled("idle", 0, idle_src, bw, bh)
        screen.blit(img, img.get_rect(center=(W // 2, H // 2)))
        if pet.mode == "pet":
            ov = scaled("pet", pet.index, pet_src[pet.index], bw, bh)
            screen.blit(ov, ov.get_rect(center=(W // 2, H // 2)))

        # COMBO text (top-center, marginTop 8dp)
        if pet.combo_shown > 0:
            px = int(combo_text_size_sp(pet.combo_shown) * unit * 1.5)
            f = font(px)
            txt = "COMBO x%d" % pet.combo_shown
            col = combo_color(pet.combo_shown)
            main_s = f.render(txt, True, col)
            sh = f.render(txt, True, (0, 0, 0))
            sh.set_alpha(128)
            x = (W - main_s.get_width()) // 2
            y = int(8 * unit)
            screen.blit(sh, (x + 1, y + 1))
            screen.blit(main_s, (x, y))

        # Spinner (bottom-right, 32dp)
        if pet.spinner:
            d = int(32 * unit)
            m = int(8 * unit)
            rect = pygame.Rect(W - m - d, H - m - d, d, d)
            a = (now / 400.0) % (2 * math.pi)
            pygame.draw.arc(screen, (230, 230, 230), rect, a, a + 4.2, max(2, int(3 * unit)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
