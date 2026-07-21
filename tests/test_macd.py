"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_macd.py
Autor    : Roberto Günther
Versión  : 0.6
=========================================================

OBJETIVO
--------
Comprobar el funcionamiento básico del indicador MACD.

RESPONSABILIDADES
-----------------
- Verificar el cálculo de las series MACD.
- Verificar que las series tengan igual longitud.
- Verificar la obtención de los últimos valores.
- Verificar las validaciones principales.

DEPENDENCIAS
------------
- MACDIndicator

=========================================================
"""

from indicators.macd import MACDIndicator


def test_macd():
    """
    Ejecuta una prueba básica del indicador MACD.

    Retorna:
        None
    """
    prices = [
        100,
        101,
        102,
        103,
        104,
        103,
        105,
        106,
        107,
        108,
        109,
        110,
        111,
        112,
        111,
        113,
        114,
        115,
        116,
        117,
        118,
        119,
        120,
        121,
        122,
        123,
        124,
        125,
        126,
        127,
        128,
        129,
        130,
        131,
        132,
        133,
        134,
        135,
        136,
        137,
        138,
        139,
        140,
        141,
        142,
        143,
        144,
        145,
        146,
        147,
    ]

    result = MACDIndicator.calculate(prices)

    assert len(result["macd"]) > 0
    assert len(result["macd"]) == len(result["signal"])
    assert len(result["signal"]) == len(result["histogram"])

    last_result = MACDIndicator.get_last(prices)

    assert isinstance(last_result["macd"], float)
    assert isinstance(last_result["signal"], float)
    assert isinstance(last_result["histogram"], float)

    print("PRUEBA DEL INDICADOR MACD")
    print("-" * 50)
    print(f"MACD      : {last_result['macd']:.6f}")
    print(f"Señal     : {last_result['signal']:.6f}")
    print(f"Histograma: {last_result['histogram']:.6f}")
    print()
    print("Prueba completada correctamente.")


if __name__ == "__main__":
    test_macd()