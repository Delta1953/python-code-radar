"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : ema.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Calcular la Media Móvil Exponencial, EMA, a partir de una
serie de precios de cierre.
La EMA es una media móvil exponencial. Da más peso a los 
precios recientes que una media simple y nos ayudará a detectar tendencia y momentum.

RESPONSABILIDADES
-----------------
- Validar los datos recibidos.
- Calcular una serie completa de valores EMA.
- Devolver el último valor EMA cuando sea necesario.

DEPENDENCIAS
------------
- Ninguna dependencia externa.

=========================================================
"""


class EMAIndicator:
    """
    Calcula la Media Móvil Exponencial de una serie de precios.
    """

    @staticmethod
    def calculate(prices, period):
        """
        Calcula una serie EMA.

        Parámetros:
            prices (list[float]): Serie de precios.
            period (int): Cantidad de períodos de la EMA.

        Retorna:
            list[float]: Serie EMA. El primer valor corresponde
            a una media simple de los primeros períodos.

        Excepciones:
            ValueError: Si el período no es válido o faltan datos.
        """
        if period <= 0:
            raise ValueError("El período debe ser mayor que cero.")

        if len(prices) < period:
            raise ValueError(
                "La cantidad de precios debe ser mayor o igual al período."
            )

        multiplier = 2 / (period + 1)

        initial_average = sum(prices[:period]) / period
        ema_values = [initial_average]

        for price in prices[period:]:
            previous_ema = ema_values[-1]

            current_ema = (
                price * multiplier
                + previous_ema * (1 - multiplier)
            )

            ema_values.append(current_ema)

        return ema_values

    @staticmethod
    def get_last(prices, period):
        """
        Obtiene solamente el último valor EMA.

        Parámetros:
            prices (list[float]): Serie de precios.
            period (int): Cantidad de períodos.

        Retorna:
            float: Último valor EMA calculado.
        """
        ema_values = EMAIndicator.calculate(prices, period)

        return ema_values[-1]