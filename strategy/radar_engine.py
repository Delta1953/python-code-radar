"""
Proyecto: Python Code de Radar
Archivo: radar_engine.py
Autor: Roberto Günther
Versión: 0.3.0

Objetivo:
    Coordinar el scanner, el analizador técnico
    y el gestor de riesgo.
"""

from config.settings import (
    DEFAULT_ATR_MULTIPLIER,
    DEFAULT_CANDLE_LIMIT,
    DEFAULT_CAPITAL,
    DEFAULT_MARKET_LIMIT,
    DEFAULT_RISK_PERCENT,
    DEFAULT_RISK_REWARD,
    DEFAULT_TIMEFRAME,
)
from risk.risk_manager import RiskManager


class RadarEngine:
    """
    Coordina la selección de mercados, el análisis técnico
    y la generación del plan de riesgo.
    """

    def __init__(
        self,
        scanner,
        analyzer,
        risk_manager=RiskManager,
    ) -> None:
        """
        Inicializa RadarEngine con sus dependencias.
        """

        self.scanner = scanner
        self.analyzer = analyzer
        self.risk_manager = risk_manager

    def run(
        self,
        limit=DEFAULT_MARKET_LIMIT,
        timeframe=DEFAULT_TIMEFRAME,
        candle_limit=DEFAULT_CANDLE_LIMIT,
        capital=DEFAULT_CAPITAL,
        risk_percent=DEFAULT_RISK_PERCENT,
        risk_reward=DEFAULT_RISK_REWARD,
        atr_multiplier=DEFAULT_ATR_MULTIPLIER,
    ) -> list:
        """
        Ejecuta el proceso completo del Radar.

        Retorna:
            Lista de resultados ordenados por score
            de mayor a menor.
        """

        markets = self.scanner.get_top_volume(
            limit=limit,
        )

        results = []

        for market in markets:
            symbol = market["symbol"]

            result = self.analyzer.analyze(
                symbol=symbol,
                timeframe=timeframe,
                limit=candle_limit,
            )

            risk_plan = self.risk_manager.calculate(
                current_price=result["current_price"],
                atr=result["atr"],
                capital=capital,
                risk_percent=risk_percent,
                risk_reward=risk_reward,
                atr_multiplier=atr_multiplier,
            )

            result["risk_plan"] = risk_plan

            results.append(result)

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results