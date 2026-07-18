"""
Proyecto: Python Code de Radar
Archivo: radar_engine.py
Autor: Roberto Günther
Versión: 0.1.0

Objetivo:
    Coordinar el proceso completo de generación del Radar de mercados.

Responsabilidades:
    - Obtener los mercados seleccionados por MarketScanner.
    - Analizar cada mercado mediante TechnicalAnalyzer.
    - Reunir los resultados de los análisis.
    - Ordenar los resultados por score de mayor a menor.
    - Devolver la lista completa ordenada.

Dependencias:
    - MarketScanner
    - TechnicalAnalyzer
"""
from config.settings import (
    DEFAULT_CANDLE_LIMIT,
    DEFAULT_MARKET_LIMIT,
    DEFAULT_TIMEFRAME,
)

class RadarEngine:
    """
    Coordina la selección de mercados y su análisis técnico.

    No calcula indicadores ni se conecta directamente con Binance.
    Su responsabilidad es coordinar el scanner y el analizador.
    """

    def __init__(self, scanner, analyzer):
        """
        Inicializa el motor del Radar.

        Parámetros:
            scanner:
                Componente encargado de seleccionar los mercados.

            analyzer:
                Componente encargado de analizar cada mercado.

        Retorna:
            None
        """
        self.scanner = scanner
        self.analyzer = analyzer

    def run(self, limit=DEFAULT_MARKET_LIMIT, timeframe=DEFAULT_TIMEFRAME, candle_limit=DEFAULT_CANDLE_LIMIT):
        """
        Ejecuta el proceso completo de generación del Radar.

        Parámetros:
            limit (int):
                Cantidad de mercados que debe seleccionar el scanner.

            timeframe (str):
                Temporalidad de las velas utilizadas para el análisis.

            candle_limit (int):
                Cantidad de velas solicitadas para cada mercado.

        Retorna:
            list[dict]:
                Lista completa de resultados ordenados por score
                de mayor a menor.
        """
        markets = self.scanner.get_top_volume(limit=limit)

        results = []

        for market in markets:
            symbol = market["symbol"]

            result = self.analyzer.analyze(
                symbol=symbol,
                timeframe=timeframe,
                limit=candle_limit,
            )

            results.append(result)

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results