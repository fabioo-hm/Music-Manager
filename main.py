import modules.controllers.perfilesController as pc
import modules.controllers.playlistController as plc
import modules.controllers.adminperfiController as apc
import modules.utils.corefiles as cf
import modules.utils.screenController as sc
import modules.ui as ui
DB_FILE = "data/dbadmincolecciones.json"

cf.initialize_json(DB_FILE, {})
def menu():
    sc.borrar_pantalla()
    print(ui.MAIN_MENU)
    try:
        option = int(input(':)_'))
    except ValueError:
        print("Solo se permiten valores numericos")
        sc.pausar_pantalla()
        return menu()
    else:
        match option:
            case 1:
                sc.borrar_pantalla()
                pc.agregarPerfil()
                sc.pausar_pantalla()
                return menu()
            case 2:
                sc.borrar_pantalla()
                pc.eliminarPerfil()
                sc.pausar_pantalla()
                return menu()
            case 3:
                sc.borrar_pantalla()
                pc.adminPerfil()
                sc.pausar_pantalla()
                return menu()
            case 4:
                sc.borrar_pantalla()
                pc.editPerfil()
                sc.pausar_pantalla()
                return menu()
            case 5:
                print("Saliendo del programa...")
            case _:
                sc.borrar_pantalla()
                print("Opcion invalida")
                sc.pausar_pantalla()
                return menu()

if __name__ == "__main__":
    menu()