"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_rsi.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Verificar el cálculo del indicador RSI utilizando precios
reales obtenidos desde Binance.

RESPONSABILIDADES
-----------------
- Obtener velas mediante OHLCVService.
- Extraer precios de cierre.
- Calcular RSI de 14 períodos.
- Mostrar una interpretación básica del resultado.

=========================================================
"""

from indicators.ohlcv_service import OHLCVService
from indicators.rsi import RSIIndicator


def main():
    """
    Prueba el RSI de 14 períodos para BTC/USDT.
    """
    service = OHLCVService()

    candles = service.get_candles(
        symbol="BTC/USDT",
        timeframe="5m",
        limit=100,
    )

    closing_prices = [candle[4] for candle in candles]

    current_price = closing_prices[-1]
    rsi_14 = RSIIndicator.get_last(
        closing_prices,
        period=14,
    )

    print("=" * 55)
    print("PRUEBA DEL INDICADOR RSI")
    print("=" * 55)
    print(f"Velas recibidas : {len(candles)}")
    print(f"Precio actual   : {current_price:.2f}")
    print(f"RSI 14          : {rsi_14:.2f}")
    print("-" * 55)

    if rsi_14 >= 70:
        print("Interpretación  : ZONA DE SOBRECOMPRA")
    elif rsi_14 <= 30:
        print("Interpretación  : ZONA DE SOBREVENTA")
    else:
        print("Interpretación  : ZONA NEUTRAL")


if __name__ == "__main__":
    main()