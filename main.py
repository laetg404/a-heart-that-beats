import turtle as t
import math as m
import random as r

SCALE = 100

s = t.Screen()
s.setup(600, 700)
s.bgcolor("#050002")
s.tracer(0)

p = t.Turtle()
p.hideturtle()
p.penup()


def heart(u):
    x = 1.6 * (m.sin(u) ** 3)
    y = (
        1.3 * m.cos(u)
        - 0.5 * m.cos(2 * u)
        - 0.2 * m.cos(3 * u)
        - 0.1 * m.cos(4 * u)
    )
    return x, y - 0.25          # centrado verticalmente


# -------------------------
# COLOR
# -------------------------

def get_col(f):
    f = max(0.0, min(1.0, f))
    r1, g1, b1 = 70, 0, 10
    r2, g2, b2 = 255, 30, 50
    return (
        f"#{int(r1 + (r2 - r1) * f):02x}"
        f"{int(g1 + (g2 - g1) * f):02x}"
        f"{int(b1 + (b2 - b1) * f):02x}"
    )


# -------------------------
# GENERAR PARTÍCULAS
# -------------------------

N = 2000
pts = []

for _ in range(N):
    u = r.uniform(0, 2 * m.pi)
    hx, hy = heart(u)
    rad = m.sqrt(r.random())

    x = hx * rad
    y = hy * rad
    z = 1.1 * (1 - rad) * r.uniform(-1, 1)

    f = (z + 1.1) / 2.2
    pts.append({
        "x": x, "y": y, "z": z,
        "appear": r.random(),        # momento fijo de aparición
        "size": r.uniform(1, 3),
        "color": get_col(f),
    })

# -------------------------
# RAYOS
# -------------------------

rays = [heart(r.uniform(0, 2 * m.pi)) for _ in range(80)]

# -------------------------
# ANIMACIÓN
# -------------------------

FORM_END = 1.6
t_val = 0.0
frame = 0


def loop():
    global t_val, frame

    p.clear()
    p.penup()

    progress = min(1.0, t_val)


    if t_val > FORM_END:
        pulse = 1 + 0.05 * max(0.0, m.sin(frame * 0.2)) ** 2
    else:
        pulse = 1.0

    # --- Partículas ---
    for q in pts:
        if q["appear"] > progress:
            continue

        depth = (1 + q["z"] * 0.12) * pulse
        p.goto(q["x"] * SCALE * depth, q["y"] * SCALE * depth)
        p.color(q["color"])
        p.dot(q["size"])


    if t_val <= FORM_END:
        head = min(1.0, t_val)
        tail = max(0.0, t_val - 0.35)
        fade = max(0.0, 1.0 - (t_val - 0.7)) if t_val > 0.7 else 1.0
        red_c = int(170 * fade)

        p.width(1)
        for hx, hy in rays:
            x1, y1 = hx * tail * SCALE, hy * tail * SCALE
            x2, y2 = hx * head * SCALE, hy * head * SCALE

            p.color(f"#{red_c:02x}001a")
            p.penup()
            p.goto(x1, y1)
            p.pendown()
            p.goto(x2, y2)
            p.penup()

            if t_val < 0.9:
                p.color("#ff1a40")
                p.dot(2)

    t_val += 0.025
    frame += 1

    s.update()
    s.ontimer(loop, 25)


loop()
t.mainloop()