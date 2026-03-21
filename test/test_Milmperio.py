import pytest
from codigo_entregable import Milmprerio, AlmacenDuplicadoError, AlmacenNoEncontradoError, RepuestoDuplicadoError

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

def test_error_addRepuesto_noAlmacen(milmperio):
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    
    assert str(exinfo.value) == "El almacen Alpha no se encuentra registrado"

# Funcion: getRepuesto
def test_getRepuesto(milmperio):
    