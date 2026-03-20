import pytest
from codigo_entregable import Almacen, StockInsuficienteError, StockNoEncontradoError, RepuestoDuplicadoError, RepuestoNoEncontradoError

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
            'Filtro', 'Motor', 'Depósito','Reactor',
            'Antena', 'Sensor', 'Bláster', 'Torreta'
            ]


def test_devuelveAlmacen(lista_Almacenes):
    # Recorremos la lista de Almacenes para ver sus nombres y localizacion
    for almacen in lista_Almacenes:
        resultado = f"Nombre: {almacen.nombre} \tLocalización: {almacen.loc}"
        assert  almacen.devuelveAlmacen() == resultado

# Funcion: anyadirStockPieza
def test_anyadirStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[0]
    p = catalogo[0]
    
    almacen.altaPieza(p, 'proveedor1', 10, 5)
        
    # Recorremos el catalogo para añadir 1 unidad de cada pieza al 1er almacén
    for stock in catalogo:
        almacen.anyadirStockPieza(stock, 1)
    
    # Verificamos si la funcion funciona
    assert almacen.cat_rep[0].cant_disp == 6   
    assert len(almacen.cat_rep) == 1  

def test_error_cantidad_negativa_anyadirStockPieza(lista_Almacenes, catalogo): 
    stock = catalogo[0]
    almacen = lista_Almacenes[0]

    # En un entorno protegido, vamos ha ver si la ultima linea falla
    with pytest.raises(ValueError) as exinfo:
        almacen.anyadirStockPieza(stock, -1)
    
    assert str(exinfo.value) == "La cantidad introducida no es correcta"

def test_error_stock_noencontrado_anyadirStockPieza(lista_Almacenes, catalogo): 
    almacen = lista_Almacenes[1]
    for stock in catalogo:
        almacen.anyadirStockPieza(stock, 1)

    # En un entorno protegido, vamos a ver si se produce el fallo
    with pytest.raises(StockNoEncontradoError) as exinfo:
        almacen.anyadirStockPieza('Ala', 12)
    
    assert str(exinfo.value) == "No existe la pieza Ala"


# Funcion: altapieza
def test_altaPieza(lista_Almacenes, catalogo):
    # Añadimos al catalogo de repuestos de cada almacen la lista catalogo
    almacen1 = lista_Almacenes[0]
    pieza1 = catalogo[0]
    almacen1.altaPieza(pieza1, 'proveedor1', 12, 5)
    
    # Verificaciones
    assert pieza1 == almacen1.cat_rep[0].nombre
    assert almacen1.cat_rep[0].cant_disp == 5
    assert almacen1.cat_rep[0].precio == 12

def test_error_duplicado_altaPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[1]
    pieza1 = catalogo[1]
    
    # Añadimos en la lista cat_rep del almacen 2, el catalogo
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)
    
    # En un entorno protegido, vamos a ver si se produce el fallo
    with pytest.raises(RepuestoDuplicadoError) as exinfo:
        almacen.altaPieza(pieza1, 'proveedor1', 12, 5)
    
    assert str(exinfo.value) == 'Almacen Bravo: pieza Motor ya esta registrado'

# Funcion: retirar_repuesto
def test_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)
    
    # Retiramos una unidad de pieza 
    resultado = almacen.retirarStockPieza(pieza, 1)
    
    # Verificamos
    assert resultado == 12
    assert almacen.cat_rep[2].cant_rep == 4

def test_error_cantidad_negativa_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)
    
    # Retiramos una unidad de pieza 
    with pytest.raises(ValueError) as exinfo:
        almacen.retirarStockPieza(pieza, -1)
    
    assert str(exinfo.value) == "La cantidad introducida está en el formato incorrecto"

def test_error_stock_insuficiente_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza = catalogo[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)
    
    
    with pytest.raises(StockInsuficienteError) as exinfo:
        almacen.retirarStockPieza(pieza, 6)
    
    assert str(exinfo.value) == "La cantidad que desea retirar excede la cantidad disponible"

def test_error_respuesto_noencontrado_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    
    # Añadimos el catálogo del almacen correspondiente
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)
    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        almacen.retirarStockPieza('Ala', 1)
    
    assert str(exinfo.value) == "En el almacen Charlie: pieza Ala no se ha encontrado"

# Funcion: eliminarPieza
def test_eliminarPieza(lista_Almacenes, catalogo):
    pieza = catalogo[3]
    almacen = lista_Almacenes[3]
    
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 10, 5)
    
    resultado = almacen.eliminarPieza(pieza)
    assert resultado == f"La pieza {pieza} se ha borrado"


def test_eliminarPieza_no_encontrado(lista_Almacenes, catalogo):
    pieza = 'Ala'
    almacen = lista_Almacenes[3]
    
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 10, 5)
    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        almacen.eliminaPieza(pieza)
    
    assert str(exinfo.value) == f"La pieza {pieza} no se ha encontrado"