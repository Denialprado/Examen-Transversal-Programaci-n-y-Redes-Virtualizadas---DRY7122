
import requests
import urllib.parse
import os

CLAVE_API = "9e0a6d97-4107-468b-8eff-8abee34a9586"

def obtener_coordenadas(ubicacion, clave):
    """Convierte un nombre de ubicación en coordenadas geográficas."""
    url_geocodificacion = "https://graphhopper.com/api/1/geocode?"
    url_completa = url_geocodificacion + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": clave})
    try:
        respuesta = requests.get(url_completa)
        datos_json = respuesta.json()
        if respuesta.status_code == 200 and len(datos_json.get("hits", [])) > 0:
            lat = datos_json["hits"][0]["point"]["lat"]
            lng = datos_json["hits"][0]["point"]["lng"]
            return respuesta.status_code, lat, lng
        else:
            print(f"\nError: No se pudo encontrar la ubicación '{ubicacion}'.")
            return respuesta.status_code, None, None
    except requests.exceptions.RequestException:
        print("\nError de conexión.")
        return None, None, None

def principal():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Diccionario para traducir las opciones de transporte
        mapa_transporte = {"auto": "car", "bicicleta": "bike", "caminar": "foot"}

        origen = input("Ciudad de Origen (o 's' para salir): ")
        if origen.lower() == 's': break
        
        destino = input("Ciudad de Destino (o 's' para salir): ")
        if destino.lower() == 's': break
        
        transporte_usuario = input("Selecciona el medio de transporte (Auto, Bicicleta, Caminar): ").lower()
        if transporte_usuario == 's': break

        vehiculo_api = mapa_transporte.get(transporte_usuario, "car")

        status_origen, lat_origen, lng_origen = obtener_coordenadas(origen, CLAVE_API)
        status_destino, lat_destino, lng_destino = obtener_coordenadas(destino, CLAVE_API)

        if status_origen == 200 and status_destino == 200:
            url_ruta = "https://graphhopper.com/api/1/route?"
            punto_origen = f"&point={lat_origen},{lng_origen}"
            punto_destino = f"&point={lat_destino},{lng_destino}"
            url_completa_ruta = url_ruta + urllib.parse.urlencode({"key": CLAVE_API, "vehicle": vehiculo_api}) + punto_origen + punto_destino
            
            datos_ruta = requests.get(url_completa_ruta).json()

            if "paths" in datos_ruta:
                dist_km = datos_ruta["paths"][0]["distance"] / 1000
                dist_millas = dist_km * 0.621371
                
                segundos_totales = int(datos_ruta["paths"][0]["time"] / 1000)
                minutos, segundos = divmod(segundos_totales, 60)
                horas, minutos = divmod(minutos, 60)

                # --- SECCIÓN DE SALIDA AJUSTADA AL FORMATO SOLICITADO ---
                print(f"Viajarás en: {transporte_usuario}")
                print(f"Distancia entre {origen} y {destino}: {dist_km:.2f} km / {dist_millas:.2f} millas")
                print(f"Duracion del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
                print(f"Viajarás desde {origen}, hacia {destino} ¡Buen viaje!.")
                print("="*50)

            else:
                print(f"\nNo se pudo calcular la ruta. Error: {datos_ruta.get('message', 'Ruta no encontrada')}")
        
        siguiente = input("Presiona enter para continuar o 's' para salir: ").lower()
        if siguiente == 's':
            break

if __name__ == "__main__":
    principal()
