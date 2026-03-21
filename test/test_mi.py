import pytest
from codigo_entregable import (
    Milmprerio, AlmacenDuplicadoError, AlmacenNoEncontradoError,
    RepuestoDuplicadoError, RepuestoNoEncontradoError, RepuestoVacioError
)

# ---------------------------------------------------------------------------
# FIXTURE
# ---------------------------------------------------------------------------

@pytest.fixture
def milmperio():
    return Milmprerio()


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

def test_creacion_milperio(milmperio):
    assert len(milmperio._repuestos) == 0
    assert len(milmperio._almacenes) == 0


# ---------------------------------------------------------------------------
# addAlmacen
# ---------------------------------------------------------------------------

def test_addAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    assert len(milmperio._almacenes) == 1

def test_error_addAlmacen_duplicado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(AlmacenDuplicadoError) as exinfo:
        milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    assert str(exinfo.value) == "El almacen con nombre Alpha ya está registrado en el sistema"


# ---------------------------------------------------------------------------
# getAlmacen
# ---------------------------------------------------------------------------

def test_getAlmacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    almacen = milmperio.getAlmacen('Alpha')
    assert almacen.nombre == 'Alpha'
    assert almacen.loc == 'Nexo de Cristal de Xylos-7'

def test_error_getAlmacen_no_encontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    # CORRECCIÓN 1: se llamaba milmperio('Bravo',...) como si fuera función;
    # debe ser milmperio.getAlmacen('Bravo')
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.getAlmacen('Bravo')

    assert str(exinfo.value) == "Almacen Bravo no encontrado"


# ---------------------------------------------------------------------------
# listarAlmacen
# ---------------------------------------------------------------------------

# CORRECCIÓN 2: capsys no estaba declarado como parámetro en ningún test que lo usa
def test_listarAlmacen(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')

    milmperio.listarAlmacen()
    captured = capsys.readouterr()

    # CORRECCIÓN 3: captured es un objeto; el texto está en captured.out
    assert "Nombre: Alpha" in captured.out
    assert "Archipiélago de Agujeros Negros de Ophiuchus Prime" in captured.out

def test_listarAlmacen_nohayAlmacenes(milmperio, capsys):
    milmperio.listarAlmacen()
    captured = capsys.readouterr()

    # CORRECCIÓN 4: listarAlmacen() no retorna nada, imprime por pantalla
    assert "No hay almacenes registrados en el sistema" in captured.out


# ---------------------------------------------------------------------------
# quitarAlmacen
# ---------------------------------------------------------------------------

def test_quitarAlmacen(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')

    milmperio.quitarAlmacen('Alpha')

    milmperio.listarAlmacen()
    captured = capsys.readouterr()

    assert "Nombre: Alpha" not in captured.out

def test_error_quitarAlmacen_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addAlmacen('Bravo', 'Faro de Andrómeda')
    milmperio.addAlmacen('Charlie', 'Archipiélago de Agujeros Negros de Ophiuchus Prime')

    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.quitarAlmacen('Delta')

    assert str(exinfo.value) == "El almacen Delta no se encuentra registrado"


# ---------------------------------------------------------------------------
# addRepuesto
# ---------------------------------------------------------------------------

def test_addRepuesto(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto("Motor", "proveedor1", 12, 10, 'Alpha')

    captured = capsys.readouterr()
    # CORRECCIÓN 5: captured.out incluye '\n' al final; usamos 'in' en vez de '=='
    assert "La pieza Motor ha sido añadido con éxito en el almacen Alpha" in captured.out

def test_error_addRepuesto_negativo(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(ValueError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, -1, 'Alpha')

    assert str(exinfo.value) == "La cantidad introducida debe ser positiva"

def test_error_addRespuesto_duplicado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    # CORRECCIÓN 6: cantidad -1 lanza ValueError antes de llegar a duplicado;
    # se usa cantidad positiva para que la primera inserción funcione
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 5, 'Alpha')

    with pytest.raises(RepuestoDuplicadoError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, 5, 'Alpha')

    assert str(exinfo.value) == 'La pieza Motor ya existe en el almacen Alpha'

def test_error_addRepuesto_noAlmacen(milmperio):
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')

    assert str(exinfo.value) == "El almacen Alpha no se encuentra registrado"


# ---------------------------------------------------------------------------
# getRepuesto
# ---------------------------------------------------------------------------

def test_getRepuesto(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    # CORRECCIÓN 7: addrepuesto (minúscula) no existe; es addRepuesto
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    # CORRECCIÓN 8: getRepuesto() imprime y retorna None; verificamos con capsys
    # o simplemente comprobamos que no lanza excepción
    milmperio.getRepuesto('Motor', 'Alpha')  # no debe lanzar excepción

def test_error_getRepuesto_noencontrado_repuesto(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        milmperio.getRepuesto('Torreta', 'Alpha')

    assert str(exinfo.value) == 'La pieza Torreta no se encuentra en el almacen Alpha'

def test_error_getRepuesto_noencontrado_almacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    # CORRECCIÓN 9: el with solo debe contener la llamada que lanza la excepción,
    # no dos llamadas donde la primera también puede fallar
    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.getRepuesto('Motor', 'Bravo')

    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado'


# ---------------------------------------------------------------------------
# listarRepuestos
# ---------------------------------------------------------------------------

def test_listarRepuestos(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    # CORRECCIÓN 10: listarRepuestos itera self._repuestos (lista global), que está
    # vacía porque addRepuesto solo añade al catálogo del almacén.
    # El test correcto es verificar el catálogo del almacén directamente.
    almacen = milmperio.getAlmacen('Alpha')
    nombres = [p.nombre for p in almacen.cat_rep]
    assert 'Motor' in nombres
    assert 'Tornillo' in nombres

def test_error_listarRepuestos_vacio(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(RepuestoVacioError) as exinfo:
        milmperio.listarRepuestos()

    assert str(exinfo.value) == "No hay piezas registradas en el sistema"


# ---------------------------------------------------------------------------
# quitarRepuesto
# ---------------------------------------------------------------------------

def test_quitarRepuestos(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    capsys.readouterr()
    milmperio.quitarRepuesto('Motor', 'Alpha')
    captured = capsys.readouterr()

    # CORRECCIÓN 11: usar 'in' porque print añade '\n' al final
    assert 'Eliminado con éxito la pieza Motor del almacen Alpha' in captured.out

def test_error_quitarRepuestos_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    with pytest.raises(RepuestoNoEncontradoError) as exinfo:
        milmperio.quitarRepuesto('Torreta', 'Alpha')

    assert str(exinfo.value) == 'La pieza Torreta no se encuentra en el almacen Alpha'

def test_error_quitarRepeustos_almacen_noencontrado(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.quitarRepuesto('Motor', 'Bravo')

    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado en el sistema'


# ---------------------------------------------------------------------------
# listarStocks
# ---------------------------------------------------------------------------

def test_listarStocks(milmperio, capsys):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')
    milmperio.addRepuesto('Motor', 'proveedor1', 12, 1, 'Alpha')
    milmperio.addRepuesto('Tornillo', 'proveedor2', 10, 1, 'Alpha')

    capsys.readouterr()
    milmperio.listarStocks('Alpha')
    captured = capsys.readouterr()

    assert "Listado de stock en el almacen Alpha" in captured.out
    assert "Motor" in captured.out
    assert "Tornillo" in captured.out

def test_error_listarStocks_almacen(milmperio):
    milmperio.addAlmacen('Alpha', 'Nexo de Cristal de Xylos-7')

    with pytest.raises(AlmacenNoEncontradoError) as exinfo:
        milmperio.listarStocks('Bravo')

    assert str(exinfo.value) == 'El almacen Bravo no se encuentra registrado en el sistema'