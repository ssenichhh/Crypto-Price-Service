from django.views import View
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache
from .utils import normalize_pair_name


class PriceView(View):
    template_name = 'prices.html'

    def get(self, request):
        exchange = request.GET.get('exchange')
        pair = request.GET.get('pair')

        filtered_data = [value for key, value in cache.get('price_data', {}).items() if
                         (not exchange or value['exchange'] == exchange.lower())
                         and (not pair or value['pair'] == normalize_pair_name(pair))]

        context = {'prices': filtered_data, 'exchange': exchange, 'pair': pair}

        return render(request, self.template_name, context)


class PairPriceView(View):
    template_name = 'pair_prices.html'

    def get(self, request, pair):
        normalized_pair = normalize_pair_name(pair)

        filtered_data = [value for key, value in cache.get('price_data',
                                                           {}).items() if value['pair'] == normalized_pair]

        context = {'prices': filtered_data, 'pair': pair}

        return render(request, self.template_name, context)


class ExchangePriceView(View):
    template_name = 'exchange_prices.html'

    def get(self, request, exchange):
        exchange = exchange.lower()

        filtered_data = [value for key, value in cache.get('price_data', {}).items() if value['exchange'] == exchange]

        context = {'prices': filtered_data, 'exchange': exchange}

        return render(request, self.template_name, context)


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        price_data = cache.get('price_data', {})
        context = {'price_data': price_data}
        return render(request, self.template_name, context)
