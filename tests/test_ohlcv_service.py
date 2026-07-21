"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_ohlcv_service.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Verificar que OHLCVService pueda obtener múltiples velas
OHLCV desde Binance.

RESPONSABILIDADES
-----------------
- Instanciar OHLCVService.
- Solicitar velas de un símbolo.
- Validar la cantidad recibida.
- Mostrar algunas velas para inspección manual.

=========================================================
"""

from datetime import datetime
from services.ohlcv_service import OHLCVService
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


def main():
    """
    Prueba la obtención de velas mediante OHLCVService.
    """
    service = OHLCVService()

    candles = service.get_candles(
        symbol="BTC/USDT",
        timeframe=DEFAULT_TIMEFRAME,
        limit=DEFAULT_CANDLE_LIMIT,
    )

    print("=" * 70)
    print("PRUEBA DE OHLCV SERVICE")
    print("=" * 70)

    print(f"Cantidad de velas recibidas: {len(candles)}")

    if len(candles) != 10:
        print("ADVERTENCIA: no se recibieron las 10 velas solicitadas.")

    print()

    for candle in candles[:3]:
        timestamp, open_price, high, low, close, volume = candle

        date_time = datetime.fromtimestamp(timestamp / 1000)

        print(
            f"{date_time:%Y-%m-%d %H:%M:%S} | "
            f"O: {open_price} | "
            f"H: {high} | "
            f"L: {low} | "
            f"C: {close} | "
            f"V: {volume}"
        )

    print()
    print("Prueba finalizada correctamente.")


if __name__ == "__main__":
    main()