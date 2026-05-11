# Este código implementa un filtro de partículas
# para estimar la posición de un objeto
# usando movimiento y mediciones con ruido.

import numpy as np

class FiltradoParticulas:

    def __init__(self, n_particulas, rango, ruido_mov, ruido_medicion):

        # cantidad de particulas
        self.n_particulas = n_particulas

        # ruido del movimiento
        self.ruido_mov = ruido_mov

        # ruido de las mediciones
        self.ruido_medicion = ruido_medicion

        # crear particulas aleatorias dentro del rango
        self.particulas = np.random.uniform(
            -rango,
            rango,
            n_particulas
        )

    def predecir(self, movimiento):
        """
        mueve las particulas
        usando el movimiento esperado
        mas un poco de ruido aleatorio
        """

        self.particulas += (
            movimiento
            + np.random.normal(
                0,
                self.ruido_mov,
                self.n_particulas
            )
        )

    def actualizar(self, medicion):
        """
        calcula que tan probable es cada particula
        segun la medicion observada
        """

        # distribucion gaussiana
        pesos = (
            1 / (np.sqrt(2 * np.pi) * self.ruido_medicion)
        ) * np.exp(
            -0.5 *
            (
                (self.particulas - medicion)
                / self.ruido_medicion
            ) ** 2
        )

        # normalizar pesos
        pesos /= np.sum(pesos)

        # resampling:
        # particulas con mas peso sobreviven mas veces
        indices = np.random.choice(
            range(self.n_particulas),
            size=self.n_particulas,
            p=pesos
        )

        self.particulas = self.particulas[indices]

    def estimar(self):
        """
        usa el promedio de las particulas
        como estimacion final
        """

        return np.mean(self.particulas)

    def mostrar_resumen(self):
        """
        muestra informacion basica
        sobre las particulas
        """

        print("minimo :", round(np.min(self.particulas), 2))
        print("maximo :", round(np.max(self.particulas), 2))
        print("media  :", round(np.mean(self.particulas), 2))

# =========================
# PARAMETROS
# =========================

n_particulas = 1000
rango = 10

ruido_mov = 1.0
ruido_medicion = 2.0

# crear filtro
filtro = FiltradoParticulas(
    n_particulas,
    rango,
    ruido_mov,
    ruido_medicion
)

# =========================
# SIMULACION
# =========================

movimientos = [1, 1, 1, 1, 1]

mediciones = [1.2, 2.8, 4.1, 5.9, 7.5]

print("=== filtrado de particulas ===\n")

for i, (movimiento, medicion) in enumerate(
    zip(movimientos, mediciones)
):

    # prediccion
    filtro.predecir(movimiento)

    # correccion usando medicion
    filtro.actualizar(medicion)

    # estimacion final
    estimacion = filtro.estimar()

    print(
        "paso", i + 1,
        "-> movimiento =", movimiento,
        "| medicion =", round(medicion, 2),
        "| estimacion =", round(estimacion, 2)
    )

# =========================
# RESUMEN FINAL
# =========================

print("\n=== resumen de particulas ===")
filtro.mostrar_resumen()