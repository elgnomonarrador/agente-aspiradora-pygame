# Agente Inteligente - Aspiradora (Python + Pygame)

Simulación visual de un **agente inteligente reflexivo** tipo aspiradora en un entorno con **dos habitaciones (A y B)**.  
El agente **percibe** el estado de la habitación actual (limpio/sucio), **decide** con base en reglas y **actúa** limpiando o moviéndose.

## Objetivo
Dejar ambas habitaciones **limpias** (A y B), partiendo de estados iniciales aleatorios.

## ¿Qué conceptos de agentes inteligentes incluye?
- **Percepción:** el agente consulta el estado de la habitación actual mediante `percibir(posicion)`.
- **Acciones:** `limpiar` (cambia "sucio" → "limpio") o `moverse` (cambia A ↔ B).
- **Autonomía:** el agente ejecuta su lógica automáticamente cada intervalo de tiempo sin intervención del usuario.
- **Racionalidad:** sus decisiones están orientadas a alcanzar la meta (ambas habitaciones limpias).
- **Extensión (Memoria):** guarda el último estado percibido en `memoria["A"]` y `memoria["B"]`.
- **Extensión (Registro):** genera un archivo `.json` con historial de pasos y métricas al finalizar.

## Reglas del agente
1. Si la habitación actual está **sucia** → **limpiar**.
2. Si está **limpia** → **moverse** a la otra habitación.

El sistema se detiene cuando:
- Ambas habitaciones están limpias (**éxito**), o
- Se alcanza el límite de pasos `MAX_PASOS` (**seguridad**).

## Requisitos
- Python 3.9+ (recomendado)
- Pygame

## Instalación
```bash
pip install -r requirements.txt
