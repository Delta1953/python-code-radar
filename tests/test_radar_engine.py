"""
Proyecto: Python Code de Radar
Archivo: test_radar_engine.py
Autor: Roberto Günther
Versión: 0.2.0

Objetivo:
    Verificar el funcionamiento integrado de RadarEngine.

Responsabilidades:
    - Crear las dependencias reales del Radar.
    - Ejecutar el proceso completo.
    - Validar la estructura de los resultados.
    - Verificar el orden por score.
    - Mostrar el ranking final por consola.
"""

import pytest

from config.settings import (
    DEFAULT_CANDLE_LIMIT,
    DEFAULT_MARKET_LIMIT,
    DEFAULT_TIMEFRAME,
    DEFAULT_ATR_MULTIPLIER,
    DEFAULT_RISK_REWARD,
)

from strategy.radar_engine import RadarEngine
from scanners.market_scanner import MarketScanner
from services.ohlcv_service import OHLCVService
from strategy.technical_analyzer import TechnicalAnalyzer
from risk.risk_manager import RiskStatus

@pytest.fixture(scope="module")
def radar_results() -> list:
    """
    Ejecuta RadarEngine una sola vez para todas
    las pruebas de este archivo.
    """

    scanner = MarketScanner()
    ohlcv_service = OHLCVService()
    analyzer = TechnicalAnalyzer(ohlcv_service)

    radar = RadarEngine(
        scanner=scanner,
        analyzer=analyzer,
    )

    return radar.run(
        limit=DEFAULT_MARKET_LIMIT,
        timeframe=DEFAULT_TIMEFRAME,
        candle_limit=DEFAULT_CANDLE_LIMIT,
    )


def test_radar_returns_list(
    radar_results: list,
) -> None:
    """
    Verifica que RadarEngine retorne una lista.
    """

    assert isinstance(radar_results, list), (
        "RadarEngine debe retornar una lista."
    )


def test_radar_returns_results(
    radar_results: list,
) -> None:
    """
    Verifica que el Radar genere al menos un resultado.
    """

    assert radar_results, (
        "RadarEngine retornó una lista vacía."
    )


def test_radar_respects_market_limit(
    radar_results: list,
) -> None:
    """
    Verifica que la cantidad de resultados no supere
    el límite configurado.
    """

    assert len(radar_results) <= DEFAULT_MARKET_LIMIT, (
        f"Se esperaban como máximo {DEFAULT_MARKET_LIMIT} "
        f"resultados, pero se obtuvieron {len(radar_results)}."
    )


def test_radar_results_are_dictionaries(
    radar_results: list,
) -> None:
    """
    Verifica que cada resultado sea un diccionario.
    """

    assert all(
        isinstance(result, dict)
        for result in radar_results
    ), "Cada resultado del Radar debe ser un diccionario."


def test_radar_results_have_required_fields(
    radar_results: list,
) -> None:
    """
    Verifica que cada resultado contenga los campos
    principales requeridos.
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
        "score",
        "recommendation",
    }

    for position, result in enumerate(
        radar_results,
        start=1,
    ):
        missing_fields = required_fields - result.keys()

        assert not missing_fields, (
            f"El resultado en la posición {position} "
            f"no contiene los campos: {sorted(missing_fields)}"
        )

def test_radar_results_have_risk_plan(
    radar_results: list,
) -> None:
    """
    Verifica que cada resultado incluya un plan de riesgo.
    """

    for result in radar_results:
        assert "risk_plan" in result, (
            f"El resultado de {result['symbol']} "
            "no contiene risk_plan."
        )

        assert isinstance(
            result["risk_plan"],
            dict,
        ), (
            f"risk_plan debe ser un diccionario "
            f"para {result['symbol']}."
        )

def test_risk_plan_has_required_fields(
    radar_results: list,
) -> None:
    """
    Verifica que el plan de riesgo contenga
    todos los campos principales.
    """

    required_fields = {
        "status",
        "message",
        "trade",
        "position",
        "risk",
    }

    for result in radar_results:
        risk_plan = result["risk_plan"]

        missing_fields = (
            required_fields
            - risk_plan.keys()
        )

        assert not missing_fields, (
            f"El plan de riesgo de {result['symbol']} "
            f"no contiene los campos: "
            f"{sorted(missing_fields)}"
        )

def test_risk_plan_uses_analysis_price_and_atr(
    radar_results: list,
) -> None:
    """
    Verifica que RiskManager utilice el precio
    y el ATR calculados por TechnicalAnalyzer.
    """

    for result in radar_results:
        risk_plan = result["risk_plan"]

        if risk_plan["status"] not in {
            RiskStatus.OK,
            RiskStatus.CAPITAL_LIMITED,
        }:
            continue

        trade = risk_plan["trade"]

        assert trade["entry_price"] == pytest.approx(
            result["current_price"]
        )

        assert trade["stop_distance"] == pytest.approx(
            result["atr"] * DEFAULT_ATR_MULTIPLIER
        )

def test_risk_plan_stop_loss_and_take_profit(
    radar_results: list,
) -> None:
    """
    Verifica que Stop Loss y Take Profit
    sean consistentes con las fórmulas del
    RiskManager.
    """

    for result in radar_results:
        risk_plan = result["risk_plan"]

        if risk_plan["status"] not in {
            RiskStatus.OK,
            RiskStatus.CAPITAL_LIMITED,
        }:
            continue

        trade = risk_plan["trade"]

        expected_stop_loss = (
            trade["entry_price"]
            - trade["stop_distance"]
        )

        expected_take_profit = (
            trade["entry_price"]
            + (
                trade["stop_distance"]
                * DEFAULT_RISK_REWARD
            )
        )

        assert trade["stop_loss"] == pytest.approx(
            expected_stop_loss
        )

        assert trade["take_profit"] == pytest.approx(
            expected_take_profit
        )

def test_radar_is_sorted_by_score(
    radar_results: list,
) -> None:
    """
    Verifica que los resultados estén ordenados
    de mayor a menor score.
    """

    scores = [
        result["score"]
        for result in radar_results
    ]

    assert scores == sorted(scores, reverse=True), (
        "Los resultados no están ordenados "
        "de mayor a menor score."
    )


def test_radar_scores_are_in_valid_range(
    radar_results: list,
) -> None:
    """
    Verifica que todos los scores estén entre 0 y 100.
    """

    for result in radar_results:
        assert 0 <= result["score"] <= 100, (
            f"Score inválido para {result['symbol']}: "
            f"{result['score']}"
        )


def test_radar_recommendations_are_valid(
    radar_results: list,
) -> None:
    """
    Verifica que todas las recomendaciones sean válidas.
    """

    valid_recommendations = {
        "CANDIDATO",
        "VIGILAR",
        "ESPERAR",
        "DEBIL",
        "DESCARTAR",
    }

    for result in radar_results:
        assert (
            result["recommendation"]
            in valid_recommendations
        ), (
            f"Recomendación inválida para "
            f"{result['symbol']}: "
            f"{result['recommendation']}"
        )


def test_radar_trends_are_valid(
    radar_results: list,
) -> None:
    """
    Verifica que todas las tendencias sean válidas.
    """

    valid_trends = {
        "ALCISTA",
        "BAJISTA",
        "LATERAL",
    }

    for result in radar_results:
        assert result["trend"] in valid_trends, (
            f"Tendencia inválida para "
            f"{result['symbol']}: "
            f"{result['trend']}"
        )


def test_radar_rsi_values_are_valid(
    radar_results: list,
) -> None:
    """
    Verifica que todos los valores RSI estén
    entre 0 y 100.
    """

    for result in radar_results:
        assert 0 <= result["rsi_14"] <= 100, (
            f"RSI inválido para {result['symbol']}: "
            f"{result['rsi_14']}"
        )


def test_radar_adx_values_are_valid(
    radar_results: list,
) -> None:
    """
    Verifica que todos los valores ADX estén
    entre 0 y 100.
    """

    for result in radar_results:
        assert 0 <= result["adx"] <= 100, (
            f"ADX inválido para {result['symbol']}: "
            f"{result['adx']}"
        )


def test_radar_prices_and_atr_are_positive(
    radar_results: list,
) -> None:
    """
    Verifica que el precio actual y ATR sean positivos.
    """

    for result in radar_results:
        assert result["current_price"] > 0, (
            f"Precio inválido para {result['symbol']}."
        )

        assert result["atr"] > 0, (
            f"ATR inválido para {result['symbol']}."
        )


def test_print_radar_results(
    radar_results: list,
) -> None:
    """
    Muestra el ranking final generado por RadarEngine.
    """

    print()
    print("=" * 122)
    print(" " * 47 + "RANKING FINAL DEL RADAR")
    print("=" * 122)

    print(
        f"Mercados seleccionados: {len(radar_results)}"
    )
    print(
        f"Timeframe: {DEFAULT_TIMEFRAME}"
    )
    print(
        f"Velas por mercado: {DEFAULT_CANDLE_LIMIT}"
    )
    print()

    header = (
        f"{'POS':>3}  "
        f"{'SÍMBOLO':<15} "
        f"{'PRECIO':>16} "
        f"{'SCORE':>8} "
        f"{'TENDENCIA':<12} "
        f"{'RSI':>8} "
        f"{'ADX':>8} "
        f"{'RECOMENDACIÓN':<16}"
    )

    print(header)
    print("-" * 122)

    for position, result in enumerate(
        radar_results,
        start=1,
    ):
        print(
            f"{position:>3}  "
            f"{result['symbol']:<15} "
            f"{result['current_price']:>16.8f} "
            f"{result['score']:>8.2f} "
            f"{result['trend']:<12} "
            f"{result['rsi_14']:>8.2f} "
            f"{result['adx']:>8.2f} "
            f"{result['recommendation']:<16}"
        )

    print("-" * 122)
    print("Resultados ordenados de mayor a menor score.")
    print("=" * 122)

    assert radar_results