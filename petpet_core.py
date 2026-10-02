"""Logic petpet (port 1:1 từ PetpetWidgetProvider.kt), không phụ thuộc pygame.

Thời gian tính bằng ms, do bên ngoài truyền vào -> test được không cần cửa sổ.
"""

PET_FRAMES = 5
PET_DELAY = 60
COMBO_EXPLODE = 50


class Petpet:
    def __init__(self, explosion_delays):
        self.exp_delays = list(explosion_delays)
        self.has_state = False      # comboStates[widgetId] != null
        self.combo = 0
        self.frame = 0
        self.tapped = False
        self.is_explosion = False
        self.animating = False      # handlers.containsKey(widgetId)
        self.next_at = 0
        # view model
        self.mode = "idle"          # idle | pet | explosion
        self.index = 0
        self.combo_shown = 0        # 0 = ẩn comboText
        self.spinner = False

    # ---- input ----
    def tap(self, now):
        # Khi nổ, widget bị set RemoteViews không có click -> bỏ qua tap
        if self.is_explosion and self.animating:
            return
        if not self.has_state:
            self.has_state = True
            self.combo = 0
        elif self.animating:
            self.combo += 1
            self.tapped = True
        self._start_pet(now)

    # ---- tick ----
    def update(self, now):
        while self.animating and now >= self.next_at:
            t = self.next_at
            if self.is_explosion:
                self._step_explosion(t)
            else:
                self._step_pet(t)

    # ---- nội bộ ----
    def _start_pet(self, now):
        self.animating = True
        self.frame = 0
        self.tapped = False
        self._step_pet(now)

    def _step_pet(self, t):
        if self.frame < PET_FRAMES:
            self.mode, self.index = "pet", self.frame
            self.spinner = True
            self.combo_shown = self.combo
            self.frame += 1
            self.next_at = t + PET_DELAY
            return
        if self.combo >= COMBO_EXPLODE:
            self._start_explosion(t)
            return
        if not self.tapped:
            self.combo = 0
        self._show_idle(self.combo)
        self.animating = False

    def _start_explosion(self, t):
        self.is_explosion = True
        self.frame = 0
        self._step_explosion(t)

    def _step_explosion(self, t):
        if self.frame >= len(self.exp_delays):
            self.is_explosion = False
            self.combo = 0
            self.frame = 0
            self._show_idle(0)
            self.animating = False
            return
        self.mode, self.index = "explosion", self.frame
        self.spinner = False
        self.combo_shown = 0
        self.next_at = t + self.exp_delays[self.frame]
        self.frame += 1

    def _show_idle(self, combo):
        self.mode, self.index = "idle", 0
        self.spinner = False
        self.combo_shown = combo


def combo_color(c):
    if c <= 3:
        return (0x4F, 0xC3, 0xF7)
    if c <= 6:
        return (0x15, 0x65, 0xC0)
    if c <= 9:
        return (0x7B, 0x1F, 0xA2)
    if c <= 15:
        return (0xD3, 0x2F, 0x2F)
    return (0xFF, 0x17, 0x44)


def combo_text_size_sp(c):
    return min(c, 50) * 0.5 + 16.0
