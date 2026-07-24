"""
Proyecto: Python Code de Radar
Archivo: test_scanner.py

Objetivo:
    Verificar el funcionamiento de MarketScanner.

Responsabilidades:
    - Obtener pares spot activos contra USDT.
    - Obtener los mercados con mayor volumen.
    - Validar la estructura y los valores retornados.
"""

import pytest

from scanners.market_scanner import MarketScanner


TOP_LIMIT = 10


@pytest.fixture(scope="module")
def scanner() -> MarketScanner:
    """
    Crea una única instancia de MarketScanner
    para todas las pruebas del módulo.
    """

    return MarketScanner()


@pytest.fixture(scope="module")
def top_markets(scanner: MarketScanner) -> list:
    """
    Obtiene los mercados con mayor volumen.
    """

    return scanner.get_top_volume(limit=TOP_LIMIT)


@pytest.fixture(scope="module")
def usdt_symbols(scanner: MarketScanner) -> list:
    """
    Obtiene los pares spot activos contra USDT.
    """

    return scanner.get_usdt_spot_symbols()


def test_scanner_instance(scanner: MarketScanner) -> None:
    """
    Verifica que MarketScanner pueda instanciarse.
    """

    assert isinstance(scanner, MarketScanner)


def test_usdt_symbols_returns_list(
    usdt_symbols: list,
) -> None:
    """
    Verifica que get_usdt_spot_symbols retorne una lista.
    """

    assert isinstance(usdt_symbols, list), (
        "get_usdt_spot_symbols debe retornar una lista."
    )


def test_usdt_symbols_is_not_empty(
    usdt_symbols: list,
) -> None:
    """
    Verifica que se encuentren pares spot contra USDT.
    """

    assert usdt_symbols, (
        "No se encontraron pares spot activos contra USDT."
    )


def test_usdt_symbols_are_strings(
    usdt_symbols: list,
) -> None:
    """
    Verifica que todos los símbolos sean cadenas de texto.
    """

    assert all(
        isinstance(symbol, str)
        for symbol in usdt_symbols
    ), "Todos los símbolos deben ser cadenas de texto."


def test_usdt_symbols_end_with_usdt(
    usdt_symbols: list,
) -> None:
    """
    Verifica que todos los símbolos estén expresados contra USDT.
    """

    invalid_symbols = [
        symbol
        for symbol in usdt_symbols
        if not symbol.upper().endswith("USDT")
    ]

    assert not invalid_symbols, (
        "Se encontraron símbolos que no terminan en USDT: "
        f"{invalid_symbols[:10]}"
    )


def test_top_markets_returns_list(
    top_markets: list,
) -> None:
    """
    Verifica que get_top_volume retorne una lista.
    """

    assert isinstance(top_markets, list), (
        "get_top_volume debe retornar una lista."
    )


def test_top_markets_is_not_empty(
    top_markets: list,
) -> None:
    """
    Verifica que se hayan obtenido mercados.
    """

    assert top_markets, (
        "get_top_volume retornó una lista vacía."
    )


def test_top_markets_respects_limit(
    top_markets: list,
) -> None:
    """
    Verifica que la cantidad de resultados no supere el límite.
    """

    assert len(top_markets) <= TOP_LIMIT, (
        f"Se solicitaron como máximo {TOP_LIMIT} mercados, "
        f"pero se obtuvieron {len(top_markets)}."
    )


def test_top_markets_are_dictionaries(
    top_markets: list,
) -> None:
    """
    Verifica que cada mercado sea un diccionario.
    """

    assert all(
        isinstance(market, dict)
        for market in top_markets
    ), "Cada mercado debe estar representado por un diccionario."


def test_top_markets_have_required_fields(
    top_markets: list,
) -> None:
    """
    Verifica que cada mercado contenga los campos requeridos.
    """

    required_fields = {
        "symbol",
        "last",
        "quote_volume",
        "percentage",
    }

    for position, market in enumerate(top_markets, start=1):
        missing_fields = required_fields - market.keys()

        assert not missing_fields, (
            f"El mercado en la posición {position} "
            f"no contiene los campos: {sorted(missing_fields)}"
        )


def test_top_market_symbols_are_strings(
    top_markets: list,
) -> None:
    """
    Verifica que los símbolos de los mercados sean texto.
    """

    for market in top_markets:
        assert isinstance(market["symbol"], str), (
            "El campo symbol debe ser una cadena de texto."
        )

        assert market["symbol"], (
            "El campo symbol no debe estar vacío."
        )


def test_top_market_prices_are_valid(
    top_markets: list,
) -> None:
    """
    Verifica que los precios sean numéricos y positivos.
    """

    for market in top_markets:
        price = market["last"]

        assert isinstance(price, (int, float)), (
            f"El precio de {market['symbol']} debe ser numérico."
        )

        assert price > 0, (
            f"El precio de {market['symbol']} debe ser mayor que cero."
        )


def test_top_market_volumes_are_valid(
    top_markets: list,
) -> None:
    """
    Verifica que los volúmenes sean numéricos y no negativos.
    """

    for market in top_markets:
        volume = market["quote_volume"]

        assert isinstance(volume, (int, float)), (
            f"El volumen de {market['symbol']} debe ser numérico."
        )

        assert volume >= 0, (
            f"El volumen de {market['symbol']} no puede ser negativo."
        )


def test_top_market_percentages_are_numeric(
    top_markets: list,
) -> None:
    """
    Verifica que la variación porcentual sea numérica.
    """

    for market in top_markets:
        percentage = market["percentage"]

        assert isinstance(percentage, (int, float)), (
            "La variación porcentual de "
            f"{market['symbol']} debe ser numérica."
        )


def test_top_markets_are_sorted_by_volume(
    top_markets: list,
) -> None:
    """
    Verifica que los mercados estén ordenados
    de mayor a menor volumen.
    """

    volumes = [
        market["quote_volume"]
        for market in top_markets
    ]

    assert volumes == sorted(volumes, reverse=True), (
        "Los mercados no están ordenados "
        "de mayor a menor volumen."
    )

def test_print_top_markets(
    top_markets: list,
    usdt_symbols: list,
) -> None:
    """
    Muestra los mercados obtenidos para inspección visual.

    Esta prueba conserva la salida informativa
    que tenía el antiguo main().
    """

    print()
    print("============================================")
    print("  PARES SPOT ACTIVOS CONTRA USDT")
    print("============================================")
    print(f"Cantidad encontrada: {len(usdt_symbols)}")
    print()

    for position, market in enumerate(top_markets, start=1):
        symbol = market["symbol"]
        price = market["last"]
        volume = market["quote_volume"]
        variation = market["percentage"]

        print(
            f"{position:>2}. "
            f"{symbol:<15} "
            f"Precio: {price!s:<15} "
            f"Volumen USDT: {volume:>18,.2f} "
            f"Variación: {variation!s}%"
        )

    assert top_markets