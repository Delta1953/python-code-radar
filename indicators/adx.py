"""
Indicador Average Directional Index (ADX).

Calcula la fuerza de una tendencia utilizando
el método de suavizado desarrollado por Welles Wilder.
"""

from __future__ import annotations


class ADXIndicator:
    """
    Calcula el indicador ADX a partir de velas OHLCV.

    Formato esperado de cada vela:

    [
        timestamp,
        open,
        high,
        low,
        close,
        volume,
    ]
    """

    @staticmethod
    def calculate(
        candles: list[list[float]],
        period: int = 14,
    ) -> list[float]:
        """
        Calcula la serie de valores ADX.

        Parámetros:
            candles:
                Lista de velas OHLCV.

            period:
                Período utilizado para el cálculo.
                El valor estándar es 14.

        Retorna:
            Lista de valores ADX.

        Lanza:
            ValueError:
                Cuando los parámetros o la cantidad
                de velas no son válidos.
        """

        if period <= 0:
            raise ValueError(
                "El período del ADX debe ser mayor que cero."
            )

        minimum_candles = period * 2

        if len(candles) < minimum_candles:
            raise ValueError(
                "No hay suficientes velas para calcular el ADX. "
                f"Se requieren al menos {minimum_candles}."
            )

        true_ranges = []
        plus_dm_values = []
        minus_dm_values = []

        # Calculamos True Range, +DM y -DM.
        for index in range(1, len(candles)):
            current_high = float(candles[index][2])
            current_low = float(candles[index][3])

            previous_high = float(candles[index - 1][2])
            previous_low = float(candles[index - 1][3])
            previous_close = float(candles[index - 1][4])

            true_range = max(
                current_high - current_low,
                abs(current_high - previous_close),
                abs(current_low - previous_close),
            )

            upward_move = current_high - previous_high
            downward_move = previous_low - current_low

            plus_dm = (
                upward_move
                if upward_move > downward_move
                and upward_move > 0
                else 0.0
            )

            minus_dm = (
                downward_move
                if downward_move > upward_move
                and downward_move > 0
                else 0.0
            )

            true_ranges.append(true_range)
            plus_dm_values.append(plus_dm)
            minus_dm_values.append(minus_dm)

        # Valores suavizados iniciales de Wilder.
        smoothed_tr = sum(true_ranges[:period])
        smoothed_plus_dm = sum(plus_dm_values[:period])
        smoothed_minus_dm = sum(minus_dm_values[:period])

        dx_values = []

        first_dx = ADXIndicator._calculate_dx(
            smoothed_tr=smoothed_tr,
            smoothed_plus_dm=smoothed_plus_dm,
            smoothed_minus_dm=smoothed_minus_dm,
        )

        dx_values.append(first_dx)

        # Suavizado sucesivo de TR, +DM y -DM.
        for index in range(period, len(true_ranges)):
            smoothed_tr = (
                smoothed_tr
                - (smoothed_tr / period)
                + true_ranges[index]
            )

            smoothed_plus_dm = (
                smoothed_plus_dm
                - (smoothed_plus_dm / period)
                + plus_dm_values[index]
            )

            smoothed_minus_dm = (
                smoothed_minus_dm
                - (smoothed_minus_dm / period)
                + minus_dm_values[index]
            )

            dx = ADXIndicator._calculate_dx(
                smoothed_tr=smoothed_tr,
                smoothed_plus_dm=smoothed_plus_dm,
                smoothed_minus_dm=smoothed_minus_dm,
            )

            dx_values.append(dx)

        if len(dx_values) < period:
            raise ValueError(
                "No hay suficientes valores DX para calcular el ADX."
            )

        # El primer ADX es el promedio de los primeros DX.
        first_adx = sum(dx_values[:period]) / period

        adx_values = [first_adx]
        previous_adx = first_adx

        # Suavizado de Wilder para los siguientes valores ADX.
        for dx in dx_values[period:]:
            current_adx = (
                ((previous_adx * (period - 1)) + dx)
                / period
            )

            adx_values.append(current_adx)
            previous_adx = current_adx

        return adx_values

    @staticmethod
    def _calculate_dx(
        smoothed_tr: float,
        smoothed_plus_dm: float,
        smoothed_minus_dm: float,
    ) -> float:
        """
        Calcula un valor DX a partir de los movimientos
        direccionales suavizados.
        """

        if smoothed_tr == 0:
            return 0.0

        plus_di = (
            100 * smoothed_plus_dm / smoothed_tr
        )

        minus_di = (
            100 * smoothed_minus_dm / smoothed_tr
        )

        directional_sum = plus_di + minus_di

        if directional_sum == 0:
            return 0.0

        return (
            100
            * abs(plus_di - minus_di)
            / directional_sum
        )

    @staticmethod
    def get_last(
        candles: list[list[float]],
        period: int = 14,
    ) -> float:
        """
        Devuelve el último valor ADX disponible.
        """

        adx_values = ADXIndicator.calculate(
            candles=candles,
            period=period,
        )

        return adx_values[-1]