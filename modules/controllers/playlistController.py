import modules.utils.corefiles as cf
import modules.utils.screenController as sc
from modules.ui import MENU_PLAYLIST
DB_FILE = "data/database.json"

def agregarcancion():
    sc.borrar_pantalla()
    print(MENU_PLAYLIST)
    try:
        option = int(input(':)_'))
    except ValueError:
        print("Solo se permiten valores numericos")
        sc.pausar_pantalla()
        return agregarcancion()
    else :
        match option:
            case 1 :
                title = input("Titulo: ")
                artist = input("Artista: ")
                genre = input("Genero: ")
                new_song = {
                        "title": title,
                        "artist": artist,
                        "genre": genre
                }
                cf.update_json(DB_FILE, new_song, ["playlist"])
def eliminarcancion():
    sc.borrar_pantalla()
    print("""
==================================
        Eliminar canciones
==================================
1.Eliminar por Titulo
2.Eliminar por Artista
3.Eliminar por Genero
==================================""")
    try:
        option = int(input(':)_'))
    except ValueError:
        print("Solo se permiten valores numericos")
        sc.pausar_pantalla
        return eliminarcancion()
    else:
        match option:
            case "1":
                data = cf.read_json(DB_FILE)
                categorias = ["libros", "peliculas", "musica"]
                elementos_disponibles = []
                print("Elementos Disponibles para Eliminar:\n")
                for categoria in categorias:
                    elementos = data.get(categoria, {})
                    for isbn, info in elementos.items():
                        elementos_disponibles.append([
                            categoria,
                            isbn,
                            info.get("title", ""),
                            info.get("artist", ""),
                            info.get("genre", ""),
                        ])
                headers = ["Categoría", "ISBN", "Título", "Autor/Director/Artista", "Género"]
                print(tabulate(elementos_disponibles, headers=headers, tablefmt="grid"))
                eliminar_titulo = input("Ingrese el título del elemento a eliminar: ")
                encontrado = False
                for categoria in categorias:
                    elementos = data.get(categoria, {})
                    isbn_a_eliminar = None
                    for isbn, info in elementos.items():
                        if info.get("title","").lower() == eliminar_titulo.lower():
                            isbn_a_eliminar = isbn
                    if isbn_a_eliminar:
                        confirmacion = input(f"Quiere eliminar '{eliminar_titulo}'? s/n: ").lower()
                        if confirmacion == 's':
                            del data[categoria][isbn_a_eliminar]
                            cf.write_json(DB_FILE, data)
                            print("El elemento ha sido eliminado.")
                            encontrado = True
                        else:
                            print("Operacion cancelada.")
                            sc.pausar_pantalla()
                            return eliminarcancion()
                if not encontrado:
                    print("No se encontro ningun elemento con ese titulo.")
                sc.pausar_pantalla()
                return eliminarcancion()
                
def buscarcancion():
    sc.borrar_pantalla()
    print("""
==================================
        Buscar canciones
==================================
1.Buscar por Titulo
2.Buscar por Artista
3.Buscar por Genero
==================================""")
    try:
        option = int(input(':)_'))
    except ValueError:
        return mostrarMenubuscar()
    else:
        match option:
            case 1:
                titulo = input("Ingrese el título del elemento que desea buscar: ")
                data = cf.read_json(DB_FILE)
                categorias = ["musica"]
                encontrado = False
                for categoria in categorias:
                    elementos = data.get(categoria, {})
                    for isbn, info in elementos.items():
                        if info.get("title","").lower() == titulo.lower():
                            print(f"\nElemento encontrado en: {categoria}")
                            print(f"ISBN: {isbn}")
                            print(f"Título: {info['title']}")
                            print(f"Artista: {info.get('artist')}")	
                            print(f"Género: {info['genre']}\n")
                            encontrado = True
                sc.pausar_pantalla()
                if not encontrado:
                    print("No se encontró ningún elemento con este título.\n")
                    sc.pausar_pantalla()
                return mostrarMenubuscar()
            