import modules.utils.corefiles as cf
import modules.utils.screenController as sc
from tabulate import tabulate
from modules.ui import MENU_PLAYLIST
DB_FILE = "data/database.json"


def menuplaylist():
    sc.borrar_pantalla()
    print(MENU_PLAYLIST)
    try:
        option = int(input(":)_"))
    except ValueError:
        print("Solo se permiten valores numericos")
        sc.pausar_pantalla()
        return menuplaylist()
    else:
        match option:
            case 1:
                sc.borrar_pantalla()
                agregarcancion()
                sc.pausar_pantalla()
                return menuplaylist()
            case 2:
                sc.borrar_pantalla()
                eliminarcancion()
                sc.pausar_pantalla()
                return menuplaylist()
            case 3:
                sc.borrar_pantalla()
                buscarcancion()
                sc.pausar_pantalla()
                return menuplaylist()
            case 4:
                sc.borrar_pantalla()
                mostrarcanciones()
                sc.pausar_pantalla()
                return menuplaylist()
            case 5:
                print("Regresando al menu anterior...")
                sc.pausar_pantalla()
            case _:
                sc.borrar_pantalla()
                print("Opcion invalida")
                sc.pausar_pantalla()
                return menuplaylist()
def agregarcancion():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados.")
        sc.pausar_pantalla()
        return
    print("Perfiles disponibles para elegir:\n")
    lista_perfiles = list(perfiles.keys())
    for i, perfil in enumerate(lista_perfiles, 1):
        print(f"{i}. {perfil}")
    try:
        opcion = int(input("\nIngrese el número del perfil a elegir: ")) - 1
        if opcion < 0 or opcion >= len(lista_perfiles):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return agregarcancion()
    perfil_seleccionado = lista_perfiles[opcion]
    playlists = perfiles[perfil_seleccionado].get("Playlists", {})
    if not playlists:
        print(f"El perfil '{perfil_seleccionado}' no tiene playlists registradas.")
        sc.pausar_pantalla()
        return
    print("\nPlaylists disponibles para agregar canciones:\n")
    lista_playlist = list(playlists.keys())
    for i, nombre_playlist in enumerate(lista_playlist, 1):
        print(f"{i}. {nombre_playlist}")
    try:
        opcion = int(input("\nIngrese el número de la playlist a elegir: ")) - 1
        if opcion < 0 or opcion >= len(lista_playlist):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return agregarcancion()
    playlist_seleccionada = lista_playlist[opcion]
    titulo = input("Ingrese el título de la canción: ")
    artista = input("Ingrese el nombre del artista: ")
    genero = input("Ingrese el género musical: ")
    cancion = {
        "Título": titulo,
        "Artista": artista,
        "Género": genero
    }
    perfiles[perfil_seleccionado]["Playlists"][playlist_seleccionada].append(cancion)
    cf.write_json(DB_FILE, data)
    print(f"\nCanción '{titulo}' agregada a la playlist '{playlist_seleccionada}' en el perfil '{perfil_seleccionado}'.")
    sc.pausar_pantalla()

def eliminarcancion():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados.")
        sc.pausar_pantalla()
        return
    print("Perfiles disponibles para elegir:\n")
    lista_perfiles = list(perfiles.keys())
    for i, perfil in enumerate(lista_perfiles, 1):
        print(f"{i}. {perfil}")
    try:
        opcion = int(input("\nIngrese el número del perfil a elegir: ")) - 1
        if opcion < 0 or opcion >= len(lista_perfiles):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return eliminarcancion()
    perfil_seleccionado = lista_perfiles[opcion]
    playlists = perfiles[perfil_seleccionado].get("Playlists", {})
    if not playlists:
        print(f"El perfil '{perfil_seleccionado}' no tiene playlists registradas.")
        sc.pausar_pantalla()
        return
    print("\nPlaylists disponibles para eliminar canciones:\n")
    lista_playlist = list(playlists.keys())
    for i, nombre_playlist in enumerate(lista_playlist, 1):
        print(f"{i}. {nombre_playlist}")
    try:
        opcion = int(input("\nIngrese el número de la playlist a elegir: ")) - 1
        if opcion < 0 or opcion >= len(lista_playlist):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return eliminarcancion()
    playlist_seleccionada = lista_playlist[opcion]
    canciones = perfiles[perfil_seleccionado]["Playlists"][playlist_seleccionada]
    if not canciones:
        print("No hay canciones en esta playlist.")
        sc.pausar_pantalla()
        return
    titulo = input("Ingrese el título de la canción a eliminar: ").strip().lower()
    canciones_filtradas = [c for c in canciones if c["Título"].lower() != titulo]
    if len(canciones) == len(canciones_filtradas):
        print("No se encontró ninguna canción con ese título.")
    else:
        confirmacion = input(f"¿Seguro que desea eliminar la canción '{titulo}'? (s/n): ").lower()
        if confirmacion == 's':
            perfiles[perfil_seleccionado]["Playlists"][playlist_seleccionada] = canciones_filtradas
            cf.write_json(DB_FILE, data)
            print("La canción ha sido eliminada.")
        else:
            print("Operación cancelada.")
    sc.pausar_pantalla()
              
def buscarcancion():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados.")
        sc.pausar_pantalla()
        return
    titulo_buscar = input("Ingrese el título de la canción que desea buscar: ").strip().lower()
    resultados = []
    for perfil, datos in perfiles.items():
        for playlist, canciones in datos.get("Playlists", {}).items():
            for cancion in canciones:
                if cancion["Título"].lower() == titulo_buscar:
                    resultados.append((perfil, playlist, cancion))
    if not resultados:
        print("No se encontró ninguna canción con ese título.")
    else:
        print("\nCanción encontrada en:")
        from tabulate import tabulate
        tabla = [[perfil, playlist, c["Título"], c["Artista"], c["Género"]] for perfil, playlist, c in resultados]
        print(tabulate(tabla, headers=["Perfil", "Playlist", "Título", "Artista", "Género"], tablefmt="grid"))
    sc.pausar_pantalla()

def mostrarcanciones():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados.")
        sc.pausar_pantalla()
        return
    print("Perfiles disponibles para elegir:\n")
    lista_perfiles = list(perfiles.keys())
    for i, perfil in enumerate(lista_perfiles, 1):
        print(f"{i}. {perfil}")
    try:
        opcion = int(input("\nIngrese el número del perfil a elegir: ")) - 1
        if opcion < 0 or opcion >= len(lista_perfiles):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return mostrarcanciones()
    perfil_seleccionado = lista_perfiles[opcion]
    playlists = perfiles[perfil_seleccionado].get("Playlists", {})
    if not playlists:
        print(f"El perfil '{perfil_seleccionado}' no tiene playlists registradas.")
        sc.pausar_pantalla()
        return
    print("\nPlaylists disponibles para ver canciones:\n")
    lista_playlist = list(playlists.keys())
    for i, nombre_playlist in enumerate(lista_playlist, 1):
        print(f"{i}. {nombre_playlist}")
    try:
        opcion = int(input("\nIngrese el número de la playlist a visualizar: ")) - 1
        if opcion < 0 or opcion >= len(lista_playlist):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return mostrarcanciones()
    playlist_seleccionada = lista_playlist[opcion]
    canciones = perfiles[perfil_seleccionado]["Playlists"][playlist_seleccionada]
    if not canciones:
        print("No hay canciones en esta playlist.")
    else:
        print(f"\nCanciones en la playlist '{playlist_seleccionada}' de {perfil_seleccionado}\n")
        tabla = [[c["Título"], c["Artista"], c["Género"]] for c in canciones]
        print(tabulate(tabla, headers=["Título", "Artista", "Género"], tablefmt="grid"))
    sc.pausar_pantalla()
