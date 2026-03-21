import pytest
from codigo_entregable import Estacion_Espacial

@pytest.fixture
def estacion_espacial():
    return Estacion_Espacial(
        					'NSS Éxodo', 15, 'Nebulosa de los Suspiros', 
            				5500000, "Alpha48", "Echo-7-Amber"
                )

# Funcion: __init__
def test_creacion_estacion_espacial(estacion_espacial):
    assert estacion_espacial.nombre == 'NSS Éxodo'
    assert estacion_espacial.clave_trans == "Echo-7-Amber"

# Funcion: devuelveInfo
def test_devuelveInfo(estacion_espacial):
    resultado = estacion_espacial.devuelveInfo()
    
    assert "Nombre: NSS Éxodo" in resultado
    assert "Clave Transmisión: Echo-7-Amber" in resultado

# Funcion: devuelveUbi
def test_devuelveUbi(estacion_espacial):
    resultado = estacion_espacial.devuelveUbi()
    
    assert resultado == "Ubicación de NSS Éxodo: Nebulosa de los Suspiros"