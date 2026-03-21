import pytest
from codigo_entregable import Caza_Estelar

@pytest.fixture
def caza_estelar():
    return Caza_Estelar('TIE Advanced x1', 1, 'INT-A98', '4F9Z-29KL')

# Funcion: __init__
def test_creacion_caza_estelar(caza_estelar):
    assert caza_estelar.nombre == 'TIE Advanced x1'
    assert caza_estelar.clave_trans == '4F9Z-29KL'

# Funcion: devuelveInfo
def test_devuelveInfo(caza_estelar):
    resultado = caza_estelar.devuelveInfo()
    
    assert "Nombre: TIE Advanced x1" in resultado
    assert "Clave Transmisión: 4F9Z-29KL" in resultado

# Funcion: devuelveDotacion
def test_devuelveDotacion(caza_estelar):
    resultado = caza_estelar.devuelveDotacion()
    
    assert "Dotación de TIE Advanced x1: 1" == resultado