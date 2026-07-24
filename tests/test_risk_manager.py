import pytest

from risk.risk_manager import RiskManager, RiskStatus


def test_capital_limited() -> None:
    result = RiskManager.calculate(
        current_price=66345.77,
        atr=145,
        capital=10000,
        risk_percent=1,
        risk_reward=2,
        atr_multiplier=2,
    )

    assert result["status"] == RiskStatus.CAPITAL_LIMITED
    assert result["trade"] is not None
    assert result["position"] is not None
    assert result["risk"] is not None

    assert result["trade"]["entry_price"] == pytest.approx(66345.77)
    assert result["trade"]["stop_distance"] == pytest.approx(290)
    assert result["trade"]["stop_loss"] == pytest.approx(66055.77)
    assert result["trade"]["take_profit"] == pytest.approx(66925.77)

    assert result["position"]["position_size"] == pytest.approx(
        10000 / 66345.77
    )
    assert result["position"]["investment"] == pytest.approx(10000)

    assert result["risk"]["capital_limited"] is True
    assert result["risk"]["capital_at_risk"] == pytest.approx(
        (10000 / 66345.77) * 290
    )
    assert result["risk"]["actual_risk_percent"] == pytest.approx(
        ((10000 / 66345.77) * 290 / 10000) * 100
    )


def test_normal_plan() -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
        risk_percent=1,
        risk_reward=2,
        atr_multiplier=2,
    )

    assert result["status"] == RiskStatus.OK
    assert result["message"] == "Plan de riesgo calculado correctamente."

    assert result["trade"]["entry_price"] == pytest.approx(100)
    assert result["trade"]["stop_distance"] == pytest.approx(10)
    assert result["trade"]["stop_loss"] == pytest.approx(90)
    assert result["trade"]["take_profit"] == pytest.approx(120)
    assert result["trade"]["risk_reward"] == pytest.approx(2)
    assert result["trade"]["atr_multiplier"] == pytest.approx(2)

    assert result["position"]["position_size"] == pytest.approx(10)
    assert result["position"]["investment"] == pytest.approx(1000)
    assert result["position"]["requested_position_size"] == pytest.approx(10)
    assert result["position"]["requested_investment"] == pytest.approx(1000)

    assert result["risk"]["requested_risk_percent"] == pytest.approx(1)
    assert result["risk"]["requested_capital_at_risk"] == pytest.approx(100)
    assert result["risk"]["capital_at_risk"] == pytest.approx(100)
    assert result["risk"]["actual_risk_percent"] == pytest.approx(1)
    assert result["risk"]["capital_limited"] is False


def test_invalid_price() -> None:
    result = RiskManager.calculate(
        current_price=0,
        atr=5,
        capital=10000,
    )

    assert result["status"] == RiskStatus.INVALID_PRICE
    assert result["message"] == "El precio actual debe ser mayor que cero."
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


def test_invalid_atr() -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=0,
        capital=10000,
    )

    assert result["status"] == RiskStatus.INVALID_ATR
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


def test_invalid_capital() -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=0,
    )

    assert result["status"] == RiskStatus.INVALID_CAPITAL
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


@pytest.mark.parametrize(
    "risk_percent",
    [
        0,
        -1,
        101,
    ],
)
def test_invalid_risk_percent(risk_percent: float) -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
        risk_percent=risk_percent,
    )

    assert result["status"] == RiskStatus.INVALID_RISK_PERCENT
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


@pytest.mark.parametrize(
    "risk_reward",
    [
        0,
        -1,
    ],
)
def test_invalid_risk_reward(risk_reward: float) -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
        risk_reward=risk_reward,
    )

    assert result["status"] == RiskStatus.INVALID_RISK_REWARD
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


@pytest.mark.parametrize(
    "atr_multiplier",
    [
        0,
        -1,
    ],
)
def test_invalid_atr_multiplier(atr_multiplier: float) -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
        atr_multiplier=atr_multiplier,
    )

    assert result["status"] == RiskStatus.INVALID_ATR_MULTIPLIER
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


def test_invalid_stop_loss_when_stop_distance_exceeds_price() -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=60,
        capital=10000,
        atr_multiplier=2,
    )

    assert result["status"] == RiskStatus.INVALID_STOP_LOSS
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


def test_invalid_stop_loss_when_stop_distance_equals_price() -> None:
    result = RiskManager.calculate(
        current_price=100,
        atr=50,
        capital=10000,
        atr_multiplier=2,
    )

    assert result["status"] == RiskStatus.INVALID_STOP_LOSS
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None

def test_result_has_required_sections() -> None:
    """
    Verifica la estructura general de una respuesta válida.
    """

    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
    )

    required_fields = {
        "status",
        "message",
        "trade",
        "position",
        "risk",
    }

    missing_fields = required_fields - result.keys()

    assert not missing_fields, (
        "Faltan campos principales en el resultado: "
        f"{sorted(missing_fields)}"
    )


@pytest.mark.parametrize(
    ("parameters", "expected_status"),
    [
        (
            {
                "current_price": 0,
                "atr": 5,
                "capital": 10000,
            },
            RiskStatus.INVALID_PRICE,
        ),
        (
            {
                "current_price": 100,
                "atr": 0,
                "capital": 10000,
            },
            RiskStatus.INVALID_ATR,
        ),
        (
            {
                "current_price": 100,
                "atr": 5,
                "capital": 0,
            },
            RiskStatus.INVALID_CAPITAL,
        ),
    ],
)
def test_error_results_have_uniform_structure(
    parameters: dict,
    expected_status: str,
) -> None:
    """
    Verifica que los errores mantengan una estructura uniforme.
    """

    result = RiskManager.calculate(**parameters)

    assert result["status"] == expected_status
    assert isinstance(result["message"], str)
    assert result["message"]
    assert result["trade"] is None
    assert result["position"] is None
    assert result["risk"] is None


def test_print_risk_plan() -> None:
    """
    Muestra un plan de riesgo completo para validación visual.
    """

    result = RiskManager.calculate(
        current_price=100,
        atr=5,
        capital=10000,
        risk_percent=1,
        risk_reward=2,
        atr_multiplier=2,
    )

    assert result["status"] == RiskStatus.OK

    trade = result["trade"]
    position = result["position"]
    risk = result["risk"]

    print()
    print("=" * 62)
    print("                  PLAN DE GESTIÓN DE RIESGO")
    print("=" * 62)

    print(f"Estado                  : {result['status']}")
    print(f"Mensaje                 : {result['message']}")
    print()

    print("---------------- OPERACIÓN ----------------")
    print(f"Precio de entrada       : {trade['entry_price']:.8f}")
    print(f"Stop Loss               : {trade['stop_loss']:.8f}")
    print(f"Take Profit             : {trade['take_profit']:.8f}")
    print(f"Distancia al Stop       : {trade['stop_distance']:.8f}")
    print(f"Riesgo/Beneficio        : {trade['risk_reward']:.2f}")
    print(f"Multiplicador ATR       : {trade['atr_multiplier']:.2f}")
    print()

    print("---------------- POSICIÓN -----------------")
    print(f"Tamaño de posición      : {position['position_size']:.8f}")
    print(f"Inversión               : {position['investment']:.2f}")
    print()

    print("------------------ RIESGO -----------------")
    print(
        "Riesgo solicitado      : "
        f"{risk['requested_risk_percent']:.2f}%"
    )
    print(
        "Riesgo real            : "
        f"{risk['actual_risk_percent']:.2f}%"
    )
    print(
        "Capital en riesgo      : "
        f"{risk['capital_at_risk']:.2f}"
    )
    print(
        "Limitado por capital   : "
        f"{risk['capital_limited']}"
    )

    print("=" * 62)    