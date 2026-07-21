"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_ema.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Verificar el cálculo del indicador EMA utilizando precios
reales obtenidos desde Binance.

RESPONSABILIDADES
-----------------
- Obtener velas mediante OHLCVService.
- Extraer los precios de cierre.
- Calcular EMA 9 y EMA 21.
- Mostrar e interpretar los resultados.

=========================================================
"""

from indicators.ema import EMAIndicator
from services.ohlcv_service import OHLCVService
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


def main():
    """
    Prueba EMA 9 y EMA 21 para BTC/USDT con velas de cinco minutos.
    """
    service = OHLCVService()

    candles = service.get_candles(
        symbol="BTC/USDT",
        timeframe=DEFAULT_TIMEFRAME,
        limit=DEFAULT_CANDLE_LIMIT,
    )

    closing_prices = [candle[4] for candle in candles]  # Guarda el precio de cierre de cada vela en una lista

    current_price = closing_prices[-1]
    ema_9 = EMAIndicator.get_last(closing_prices, period=9)
    ema_21 = EMAIndicator.get_last(closing_prices, period=21)

    print("=" * 55)
    print("PRUEBA DEL INDICADOR EMA")
    print("=" * 55)
    print(f"Velas recibidas : {len(candles)}")
    print(f"Precio actual   : {current_price:.2f}")
    print(f"EMA 9           : {ema_9:.2f}")
    print(f"EMA 21          : {ema_21:.2f}")
    print("-" * 55)

    if ema_9 > ema_21:
        print("Tendencia corta: ALCISTA")
    elif ema_9 < ema_21:
        print("Tendencia corta: BAJISTA")
    else:
        print("Tendencia corta: NEUTRAL")


if __name__ == "__main__":
    main()