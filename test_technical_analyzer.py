"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : test_technical_analyzer.py
Autor    : Roberto Günther
Versión  : 0.5
=========================================================

OBJETIVO
--------
Verificar el funcionamiento del primer analizador técnico
del proyecto.

RESPONSABILIDADES
-----------------
- Analizar BTC/USDT.
- Mostrar los indicadores calculados.
- Mostrar tendencia, estado del RSI y score.
- Validar que el score esté entre 0 y 100.

=========================================================
"""

from strategy.technical_analyzer import TechnicalAnalyzer


def main():
    """
    Ejecuta una prueba de análisis técnico para BTC/USDT.
    """
    analyzer = TechnicalAnalyzer()

    result = analyzer.analyze(
        symbol="BTC/USDT",
        timeframe="5m",
        limit=100,
    )

    print("=" * 60)
    print("PRUEBA DEL ANALIZADOR TÉCNICO")
    print("=" * 60)
    print(f"Símbolo        : {result['symbol']}")
    print(f"Temporalidad   : {result['timeframe']}")
    print(f"Velas          : {result['candles']}")
    print(f"Precio actual  : {result['current_price']:.2f}")
    print(f"EMA 9          : {result['ema_9']:.2f}")
    print(f"EMA 21         : {result['ema_21']:.2f}")
    print(f"RSI 14         : {result['rsi_14']:.2f}")
    print(f"Tendencia      : {result['trend']}")
    print(f"Estado RSI     : {result['rsi_status']}")
    print(f"Score técnico  : {result['score']}/100")
    print("-" * 60)
    print("Este score es deliberadamente simple y educativo")
    print("No representa todavía una probabilidad de éxito ni una recomendación de trading")
    print("Significa que varias condiciones técnicas definidas por nosotros están alineadas. " )
    print("No significa que exista un 85 % de probabilidad de que el precio suba")

    if not 0 <= result["score"] <= 100:
        raise ValueError("El score está fuera del rango permitido.")

    print("Prueba finalizada correctamente.")


if __name__ == "__main__":
    main()