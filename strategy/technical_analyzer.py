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
from indicators.macd import MACDIndicator


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

        macd = MACDIndicator.get_last(
            closing_prices,
        )

        macd_status = self._interpret_macd(
            macd_value=macd["macd"],
            signal_value=macd["signal"],
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
            macd_value=macd["macd"],
            signal_value=macd["signal"],
        )

        recommendation = self._determine_recommendation(score)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "candles": len(candles),
            "current_price": current_price,
            "ema_9": ema_9,
            "ema_21": ema_21,
            "rsi_14": rsi_14,
            "macd": macd["macd"],
            "signal": macd["signal"],
            "histogram": macd["histogram"],
            "macd_status": macd_status,
            "trend": trend,
            "rsi_status": rsi_status,
            "score": score,
            "recommendation": recommendation,
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
    def _interpret_macd(
        macd_value,
        signal_value,
    ):
        """
        Interpreta el estado del MACD según su relación con
        la línea de señal y la línea cero.

        Parámetros:
            macd_value (float):
                Último valor de la línea MACD.

            signal_value (float):
                Último valor de la línea de señal.

        Retorna:
            str:
                Estado técnico del MACD.
        """
        if macd_value > signal_value and macd_value > 0:
            return "ALCISTA_CONFIRMADO"

        if macd_value > signal_value and macd_value <= 0:
            return "RECUPERACION_ALCISTA"

        if macd_value < signal_value and macd_value >= 0:
            return "DEBILITAMIENTO_ALCISTA"

        if macd_value < signal_value and macd_value < 0:
            return "BAJISTA_CONFIRMADO"

        return "NEUTRAL"

    @staticmethod
    def _determine_recommendation(score):
        """
        Determina una recomendación técnica según el score.

        La recomendación permite clasificar rápidamente
        los activos analizados por el Radar.

        No representa una orden automática de compra
        o venta.

        Parámetros:
            score (int):
                Puntuación técnica entre cero y cien.

        Retorna:
            str:
                Clasificación técnica del activo.
        """
        if score >= 85:
            return "CANDIDATO_FUERTE"

        if score >= 70:
            return "VIGILAR"

        if score >= 50:
            return "ESPERAR"

        if score >= 30:
            return "DEBIL"

        return "DESCARTAR"

    @staticmethod
    def _calculate_score(
        current_price,
        ema_9,
        ema_21,
        rsi_14,
        macd_value,
        signal_value,
    ):
        """
        Calcula una puntuación técnica entre cero y cien.

        La puntuación considera cuatro grupos de evidencia:

        - Tendencia según EMA 9 y EMA 21.
        - Posición del precio respecto de ambas EMA.
        - Momentum según RSI.
        - Estado combinado del MACD.

        Parámetros:
            current_price (float):
                Último precio de cierre.

            ema_9 (float):
                EMA de 9 períodos.

            ema_21 (float):
                EMA de 21 períodos.

            rsi_14 (float):
                RSI de 14 períodos.

            macd_value (float):
                Último valor de la línea MACD.

            signal_value (float):
                Último valor de la línea de señal.

        Retorna:
            int:
                Puntuación entre 0 y 100.
        """
        score = 50

        # Tendencia según EMA: máximo 12 puntos.
        if ema_9 > ema_21:
            score += 12
        elif ema_9 < ema_21:
            score -= 12

        # Posición del precio: máximo 8 puntos.
        if current_price > ema_9 and current_price > ema_21:
            score += 8
        elif current_price < ema_9 and current_price < ema_21:
            score -= 8

        # Momentum RSI: máximo 8 puntos.
        if 55 <= rsi_14 < 70:
            score += 8
        elif 50 <= rsi_14 < 55:
            score += 4
        elif 45 <= rsi_14 < 50:
            score -= 4
        elif 30 < rsi_14 < 45:
            score -= 8
        elif rsi_14 >= 70:
            score -= 8
        elif rsi_14 <= 30:
            score += 4

        # Momentum MACD: máximo 12 puntos.
        if macd_value > signal_value and macd_value > 0:
            score += 12
        elif macd_value > signal_value and macd_value <= 0:
            score += 6
        elif macd_value < signal_value and macd_value >= 0:
            score -= 6
        elif macd_value < signal_value and macd_value < 0:
            score -= 12

        return max(0, min(100, score))