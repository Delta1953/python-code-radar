"""
ATR (Average True Range)

Implementación basada en el método de Wilder.

Entrada:
    candles = [
        [timestamp, open, high, low, close, volume],
        ...
    ]
"""

class ATRIndicator:

    @staticmethod
    def calculate(candles, period=14):
        """
        Devuelve una lista con los valores de ATR.
        """

        if len(candles) < period + 1:
            raise ValueError(
                f"Se requieren al menos {period + 1} velas para calcular ATR."
            )

        true_ranges = []

        for i in range(1, len(candles)):
            high = candles[i][2]
            low = candles[i][3]
            previous_close = candles[i - 1][4]

            tr = max(
                high - low,
                abs(high - previous_close),
                abs(low - previous_close),
            )

            true_ranges.append(tr)

        atr_values = []

        # Primer ATR = promedio simple
        first_atr = sum(true_ranges[:period]) / period
        atr_values.append(first_atr)

        # Wilder smoothing
        previous_atr = first_atr

        for tr in true_ranges[period:]:
            atr = ((previous_atr * (period - 1)) + tr) / period
            atr_values.append(atr)
            previous_atr = atr

        return atr_values

    @staticmethod
    def get_last(candles, period=14):
        """
        Devuelve el último valor de ATR.
        """

        atr = ATRIndicator.calculate(
            candles,
            period=period,
        )

        return atr[-1]