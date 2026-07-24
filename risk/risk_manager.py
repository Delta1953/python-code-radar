"""
Risk Manager

Calcula un plan básico de operación a partir del precio actual,
la volatilidad medida mediante ATR y los parámetros de gestión de riesgo.
"""


class RiskStatus:
    """Estados posibles del Risk Manager."""

    OK = "OK"
    CAPITAL_LIMITED = "CAPITAL_LIMITED"

    INVALID_PRICE = "INVALID_PRICE"
    INVALID_ATR = "INVALID_ATR"
    INVALID_CAPITAL = "INVALID_CAPITAL"
    INVALID_RISK_PERCENT = "INVALID_RISK_PERCENT"
    INVALID_RISK_REWARD = "INVALID_RISK_REWARD"
    INVALID_ATR_MULTIPLIER = "INVALID_ATR_MULTIPLIER"
    INVALID_STOP_LOSS = "INVALID_STOP_LOSS"


class RiskManager:
    """Gestión básica de riesgo para operaciones alcistas."""

    @staticmethod
    def calculate(
        current_price: float,
        atr: float,
        capital: float,
        risk_percent: float = 1.0,
        risk_reward: float = 2.0,
        atr_multiplier: float = 2.0,
    ) -> dict:
        """
        Calcula un plan básico de operación.

        Parameters
        ----------
        current_price : float
            Precio actual del activo.

        atr : float
            Average True Range del activo.

        capital : float
            Capital disponible para la operación.

        risk_percent : float
            Porcentaje máximo de capital que se desea arriesgar.

        risk_reward : float
            Relación beneficio/riesgo deseada.

        atr_multiplier : float
            Multiplicador del ATR utilizado para calcular el Stop Loss.

        Returns
        -------
        dict
            Resultado del cálculo, incluyendo estado, operación,
            posición y riesgo.
        """

        # ----------------------------------------------------------
        # Validaciones
        # ----------------------------------------------------------

        if current_price <= 0:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_PRICE,
                message="El precio actual debe ser mayor que cero.",
            )

        if atr <= 0:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_ATR,
                message="El ATR debe ser mayor que cero.",
            )

        if capital <= 0:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_CAPITAL,
                message="El capital debe ser mayor que cero.",
            )

        if risk_percent <= 0 or risk_percent > 100:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_RISK_PERCENT,
                message=(
                    "El porcentaje de riesgo debe ser mayor que cero "
                    "y menor o igual que 100."
                ),
            )

        if risk_reward <= 0:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_RISK_REWARD,
                message="La relación riesgo/beneficio debe ser mayor que cero.",
            )

        if atr_multiplier <= 0:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_ATR_MULTIPLIER,
                message="El multiplicador del ATR debe ser mayor que cero.",
            )

        # ----------------------------------------------------------
        # Cálculos principales
        # ----------------------------------------------------------

        requested_capital_at_risk = capital * (risk_percent / 100)

        stop_distance = atr * atr_multiplier
        if stop_distance >= current_price:
            return RiskManager._error_result(
                status=RiskStatus.INVALID_STOP_LOSS,
                message=(
                    "La distancia del Stop Loss es igual o mayor "
                    "que el precio del activo."
                ),
            )

        stop_loss = current_price - stop_distance
        take_profit = current_price + (
            stop_distance * risk_reward
        )

        requested_position_size = (
            requested_capital_at_risk / stop_distance
        )

        requested_investment = (
            requested_position_size * current_price
        )

        # ----------------------------------------------------------
        # Ajuste por capital disponible
        # ----------------------------------------------------------

        if requested_investment > capital:
            status = RiskStatus.CAPITAL_LIMITED

            position_size = capital / current_price
            investment = capital

            capital_at_risk = (
                position_size * stop_distance
            )

            message = (
                "El capital disponible no permite alcanzar el riesgo "
                "solicitado. La posición fue ajustada automáticamente."
            )
        else:
            status = RiskStatus.OK

            position_size = requested_position_size
            investment = requested_investment
            capital_at_risk = requested_capital_at_risk

            message = "Plan de riesgo calculado correctamente."

        actual_risk_percent = (
            capital_at_risk / capital
        ) * 100

        return {
            "status": status,
            "message": message,

            "trade": {
                "entry_price": current_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "stop_distance": stop_distance,
                "risk_reward": risk_reward,
                "atr_multiplier": atr_multiplier,
            },

            "position": {
                "position_size": position_size,
                "investment": investment,
                "requested_position_size": requested_position_size,
                "requested_investment": requested_investment,
            },

            "risk": {
                "requested_risk_percent": risk_percent,
                "actual_risk_percent": actual_risk_percent,
                "requested_capital_at_risk": requested_capital_at_risk,
                "capital_at_risk": capital_at_risk,
                "capital_limited": (
                    status == RiskStatus.CAPITAL_LIMITED
                ),
            },
        }

    @staticmethod
    def _error_result(
        status: str,
        message: str,
    ) -> dict:
        """Genera una respuesta uniforme para parámetros inválidos."""

        return {
            "status": status,
            "message": message,
            "trade": None,
            "position": None,
            "risk": None,
        }