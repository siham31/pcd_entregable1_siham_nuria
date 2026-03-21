import pytest
from codigo_entregable import (
    Almacen, StockInsuficienteError, StockNoEncontradoError,
    RepuestoDuplicadoError, RepuestoNoEncontradoError
)

# ---------------------------------------------------------------------------
# FIXTURES
# ---------------------------------------------------------------------------

@pytest.fixture
def lista_Almacenes():
    # Se recrea en cada test (scope="function" por defecto) → tests aislados
    return [
        Almacen('Alpha',   'Nebulosa de los Suspiros Olvidados'),
        Almacen('Bravo',   'Faro de la Galaxia Andrómeda-B'),
        Almacen('Charlie', "Colmena de Neón de K'thun"),
        Almacen('Delta',   'Nexo de Cristal de Xylos-7'),
        Almacen('Echo',    'Archipiélago de Agujeros Negros de Ophiuchus Prime'),
        Almacen('Foxtrot', 'Ciudadela Flotante de Aethelgard'),
    ]

@pytest.fixture
def catalogo():
    return ['Filtro', 'Motor', 'Depósito', 'Reactor',
            'Antena', 'Sensor', 'Bláster', 'Torreta']


# ---------------------------------------------------------------------------
# test __init__ y devuelveAlmacen
# ---------------------------------------------------------------------------

def test_creacion_almacen(lista_Almacenes):
    almacen = lista_Almacenes[0]
    assert almacen.nombre == 'Alpha'
    assert almacen.loc == 'Nebulosa de los Suspiros Olvidados'

def test_devuelveAlmacen(lista_Almacenes):
    for almacen in lista_Almacenes:
        resultado = f"Nombre: {almacen.nombre} \tLocalización: {almacen.loc}"
        assert almacen.devuelveAlmacen() == resultado


# ---------------------------------------------------------------------------
# test altaPieza
# ---------------------------------------------------------------------------

def test_altaPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[0]
    pieza1 = catalogo[0]   # 'Filtro'
    almacen.altaPieza(pieza1, 'proveedor1', 12, 5)

    assert almacen.cat_rep[0].nombre    == pieza1
    assert almacen.cat_rep[0].cant_disp == 5
    assert almacen.cat_rep[0].precio    == 12

def test_error_duplicado_altaPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[1]   # Bravo
    pieza1  = catalogo[1]          # 'Motor'

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)

   
    with pytest.raises(RepuestoDuplicadoError) as exinfo:
        almacen.altaPieza(pieza1, 'proveedor1', 12, 5)

    assert str(exinfo.value) == 'Almacen: Bravo: pieza Motor ya está registrado'


# ---------------------------------------------------------------------------
# test anyadirStockPieza
# ---------------------------------------------------------------------------

def test_anyadirStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[0]

    
    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 10, 5)

    
    for p in catalogo:
        almacen.anyadirStockPieza(p, 1)

    # 'Filtro' (índice 0) pasa de 5 a 6
    assert almacen.cat_rep[0].cant_disp == 6
    # El catálogo tiene las 8 piezas
    assert len(almacen.cat_rep) == 8

def test_error_cantidad_negativa_anyadirStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[0]
    # Necesitamos dar de alta la pieza primero para que no falle por StockNoEncontradoError
    almacen.altaPieza(catalogo[0], 'proveedor1', 10, 5)

    with pytest.raises(ValueError) as exinfo:
        almacen.anyadirStockPieza(catalogo[0], -1)

    assert str(exinfo.value) == "La cantidad introducida no es correcta"

def test_error_stock_noencontrado_anyadirStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[1]   # Bravo (vacío)

    with pytest.raises(StockNoEncontradoError) as exinfo:
        almacen.anyadirStockPieza('Ala', 12)

    assert str(exinfo.value) == "No existe la pieza Ala"


# ---------------------------------------------------------------------------
# test retirarStockPieza
# ---------------------------------------------------------------------------

def test_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]   # Charlie
    pieza   = catalogo[2]          # 'Depósito'

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)

    resultado = almacen.retirarStockPieza(pieza, 1)

    assert resultado == 12
   
    assert almacen.cat_rep[2].cant_disp == 4

def test_error_cantidad_negativa_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza   = catalogo[2]

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)

    with pytest.raises(ValueError) as exinfo:
        almacen.retirarStockPieza(pieza, -1)

    assert str(exinfo.value) == "La cantidad introducida está en el formato incorrecto"

def test_error_stock_insuficiente_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]
    pieza   = catalogo[2]

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)

    with pytest.raises(StockInsuficienteError) as exinfo:
        almacen.retirarStockPieza(pieza, 6)

    assert str(exinfo.value) == "La cantidad que desea retirar excede la cantidad disponible"

def test_error_repuesto_noencontrado_retirarStockPieza(lista_Almacenes, catalogo):
    almacen = lista_Almacenes[2]

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 12, 5)

    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        almacen.retirarStockPieza('Ala', 1)

    assert str(exinfo.value) == "En el almacen Charlie: pieza Ala no se ha encontrado"


# ---------------------------------------------------------------------------
# test eliminarPieza
# ---------------------------------------------------------------------------

def test_eliminarPieza(lista_Almacenes, catalogo):
    pieza   = catalogo[3]          # 'Reactor'
    almacen = lista_Almacenes[3]   # Delta

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 10, 5)

    resultado = almacen.eliminarPieza(pieza)
    assert resultado == f"La pieza {pieza} se ha borrado"

def test_eliminarPieza_no_encontrado(lista_Almacenes, catalogo):
    pieza   = 'Ala'
    almacen = lista_Almacenes[3]

    for p in catalogo:
        almacen.altaPieza(p, 'proveedor1', 10, 5)

    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        almacen.eliminarPieza(pieza)

    assert str(exinfo.value) == f"La pieza {pieza} no se ha encontrado"