import pytest
from codigo_entregable import Almacen, Pieza, StockInsuficienteError, StockNoEncontradoError, RepuestoDuplicadoError, RepuestoNoEncontradoError

# Definimos una lista de Almacenes 
@pytest.fixture
def lista_Almacenes():
    return [
            Almacen('Alpha', 'Nebulosa de los Suspiros Olvidados'),
            Almacen('Bravo', 'Faro de la Galaxia Andrómeda-B'),
            Almacen('Charlie' , "Colmena de Neón de K'thun"),
            Almacen('Delta', 'Nexo de Cristal de Xylos-7'),
            Almacen('Echo', 'Archipiélago de Agujeros Negros de Ophiuchus Prime'),
            Almacen('Foxtrot', 'Ciudadela Flotante de Aethelgard')
            ]

# Funcion: __init__
def test_creacion_almacen(lista_Almacenes):
    almacen = lista_Almacenes[0]
    assert almacen.nombre == 'Alpha'
    assert almacen.loc == 'Nebulosa de los Suspiros Olvidados'

# Definimos una lista de stock que podemos añadir o quitar 
@pytest.fixture
def catalogo():
    return [
            Pieza('Filtro', 'prov1', 11, 10),
            Pieza('Motor', 'prov2', 11, 10),
            Pieza('Depósito', 'prov3', 11, 10),
            Pieza('Reactor', 'prov4', 11, 10),
            Pieza('Antena', 'prov5', 11, 10),
            Pieza('Sensor', 'prov6', 11, 10),
            Pieza('Bláster', 'prov7', 11, 10),
            Pieza('Torreta', 'prov8', 11, 10)
            ]


def test_devuelveAlmacen(lista_Almacenes):
    # Recorremos la lista de Almacenes para ver sus nombres y localizacion
    for almacen in lista_Almacenes:
        resultado = f"Nombre: {almacen.nombre} \tLocalización: {almacen.loc}"
        assert  almacen.devuelveAlmacen() == resultado

# Funcion: anyadirStock
def test_anyadirStock(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[0]
    
    # Recorremos el catalogo para añadir 1 unidad de cada pieza al 1er almacén
    for stock in catalogo:
        almacen.anyadirStock(stock, 1)
    
    # Verificamos si la funcion funciona
    assert almacen.cat_rep[0].nombre == 'Filtro'    #1era pieza
    assert almacen.cat_rep[7].nombre == 'Torreta'   #7ª pieza
    assert len(almacen.cat_rep) == 8                # Tamaño de cat_rep

def test_error_cantidad_negativa_anyadirStock(lista_Almacenes, catalogo): 
    stock = catalogo[0]
    almacen = lista_Almacenes[0]

    # En un entorno protegido, vamos ha ver si la ultima linea falla
    with pytest.raises(ValueError) as exinfo:
        almacen.anyadirStock(stock, -1)
    
    assert exinfo == "La cantidad introducida no es correcta"

def test_error_stock_noencontrado_anyadir_Stock(lista_Almacenes, catalogo): 
    almacen = lista_Almacenes[1]
    for stock in catalogo:
        almacen.anyadirStock(stock, 1)

    # En un entorno protegido, vamos a ver si se produce el fallo
    with pytest.raises(StockNoEncontradoError) as exinfo:
        almacen.anyadirStock('Ala', 12)
    
    assert exinfo == "No existe la pieza Ala"


# Funcion: anyadir_pieza
def test_anyadir_pieza(lista_Almacenes, catalogo):
    # Añadimos al catalogo de repuestos de cada almacen la lista catalogo
    almacen1 = lista_Almacenes[0].copy()
    pieza1 = catalogo[0]
    resultado = almacen1.anyadir_pieza(pieza1, 'proveedor1', 12, 5)
    
    # Verificaciones
    assert resultado is True
    assert pieza1 in almacen1.cat_rep
    assert almacen1.cat_rep[0].cantidad == 5
    assert almacen1.cat_rep[0].precio == 12

def test_error_duplicado_anyadir_pieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[1]
    pieza1 = catalogo[1]
    
    # Añadimos en la lista cat_rep del almacen 2, el catalogo
    for p in catalogo:
        almacen.anyadir_pieza(p, 'proveedor1', 12, 5)
    
    # En un entorno protegido, vamos a ver si se produce el fallo
    with pytest.raises(RepuestoDuplicadoError) as exinfo:
        almacen.anyadir_pieza(pieza1, 'proveedor1', 12, 5)
    
    assert exinfo == 'Almacen Beta: pieza Motor ya esta registrado'

# Funcion: retirar_repuesto
def test_retirar_repuesto(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.anyadir_pieza(p, 'proveedor1', 12, 5)
    
    # Retiramos una unidad de pieza 
    resultado = almacen.retirar_repuesto(pieza, 1)
    
    # Verificamos
    assert resultado == 12
    assert almacen.cat_rep[2].cantidad == 4

def test_error_cantidad_negativa_retirar_repuesto(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.anyadir_pieza(p, 'proveedor1', 12, 5)
    
    # Retiramos una unidad de pieza 
    with pytest.raises(ValueError) as exinfo:
        almacen.retirar_repuesto(pieza, -1)
    
    assert exinfo == "La cantidad introducida está en el formato incorrecto"

def test_error_stock_insuficiente_retirar_repuesto(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.anyadir_pieza(p, 'proveedor1', 12, 5)
    
    #
    with pytest.raises(StockInsuficienteError) as exinfo:
        almacen.retirar_repuesto(pieza, 6)
    
    assert exinfo == "La cantidad que desea retirar excede la cantidad disponible"


def test_error_respuesto_noencontrado_retirar_repuesto(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.anyadir_pieza(p, 'proveedor1', 12, 5)
    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        almacen.retirar_repuesto('Ala', 1)
    
    assert exinfo == "En el almacen Charlie: pieza Ala no se ha encontrado"