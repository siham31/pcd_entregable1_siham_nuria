import pytest
from codigo_entregable import Milmprerio, AlmacenDuplicadoError, AlmacenNoEncontradoError, RepuestoDuplicadoError, RepuestoNoEncontradoError, RepuestoVacioError

@pytest.fixture
def milperio():
    return Milmprerio()

# Función: __init__
def test_creacion_milperio(milmperio):
    assert len(milmperio._repuestos) == 0
    assert len(milmperio._almacenes) == 0

# Almacen

# Funcion: addAlmacen
def test_addAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    assert len(milmperio._almacenes) == 1

def test_error_addAlmacen_duplicado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
        
    with pytest.raises(AlmacenDuplicadoError) as exinfo:
        milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    assert str(exinfo.value) == f"El almacen con nombre Alpha ya está registrado en el sistema"


# Funcion: getAlmacen
def test_getAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    almacen = milmperio.getAlmacen('Alpha')
    assert almacen.nombre == 'Alpha'
    assert almacen.loc == 'Nexo de Cristal de Xylos-7'

def test_error_getAlmacen_no_encontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    with pytest.raises(AlmacenNoEncontradoError) as exinfo: 
        milmperio('Bravo', 'Faro de Andrómeda')
    
    assert str(exinfo.value) == "Almacen Bravo no encontrado"

# Funcion: listarAlmacen
def test_listarAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')
    
    milmperio.listarAlmacen()
    captured = capsys.readouterr()
    
    assert "Nombre: Alpha" in captured
    assert "Localización: Archipiélago de Agujeros Negros de Ophiuchus Prime" in captured

def test_listarAlmacen_nohayAlmacenes(milmperio):
    result = milmperio.listarAlmacen()
    
    assert result == "No hay almacenes registrados en el sistema"

# Funcion: quitarAlmacen
def test_quitarAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')
    
    milmperio.quitarAlmacen('Alpha')
    
    milmperio.listarAlmacen()
    captured = capsys.readouterr()
    
    assert "Nombre: Alpha" not in captured

def test_error_quitarAlmacen_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')
    
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.quitarAlmacen('Delta')
    
    assert str(exinfo.value) == "El almacen Delta no se encuentra registrado"


# Repuesto

# Funcion: addRepuesto
def test_addRepuesto(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    milmperio.addRepuesto("Motor", "proveedor1", 12, 10, 'Alpha')
    
    captured = capsys.readouterr()
    assert captured == "La pieza Motor se ha añadido con éxito en el almacen Alpha"

def test_error_addRepuesto_negativo(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    with pytest.raises(ValueError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, -1, 'Alpha')
    
    assert str(exinfo.value) == "La cantidad introducida debe ser positiva"

def test_error_addRespuesto_duplicado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, -1, 'Alpha')
    
    with pytest.raises(RepuestoDuplicadoError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, -1, 'Alpha')
    
    assert str(exinfo.value) == 'La pieza Motor ya existe en el almacen Alpha'

def test_error_addRepuesto_noAlmacen(milmperio):
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    
    assert str(exinfo.value) == "El almacen Alpha no se encuentra registrado"

# Funcion: getRepuesto
def test_getRepuesto(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    result = milmperio.getRepuesto('Motor', 'Alpha')
    assert result.nombre == 'Motor'

def test_error_getRepuesto_noencontrado_repuesto(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        milmperio.getRepuesto('Torreta', 'Alpha')
    
    assert str(exinfo.value) == 'La pieza Torreta no se encuentra en el almacen Alpha'

def test_error_getRepuesto_noencontrado_almacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Bravo')
        milmperio.getRepuesto('Motor', 'Bravo')
    
    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado'

# Funcion: listarRepuestos
def test_listarRepuestos(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    capsys.readouterr()
    milmperio.listarRepuestos()
    captured = capsys.readouterr()
    
    assert "Nombre: Motor" in captured
    assert "Precio: 10" in captured

def test_error_listarRepuestos_vacio(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(RepuestoVacioError) as exinfo:
        milmperio.listarRepuestos()
    
    assert str(exinfo.value) == "No hay piezas registradas en el sistema"

# Funcion: quitarRepuestos
def test_quitarRepuestos(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    capsys.readouterr()
    
    milmperio.quitarRepuesto('Motor', 'Alpha')
    captured = capsys.readouterr()
    
    assert captured == 'Eliminado con éxito la pieza Motor del almacen Alpha'


def test_error_quitarRepuestos_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        milmperio.quitarRepuesto('Torreta', 'Alpha')
    
    assert str(exinfo.value) == 'La pieza Torreta no se encuentra en el almacen Alpha'


def test_error_quitarRepeustos_almacen_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.quitarRepuesto('Motor', 'Bravo')
    
    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado en el sistema'


# Stock
# Funcion: listarStocks
def test_listarStocks(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addrepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')
    
    capsys.readouterr()
    
    milmperio.listarStocks('Alpha')
    captured = capsys.readouterr()
    
    assert "Listado de stock en el almacen Alpha:" in captured
    assert "Nombre: Motor" in captured
    assert "Precio: 10" in captured

def test_error_listarStocks_almacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.listarStocks('Bravo')
    
    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado en el sistema'
    