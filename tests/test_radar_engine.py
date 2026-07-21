"""
Proyecto: Python Code de Radar
Archivo: test_radar_engine.py
Autor: Roberto Günther
Versión: 0.1.0

Objetivo:
    Verificar la integración entre MarketScanner,
    TechnicalAnalyzer y RadarEngine.

Responsabilidades:
    - Crear las dependencias necesarias.
    - Ejecutar el Radar.
    - Mostrar el ranking ordenado.
    - Comprobar que los resultados estén ordenados
      por score de mayor a menor.

Dependencias:
    - BinanceClient
    - MarketScanner
    - OHLCVService
    - TechnicalAnalyzer
    - RadarEngine
"""

from scanners.market_scanner import MarketScanner
from services.ohlcv_service import OHLCVService
from strategy.technical_analyzer import TechnicalAnalyzer
from strategy.radar_engine import RadarEngine
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


def main():
    """
    Ejecuta la prueba de integración de RadarEngine.

    Parámetros:
        None

    Retorna:
        None
    """

    scanner = MarketScanner()

    ohlcv_service = OHLCVService()

    analyzer = TechnicalAnalyzer(ohlcv_service)

    radar = RadarEngine(
        scanner=scanner,
        analyzer=analyzer
    )

    results = radar.run(
        limit=5,
        timeframe=DEFAULT_TIMEFRAME,
        candle_limit=DEFAULT_CANDLE_LIMIT
    )

    print("\nRADAR DE MERCADOS")

    print(
        f"{'N°':<2} | "
        f"{'SÍMBOLO':<12} | "
        f"{'SCORE':>5} | "
        f"{'RECOMENDACIÓN':<16} | "
        f"{'TENDENCIA':<9} | "
        f"{'RSI':>6} | "
        f"{'ATR':>10} | "
        f"{'PRECIO':>10} | "
        f"{'MACD':>8} | "
        f"{'SIGNAL':>8} | "
        f"{'HIST':>8} | "
        f"{'ADX':>6} | "
        f"{'ESTADO ADX':<22} | "
        f"{'ESTADO MACD':<22}"
    )

    print("-" * 170)

    for position, result in enumerate(results, start=1):
        print(
            f"{position:02d} | "
            f"{result['symbol']:<12} | "
            f"{result['score']:>5} | "
            f"{result['recommendation']:<16} | "
            f"{result['trend']:<9} | "
            f"{result['rsi_14']:>6.2f} | "
            f"{result['atr']:>9.4f} | "
            f"{result['current_price']:>10.4f} | "
            f"{result['macd']:>8.4f} | "
            f"{result['signal']:>8.4f} | "
            f"{result['histogram']:>8.4f} | "
            f"{result['adx']:>6.2f} | "
            f"{result['adx_status']:<22} | "
            f"{result['macd_status']:<22}"
        )

    scores = [result["score"] for result in results]

    assert scores == sorted(scores, reverse=True), (
        "Los resultados del Radar no están ordenados "
        "por score de mayor a menor."
    )

    print("\nPrueba completada correctamente.")
    print("Los resultados están ordenados por score.")


if __name__ == "__main__":
    main()