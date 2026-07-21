
from services.ohlcv_service import OHLCVService
from indicators.atr import ATRIndicator
from config.settings import (
    DEFAULT_TIMEFRAME,
    DEFAULT_CANDLE_LIMIT,
)


TEST_SYMBOL = "BTC/USDT"
TEST_TIMEFRAME = DEFAULT_TIMEFRAME
TEST_LIMIT = DEFAULT_CANDLE_LIMIT


def main():

    print("\nPRUEBA DEL ATR")
    print("-" * 50)

    ohlcv_service = OHLCVService()

    candles = ohlcv_service.get_candles(
        symbol=TEST_SYMBOL,
        timeframe=TEST_TIMEFRAME,
        limit=TEST_LIMIT,
    )

    atr = ATRIndicator.get_last(
        candles,
        period=14,
    )

    print(f"Símbolo      : {TEST_SYMBOL}")
    print(f"Temporalidad : {TEST_TIMEFRAME}")
    print(f"Velas        : {TEST_LIMIT}")
    print(f"ATR (14)     : {atr:.4f}")


if __name__ == "__main__":
    main()