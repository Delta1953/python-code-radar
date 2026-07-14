from exchange.binance_client import BinanceClient

def main():
    client = BinanceClient()
    symbol = 'BTC/USDT'
    ticker = client.get_ticker(symbol)
    print("===========================================")
    print("PYTHON CODE DE RADAR")
    print("============================================")   
    print("Símbolo", ticker["symbol"])
    print("Último precio", ticker["last"])
    print("Máximo 24 h", ticker["high"])
    print("Mínimo 24 h", ticker["low"])
    print("Volumen", ticker["baseVolume"])
    print("===========================================")

if __name__ == "__main__":
    main()