import pytest
from codigo_entregable import Pieza

# Creamos una pieza para usar en los test
@pytest.fixture
def pieza():
    return Pieza('Motor', 'proveedor1', 10, 5)

# Funcion: __init__
def test_creacion_pieza(pieza):
    assert pieza.nombre == 'Motor'
    assert pieza.proveedor == 'proveedor1'
    assert pieza.precio == 10
    assert pieza.cant_disp == 5

# Funcion: devuelvePieza
def test_devuelvePieza(pieza):
    resultado = pieza.devuelvePieza()
    assert "Nombre: Motor" in resultado
    assert "Cantidad disponible: 5" in resultado
    assert "Proveedor: proveedor1" in resultado
    assert "Precio: 10" in resultado

# Funcion: get_Pieza
def test_get_Pieza(pieza):
    nombre, precio = pieza.get_Pieza()
    
    assert nombre == 'Motor'
    assert precio == 10

# Funcion: get_cantidad
def test_get_cantidad(pieza):
    assert pieza.get_cantidad() == 5


# Funcion: set_cantidad
def test_set_cantidad(pieza):
    pieza.set_cantidad(6)
    
    assert pieza.cant_disp == 6

def test_error_set_cantidad_negativa(pieza):
    
    with pytest.raises(ValueError) as exinfo:
        pieza.set_cantidad(-1)
    
    assert str(exinfo.value) == 'la cantidad no puede ser negativa'
