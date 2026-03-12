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

# Implementamos la clase abstracta Uni_Comb
class Uni_Comb(metaclass=ABCMeta):
    def __init__(self, id_combate, clave_transmision):
        self.id_combate = id_combate
        self.clave_trans = clave_transmision
    
    @abstractmethod
    def devuelve_IdComb(self):
        pass
    
    @abstractmethod
    def devuelve_ClaveTrans(self):
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
    def __init__(self, nombre, ub_localizacion):
        self.nombre = nombre
        self.loc = ub_localizacion
        self.cat_rep = {}
    
    def devuelveAlmacen(self):
        return f"Nombre: {self.nombre} \tLocalización: {self.loc}"
    
    def añadirStock(self, nombre, cantidad):
        for s in self.cat_rep:
            if (s == nombre):
                self.cat_rep[nombre] += cantidad
                return
        print(f"No existe la pieza {nombre}")
    
    
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
    def __init__(self, nombre, proveedor, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.cant_disp = 
        self.precio = precio
    
    def devuelvePieza(self):
        return f"""Nombre: {self.nombre}\tCantidad disponible: {self.cant_disp}\n
    				Proveedor: {self.proveedor}\tPrecio: {self.precio}"""
    
    def get_Pieza(self):
        return self.nombre, self.precio        


class Milmprerio:
    def __init__(self):
        self.repuestos = []
        self.almacenes = []
    
    def add_Almacen(self, nombre, localizacion):
        for a in self.almacenes:
            if a == nombre:
                print(f"Almacen {nombre} ya existe en el sistema")
                return
        self.almacenes.append(Almacen(nombre, localizacion))
    