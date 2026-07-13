import requests

API_KEY = "a6e24750-fe94-4997-97c7-625132e88786"

def obtener_coordenadas(ciudad, pais):
    url = "https://graphhopper.com/api/1/geocode"
    parametros = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros, timeout=15)
    respuesta.raise_for_status()
    datos = respuesta.json()

    if not datos.get("hits"):
        raise ValueError(f"No se encontró la ciudad: {ciudad}")

    punto = datos["hits"][0]["point"]
    return punto["lat"], punto["lng"]


def calcular_ruta(origen, destino, transporte):
    url = "https://graphhopper.com/api/1/route"
    parametros = {
        "point": [
            f"{origen[0]},{origen[1]}",
            f"{destino[0]},{destino[1]}"
        ],
        "profile": transporte,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros, timeout=30)
    respuesta.raise_for_status()
    datos = respuesta.json()

    if not datos.get("paths"):
        raise ValueError("No se pudo calcular la ruta.")

    return datos["paths"][0]


while True:
    print("\n=== Cálculo de viaje Chile - Argentina ===")
    ciudad_origen = input("Ciudad de Origen en Chile (o s para salir): ").strip()

    if ciudad_origen.lower() == "s":
        print("Programa finalizado.")
        break

    ciudad_destino = input("Ciudad de Destino en Argentina: ").strip()

    print("\nMedios de transporte disponibles:")
    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Seleccione una opción: ").strip()

    perfiles = {
        "1": ("car", "automóvil"),
        "2": ("bike", "bicicleta"),
        "3": ("foot", "caminando")
    }

    if opcion not in perfiles:
        print("Opción de transporte inválida.")
        continue

    perfil, nombre_transporte = perfiles[opcion]

    try:
        origen = obtener_coordenadas(ciudad_origen, "Chile")
        destino = obtener_coordenadas(ciudad_destino, "Argentina")
        ruta = calcular_ruta(origen, destino, perfil)

        kilometros = ruta["distance"] / 1000
        millas = kilometros * 0.621371
        minutos_totales = int(ruta["time"] / 60000)
        horas = minutos_totales // 60
        minutos = minutos_totales % 60

        print("\n=== Resumen del viaje ===")
        print(f"Origen: {ciudad_origen}, Chile")
        print(f"Destino: {ciudad_destino}, Argentina")
        print(f"Transporte: {nombre_transporte}")
        print(f"Distancia: {kilometros:.2f} km")
        print(f"Distancia: {millas:.2f} millas")
        print(f"Duración aproximada: {horas} horas y {minutos} minutos")

        print("\n=== Narrativa del viaje ===")
        for instruccion in ruta["instructions"]:
            print(f"- {instruccion['text']}")

    except requests.RequestException as error:
        print(f"Error al consultar GraphHopper: {error}")
    except (ValueError, KeyError, IndexError) as error:
        print(f"Error: {error}")

