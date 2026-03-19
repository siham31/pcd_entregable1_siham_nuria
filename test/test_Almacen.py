import pytest
from codigo_entregable import Almacen, Pieza, AlmacenDuplicadoError, AlmacenNoEncontradoError, AlmacenVacioError, StockInsuficienteError, StockNoEncontradoError

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
    stock = lista_Almacenes[0]
    almacen = lista_Almacenes[0]

    # En un entorno protegido, vamos ha ver si la ultima linea falla
    with pytest.raises(ValueError):
        almacen.anyadirStock(stock, -1)


def test_error_stock_anyadir_Stock():
    

def test_anyadir_pieza(lista_Almacenes, catalogo):
    # Añadimos al catalogo de repuestos de cada almacen la lista catalogo
    almacen1 = lista_Almacenes[0].copy()
    pieza1 = catalogo[0]
    resultado = almacen1.anyadir_pieza(pieza1, 'proveedor1', 12, 5)
    
    assert resultado is True
    assert pieza1 in almacen1.cat_rep
    assert almacen1.cat_rep[0].cantidad == 5
    assert almacen1.cat_rep[0].precio == 12

def test_error_duplicado_anyadir_pieza(lista_Almacenes):