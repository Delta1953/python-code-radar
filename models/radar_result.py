from dataclasses import dataclass


@dataclass
class RadarResult:
    symbol: str
    current_price: float
    score: int
    trend: str
    rsi_14: float