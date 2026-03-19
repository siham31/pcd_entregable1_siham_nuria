from enum import Enum
from abc import ABCMeta, abstractmethod

# Implementamos las enumeraciones
class EUbicacion(Enum):
    ENDOR = 0
    CUMULO_RAIMOS = 1
    NEBULOSA_KALIIDA = 2

class EClase(Enum):
    EJECUTOR = 0
    ECLIPSE = 1
    SOBERANO = 2



# Implemetamos las excepciones 

# Excepciones de Stock
class StockInsuficienteError(Exception):
    """ Se lanza cuando no hay suficientes stock de una pieza para atender a un pedido"""
    pass

class StockNoEncontradoError(Exception):
    """Se lanza cuando se busca el stock que no existe en el almacen"""
    pass

# Excepciones de Repuesto
class RepuestoNoEncontradoError(Exception):
    """ Se lanza cuando se busca una pieza que no existe en el catálogo
    """
    pass

class RepuestoVacioError(Exception):
    """Se lanza cuando el listado de respuestos está vacío"""
    pass 

class RepuestoDuplicadoError(Exception):
    """Se lanza cuandi se intenta añadir una pieza (repuesto) ya existe en el almacen
    seleccionado"""
    pass

# Excepciones de Almacen
class AlmacenNoEncontradoError(Exception):
    """"Se lanza cuando se busca un almacen que no existe en el listado de almacenes"""
    pass

class AlmacenDuplicadoError(Exception):
    """Se lanza cuando se intenta añadir un almacén que ya existe."""
    pass

class AlmacenVacioError(Exception):
    """Se lanza cuando el listado de almacenes está vacío"""
    pass

# Excepciones de Nave 
class NaveNoEncontradaError(Exception):
    """Se lanza cuando se intenta operar sobre una nave no registrada."""
    pass


# Implementamos la clase abstracta Uni_Comb
class Uni_Comb(metaclass=ABCMeta):
    """  clase abstracta que representa cualquier unidad de combate emperial"""
    def __init__(self, id_combate, clave_transmision):
        self.id_combate = id_combate
        self.clave_trans = clave_transmision
    
    @abstractmethod
    def devuelve_IdComb(self):
        pass
    
    @abstractmethod
    def devuelve_ClaveTrans(self) -> int:
        pass


# Implementamos el resto del codigo
class Nave:
    def __init__(self, nombre):
        self.nombre = nombre
        self.piezas_rep = {}
    
    def devuelveNave(self):
        return "Nave: " + self.nombre
    
    def devuelvePiezasRep(self):
        for p,c in self.piezas_rep.items():
            print("Nombre: ", p, "\tCantidad: ", c)


class Almacen:
    " Almacen con catalogo propio de piezas de repuesto"
    def __init__(self, nombre, ub_localizacion):
        self.nombre = nombre
        self.loc = ub_localizacion
        self.cat_rep = []  # catalogo 
    
    def devuelveAlmacen(self):
        return f"Nombre: {self.nombre} \tLocalización: {self.loc}"
    
    def anyadirStock(self, nombre, cantidad):
        if cantidad < 0:
            raise ValueError("La cantidad introducida no es correcta")
        
        for s in self.cat_rep:
            if (s.nombre == nombre):
                s.cantidad += cantidad
                print("La cantidad ha sido añadido con éxito")
                return
        raise StockNoEncontradoError(f"No existe la pieza {nombre}")
    
    def anyadir_pieza(self,pieza, proveedor, precio, cantidad):
        for p in self.cat_rep:
            if p.nombre == pieza:
                raise RepuestoDuplicadoError(f'Almacen: {self.nombre}: pieza {pieza} ya existe ya está registrado')             
            
        self.cat_rep.append(Pieza(pieza, proveedor, precio, cantidad))
        print(f"Almacen {self.nombre} pieza{p.nombre} añadida al catalogo")

    def retirar_repuesto(self,nombre,cantidad):
        """retira unidades de una pieza y devuelve el coste total"""
        for p in self.cat_rep:
            if p.nombre == nombre:
        #if nombre not in self.cat_rep:
                raise RepuestoNoEncontradoError(f"En el almacen {self.nombre}: pieza {nombre} no encontrada")
        
        for p in self.cat_rep: # pieza es un string
            if p.nombre == nombre:
                pieza = p
                pieza.cantidad -= cantidad
                coste = pieza.precio * cantidad
                return coste
        raise RepuestoNoEncontradoError(f"En el almacen {self.nombre}: pieza {nombre} no se ha encontrado")

class Estacion_Espacial(Nave,Uni_Comb):
    def __init__(self, nombre, tripulacion, ubicacion, pasaje, id_combate, clave_transmision):
        Nave.__init__(self, nombre)
        Uni_Comb.__init__(self, id_combate, clave_transmision)
        self.tripulacion = tripulacion
        self.ubi = ubicacion
        self.pasaje = pasaje
            
    def devuelveInfo(self):
        return f"""Nombre: {self.nombre}\tTripulación: {self.tripulacion}\n
    				Ubicacion: {self.ubi}\tPasaje: {self.pasaje}\n
        			Id Combate: {self.id_combate}\tClave Transmisión: {self.clave_trans}"""
    
    def devuelveUbi(self):
        return f"Ubicación de {self.nombre}: {self.ubi}"
        
class Nave_Estelar(Nave,Uni_Comb):
    def __init__(self, nombre, tripulacion, pasaje, clase, id_combate, clave_transmision):
        Nave.__init__(self,nombre)
        Uni_Comb.__init__(self,id_combate, clave_transmision)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase
        
    def devuelveInfo(self):
        return f"""Nombre: {self.nombre}\tTripulación: {self.tripulacion}\n
        			Clase: {self.clase}\tPasaje: {self.pasaje}\n
        			Id Combate: {self.id_combate}\tClave Transmisión: {self.clave_trans}"""
    
    def devuelveClase(self):
        return f"Clase de {self.nombre}: {self.clase}"

class Caza_Estelar(Nave,Uni_Comb):
    def __init__(self, nombre, dotacion, id_combate, clave_transmision):
        Nave.__init__(self,nombre)
        Uni_Comb.__init__(self,id_combate, clave_transmision)
        self.dotacion = dotacion
    
    def devuelveInfo(self):
        return f"""Nombre: {self.nombre}\tDotacion: {self.dotacion}\n
        			Id Combate: {self.id_combate}\tClave Transmisión: {self.clave_trans}"""
    
    def devuelveDotacion(self):
        return f"Dotacion de {self.nombre}: {self.dotacion}"

class Pieza:
    """    representa una pieza de respuesto almacenada en un almacen """
    def __init__(self, nombre, proveedor, precio,cantidad):
        self.nombre = nombre
        self.proveedor = proveedor
        self.cant_disp = cantidad
        self.precio = precio
    
    def devuelvePieza(self):
        return f"""Nombre: {self.nombre}\tCantidad disponible: {self.cant_disp}\n
    				Proveedor: {self.proveedor}\tPrecio: {self.precio}"""
    
    def get_Pieza(self):
        return self.nombre, self.precio  

    def get_cantidad(self) -> int:
        return self.cant_disp
    
    def set_cantidad(self,cantidad:int):
        if cantidad < 0:
            raise ValueError("la cantidad no puede ser negativa")
        self.cant_disp = cantidad
    

# Clase Milmperio
class Milmprerio:
    def __init__(self):
        self._repuestos = []
        self._almacenes = []
    
    # Almacen
    def addAlmacen(self, nombre, localizacion):
        """Añadir el almacen (nombre) con una ubicacion (localizacion) en el listado"""
        for a in self._almacenes:
            if a == nombre:
                raise AlmacenDuplicadoError(f"El almacen con nombre {a} ya está registrado en el sistema")
        self._almacenes.append(Almacen(nombre, localizacion))
        
    def getAlmacen(self,nombre):
        """Ver el almacen nombre si esta en el sistema"""
        for a in self._almacenes:
            if a.nombre == nombre :  # comparamos que los nombres coinciden
                return a
        raise AlmacenDuplicadoError(f"Almacen {nombre} no encontrado")
    
    def listarAlmacen(self):
        """Listar todos los almacenes registrados en el sistema"""
        if len(self._almacenes) == 0:
            print(f"No hay almacenes registrados en el sistema")
            return
        for a in self._almacenes:
            print(a.devuelveAlmacen())
    
    def quitarAlmacen(self, nombre):
        """Eliminar el almacen nombre del listado self._almacenes"""
        for a in self._almacenes:
            if a.nombre == nombre:
                self._almacenes.remove(nombre)
                return
        raise AlmacenNoEncontradoError(f"El almacen {nombre} no se encuentra registrado")
    
    # Repuesto
    def addRepuesto(self, nombre, proveedor, precio, cantidad, almacen):
        """Añadir la pieza (nombre) con cantidad (cantidad) en el almacen (almacen)"""
        if cantidad < 0:
            raise ValueError(f"La cantidad introducida debe ser positiva")
        
        for a in self._almacenes:
            if a.nombre == almacen:
                catalogo = a.cat_rep
                
                for p in catalogo:
                    if p.nombre == nombre:
                        raise RepuestoDuplicadoError(f"La pieza {nombre} ya existe en el almacen {almacen}")
                
                catalogo.append(Pieza(nombre, proveedor, precio, cantidad))
                print(f"La pieza {nombre} ha sido añadido con éxito en el almacen {almacen}")
                return
        raise AlmacenNoEncontradoError(f"El almacen {almacen} no se encuentra registrado")
    
    def getRepuesto(self, nombre, almacen):
        """Ver si la pieza (nombre) está en el almacen (almacen)"""
        for a in self._almacenes:
            if a.nombre == almacen:
                catalogo = a.cat_rep 
                
                for p in catalogo:
                    if p.nombre == nombre:
                        print(f"La pieza {nombre} está en el almacen {almacen}")
                        return
                raise RepuestoNoEncontradoError(f"La pieza {nombre} no se encuentra en el almacen {almacen}")
        raise AlmacenNoEncontradoError(f"El almacen {almacen} no se encuentra registrado")
    
    def listarRepuestos(self):
        """Listar todas las piezas de repuestos registrados en el sistema"""
        if len(self._repuestos) == 0:
            raise ValueError(f"No hay piezas registradas en el sistema")
        
        for p in self._repuestos:
            print(p.devuelvePieza)
    
    def quitarRepuesto(self, nombre, almacen): 
        """Quitar la pieza (nombre) del almacen (almacen)"""
        for a in self._almacenes:
            if a.nombre == almacen:
                catalogo = a.cat_rep
                
                for p in catalogo:
                    if p.nombre == nombre:
                        catalogo.remove(nombre)
                        print(f"Eliminado con éxito la pieza {nombre} del almacen {almacen}")
                        return
                raise RepuestoNoEncontradoError(f"La pieza {nombre} no se encuentra en el almacen {almacen}")
        raise AlmacenNoEncontradoError(f"El almacen {almacen} no se encuentra registrado en el sistema")
    
    # Stock
    def listarStocks(self, almacen):
        for a in self._almacenes:
            if a.nombre == almacen:
                print(f"Listado de stock en el almacen {almacen}")
                for p in a.cat_rep:
                    print(f"-\t{p}")
            raise AlmacenNoEncontradoError(f"El almacen {almacen} no se encuentra registrado en el sistema")
        




def main():

    sistema = Milmprerio()

    # -------------------------
    # PRUEBA 1: Crear almacenes
    # -------------------------
    print("PRUEBA 1: Crear almacenes")

    sistema.addAlmacen("Almacen_1", EUbicacion.ENDOR)
    sistema.addAlmacen("Almacen_2", EUbicacion.NEBULOSA_KALIIDA)

    sistema.listarAlmacen()


    # -------------------------
    # PRUEBA 2: Añadir repuestos
    # -------------------------
    print("\nPRUEBA 2: Añadir repuestos")

    sistema.addRepuesto("Motor", "Kuat Drive Yards", 5000, 10, "Almacen_1")
    sistema.addRepuesto("Laser", "BlasTech", 2000, 5, "Almacen_1")

    sistema.getRepuesto("Motor", "Almacen_1")


    # -------------------------
    # PRUEBA 3: Error repuesto duplicado
    # -------------------------
    print("\nPRUEBA 3: Repuesto duplicado")

    try:
        sistema.addRepuesto("Motor", "Kuat Drive Yards", 5000, 10, "Almacen_1")
    except RepuestoDuplicadoError as e:
        print(e)


    # -------------------------
    # PRUEBA 4: Error almacen inexistente
    # -------------------------
    print("\nPRUEBA 4: Almacen no encontrado")

    try:
        sistema.addRepuesto("Escudo", "Sienar", 3000, 3, "Almacen_X")
    except AlmacenNoEncontradoError as e:
        print(e)


    # -------------------------
    # PRUEBA 5: Crear naves
    # -------------------------
    print("\nPRUEBA 5: Crear naves")

    nave1 = Nave_Estelar(
        "Destructor Imperial",
        47000,
        1000,
        EClase.EJECUTOR,
        12345,
        999
    )

    print(nave1.devuelveInfo())


    estacion = Estacion_Espacial(
        "Estrella de la Muerte",
        200000,
        EUbicacion.CUMULO_RAIMOS,
        10000,
        9999,
        8888
    )

    print(estacion.devuelveInfo())


    caza = Caza_Estelar(
        "TIE Fighter",
        1,
        111,
        222
    )

    print(caza.devuelveInfo())


if __name__ == "__main__":
    main()














