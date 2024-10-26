import asyncio
import websockets
import json
import time
from django.core.cache import cache
from .utils import normalize_pair_name

BINANCE_WS = "wss://stream.binance.com:9443/ws/!ticker@arr"
KRAKEN_WS = "wss://ws.kraken.com"

# Price data storage (for cache)
price_data = {}


async def binance_ws_client():
    while True:
        try:
            print("Connecting to Binance WebSocket...")
            async with websockets.connect(BINANCE_WS) as websocket:
                print("Connected to Binance WebSocket.")
                while True:
                    data = await websocket.recv()
                    print("Received data from Binance:", data)
                    update_binance_data(json.loads(data))
        except Exception as e:
            print(f"Error in Binance WebSocket client: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)


async def kraken_ws_client():
    while True:
        try:
            print("Connecting to Kraken WebSocket...")
            async with websockets.connect(KRAKEN_WS) as websocket:
                print("Connected to Kraken WebSocket.")
                subscribe = {
                    "event": "subscribe",
                    "pair": ["BTC/USD", "ETH/USD"],
                    "subscription": {"name": "ticker"}
                }
                await websocket.send(json.dumps(subscribe))
                print("Subscribed to Kraken pairs.")
                while True:
                    data = await websocket.recv()
                    print("Received data from Kraken:", data)
                    update_kraken_data(json.loads(data))
        except Exception as e:
            print(f"Error in Kraken WebSocket client: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)


def update_binance_data(data):
    for ticker in data:
        pair = ticker['s']
        normalized_pair = normalize_pair_name(pair)
        bid_price = float(ticker['b'])
        ask_price = float(ticker['a'])
        avg_price = (bid_price + ask_price) / 2
        price_data[f"binance_{normalized_pair}"] = {
            'exchange': 'binance',
            'pair': normalized_pair,
            'avg_price': avg_price,
            'timestamp': time.time()
        }
    cache.set('price_data', price_data)


def update_kraken_data(data):
    if isinstance(data, list) and len(data) > 1:
        ticker_info = data[1]
        pair = data[-1]
        bid_price = float(ticker_info['b'][0])
        ask_price = float(ticker_info['a'][0])
        avg_price = (bid_price + ask_price) / 2
        normalized_pair = normalize_pair_name(pair)
        price_data[f"kraken_{normalized_pair}"] = {
            'exchange': 'kraken',
            'pair': normalized_pair,
            'avg_price': avg_price,
            'timestamp': time.time()
        }
    cache.set('price_data', price_data)
