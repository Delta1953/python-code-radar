"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : technical_analyzer.py
Autor    : Roberto Günther
Versión  : 0.5
=========================================================

OBJETIVO
--------
Combinar indicadores técnicos básicos para generar un
primer análisis estructurado de un activo.

RESPONSABILIDADES
-----------------
- Obtener velas OHLCV.
- Extraer precios de cierre.
- Calcular EMA 9, EMA 21 y RSI 14.
- Determinar el sesgo de tendencia.
- Calcular una puntuación técnica inicial.

DEPENDENCIAS
------------
- OHLCVService
- EMAIndicator
- RSIIndicator

=========================================================
"""

from config.settings import DEFAULT_CANDLE_LIMIT, DEFAULT_TIMEFRAME
from indicators.ema import EMAIndicator
from indicators.ohlcv_service import OHLCVService
from indicators.rsi import RSIIndicator


class TechnicalAnalyzer:
    """
    Combina indicadores técnicos para analizar un símbolo.
    """

    def __init__(self, ohlcv_service: OHLCVService):
        """
        Inicializa el analizador técnico.

        Parámetros:
            ohlcv_service (OHLCVService):
                Servicio utilizado para obtener las velas OHLCV.

        Retorna:
            None
        """
        self.ohlcv_service = ohlcv_service

    def analyze(
        self,
        symbol,
        timeframe=DEFAULT_TIMEFRAME,
        limit=DEFAULT_CANDLE_LIMIT,
    ):
        """
        Analiza un símbolo mediante EMA 9, EMA 21 y RSI 14.

        Parámetros:
            symbol (str):
                Símbolo del mercado, por ejemplo BTC/USDT.

            timeframe (str):
                Intervalo temporal de las velas.

            limit (int):
                Cantidad de velas a solicitar.

        Retorna:
            dict:
                Resultado estructurado del análisis.

        Excepciones:
            ValueError:
                Si no se reciben suficientes velas.
        """
        candles = self.ohlcv_service.get_candles(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )

        if len(candles) < 21:
            raise ValueError(
                "Se necesitan al menos 21 velas para realizar el análisis."
            )

        closing_prices = [candle[4] for candle in candles]

        current_price = closing_prices[-1]

        ema_9 = EMAIndicator.get_last(
            closing_prices,
            period=9,
        )

        ema_21 = EMAIndicator.get_last(
            closing_prices,
            period=21,
        )

        rsi_14 = RSIIndicator.get_last(
            closing_prices,
            period=14,
        )

        trend = self._determine_trend(
            ema_9,
            ema_21,
        )

        rsi_status = self._interpret_rsi(
            rsi_14,
        )

        score = self._calculate_score(
            current_price=current_price,
            ema_9=ema_9,
            ema_21=ema_21,
            rsi_14=rsi_14,
        )

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "candles": len(candles),
            "current_price": current_price,
            "ema_9": ema_9,
            "ema_21": ema_21,
            "rsi_14": rsi_14,
            "trend": trend,
            "rsi_status": rsi_status,
            "score": score,
        }

    @staticmethod
    def _determine_trend(ema_9, ema_21):
        """
        Determina la tendencia según la posición de las EMA.

        Parámetros:
            ema_9 (float):
                EMA corta.

            ema_21 (float):
                EMA larga.

        Retorna:
            str:
                ALCISTA, BAJISTA o NEUTRAL.
        """
        if ema_9 > ema_21:
            return "ALCISTA"

        if ema_9 < ema_21:
            return "BAJISTA"

        return "NEUTRAL"

    @staticmethod
    def _interpret_rsi(rsi_14):
        """
        Interpreta el RSI en zonas básicas.

        Parámetros:
            rsi_14 (float):
                Valor del RSI.

        Retorna:
            str:
                SOBRECOMPRA, SOBREVENTA o NEUTRAL.
        """
        if rsi_14 >= 70:
            return "SOBRECOMPRA"

        if rsi_14 <= 30:
            return "SOBREVENTA"

        return "NEUTRAL"

    @staticmethod
    def _calculate_score(
        current_price,
        ema_9,
        ema_21,
        rsi_14,
    ):
        """
        Calcula una puntuación técnica inicial de cero a cien.

        La puntuación considera:
        - Posición relativa de EMA 9 y EMA 21.
        - Posición del precio respecto de las EMA.
        - Zona del RSI.

        Parámetros:
            current_price (float):
                Último precio de cierre.

            ema_9 (float):
                EMA de 9 períodos.

            ema_21 (float):
                EMA de 21 períodos.

            rsi_14 (float):
                RSI de 14 períodos.

        Retorna:
            int:
                Puntuación entre 0 y 100.
        """
        score = 50

        if ema_9 > ema_21:
            score += 15
        elif ema_9 < ema_21:
            score -= 15

        if current_price > ema_9:
            score += 10
        elif current_price < ema_9:
            score -= 10

        if current_price > ema_21:
            score += 10
        elif current_price < ema_21:
            score -= 10

        if 50 <= rsi_14 < 70:
            score += 15
        elif 30 < rsi_14 < 50:
            score -= 5
        elif rsi_14 >= 70:
            score -= 10
        elif rsi_14 <= 30:
            score += 5

        return max(0, min(100, score))