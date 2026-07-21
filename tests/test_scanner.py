from scanners.market_scanner import MarketScanner   

def main():
    scanner = MarketScanner()
    top_markets = scanner.get_top_volume(limit=10)

    symbols = scanner.get_usdt_spot_symbols()

    print("============================================")
    print("  PARES SPOT ACTIVOS CONTRA USDT            ")
    print("============================================")   
    print(f"Cantidad encontrada: {len(symbols)}")
    print()

    for position, market in enumerate(top_markets, start=1):
        symbol = market["symbol"]
        price = market["last"]
        volume = market["quote_volume"]
        variation = market["percentage"]

        print(
            f"{position:>2}. "
            f"{symbol:<15} "
            f"Precio: {price!s:<15} "
            f"Volumen USDT: {volume:>18,.2f} "
            f"Variación: {variation!s}%"
        )


if __name__ == "__main__":
    main()


