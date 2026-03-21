import pytest
from codigo_entregable import Milmprerio, AlmacenDuplicadoError

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

