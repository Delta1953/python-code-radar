"""
Proyecto: Python Code de Radar
Archivo: test_technical_analyzer.py
Autor: Roberto Günther
Versión: 0.2.0

Objetivo:
    Verificar el funcionamiento integrado de TechnicalAnalyzer.

Responsabilidades:
    - Obtener datos OHLCV del mercado.
    - Ejecutar el análisis técnico.
    - Verificar la estructura del resultado.
    - Validar indicadores, score, tendencia y recomendación.
"""

import pytest

from config.settings import (
    DEFAULT_CANDLE_LIMIT,
    DEFAULT_TIMEFRAME,
)
from services.ohlcv_service import OHLCVService
from strategy.technical_analyzer import TechnicalAnalyzer


TEST_SYMBOL = "BTCUSDT"


@pytest.fixture(scope="module")
def analysis_result() -> dict:
    """
    Ejecuta TechnicalAnalyzer una sola vez para todas
    las pruebas de este archivo.
    """

    ohlcv_service = OHLCVService()
    analyzer = TechnicalAnalyzer(ohlcv_service)

    result = analyzer.analyze(
        symbol=TEST_SYMBOL,
        timeframe=DEFAULT_TIMEFRAME,
        limit=DEFAULT_CANDLE_LIMIT,
    )

    return result


def test_analysis_returns_dictionary(
    analysis_result: dict,
) -> None:
    """
    Verifica que el análisis retorne un diccionario.
    """

    assert isinstance(analysis_result, dict), (
        "TechnicalAnalyzer debe retornar un diccionario."
    )


def test_analysis_is_not_empty(
    analysis_result: dict,
) -> None:
    """
    Verifica que el resultado no esté vacío.
    """

    assert analysis_result, (
        "TechnicalAnalyzer retornó un resultado vacío."
    )


def test_analysis_has_required_fields(
    analysis_result: dict,
) -> None:
    """
    Verifica que el resultado contenga todos los campos
    requeridos por RadarEngine.
    """

    required_fields = {
        "symbol",
        "current_price",
        "ema_9",
        "ema_21",
        "rsi_14",
        "macd",
        "signal",
        "histogram",
        "atr",
        "adx",
        "trend",
        "macd_status",
        "adx_status",
        "score",
        "recommendation",
    }

    missing_fields = required_fields - analysis_result.keys()

    assert not missing_fields, (
        "El análisis no contiene los campos requeridos: "
        f"{sorted(missing_fields)}"
    )


def test_symbol_is_correct(
    analysis_result: dict,
) -> None:
    """
    Verifica que el símbolo analizado sea el solicitado.
    """

    assert analysis_result["symbol"] == TEST_SYMBOL, (
        f"Se esperaba {TEST_SYMBOL}, pero se obtuvo "
        f"{analysis_result['symbol']}."
    )


def test_current_price_is_positive(
    analysis_result: dict,
) -> None:
    """
    Verifica que el precio actual sea mayor que cero.
    """

    assert analysis_result["current_price"] > 0, (
        "El precio actual debe ser mayor que cero."
    )


def test_ema_values_are_positive(
    analysis_result: dict,
) -> None:
    """
    Verifica que las medias móviles sean positivas.
    """

    assert analysis_result["ema_9"] > 0, (
        "EMA 9 debe ser mayor que cero."
    )

    assert analysis_result["ema_21"] > 0, (
        "EMA 21 debe ser mayor que cero."
    )


def test_rsi_is_in_valid_range(
    analysis_result: dict,
) -> None:
    """
    Verifica que RSI esté entre 0 y 100.
    """

    assert 0 <= analysis_result["rsi_14"] <= 100, (
        f"RSI fuera de rango: {analysis_result['rsi_14']}"
    )


def test_atr_is_positive(
    analysis_result: dict,
) -> None:
    """
    Verifica que ATR sea mayor que cero.
    """

    assert analysis_result["atr"] > 0, (
        f"ATR inválido: {analysis_result['atr']}"
    )


def test_adx_is_in_valid_range(
    analysis_result: dict,
) -> None:
    """
    Verifica que ADX esté entre 0 y 100.
    """

    assert 0 <= analysis_result["adx"] <= 100, (
        f"ADX fuera de rango: {analysis_result['adx']}"
    )


def test_score_is_in_valid_range(
    analysis_result: dict,
) -> None:
    """
    Verifica que el score esté entre 0 y 100.
    """

    assert 0 <= analysis_result["score"] <= 100, (
        f"Score fuera de rango: {analysis_result['score']}"
    )


def test_recommendation_is_valid(
    analysis_result: dict,
) -> None:
    """
    Verifica que la recomendación sea una de las admitidas.
    """

    valid_recommendations = {
        "CANDIDATO",
        "VIGILAR",
        "ESPERAR",
        "DEBIL",
        "DESCARTAR",
    }

    assert (
        analysis_result["recommendation"]
        in valid_recommendations
    ), (
        "Recomendación inválida: "
        f"{analysis_result['recommendation']}"
    )


def test_trend_is_valid(
    analysis_result: dict,
) -> None:
    """
    Verifica que la tendencia sea una de las admitidas.
    """

    valid_trends = {
        "ALCISTA",
        "BAJISTA",
        "LATERAL",
    }

    assert analysis_result["trend"] in valid_trends, (
        f"Tendencia inválida: {analysis_result['trend']}"
    )


def test_macd_values_are_numeric(
    analysis_result: dict,
) -> None:
    """
    Verifica que MACD, Signal e Histogram sean valores numéricos.
    """

    macd_fields = {
        "macd",
        "signal",
        "histogram",
    }

    for field in macd_fields:
        assert isinstance(
            analysis_result[field],
            (int, float),
        ), (
            f"El campo {field} debe ser numérico, "
            f"pero se obtuvo {type(analysis_result[field]).__name__}."
        )


def test_status_fields_are_strings(
    analysis_result: dict,
) -> None:
    """
    Verifica que los estados descriptivos sean cadenas de texto.
    """

    assert isinstance(
        analysis_result["macd_status"],
        str,
    )

    assert analysis_result["macd_status"], (
        "macd_status no debe estar vacío."
    )

    assert isinstance(
        analysis_result["adx_status"],
        str,
    )

    assert analysis_result["adx_status"], (
        "adx_status no debe estar vacío."
    )

def test_print_analysis_result(
    analysis_result: dict,
) -> None:
    """
    Muestra el análisis técnico completo de un único símbolo.
    """

    print()
    print("========================================================")
    print("            RESULTADO DEL TECHNICAL ANALYZER")
    print("========================================================")

    print(f"Símbolo         : {analysis_result['symbol']}")
    print(f"Timeframe       : {analysis_result['timeframe']}")
    print(f"Velas           : {analysis_result['candles']}")

    print()
    print("-------------------- PRECIOS --------------------")
    print(f"Precio Actual   : {analysis_result['current_price']:.8f}")

    print()
    print("--------------------- EMA -----------------------")
    print(f"EMA 9           : {analysis_result['ema_9']:.8f}")
    print(f"EMA 21          : {analysis_result['ema_21']:.8f}")

    print()
    print("--------------------- RSI -----------------------")
    print(f"RSI 14          : {analysis_result['rsi_14']:.2f}")
    print(f"Estado RSI      : {analysis_result['rsi_status']}")

    print()
    print("-------------------- MACD -----------------------")
    print(f"MACD            : {analysis_result['macd']:.8f}")
    print(f"Signal          : {analysis_result['signal']:.8f}")
    print(f"Histograma      : {analysis_result['histogram']:.8f}")
    print(f"Estado MACD     : {analysis_result['macd_status']}")

    print()
    print("--------------------- ATR -----------------------")
    print(f"ATR             : {analysis_result['atr']:.8f}")

    print()
    print("--------------------- ADX -----------------------")
    print(f"ADX             : {analysis_result['adx']:.2f}")
    print(f"Estado ADX      : {analysis_result['adx_status']}")

    print()
    print("------------------ RESULTADO --------------------")
    print(f"Tendencia       : {analysis_result['trend']}")
    print(f"Score           : {analysis_result['score']}")
    print(f"Recomendación   : {analysis_result['recommendation']}")

    print("========================================================")

    assert analysis_result 