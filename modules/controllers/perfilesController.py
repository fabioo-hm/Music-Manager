import modules.utils.corefiles as cf
import modules.utils.screenController as sc
import modules.ui as ui
from tabulate import tabulate
DB_FILE = "data/database.json"
def agregarPerfil():
    sc.borrar_pantalla()
    nombre = input('Ingrese el nombre del perfil que desea crear\n ->').lower()
    new_profile = {
            nombre: {}  
    }
    cf.update_json (DB_FILE, new_profile, ["Perfiles"])  

def eliminarPerfil():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados para eliminar.")
        sc.pausar_pantalla()
        return
    print("Perfiles disponibles para eliminar:\n")
    lista_perfiles = list(perfiles.keys())
    for i, perfil in enumerate(lista_perfiles, 1):
        print(f"{i}. {perfil}")
    try:
        opcion = int(input("\nIngrese el número del perfil a eliminar: ")) - 1
        if opcion < 0 or opcion >= len(lista_perfiles):
            raise ValueError
    except ValueError:
        print("Opción inválida. Intente de nuevo.")
        sc.pausar_pantalla()
        return eliminarPerfil()
    perfil_a_eliminar = lista_perfiles[opcion]
    confirmacion = input(f"¿Seguro que desea eliminar el perfil '{perfil_a_eliminar}'? (s/n): ").lower()
    if confirmacion == 's':
        del data["Perfiles"][perfil_a_eliminar]
        cf.write_json(DB_FILE, data)
        print("El perfil ha sido eliminado exitosamente.")
    else:
        print("Operación cancelada.")
    sc.pausar_pantalla()
def adminPerfil():
    pass
def editPerfil():
    data = cf.read_json(DB_FILE)
    perfiles = data.get("Perfiles", {})
    if not perfiles:
        print("No hay perfiles registrados para editar.")
        sc.pausar_pantalla()
        return
    print("Perfiles disponibles para editar:\n")
    lista_perfiles = list(perfiles.keys())
    for i, perfil in enumerate(lista_perfiles, 1):
        print(f"{i}. {perfil}")
    while True:
        try:
            opcion = int(input("\nIngrese el número del perfil a editar: ")) - 1
            if 0 <= opcion < len(lista_perfiles):
                break
            else:
                print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Solo puede ingresar números.")
    perfil_a_editar = lista_perfiles[opcion]
    while True:
        nuevo_nombre = input(f"Ingrese el nuevo nombre para '{perfil_a_editar}': ").strip()
        if not nuevo_nombre:
            print("El nombre no puede estar vacío.")
        elif nuevo_nombre in perfiles:
            print("Ese nombre ya existe. Intente con otro.")
        else:
            break
    perfiles[nuevo_nombre] = perfiles.pop(perfil_a_editar)
    cf.write_json(DB_FILE, data)

    print(f"El perfil '{perfil_a_editar}' ha sido renombrado a '{nuevo_nombre}'.")
    sc.pausar_pantalla()