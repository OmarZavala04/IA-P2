# Carga una imagen en escala de grises,
# aplica suavizado Gaussiano y después
# usa el detector de bordes Canny.
# Finalmente muestra:
# - imagen original
# - imagen suavizada
# - bordes detectados

import cv2
import numpy as np
from matplotlib import pyplot as plt

# ======================= CARGA DE IMAGEN =======================

ruta_imagen = "Soldaditos.JPG"

imagen = cv2.imread(
    ruta_imagen,
    cv2.IMREAD_GRAYSCALE
)

# ======================= VALIDACIÓN =======================

if imagen is None:

    print("ERROR:")
    print("No se pudo cargar la imagen.")
    print("Verifica que la ruta exista:")
    print(ruta_imagen)

else:

    print("Imagen cargada correctamente")
    print("Dimensiones:", imagen.shape)

    # ======================= PREPROCESAMIENTO =======================

    # Aplicar desenfoque Gaussiano
    # ayuda a reducir ruido antes de detectar bordes
    imagen_suavizada = cv2.GaussianBlur(
        imagen,
        (5, 5),
        0
    )

    # ======================= DETECCIÓN DE BORDES =======================

    # umbral bajo = 100
    # umbral alto = 200
    bordes = cv2.Canny(
        imagen_suavizada,
        100,
        200
    )

    # ======================= INFORMACIÓN =======================

    cantidad_bordes = np.count_nonzero(bordes)

    print("Cantidad de píxeles detectados como borde:", cantidad_bordes)

    # ======================= VISUALIZACIÓN =======================

    plt.figure(figsize=(15, 5))

    # ---------- Imagen original ----------

    plt.subplot(1, 3, 1)

    plt.imshow(
        imagen,
        cmap='gray'
    )

    plt.title("Imagen Original")

    plt.axis("off")

    # ---------- Imagen suavizada ----------

    plt.subplot(1, 3, 2)

    plt.imshow(
        imagen_suavizada,
        cmap='gray'
    )

    plt.title("Imagen Suavizada")

    plt.axis("off")

    # ---------- Bordes detectados ----------

    plt.subplot(1, 3, 3)

    plt.imshow(
        bordes,
        cmap='gray'
    )

    plt.title("Detector de Bordes Canny")

    plt.axis("off")

    # Ajustar diseño
    plt.tight_layout()

    # Mostrar resultados
    plt.show()