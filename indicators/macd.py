"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : macd.py
Autor    : Roberto Günther
Versión  : 0.6
=========================================================

OBJETIVO
--------
Calcular el indicador MACD, Moving Average Convergence
Divergence, a partir de una serie de precios de cierre.

El MACD permite evaluar la dirección (conformacion de tendencia)
y el momentum del mercado mediante la relación entre dos medias móviles
exponenciales.

RESPONSABILIDADES
-----------------
- Validar los datos recibidos.
- Calcular la línea MACD.
- Calcular la línea de señal.
- Calcular el histograma.
- Devolver las series completas o sus últimos valores.

DEPENDENCIAS
------------
- EMAIndicator

PARÁMETROS ESTÁNDAR
-------------------
- EMA rápida: 12 períodos.
- EMA lenta: 26 períodos.
- Línea de señal: 9 períodos.

=========================================================
"""

from indicators.ema import EMAIndicator


class MACDIndicator:
    """
    Calcula el indicador MACD de una serie de precios.
    """

    @staticmethod
    def calculate(
        prices,
        fast_period=12,
        slow_period=26,
        signal_period=9,
    ):
        """
        Calcula las series MACD, señal e histograma.

        Las tres series devueltas están alineadas y tienen
        la misma cantidad de elementos.

        Parámetros:
            prices (list[float]):
                Serie de precios de cierre.

            fast_period (int):
                Período de la EMA rápida.

            slow_period (int):
                Período de la EMA lenta.

            signal_period (int):
                Período de la EMA aplicada a la línea MACD.

        Retorna:
            dict:
                Diccionario con las series:

                {
                    "macd": list[float],
                    "signal": list[float],
                    "histogram": list[float],
                }

        Excepciones:
            ValueError:
                Si los períodos no son válidos, no mantienen
                una relación correcta o faltan precios.
        """
        MACDIndicator._validate_parameters(
            prices=prices,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
        )

        fast_ema_values = EMAIndicator.calculate(
            prices,
            period=fast_period,
        )

        slow_ema_values = EMAIndicator.calculate(
            prices,
            period=slow_period,
        )

        alignment_offset = slow_period - fast_period

        aligned_fast_ema_values = fast_ema_values[
            alignment_offset:
        ]

        macd_values = []

        for fast_ema, slow_ema in zip(
            aligned_fast_ema_values,
            slow_ema_values,
        ):
            macd_values.append(fast_ema - slow_ema)

        signal_values = EMAIndicator.calculate(
            macd_values,
            period=signal_period,
        )

        aligned_macd_values = macd_values[
            signal_period - 1:
        ]

        histogram_values = []

        for macd_value, signal_value in zip(
            aligned_macd_values,
            signal_values,
        ):
            histogram_values.append(
                macd_value - signal_value
            )

        return {
            "macd": aligned_macd_values,
            "signal": signal_values,
            "histogram": histogram_values,
        }

    @staticmethod
    def get_last(
        prices,
        fast_period=12,
        slow_period=26,
        signal_period=9,
    ):
        """
        Obtiene los últimos valores del indicador MACD.

        Parámetros:
            prices (list[float]):
                Serie de precios de cierre.

            fast_period (int):
                Período de la EMA rápida.

            slow_period (int):
                Período de la EMA lenta.

            signal_period (int):
                Período de la línea de señal.

        Retorna:
            dict:
                Últimos valores calculados:

                {
                    "macd": float,
                    "signal": float,
                    "histogram": float,
                }
        """
        result = MACDIndicator.calculate(
            prices=prices,
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
        )

        return {
            "macd": result["macd"][-1],
            "signal": result["signal"][-1],
            "histogram": result["histogram"][-1],
        }

    @staticmethod
    def _validate_parameters(
        prices,
        fast_period,
        slow_period,
        signal_period,
    ):
        """
        Valida los parámetros necesarios para calcular MACD.

        Parámetros:
            prices (list[float]):
                Serie de precios de cierre.

            fast_period (int):
                Período de la EMA rápida.

            slow_period (int):
                Período de la EMA lenta.

            signal_period (int):
                Período de la línea de señal.

        Retorna:
            None

        Excepciones:
            ValueError:
                Si alguno de los parámetros es inválido.
        """
        if fast_period <= 0:
            raise ValueError(
                "El período rápido debe ser mayor que cero."
            )

        if slow_period <= 0:
            raise ValueError(
                "El período lento debe ser mayor que cero."
            )

        if signal_period <= 0:
            raise ValueError(
                "El período de señal debe ser mayor que cero."
            )

        if fast_period >= slow_period:
            raise ValueError(
                "El período rápido debe ser menor que el período lento."
            )

        minimum_prices = slow_period + signal_period - 1

        if len(prices) < minimum_prices:
            raise ValueError(
                "Se necesitan al menos "
                f"{minimum_prices} precios para calcular el MACD."
            )