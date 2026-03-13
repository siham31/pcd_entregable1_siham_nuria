from enum import Enum
from abc import ABCMeta, abstractmethod

# Implementamos las enumeraciones
class EUbicacion(Enum):
    ENDOR = 0,
    CUMULO_RAIMOS = 1,
    NEBULOSA_KALIIDA = 2

class EClase(Enum):
    EJECUTOR = 0,
    ECLIPSE = 1,
    SOBERANO = 2



# implemetamos las excepciones 
class StockInsuficienteError(Exception):
    """ Se lanza cuando no hay suficientes stock de una pieza para atender a un pedido"""
    pass

class RepuestoNoEncontradoError(Exception):
    """ Se lanza cuando se busca una pieza que no existe en el catálogo
    """
    pass

class AlmacenNoEncontradoError(Exception):
    """"Se lamza cuando se busca un almacen que no existe en el listado de almacenes"""

class AlmacenDuplicadoError(Exception):
    """Se lanza cuando se intenta añadir un almacén que ya existe."""
    pass

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
        for p,c in self.piezas_rep.items:
            print("Nombre: ", p, "\tCantidad: ", c)


class Almacen:
    " Almacen con catalogo propio de piezas de repuesto"
    def __init__(self, nombre, ub_localizacion):
        self.nombre = nombre
        self.loc = ub_localizacion
        self.cat_rep = dict[str,Pieza] = {}
    
    def devuelveAlmacen(self):
        return f"Nombre: {self.nombre} \tLocalización: {self.loc}"
    
    def anyadirStock(self, nombre, cantidad):
        for s in self.cat_rep:
            if (s == nombre):
                self.cat_rep[nombre] += cantidad
                return
        print(f"No existe la pieza {nombre}")
    
    def anyadir_pieza(self,pieza):
        if pieza.nombre in self.cat_rep:
            print(f"almacen {self.nombre}  La pieza :{pieza.nombre} ya existe en el catalogo")
        else:
            self.cat_rep[pieza.nombre]=pieza
            print(f"Almacen {self.nombre} pieza{pieza.nombre} añadida al catalogo")

    def retirar_repuesto(self,nombre,cantidad):
        """   retira unidades de una pieza y devuelve el coste total"""
        if nombre not in self.cat_rep:
            raise RepuestoNoEncontradoError(f"ALmacen {self.nombre} pieza {nombre} no encontrada")
        pieza = self.cat_rep[nombre]
        pieza.retirar_stock(cantidad)
        coste = pieza.precio * cantidad
        return coste

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
        if cantidad <0:
            raise ValueError("la cantidad no puede ser negativa")
        self.cant_disp = cantidad
    

class Milmprerio:
    def __init__(self):
        self.repuestos = []
        self.almacenes = []
    
    def add_Almacen(self, nombre, localizacion):
        for a in self.almacenes:
            if a == nombre:
                raise AlmacenDuplicadoError(f"El almacen con nombre {a} ya está registrado en el sistema")
        self.almacenes.append(Almacen(nombre, localizacion))
        
        
    def get_almacen(self,nombre):
        for a in self.almacenes:
            if a.nombre == nombre :  # comparamos que los nombres coinciden
                return a
        raise RepuestoNoEncontradoError(f"Almacen {nombre} no encontrado")
    
    def listarAlmacen(self):
        if len(self.almacenes) == 0:
            print(f"No hay almacenes registrados en el sistema")
            return
        for a in self.almacenes:
            print(a.devuelveAlmacen)
    
    def listarRepuestos(self):
        if len(self.repuestos) == 0:
            print("No hay piezas registradas en el sistema")
            return
        for p in self.repuestos:
            print(p.devuelvePieza)
    
    def 