# from django.core.management import BaseCommand
# import asyncio
# from prices.services import binance_ws_client, kraken_ws_client
#
#
# class Command(BaseCommand):
#     help = 'Run WebSocket clients for Binance and Kraken'
#
#     def handle(self, *args, **kwargs):
#         try:
#             asyncio.run(self.run_websockets())
#         except KeyboardInterrupt:
#             print("WebSocket clients stopped manually.")
#
#     async def run_websockets(self):
#         await asyncio.gather(binance_ws_client(), kraken_ws_client())

from django.core.management import BaseCommand
import asyncio
from prices.services import binance_ws_client, kraken_ws_client


class Command(BaseCommand):
    help = 'Run WebSocket clients for Binance and Kraken'

    def handle(self, *args, **kwargs):
        try:
            asyncio.run(self.run_websockets())
        except KeyboardInterrupt:
            print("WebSocket clients stopped manually.")

    async def run_websockets(self):
        await asyncio.gather(binance_ws_client(), kraken_ws_client())
