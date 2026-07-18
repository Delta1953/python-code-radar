"""
=========================================================
Proyecto : Python Code de Radar
Archivo  : market_scanner.py
Autor    : Roberto Günther
Versión  : 0.4
=========================================================

OBJETIVO
--------
Seleccionar mercados spot activos que coticen contra USDT
y ordenarlos según su volumen negociado.

RESPONSABILIDADES
-----------------
- Obtener los mercados disponibles desde Binance.
- Filtrar mercados spot activos.
- Seleccionar únicamente pares cotizados contra USDT.
- Excluir stablecoins y activos no adecuados para el Radar.
- Ordenar los mercados por volumen negociado.

DEPENDENCIAS
------------
- BinanceClient

=========================================================
"""

from exchange.binance_client import BinanceClient


class MarketScanner:
    """
    Selecciona mercados válidos para el Radar.
    """

    EXCLUDED_BASE_ASSETS = {
        "USDC",
        "FDUSD",
        "TUSD",
        "USDP",
        "DAI",
        "USD1",
        "EUR",
        "AEUR",
    }

    def __init__(self):
        """
        Inicializa el scanner de mercados.

        Retorna:
            None
        """
        self.client = BinanceClient()

    def get_markets(self):
        """
        Obtiene todos los mercados disponibles en Binance.

        Retorna:
            dict:
                Diccionario con la información de los mercados.
        """
        return self.client.exchange.load_markets()

    def get_usdt_spot_symbols(self):
        """
        Obtiene símbolos spot activos que cotizan contra USDT.

        También excluye stablecoins y otros activos que no
        resultan adecuados para el análisis técnico del Radar.

        Retorna:
            list[str]:
                Lista de símbolos válidos ordenados alfabéticamente.
        """
        markets = self.get_markets()
        symbols = []

        for symbol, market in markets.items():
            base_asset = market.get("base")

            if (
                market.get("spot")
                and market.get("active")
                and market.get("quote") == "USDT"
                and base_asset not in self.EXCLUDED_BASE_ASSETS
            ):
                symbols.append(symbol)

        return sorted(symbols)

    def get_top_volume(self, limit=20):
        """
        Obtiene los mercados con mayor volumen negociado.

        Parámetros:
            limit (int):
                Cantidad máxima de mercados a devolver.

        Retorna:
            list[dict]:
                Lista de mercados ordenados por volumen de mayor
                a menor.
        """
        valid_symbols = set(self.get_usdt_spot_symbols())
        tickers = self.client.get_tickers()
        results = []

        for symbol, ticker in tickers.items():
            if symbol not in valid_symbols:
                continue

            quote_volume = ticker.get("quoteVolume")

            if quote_volume is None:
                continue

            results.append(
                {
                    "symbol": symbol,
                    "last": ticker.get("last"),
                    "quote_volume": quote_volume,
                    "percentage": ticker.get("percentage"),
                }
            )

        results.sort(
            key=lambda item: item["quote_volume"],
            reverse=True,
        )

        return results[:limit]