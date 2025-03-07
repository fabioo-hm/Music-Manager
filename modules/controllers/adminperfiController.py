import modules.utils.corefiles as cf
import modules.utils.screenController as sc
import modules.ui as ui
import modules.controllers.playlistController as plc
from tabulate import tabulate
DB_FILE = "data/database.json"

def menuadmin():
    sc.borrar_pantalla()
    print(ui.MENU_ADMIN)
    try:
        option = int(input(":)_"))
    except ValueError:
        print("Solo se permiten valores numericos")
        sc.pausar_pantalla()
        return menuadmin()
    else:
        match option:
            case 1:
                sc.borrar_pantalla()
                agregarPlaylist()
                sc.pausar_pantalla()
                return menuadmin()
            case 2:
                sc.borrar_pantalla()
                plc.menuplaylist()
                sc.pausar_pantalla()
                return menuadmin()
            case 3:
                sc.borrar_pantalla()
                eliminarPlaylist()
                sc.pausar_pantalla()
                return menuadmin()
            case 4:
                sc.borrar_pantalla()
                mostrarPlaylists()
                sc.pausar_pantalla()
                return menuadmin()
            case 5:
                print("Regresando al menu anterior...")
                sc.pausar_pantalla()
            case _:
                sc.borrar_pantalla()
                print("Opcion invalida")
                sc.pausar_pantalla()
                return menuadmin()


def agregarPlaylist():
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
        return agregarPlaylist()
    
    perfil_seleccionado = lista_perfiles[opcion]
    
    sc.borrar_pantalla()
    nombre_playlist = input('Ingrese el nombre de la playlist que desea crear\n -> ').lower()
    if "Playlists" not in perfiles[perfil_seleccionado]:
        perfiles[perfil_seleccionado]["Playlists"] = {}
    perfiles[perfil_seleccionado]["Playlists"][nombre_playlist] = []
    cf.write_json(DB_FILE, data)  
    print(f"\nPlaylist '{nombre_playlist}' creada en el perfil '{perfil_seleccionado}'.")
    sc.pausar_pantalla()

def eliminarPlaylist():
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
        return eliminarPlaylist()
    perfil_seleccionado = lista_perfiles[opcion]
    playlists = perfiles[perfil_seleccionado].get("Playlists", {})
    if not playlists:
        print(f"El perfil '{perfil_seleccionado}' no tiene playlists registradas.")
        sc.pausar_pantalla()
        return
    print("\nPlaylists disponibles para eliminar:\n")
    lista_playlist = list(playlists.keys())
    for i, playlist_nombre in enumerate(lista_playlist, 1):
        print(f"{i}. {playlist_nombre}")
    try:
        opcion = int(input("\nIngrese el número de la playlist que desea eliminar: ")) - 1
        if opcion < 0 or opcion >= len(lista_playlist):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return eliminarPlaylist()
    playlist_a_eliminar = lista_playlist[opcion]
    confirmacion = input(f"¿Seguro que desea eliminar la playlist '{playlist_a_eliminar}'? (s/n): ").lower()
    if confirmacion == 's':
        del perfiles[perfil_seleccionado]["Playlists"][playlist_a_eliminar]
        cf.write_json(DB_FILE, data)
        print(f"La playlist '{playlist_a_eliminar}' ha sido eliminada exitosamente.")
    else:
        print("Operación cancelada.")
    sc.pausar_pantalla()

def mostrarPlaylists():
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
        return mostrarPlaylists()
    perfil_seleccionado = lista_perfiles[opcion]
    playlists = perfiles[perfil_seleccionado].get("Playlists", {})
    if not playlists:
        print(f"El perfil '{perfil_seleccionado}' no tiene playlists registradas.")
    else:
        print(f"\nPlaylists de {perfil_seleccionado}:")
        tabla = [[i + 1, nombre]for i, nombre in enumerate(playlists.keys())]
        print(tabulate(tabla, headers=["#", "Nombre de la Playlist"], tablefmt="grid"))
    sc.pausar_pantalla()