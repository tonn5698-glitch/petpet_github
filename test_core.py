from petpet_core import *

d = [264] + [33] * 6 + [66] + [33] * 43 + [66]
assert len(d) == 52

# 1 tap -> pet 5 frame x 60ms -> idle
p = Petpet(d); p.tap(0)
seen = []
for t in range(0, 400, 10):
    p.update(t); seen.append((p.mode, p.index))
assert ("pet", 0) in seen and ("pet", 4) in seen and p.mode == "idle" and p.combo_shown == 0

# tap nhanh: combo tăng, hiển thị trong lúc animate
p = Petpet(d); p.tap(0); p.update(100); p.tap(100); p.update(110)
assert p.combo == 1 and p.combo_shown == 1 and p.mode == "pet" and p.index == 0

# 51 tap liên tục cách 100ms -> nổ
p = Petpet(d)
for i in range(51):
    p.update(i * 100); p.tap(i * 100)
assert p.combo == 50
p.update(5000 + 299); assert p.mode == "pet"
p.update(5000 + 301); assert p.mode == "explosion" and p.index == 0, (p.mode, p.index)
p.tap(5400)  # bị bỏ qua khi nổ
total = sum(d)
p.update(5000 + 300 + total - 1); assert p.mode == "explosion" and p.index == 51
p.update(5000 + 300 + total + 1); assert p.mode == "idle" and p.combo == 0 and not p.animating

# tap chậm (>300ms) -> không combo
p = Petpet(d); p.tap(0); p.update(500); p.tap(500); p.update(520)
assert p.combo == 0
print("OK")
