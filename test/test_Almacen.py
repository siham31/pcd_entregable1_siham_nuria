import pytest
from codigo_entregable import Almacen, AlmacenDuplicadoError, AlmacenNoEncontradoError, AlmacenVacioError, StockInsuficienteError, StockNoEncontradoError

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
    return ['Filtro', 'Motor', 
            'Depósito', 'Reactor', 
            'Antena', 'Sensor', 
            'Bláster', 'Torreta'
            ]


def test_devuelveAlmacen(lista_Almacenes):
    for almacen in lista_Almacenes:
        resultado = f"Nombre: {almacen.nombre} \tLocalización: {almacen.loc}"
        assert  almacen.devuelveAlmacen() == resultado

def test_anyadirStock(lista_Almacenes, catalogo):
    # Añadimos al catalogo de repuestos de cada almacen la lista catalogo
    for stock in catalogo:    
        for almacen in lista_Almacenes:  
            almacen.anyadirStock(stock, 1)
    assert lista_Almacenes[0].cat_rep[0] == 
    

def test_error_cantidad_anyadirStock(): 
    

def test_error_stock_anyadir_Stock():