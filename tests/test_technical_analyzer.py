"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_technical_analyzer.py
Autor    : Roberto Günther
Versión  : 0.6
=========================================================

OBJETIVO
--------
Verificar el funcionamiento del analizador técnico
del proyecto.

RESPONSABILIDADES
-----------------
- Crear el cliente de Binance.
- Crear el servicio de velas OHLCV.
- Analizar BTC/USDT.
- Mostrar los indicadores calculados.
- Mostrar tendencia, estados técnicos y recomendación.
- Validar que el score esté entre 0 y 100.

=========================================================
"""

from services.ohlcv_service import OHLCVService
from strategy.technical_analyzer import TechnicalAnalyzer
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


def main():
    """
    Ejecuta una prueba de análisis técnico para BTC/USDT.
    """
    TEST_SYMBOL = "BTC/USDT"
    TEST_TIMEFRAME = DEFAULT_TIMEFRAME
    TEST_LIMIT = DEFAULT_CANDLE_LIMIT

    ohlcv_service = OHLCVService()

    analyzer = TechnicalAnalyzer(
        ohlcv_service,
    )

    result = analyzer.analyze(
        symbol=TEST_SYMBOL,
        timeframe=TEST_TIMEFRAME,
        limit=TEST_LIMIT,
    )

    print("=" * 60)
    print("PRUEBA DEL ANALIZADOR TÉCNICO")
    print("=" * 60)

    print(f"Símbolo        : {result['symbol']}")
    print(f"Temporalidad   : {result['timeframe']}")
    print(f"Velas          : {result['candles']}")

    print("-" * 60)
    print("ANÁLISIS DE TENDENCIA")
    print("-" * 60)

    print(f"Precio actual  : {result['current_price']:.2f}")
    print(f"EMA 9          : {result['ema_9']:.2f}")
    print(f"EMA 21         : {result['ema_21']:.2f}")
    print(f"Tendencia      : {result['trend']}")

    print(f"ADX 14         : {result['adx']:.2f}")
    print(f"Estado ADX     : {result['adx_status']}")

    print("-" * 60)
    print("MOMENTUM")
    print("-" * 60)

    print(f"RSI 14         : {result['rsi_14']:.2f}")
    print(f"Estado RSI     : {result['rsi_status']}")

    print(f"MACD           : {result['macd']:.4f}")
    print(f"Señal MACD     : {result['signal']:.4f}")
    print(f"Histograma     : {result['histogram']:.4f}")
    print(f"Estado MACD    : {result['macd_status']}")

    print("-" * 60)
    print("VOLATILIDAD")
    print("-" * 60)

    print(f"ATR 14         : {result['atr']:.4f}")

    print("-" * 60)
    print("RESULTADO")
    print("-" * 60)

    print(f"Score técnico  : {result['score']}/100")
    print(f"Recomendación  : {result['recommendation']}")

    print("=" * 60)

    print(
        "El score representa la alineación de las condiciones "
        "técnicas definidas por el Radar."
    )
    print(
        "No representa una probabilidad de éxito ni una orden "
        "automática de trading."
    )

    if not 0 <= result["score"] <= 100:
        raise ValueError(
            "El score está fuera del rango permitido."
        )

    if not 0 <= result["adx"] <= 100:
        raise ValueError(
            "El ADX está fuera del rango permitido."
        )

    print("-" * 60)
    print("Prueba finalizada correctamente.")


if __name__ == "__main__":
    main()