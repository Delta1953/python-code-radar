"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : rsi.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Calcular el Índice de Fuerza Relativa, RSI, a partir de
una serie de precios de cierre.
El RSI mide la fuerza relativa de los movimientos alcistas y bajistas. 
En el Radar lo usaremos como una pieza del score, no como señal aislada.

RESPONSABILIDADES
-----------------
- Validar los datos recibidos.
- Calcular ganancias y pérdidas entre cierres consecutivos.
- Calcular el RSI mediante el método suavizado de Wilder.
- Devolver la serie completa o el último valor calculado.

DEPENDENCIAS
------------
- Ninguna dependencia externa.

El RSI se interpreta normalmente así:
RSI >= 70  → mercado extendido al alza
RSI <= 30  → mercado extendido a la baja
30 < RSI < 70 → zona intermedia

Pero una advertencia importante: sobrecompra no significa venta automática 
y sobreventa no significa compra automática. En una tendencia fuerte, el RSI 
puede permanecer bastante tiempo en zonas extremas.

Después de probarlo, el próximo paso será combinar EMA 9, EMA 21 y RSI 14 en un 
único análisis para empezar a construir el primer score del Radar.
=========================================================
"""


class RSIIndicator:
    """
    Calcula el Índice de Fuerza Relativa de una serie de precios.
    """

    @staticmethod
    def calculate(prices, period=14):
        """
        Calcula una serie de valores RSI.

        Parámetros:
            prices (list[float]): Serie de precios de cierre.
            period (int): Cantidad de períodos del RSI.

        Retorna:
            list[float]: Serie de valores RSI calculados.

        Excepciones:
            ValueError: Si el período no es válido o faltan datos.
        """
        if period <= 0:
            raise ValueError("El período debe ser mayor que cero.")

        if len(prices) <= period:
            raise ValueError(
                "La cantidad de precios debe ser mayor que el período."
            )

        gains = []
        losses = []

        for index in range(1, len(prices)):
            change = prices[index] - prices[index - 1]

            gains.append(max(change, 0))
            losses.append(max(-change, 0))

        average_gain = sum(gains[:period]) / period
        average_loss = sum(losses[:period]) / period

        rsi_values = [
            RSIIndicator._calculate_rsi(
                average_gain,
                average_loss,
            )
        ]

        for index in range(period, len(gains)):
            average_gain = (
                (average_gain * (period - 1)) + gains[index]
            ) / period

            average_loss = (
                (average_loss * (period - 1)) + losses[index]
            ) / period

            rsi_values.append(
                RSIIndicator._calculate_rsi(
                    average_gain,
                    average_loss,
                )
            )

        return rsi_values

    @staticmethod
    def _calculate_rsi(average_gain, average_loss):
        """
        Calcula un valor RSI a partir de la ganancia y pérdida medias.

        Parámetros:
            average_gain (float): Ganancia promedio.
            average_loss (float): Pérdida promedio.

        Retorna:
            float: Valor RSI entre 0 y 100.
        """
        if average_loss == 0:
            return 100.0

        relative_strength = average_gain / average_loss

        return 100 - (100 / (1 + relative_strength))

    @staticmethod
    def get_last(prices, period=14):
        """
        Obtiene el último valor RSI.

        Parámetros:
            prices (list[float]): Serie de precios de cierre.
            period (int): Cantidad de períodos.

        Retorna:
            float: Último valor RSI calculado.
        """
        return RSIIndicator.calculate(prices, period)[-1]