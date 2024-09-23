class Proveedor:
    def __init__(self, codigo, nombre, estado):
        self.codigo = codigo
        self.nombre = nombre.strip().upper()
        self.estado = estado.strip().upper()


class Producto:
    def __init__(self, id_prod, nombre, estado):
        self.id_prod = id_prod
        self.nombre = nombre.strip().upper()
        self.estado = estado.strip().upper()


class RelacionProductoProveedor:
    def __init__(self, codigo_proveedor, codigo_producto, estado):
        self.codigo_proveedor = codigo_proveedor
        self.codigo_producto = codigo_producto
        self.estado = estado.strip().upper()


class GestionarProductos:
    def __init__(self):
        """Inicializa el gestor cargando datos desde archivos."""
        self.proveedores = self.cargar_datos('Proveedor.txt', self.procesar_linea_proveedor, dict)
        self.productos = self.cargar_datos('Productos.txt', self.procesar_linea_producto, dict)
        self.relaciones = self.cargar_datos('Prod_Proveedor.txt', self.procesar_linea_relacion, list)

    def cargar_datos(self, archivo, procesar_func, tipo):
        """Carga y procesa datos de un archivo en una estructura dada."""
        datos = tipo()
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                for linea in file.readlines()[1:]:
                    resultado = procesar_func(linea)
                    if resultado:
                        if isinstance(datos, dict) and resultado[0] not in datos:
                            datos[resultado[0]] = resultado[1]
                        elif isinstance(datos, list):
                            datos.append(resultado)
        except FileNotFoundError:
            print(f'Error: El archivo "{archivo}" no se encontró.')
        return datos

    def procesar_linea_proveedor(self, linea):
        """Convierte una línea del archivo de proveedores en un objeto Proveedor."""
        datos = linea.split()
        return (int(datos[0]), Proveedor(int(datos[0]), ' '.join(datos[1:-1]), datos[-1])) \
            if len(datos) >= 3 and datos[0].isdigit() else None

    def procesar_linea_producto(self, linea):
        """Convierte una línea del archivo de productos en un objeto Producto."""
        datos = linea.split()
        return (int(datos[0]), Producto(int(datos[0]), ' '.join(datos[1:-1]), datos[-1])) \
            if len(datos) >= 3 and datos[0].isdigit() else None

    def procesar_linea_relacion(self, linea):
        """Convierte una línea del archivo de productos por proveedor en un objeto RelacionProductoProveedor."""
        datos = linea.split()
        return RelacionProductoProveedor(int(datos[0]), int(datos[1]), datos[2]) \
            if len(datos) == 3 and datos[0].isdigit() and datos[1].isdigit() else None

    def modificar_producto(self, nombre_producto, nuevo_nombre, nuevo_estado, proveedor_nombre):
        """Modifica un producto buscando por nombre, nuevo nombre, nuevo estado y proveedor."""
        id_proveedor = self.obtener_id_proveedor(proveedor_nombre)
        if id_proveedor is None:
            print(f'Proveedor "{proveedor_nombre}" no encontrado.')
            return
        for rel in self.relaciones:
            if rel.codigo_proveedor == id_proveedor:
                producto = self.productos.get(rel.codigo_producto)
                if producto and producto.nombre.lower() == nombre_producto.lower():
                    producto.nombre = nuevo_nombre.strip().upper()
                    producto.estado = nuevo_estado.strip().upper()
                    rel.estado = nuevo_estado.strip().upper()
                    self.guardar_productos()
                    self.guardar_relaciones()
                    print(f'Producto "{nombre_producto}" modificado exitosamente.')
                    return
        print(f'Producto "{nombre_producto}" no encontrado.')

    def obtener_id_proveedor(self, nombre_proveedor):
        """Devuelve el ID de un proveedor dado su nombre."""
        return next((k for k, v in self.proveedores.items()
                     if v.nombre.lower() == nombre_proveedor.lower()), None)

    def guardar_productos(self):
        """Guarda la lista de productos en 'Productos.txt'."""
        with open('Productos.txt', 'w', encoding='utf-8') as file:
            file.write('ID PRODUCTO ESTADO\n')
            for producto in self.productos.values():
                file.write(f'{producto.id_prod} {producto.nombre} {producto.estado}\n')

    def guardar_relaciones(self):
        """Guarda la lista de relaciones en 'Prod_Proveedor.txt'."""
        with open('Prod_Proveedor.txt', 'w', encoding='utf-8') as file:
            file.write('PRV_COD PRO_COD ESTADO\n')
            for rel in self.relaciones:
                file.write(f'{rel.codigo_proveedor} {rel.codigo_producto} {rel.estado}\n')

    def consultar_producto(self, nombre_proveedor):
        """Consulta y muestra los productos de un proveedor específico."""
        id_proveedor = self.obtener_id_proveedor(nombre_proveedor)
        if id_proveedor is None:
            print(f'Proveedor "{nombre_proveedor}" no encontrado.')
            return

        proveedor = self.proveedores[id_proveedor]
        print(f'Proveedor: {proveedor.nombre}')
        print(f'Estado: {proveedor.estado}')
        print('ID PRODUCTO ESTADO')

        total_productos = 0

        for rel in self.relaciones:
            if rel.codigo_proveedor == id_proveedor:
                producto = self.productos.get(rel.codigo_producto)
                if producto:
                    print(f'{producto.id_prod} {producto.nombre} {rel.estado}')
                    total_productos += 1

        print(f'\nTotal de productos: {total_productos}')


def main():
    """Función principal para ejecutar el gestor de productos."""
    global nuevo_nombre, nuevo_estado
    gestor = GestionarProductos()

    print('¡Hola! Bienvenido al Gestor de Productos')
    print('Puedes modificar o consultar productos asociados a los proveedores.')

    while True:
        print('\n__ Menú de Opciones __')
        print('1. Modificar Producto')
        print('2. Consultar Producto')
        print('3. Salir')
        opcion = input('Selecciona una opción: ')

        if opcion == '1':
            # Ingresar nombre del proveedor
            nombre_proveedor = input('Ingresa el nombre del proveedor: ')

            while True:
                nombre_producto = input('Ingresa el nombre del producto a modificar: ').strip()
                if not nombre_producto:
                    print('El nombre del producto no puede estar vacío.')
                    continue

                nuevo_nombre = input('Ingresa el nuevo nombre del producto: ').strip()
                if not nuevo_nombre:
                    print('El nuevo nombre del producto no puede estar vacío.')
                    continue

                nuevo_estado = input('Selecciona el estado del nuevo producto (A/I): ').strip().upper()
                if nuevo_estado not in ['A', 'I']:
                    print('Estado inválido. Ingresa "A" para Activo o "I" para Inactivo.')
                    continue
                break
            gestor.modificar_producto(nombre_producto, nuevo_nombre, nuevo_estado, nombre_proveedor)
        elif opcion == '2':
            nombre_proveedor = input('Ingresa el nombre del proveedor: ')
            gestor.consultar_producto(nombre_proveedor)
        elif opcion == '3':
            print('Saliendo del gestor de productos. ¡Hasta luego! Esperamos verte pronto.')
            break
        else:
            print('Opción no válida. Intenta nuevamente.')

if __name__ == '__main__':
    main()



