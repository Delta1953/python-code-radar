"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : settings.py
Autor    : Roberto Günther
Versión  : 0.1
=========================================================

OBJETIVO
--------
Centralizar los parámetros generales de configuración
utilizados por los distintos módulos del Radar.
=========================================================
"""
# ==========================================================
# Radar
# ==========================================================
DEFAULT_TIMEFRAME = "15m"
DEFAULT_CANDLE_LIMIT = 100
DEFAULT_MARKET_LIMIT = 10

# ==========================================================
# Risk Manager
# ==========================================================
DEFAULT_CAPITAL = 10_000.00
DEFAULT_RISK_PERCENT = 1.0
DEFAULT_RISK_REWARD = 2.0
DEFAULT_ATR_MULTIPLIER = 2.0