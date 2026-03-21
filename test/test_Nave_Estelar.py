import pytest
from codigo_entregable import Nave_Estelar

@pytest.fixture
def nave_estelar():
    return Nave_Estelar(
        				'Elipse', 100, 505555410, 'Nave Capital', 
                        'Bravo752', 'Constelación Errante'
                        )

# Funcion: devuelveInfo
def test_devuelveInfo(nave_estelar):
    resultado = nave_estelar.devuelveInfo()
    
    assert "Nombre: Elipse" in resultado
    assert "Clave Transmisión: Constelación Errante" in resultado

# Funcion: devuelveClase
def test_devuelveClase(nave_estelar):
    resultado = nave_estelar.devuelveClase()
    
    assert "Clase de Elipse: Nave Capital" == resultado