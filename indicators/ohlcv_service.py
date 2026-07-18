"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : ohlcv_service.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Centralizar la obtención de velas OHLCV para todos los
indicadores técnicos del sistema.

RESPONSABILIDADES
-----------------
- Solicitar velas al BinanceClient.
- Ofrecer una interfaz única para los indicadores.
- Evitar duplicar consultas al exchange.

=========================================================
¿Por qué crear este servicio?

Hoy podría parecer innecesario porque solo llama a BinanceClient, pero más adelante nos permitirá:

almacenar datos en caché para reducir llamadas al exchange;
reutilizar la misma serie de velas entre varios indicadores;
incorporar otros exchanges sin modificar los indicadores;
facilitar las pruebas unitarias simulando datos históricos.

Es una decisión de diseño que hará crecer el proyecto de forma ordenada.
"""

from config.settings import DEFAULT_CANDLE_LIMIT, DEFAULT_TIMEFRAME
from exchange.binance_client import BinanceClient


class OHLCVService:
    """
    Servicio encargado de obtener series OHLCV desde el exchange.
    """

    def __init__(self):
        self.client = BinanceClient()

    def get_candles(self, symbol, timeframe=DEFAULT_TIMEFRAME, limit=DEFAULT_CANDLE_LIMIT):
        """
        Obtiene una serie de velas OHLCV.

        Parámetros:
            symbol (str): Ej. BTC/USDT
            timeframe (str): Intervalo.
            limit (int): Cantidad de velas.

        Retorna:
            list[list]
        """
        return self.client.get_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )