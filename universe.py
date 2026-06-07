# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 21:49:27 2026

@author: brain
"""

from ursina import *
import random

app = Ursina()

G = 0.05          # Constante gravitacional simplificada
DIST_FUSION = 0.3

particulas = []

class Particula(Entity):
    def __init__(self, masa=1, posicion=Vec3(0,0,0), velocidad=Vec3(0,0,0)):
        super().__init__(
            model='sphere',
            color=color.white,
            scale=max(0.2, masa * 0.1),
            position=posicion
        )

        self.masa = masa
        self.velocidad = velocidad


# Crear partículas iniciales
for _ in range(50):

    masa = random.uniform(0.5, 2)

    posicion = Vec3(
        random.uniform(-5, 5),
        random.uniform(-5, 5),
        random.uniform(-5, 5)
    )

    velocidad = Vec3(
        random.uniform(-0.5, 0.5),
        random.uniform(-0.5, 0.5),
        random.uniform(-0.5, 0.5)
    )

    p = Particula(masa, posicion, velocidad)
    particulas.append(p)


def update():

    # Aplicar gravedad
    for i in range(len(particulas)):

        p1 = particulas[i]

        for j in range(i + 1, len(particulas)):

            p2 = particulas[j]

            direccion = p2.position - p1.position
            distancia = direccion.length()

            if distancia < 0.01:
                continue

            direccion = direccion.normalized()

            fuerza = G * p1.masa * p2.masa / (distancia ** 2)

            aceleracion1 = direccion * (fuerza / p1.masa)
            aceleracion2 = -direccion * (fuerza / p2.masa)

            p1.velocidad += aceleracion1 * time.dt
            p2.velocidad += aceleracion2 * time.dt

    # Mover partículas
    for p in particulas:
        p.position += p.velocidad * time.dt

    # Fusionar partículas
    i = 0

    while i < len(particulas):

        fusion_realizada = False

        j = i + 1

        while j < len(particulas):

            p1 = particulas[i]
            p2 = particulas[j]

            distancia = distance(p1.position, p2.position)

            if distancia < DIST_FUSION:

                nueva_masa = p1.masa + p2.masa

                nueva_posicion = (p1.position + p2.position) / 2

                nueva_velocidad = (
                    p1.velocidad * p1.masa +
                    p2.velocidad * p2.masa
                ) / nueva_masa

                destroy(p1)
                destroy(p2)

                particulas.pop(j)
                particulas.pop(i)

                nueva = Particula(
                    nueva_masa,
                    nueva_posicion,
                    nueva_velocidad
                )

                nueva.scale = max(0.2, nueva_masa * 0.1)

                particulas.append(nueva)

                fusion_realizada = True
                break

            j += 1

        if not fusion_realizada:
            i += 1


EditorCamera()

app.run()