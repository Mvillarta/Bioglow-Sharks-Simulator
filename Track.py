import math
import sys
import os
import tkinter as tk
from PIL import ImageTk
from PIL import Image, ImageTk

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
except Exception:
    CTK_AVAILABLE = False

MAX_WIDTH = 1000
MAX_HEIGHT = 700
TAPETE_WIDTH_CM = 200
TAPETE_HEIGHT_CM = 114

ROBO_W = 44
ROBO_H = 44

movimentos = [
    ("reto", 87, 50),
    ("giro", 90, 90),
    ("reto", 60, 30),
    ("giro", 90, 70),
    ("reto", 85, 70),
    ("giro", -90, 100),
    ("reto", 60, 90),
]

# ============================================================
# MISSÕES
# ============================================================
missoes = [
    {
        "nome": "Missão 1",
        "vertices_cm": [(58.2, 2.8), (118.7, 2.8), (118.7, 10.3), (58.2, 10.3)],
        "ponto_ativacao": (56.0, 6.6),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None
    },
    {
        "nome": "Missão 2",
        "vertices_cm": [(59.6, 57.9), (67.1, 57.9), (67.1, 50.5), (59.6, 50.5)],
        "ponto_ativacao": (56.2, 48.9),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 3",
        "vertices_cm": [(2.2, 59), (2.2, 75.1), (14.1, 59), (14.1, 75.1)],
        "ponto_ativacao": (20.5, 65.5),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 4",
        "vertices_cm": [(7.5, 108.5), (25.1, 108.5), (25.1, 95.7), (7.5, 95.7)],
        "ponto_ativacao": (20.9, 93.7),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 5",
        "vertices_cm": [(39.2, 108.2), (41.8, 107.2), (41.8, 112.6), (39.2, 112.6)],
        "ponto_ativacao": (50.2, 93.8),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 6",
        "vertices_cm": [(145.2, 105.2), (150.2, 100.5), (152.2, 113.0), (157.8, 107.0)],
        "ponto_ativacao": (143.2, 95.7),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 7",
        "vertices_cm": [(156.2, 103.2), (161.4, 103.2), (161.6, 107.6), (156.2, 107.6)],
        "ponto_ativacao": (158.8, 98.1),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 8",
        "vertices_cm": [(50.2, 99.5), (50.2, 112.4), (65.3, 112.4), (65.3, 99.5)],
        "ponto_ativacao": (63.5, 98.9),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 9",
        "vertices_cm": [(53.6, 102.7), (56.2, 111.6), (64.7, 109), (59.6, 99.3)],
        "ponto_ativacao": (56.8, 95.7),
        "raio_ativacao": 10.0,
        "status": "pendente",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
    {
        "nome": "Missão 10_2",
        "vertices_cm": [(69.9, 99), (69.9, 108), (81, 108), (79.9, 99)],
        "ponto_ativacao": (56.8, 95.7),
        "raio_ativacao": 10.0,
        "status": "concluida",
        "cor_pendente": "#fbbf24",
        "cor_concluida": "#10b981",
        "canvas_ids": [],
        "passou_em": None,
    },
]

# ============================================================
# POSIÇÃO INICIAL
# ============================================================

x_inicial = 13
y_inicial = 13
angulo_inicial = 0

x_atual = x_inicial
y_atual = y_inicial
angulo_atual = angulo_inicial

# ============================================================
# GERA A TRAJETÓRIA A PARTIR DOS MOVIMENTOS
# ============================================================

coordenadas = [
    {
        "x_cm": x_inicial,
        "y_cm": y_inicial,
        "color": "#e74c3c",
        "angle": angulo_inicial,
        "vel": 0,
        "tipo": "inicio",
    }
]

def gerar_trajetoria():
    global coordenadas
    x = x_inicial
    y = y_inicial
    angulo = angulo_inicial
    coordenadas = [
        {
            "x_cm": x,
            "y_cm": y,
            "color": "#e74c3c",
            "angle": angulo,
            "vel": 0,
            "tipo": "inicio",
        }
    ]
    for tipo, valor, vel in movimentos:
        if tipo == "giro":
            angulo = (angulo + valor) % 360
            coordenadas.append(
                {
                    "x_cm": x,
                    "y_cm": y,
                    "color": "#e74c3c",
                    "angle": angulo,
                    "vel": vel,
                    "tipo": "giro",
                }
            )
        elif tipo == "reto":
            rad = math.radians(angulo)
            x += valor * math.sin(rad)
            y += valor * math.cos(rad)
            coordenadas.append(
                {
                    "x_cm": x,
                    "y_cm": y,
                    "color": "#e74c3c",
                    "angle": angulo,
                    "vel": vel,
                    "tipo": "reto",
                }
            )

gerar_trajetoria()

# ============================================================
# JANELA
# ============================================================

if CTK_AVAILABLE:
    root = ctk.CTk()
    Frame = ctk.CTkFrame
    Button = ctk.CTkButton
    Slider = ctk.CTkSlider
    Label = ctk.CTkLabel
    OptionMenu = ctk.CTkOptionMenu
    root.geometry("1200x760")
    root.title("Simulador Estratégias — FLL")
else:
    root = tk.Tk()
    Frame = tk.Frame
    Button = tk.Button
    Slider = tk.Scale
    Label = tk.Label
    OptionMenu = tk.OptionMenu
    root.geometry("1200x760")
    root.title("Simulador Estratégias — FLL")
    root.configure(bg="#1f2937")

# ============================================================
# CARREGA IMAGEM DO TAPETE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "tapete_novo.png")
try:
    img_original = Image.open(IMAGE_PATH).convert("RGBA")
except FileNotFoundError:
    print(f"\nImagem não encontrada:\n{IMAGE_PATH}\n\nColoque 'tapete_novo.png' na mesma pasta deste programa.")
    sys.exit(1)

scale_default = min(MAX_WIDTH / img_original.width, MAX_HEIGHT / img_original.height, 1.0)
width_px = int(img_original.width * scale_default)
height_px = int(img_original.height * scale_default)
img = img_original.resize((width_px, height_px), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)

# ============================================================
# LAYOUT
# ============================================================

if CTK_AVAILABLE:
    panel_left = Frame(root, width=340, height=height_px, fg_color="#111827")
else:
    panel_left = Frame(root, width=340, height=height_px, bg="#111827")
panel_left.pack(side="left", fill="y", padx=18, pady=18)

if not CTK_AVAILABLE:
    panel_left.pack_propagate(False)

if CTK_AVAILABLE:
    panel_right = Frame(root, width=340, height=height_px, fg_color="#111827")
else:
    panel_right = Frame(root, width=340, height=height_px, bg="#111827")
panel_right.pack(side="right", fill="y", padx=18, pady=18)

if not CTK_AVAILABLE:
    panel_right.pack_propagate(False)

# ============================================================
# HUD
# ============================================================
if CTK_AVAILABLE:
    header = Label(panel_left, text="Painel FLL", font=("Inter", 20, "bold"))
else:
    header = Label(panel_left, text="Painel FLL", font=("Segoe UI", 18, "bold"), fg="white", bg="#111827")

header.pack(pady=(8, 14))

if CTK_AVAILABLE:
    header1 = Label(panel_right, text="Missões FLL", font=("Inter", 20, "bold"))
else:
    header1 = Label(panel_right, text="Missões FLL", font=("Segoe UI", 18, "bold"), fg="white", bg="#111827")

header1.pack(pady=(8, 14))

hud_labels = {}

def atualizar_hud():
    for missao in missoes:
        nome = missao["nome"]
        if nome not in hud_labels:
            continue
        if missao["status"] == "concluida":
            texto = f"✅ {nome}\n"
        else:
            ponto = missao.get("ponto_ativacao")
            if ponto:
                px, py = ponto
                texto = f"⏳ {nome}\n   Alvo: ({px:.1f}, {py:.1f}) cm"
            else:
                texto = f"⏳ {nome}\n   Aguardando..."
        hud_labels[nome].configure(text=texto)

if CTK_AVAILABLE:
    hud_frame = Frame(panel_right, fg_color="#0b1220")
else:
    hud_frame = Frame(panel_right, bg="#0b1220")

hud_frame.pack(fill="x", pady=(20, 10), padx=10)
for missao in missoes:
    if CTK_AVAILABLE:
        lbl = Label(hud_frame, text=f"⏳ {missao['nome']}", font=("Consolas", 12), anchor="w")
    else:
        lbl = Label(hud_frame, text=f"⏳ {missao['nome']}", font=("Consolas", 12), anchor="w", fg="white", bg="#0b1220")
    lbl.pack(fill="x", pady=2)
    hud_labels[missao["nome"]] = lbl

# ============================================================
# CARDS DE INFORMAÇÃO
# ============================================================

def make_info_card(parent, title, value_text):
    if CTK_AVAILABLE:
        container = Frame(parent, fg_color="#0b1220")
    else:
        container = Frame(parent, bg="#0b1220")

    container.pack(fill="x", pady=8, padx=10)

    if CTK_AVAILABLE:
        t = Label(container, text=title, font=("Consolas", 9), anchor="w")
        v = Label(container, text=value_text, font=("Consolas", 12, "bold"), anchor="w")
    else:
        t = Label(container, text=title, font=("Consolas", 9), anchor="w", fg="#9ca3af", bg="#0b1220")
        v = Label(container, text=value_text, font=("Consolas", 12, "bold"), anchor="w", fg="#e6edf3", bg="#0b1220")

    t.pack(anchor="w", padx=10, pady=(10, 0))
    v.pack(anchor="w", padx=10, pady=(4, 10))

    return v

label_pos = make_info_card(panel_left, "Posição (cm):", f"({x_inicial:.1f}, {y_inicial:.1f})")
label_angle = make_info_card(panel_left, "Ângulo (°):", f"{angulo_inicial:.1f}")
label_mouse = make_info_card(panel_left, "Mouse (px / cm):", "—")

# ============================================================
# CONTROLES
# ============================================================

if CTK_AVAILABLE:
    ctrl_frame = Frame(panel_left, fg_color="transparent")
else:
    ctrl_frame = Frame(panel_left, bg="#111827")

ctrl_frame.pack(fill="x", pady=(12, 6))

if CTK_AVAILABLE:
    speed_label = Label(ctrl_frame, text="Velocidade geral", anchor="w")
    speed_label.pack(fill="x")
    slider_speed = Slider(ctrl_frame, from_=0.2, to=3.0, number_of_steps=28)
    slider_speed.set(1.0)
else:
    speed_label = Label(ctrl_frame, text="Velocidade geral", fg="white", bg="#111827", anchor="w")
    speed_label.pack(fill="x")
    slider_speed = Slider(ctrl_frame, from_=0.2, to=3.0, orient="horizontal", resolution=0.01, fg="#111827", bg="#111827", highlightthickness=0)
    slider_speed.set(1.0)
slider_speed.pack(fill="x", pady=(6, 10))

# ============================================================
# ZOOM
# ============================================================

if CTK_AVAILABLE:
    zoom_label = Label(ctrl_frame, text="Zoom", anchor="w")
    zoom_label.pack(fill="x")
    slider_zoom = Slider(ctrl_frame, from_=0.5, to=1.5, number_of_steps=40)
    slider_zoom.set(scale_default)
else:
    zoom_label = Label(ctrl_frame, text="Zoom", fg="white", bg="#111827", anchor="w")
    zoom_label.pack(fill="x")
    slider_zoom = Slider(ctrl_frame, from_=0.5, to=1.5, resolution=0.025, orient="horizontal", fg="#111827", bg="#111827", highlightthickness=0)
    slider_zoom.set(scale_default)

# ============================================================
# CANVAS
# ============================================================

canvas_container = Frame(root)
canvas_container.pack(side="right", expand=True, fill="both", padx=18, pady=18)

canvas = tk.Canvas(canvas_container, width=width_px, height=height_px, bg="#0f1724", highlightthickness=2, highlightbackground="#06b6d4")
canvas.pack(expand=True)

# ============================================================
# IMAGEM BASE
# ============================================================

canvas_img_id = canvas.create_image(0, 0, anchor="nw", image=photo)

# ============================================================
# CONVERSÕES CM <-> PIXEL
# ============================================================

def cm_to_pixel(x_cm, y_cm, w_px, h_px):
    x_pixel = (x_cm / TAPETE_WIDTH_CM) * w_px
    y_pixel = ((TAPETE_HEIGHT_CM - y_cm) / TAPETE_HEIGHT_CM) * h_px
    return x_pixel, y_pixel

def pixel_to_cm(x_px, y_px, w_px, h_px):
    if w_px <= 0 or h_px <= 0:
        return 0, 0
    x_cm = (x_px / w_px) * TAPETE_WIDTH_CM
    y_cm = ((h_px - y_px) / h_px) * TAPETE_HEIGHT_CM
    return x_cm, y_cm

# ============================================================
# PONTOS DA TRAJETÓRIA
# ============================================================

points_list = []
def rebuild_points_list(current_w, current_h):
    points_list.clear()
    for pt in coordenadas:
        x_px, y_px = cm_to_pixel(pt["x_cm"], pt["y_cm"], current_w, current_h)
        points_list.append(
            {
                "x_px": x_px,
                "y_px": y_px,
                "x_cm": pt["x_cm"],
                "y_cm": pt["y_cm"],
                "color": pt["color"],
                "angle": pt["angle"],
                "vel": pt["vel"],
                "tipo": pt["tipo"],
            }
        )

# ============================================================
# DESENHO DAS MISSÕES
# ============================================================
def desenhar_missoes(w_px, h_px):
    for missao in missoes:
        for item_id in missao["canvas_ids"]:
            canvas.delete(item_id)
        missao["canvas_ids"].clear()
        pts_px = []
        for x_cm, y_cm in missao["vertices_cm"]:
            px, py = cm_to_pixel(x_cm, y_cm, w_px, h_px)
            pts_px.extend([px, py])
        
        cor = missao["cor_concluida"] if missao["status"] == "concluida" else missao["cor_pendente"]
        
        poly_id = canvas.create_polygon(
            pts_px,
            fill=cor,
            outline="white",
            width=2,
            stipple="gray25",
            tags="missoes",
        )
        xs = [p[0] for p in missao["vertices_cm"]]
        ys = [p[1] for p in missao["vertices_cm"]]
        cx_cm = sum(xs) / len(xs)
        cy_cm = sum(ys) / len(ys)
        cx_px, cy_px = cm_to_pixel(cx_cm, cy_cm, w_px, h_px)
        text_id = canvas.create_text(cx_px, cy_px, text=missao["nome"], font=("Consolas", 10, "bold"), fill="white", tags="missoes")
       
        missao["canvas_ids"] = [poly_id, text_id]

        canvas.tag_lower(poly_id)
        canvas.tag_lower(text_id)
    atualizar_hud()

# ============================================================
# TRAJETÓRIA
# ============================================================

traj_tag = "traj"

def redraw_trajectories(current_w, current_h):
    canvas.delete(traj_tag)
    rebuild_points_list(current_w, current_h)
    coords = []

    for p in points_list:
        coords.extend([p["x_px"], p["y_px"]])

    if len(coords) >= 4:
        canvas.create_line(*coords, width=4, smooth=True, splinesteps=36, fill="#60a5fa", tags=traj_tag)
        canvas.create_line(*coords, width=2, smooth=True, splinesteps=36, fill="#bfdbfe", tags=traj_tag)
    for p in points_list:
        x = p["x_px"]
        y = p["y_px"]
        canvas.create_oval(
            x - 7, y - 7, x + 7, y + 7,
            fill="#111827",
            outline=p["color"],
            width=3,
            tags=traj_tag,
        )
        canvas.create_text(x, y - 18, text=f"{p['x_cm']:.0f},{p['y_cm']:.0f}", font=("Consolas", 9, "bold"), fill="#e6edf3", tags=traj_tag)
        rad = math.radians(p["angle"])
        ax = x + 18 * math.sin(rad)
        ay = y - 18 * math.cos(rad)
        canvas.create_line(x, y, ax, ay, arrow="last", width=2, fill="#7dd3fc", tags=traj_tag)

    if points_list:
        s = points_list[0]
        e = points_list[-1]
        canvas.create_oval(s["x_px"] - 12, s["y_px"] - 12, s["x_px"] + 12, s["y_px"] + 12, outline="#10b981", width=3, tags=traj_tag)
        canvas.create_oval(e["x_px"] - 12, e["y_px"] - 12, e["x_px"] + 12, e["y_px"] + 12, outline="#ef4444", width=3, tags=traj_tag)
   
# ============================================================
# DETECÇÃO DE PONTO DENTRO DO POLÍGONO
# ============================================================
def ponto_em_poligono(x, y, vertices):
    inside = False
    n = len(vertices)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        xi, yi = vertices[i]
        xj, yj = vertices[j]
        if (yi > y) != (yj > y):
            intersecao = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < intersecao:
                inside = not inside
        j = i
    return inside

def robo_encostou_na_missao(x_cm, y_cm, vertices, margem=0.5):
    if ponto_em_poligono(x_cm, y_cm, vertices):
        return True

    def distancia_ponto_segmento(px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        ponto_x = x1 + t * dx
        ponto_y = y1 + t * dy
        return math.hypot(px - ponto_x, py - ponto_y)

    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        distancia = distancia_ponto_segmento(x_cm, y_cm, x1, y1, x2, y2)
        if distancia <= margem:
            return True
    return False

# ============================================================
# VERIFICA MISSÕES
# ============================================================

def verificar_missoes(x_px, y_px):
    current_w = canvas.winfo_width() or width_px
    current_h = canvas.winfo_height() or height_px
    x_cm, y_cm = pixel_to_cm(x_px, y_px, current_w, current_h)
    alterou = False
    for missao in missoes:
        if missao["status"] == "concluida":
            continue

        ponto = missao.get("ponto_ativacao")
        if ponto is None:
            continue

        ponto_x, ponto_y = ponto
        distancia = math.hypot(x_cm - ponto_x, y_cm - ponto_y)
        raio = missao.get("raio_ativacao", 10.0)

        if distancia <= raio:
            missao["status"] = "concluida"
            missao["passou_em"] = (x_cm, y_cm)
            print('✅')
            print(f"   Robô passou em: ({x_cm:.1f},{y_cm:.1f}) cm")
            print(f"   Distância do ponto: {distancia:.1f} cm")
            alterou = True

    if alterou:
        desenhar_missoes(current_w, current_h)
        atualizar_hud()

# ============================================================
# ROBÔ VISUAL
# ============================================================
robot_color = "#0f1724"
robot_outline = "#22d3ee"

robot_id = canvas.create_polygon(
    [1, 1, 1, 1, 1, 1],
    fill=robot_color,
    outline=robot_outline,
    width=3,
    tags="robot",
)

glow_id = canvas.create_oval(0, 0, 0, 0, outline="#10b981", width=2, tags="glow")

def draw_robot_at(x, y, angle):
    global robot_color, robot_outline
    verificar_missoes(x, y)

    current_w = canvas.winfo_width() or width_px
    current_h = canvas.winfo_height() or height_px

    x_cm, y_cm = pixel_to_cm(x, y, current_w, current_h)

    encostou = False
    for missao in missoes:
        vertices = missao.get("vertices_cm", [])
        if not vertices:
            continue
        if robo_encostou_na_missao(x_cm, y_cm, vertices, margem=0.5):
            encostou = True
            break

    if encostou:
        robot_color = "#facc15"
        robot_outline = "#fef08a"
    else:
        robot_color = "#0f1724"
        robot_outline = "#22d3ee"

    canvas.itemconfigure(
        robot_id,
        fill=robot_color,
        outline=robot_outline
    )
    rad = math.radians(angle)

    w = ROBO_W / 2
    h = ROBO_H / 2

    verts = [(-w, -h), (w, -h), (w, h), (-w, h)]
    pts = []
    for vx, vy in verts:
        xr = (vx * math.cos(rad) - vy * math.sin(rad) + x)
        yr = (vx * math.sin(rad) + vy * math.cos(rad) + y)
        pts.extend([xr, yr])

    canvas.coords(robot_id, *pts)
    glow_pad = 18
    canvas.coords(glow_id, x - w - glow_pad, y - h - glow_pad, x + w + glow_pad, y + h + glow_pad)
    canvas.tag_raise(glow_id)
    canvas.tag_raise(robot_id)

# ============================================================
# EFEITO DE GLOW
# ============================================================

_glow_phase = 0.0
def pulse_glow():
    global _glow_phase
    _glow_phase += 0.07
    intensity = (math.sin(_glow_phase) + 1) / 2
    outer_width = 1 + intensity * 3

    c1 = (16, 185, 129)
    c2 = (56, 189, 248)
    t = 0.65 * intensity + 0.35
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)

    cor = f"#{r:02x}{g:02x}{b:02x}"
    try:
        canvas.itemconfigure(glow_id, outline=cor, width=outer_width)
    except tk.TclError:
        pass

    root.after(40, pulse_glow)

# ============================================================
# MOUSE TRACKING
# ============================================================

crosshair_h = canvas.create_line(0, 0, 0, 0, fill="#94a3b8", dash=(4, 4), tags="mouse")
crosshair_v = canvas.create_line(0, 0, 0, 0, fill="#94a3b8", dash=(4, 4), tags="mouse")
mouse_dot = canvas.create_oval(0, 0, 0, 0, fill="#fef3c7", outline="#f59e0b", width=2, tags="mouse")

def on_mouse_move(event):
    cx = canvas.canvasx(event.x)
    cy = canvas.canvasy(event.y)
    current_w = canvas.winfo_width()
    current_h = canvas.winfo_height()
    canvas.coords(crosshair_h, 0, cy, current_w, cy)
    canvas.coords(crosshair_v, cx, 0, cx, current_h)

    r = 5
    canvas.coords(mouse_dot, cx - r, cy - r, cx + r, cy + r)

    if 0 <= cx <= current_w and 0 <= cy <= current_h:
        mx_cm, my_cm = pixel_to_cm(cx, cy, current_w, current_h)
        label_mouse.configure(text=f"{int(cx)}px, {int(cy)}px / {mx_cm:.1f}cm, {my_cm:.1f}cm")
    else:
        label_mouse.configure(text="fora do tapete")

canvas.bind("<Motion>", on_mouse_move)

# ============================================================
# ANIMAÇÃO
# ============================================================

_anim_running = False
_anim_job = None
anim_idx = 0
anim_sub = 0

def stop_animation():
    global _anim_running, _anim_job
    _anim_running = False
    if _anim_job is not None:
        try:
            root.after_cancel(_anim_job)
        except Exception:
            pass
        _anim_job = None

def reset_robot_to_start():
    global x_atual, y_atual, angulo_atual
    x_atual = x_inicial
    y_atual = y_inicial
    angulo_atual = angulo_inicial
    current_w = canvas.winfo_width() or width_px
    current_h = canvas.winfo_height() or height_px
    x_px, y_px = cm_to_pixel(x_atual, y_atual, current_w, current_h)
    draw_robot_at(x_px, y_px, angulo_atual)
    label_pos.configure(text=f"({x_atual:.1f}, {y_atual:.1f})")
    label_angle.configure(text=f"{angulo_atual:.1f}")

def iniciar_animacao():
    global _anim_running, anim_idx, anim_sub
    if _anim_running:
        return
    if not points_list:
        return
    _anim_running = True
    anim_idx = 0
    anim_sub = 0
    executar_passo()

def executar_passo():
    global _anim_running, _anim_job, anim_idx, anim_sub
    if not _anim_running:
        return

    if anim_idx >= len(points_list) - 1:
        _anim_running = False
        _anim_job = None
        ultimo = points_list[-1]
        draw_robot_at(ultimo["x_px"], ultimo["y_px"], ultimo["angle"])
        label_pos.configure(text=f"({ultimo['x_cm']:.1f}, {ultimo['y_cm']:.1f})")
        label_angle.configure(text=f"{ultimo['angle']:.1f}")
        return

    start = points_list[anim_idx]
    end = points_list[anim_idx + 1]
    speed_factor = float(slider_speed.get())
    current_w = canvas.winfo_width() or width_px
    current_h = canvas.winfo_height() or height_px

    if end["tipo"] == "reto":
        distancia_cm = math.hypot(end["x_cm"] - start["x_cm"], end["y_cm"] - start["y_cm"])
        velocidade = max(end["vel"], 1)
        duracao = distancia_cm / velocidade
        total_steps = max(int(duracao * 1000 / 16 / speed_factor), 1)
        t = anim_sub / total_steps
        t = min(t, 1.0)
        x_cm = start["x_cm"] + (end["x_cm"] - start["x_cm"]) * t
        y_cm = start["y_cm"] + (end["y_cm"] - start["y_cm"]) * t
        angle = end["angle"]

    elif end["tipo"] == "giro":
        delta_angle = end["angle"] - start["angle"]
        if delta_angle > 180:
            delta_angle -= 360
        if delta_angle < -180:
            delta_angle += 360
        velocidade = max(abs(end["vel"]), 1)
        duracao = abs(delta_angle) / velocidade
        total_steps = max(int(duracao * 1000 / 16 / speed_factor), 1)
        t = anim_sub / total_steps
        t = min(t, 1.0)
        angle = start["angle"] + delta_angle * t
        x_cm = start["x_cm"]
        y_cm = start["y_cm"]

    else:
        x_cm = start["x_cm"]
        y_cm = start["y_cm"]
        angle = start["angle"]
        total_steps = 1

    x_px, y_px = cm_to_pixel(x_cm, y_cm, current_w, current_h)
    draw_robot_at(x_px, y_px, angle)
    label_pos.configure(text=f"({x_cm:.1f}, {y_cm:.1f})")
    label_angle.configure(text=f"{angle:.1f}")
    atualizar_hud()
    
    anim_sub += 1
    if anim_sub > total_steps:
        anim_idx += 1
        anim_sub = 0
    _anim_job = root.after(16, executar_passo)

# ============================================================
# REINICIAR
# ============================================================
def restart_animation():
    stop_animation()
    global anim_idx, anim_sub
    anim_idx = 0
    anim_sub = 0
    for missao in missoes:
        missao["status"] = "pendente"
        missao["passou_em"] = None
    
    current_w = canvas.winfo_width() or width_px
    current_h = canvas.winfo_height() or height_px
    
    atualizar_hud()
    redraw_trajectories(current_w, current_h)
    desenhar_missoes(current_w, current_h)
    reset_robot_to_start()

# ============================================================
# BOTÕES
# ============================================================

if CTK_AVAILABLE:
    btn_frame = Frame(panel_left, fg_color="transparent")
else:
    btn_frame = Frame(panel_left, bg="#111827")
btn_frame.pack(fill="x", pady=(8, 0))

def make_button(text, command):
    if CTK_AVAILABLE:
        b = Button(btn_frame, text=text, command=command, width=200, corner_radius=10)
    else:
        b = Button(
            btn_frame,
            text=text,
            command=command,
            fg="white",
            bg="#0ea5a3",
            activebackground="#14b8a6",
            relief="flat",
            bd=0,
        )
    b.pack(fill="x", pady=6)
    return b

btn_start = make_button("▶ Iniciar / Continuar", iniciar_animacao)
btn_pause = make_button("⏸ Pausar", stop_animation)
btn_restart = make_button("🔄 Reiniciar", restart_animation)

# ============================================================
# ZOOM
# ============================================================

def on_zoom_change(value=None):
    global width_px, height_px, img, photo
    try:
        z = float(slider_zoom.get())
    except Exception:
        return
    width_px = max(1, int(img_original.width * z))
    height_px = max(1, int(img_original.height * z))
    img = img_original.resize((width_px, height_px), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    canvas.config(width=width_px, height=height_px)
    canvas.itemconfigure(canvas_img_id, image=photo)
    redraw_trajectories(width_px, height_px)
    desenhar_missoes(width_px, height_px)
    reset_robot_to_start()

slider_zoom.configure(command=on_zoom_change)

# ============================================================
# INICIALIZAÇÃO
# ============================================================

rebuild_points_list(width_px, height_px)
redraw_trajectories(width_px, height_px)
desenhar_missoes(width_px, height_px)
reset_robot_to_start()
pulse_glow()

# ============================================================
# TECLA ESC
# ============================================================
def on_escape(event=None):
    stop_animation()
    root.quit()

root.bind("<Escape>", on_escape)

# ============================================================
# CENTRALIZA JANELA
# ============================================================
try:
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    geometry = root.geometry()
    size = geometry.split("+")[0]
    win_w, win_h = map(int, size.split("x"))
    pos_x = (screen_w - win_w) // 2
    pos_y = (screen_h - win_h) // 2
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
except Exception:
    pass

# ============================================================
# INICIA PROGRAMA
# ============================================================
root.mainloop()
