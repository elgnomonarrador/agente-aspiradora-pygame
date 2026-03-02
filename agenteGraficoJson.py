import pygame
import random
import sys
import json
from datetime import datetime

# -----------------------------
# INICIALIZACIÓN
# -----------------------------
pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agente Inteligente - Aspiradora")

font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()

MAX_PASOS = 20

# Variables globales
entorno = {}
posicion = "A"
agent_x = 150
accion_actual = ""
pasos = 0
agente_activo = True

memoria = {"A": None, "B": None}
historial = []
limpiezas = 0
movimientos = 0


# -----------------------------
# GUARDAR JSON
# -----------------------------
def guardar_json():
    datos = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pasos_totales": pasos,
        "limpiezas": limpiezas,
        "movimientos": movimientos,
        "estado_final_entorno": entorno,
        "historial": historial
    }

    nombre_archivo = f"registro_agente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    print(f"\n✔ Registro guardado en {nombre_archivo}")


# -----------------------------
# REINICIAR SISTEMA
# -----------------------------
def inicializar():
    global entorno, posicion, agent_x, accion_actual, pasos, agente_activo
    global memoria, historial, limpiezas, movimientos

    entorno = {
        "A": random.choice(["limpio", "sucio"]),
        "B": random.choice(["limpio", "sucio"])
    }

    posicion = random.choice(["A", "B"])
    agent_x = 150 if posicion == "A" else 450

    accion_actual = "Sistema reiniciado"
    pasos = 0
    agente_activo = True

    memoria = {"A": None, "B": None}
    historial = []
    limpiezas = 0
    movimientos = 0


inicializar()


def percibir(posicion):
    return entorno[posicion]


# -----------------------------
# DIBUJAR
# -----------------------------
def draw():
    screen.fill((255, 255, 255))

    colorA = (139, 69, 19) if entorno["A"] == "sucio" else (144, 238, 144)
    colorB = (139, 69, 19) if entorno["B"] == "sucio" else (144, 238, 144)

    pygame.draw.rect(screen, colorA, (50, 70, 200, 200))
    pygame.draw.rect(screen, colorB, (350, 70, 200, 200))

    pygame.draw.rect(screen, (0, 0, 255), (agent_x, 150, 40, 40))

    screen.blit(font.render(f"Habitación A: {entorno['A']}", True, (0, 0, 0)), (70, 280))
    screen.blit(font.render(f"Habitación B: {entorno['B']}", True, (0, 0, 0)), (370, 280))

    screen.blit(font.render(f"Acción: {accion_actual}", True, (0, 0, 0)), (150, 320))
    screen.blit(font.render(f"Pasos: {pasos}", True, (0, 0, 0)), (250, 350))
    screen.blit(font.render(f"Limpiezas: {limpiezas} | Movimientos: {movimientos}", True, (0, 0, 0)), (190, 20))
    #screen.blit(font.render(f"Memoria A: {memoria['A']} | Memoria B: {memoria['B']}", True, (0, 0, 0)), (152, 45)) 
    valorA = memoria["A"] or "-"
    valorB = memoria["B"] or "-"
    screen.blit(font.render(f"Memoria A: {valorA} | Memoria B: {valorB}", True, (0, 0, 0)), (152, 45))
    
    pygame.draw.rect(screen, (200, 0, 0), (230, 380, 140, 40))
    screen.blit(font.render("REINICIAR", True, (255, 255, 255)), (250, 390))

    pygame.display.flip()


# -----------------------------
# LÓGICA DEL AGENTE
# -----------------------------
def agente():
    global posicion, agent_x, accion_actual, pasos
    global memoria, historial, limpiezas, movimientos

    if entorno["A"] == "limpio" and entorno["B"] == "limpio":
        accion_actual = "Objetivo alcanzado (OK)"
        guardar_json()
        return False

    if pasos >= MAX_PASOS:
        accion_actual = "Límite de pasos alcanzado (ERROR)"
        guardar_json()
        return False

    estado_actual = percibir(posicion)
    memoria[posicion] = estado_actual

    if estado_actual == "sucio":
        entorno[posicion] = "limpio"
        accion_actual = f"Limpiando habitación {posicion}"
        limpiezas += 1
        accion = "limpiar"
    else:
        posicion = "B" if posicion == "A" else "A"
        agent_x = 150 if posicion == "A" else 450
        accion_actual = f"Moviéndose a habitación {posicion}"
        movimientos += 1
        accion = "moverse"

    pasos += 1

    historial.append({
        "paso": pasos,
        "posicion": posicion,
        "percibido": estado_actual,
        "accion": accion,
        "entorno": entorno.copy(),
        "memoria": memoria.copy()
    })

    return True


# -----------------------------
# BUCLE PRINCIPAL
# -----------------------------
running = True
timer = 0

while running:
    clock.tick(60)
    timer += 1

    if timer % 60 == 0 and agente_activo:
        agente_activo = agente()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 230 <= mouse_x <= 370 and 380 <= mouse_y <= 420:
                inicializar()

    draw()

pygame.quit()
sys.exit()