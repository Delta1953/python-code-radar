import ccxt

exchange = ccxt.binance()
ticker = exchange.fetch_ticker("BTC/USDT")
print("===========================================")
print("Conexión con Binance exitosa")
print("Símbolo", ticker["symbol"])
print("Último precio", ticker["last"])
print("Máximo precio", ticker["high"])
print("Mínimo precio", ticker["low"])
print("Volumen", ticker["baseVolume"])
print("===========================================")
