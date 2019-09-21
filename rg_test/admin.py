from django.contrib import admin
from django.apps import apps
from django.conf import settings
exclude_models = ['Exchange', 'Balance', 'Coin', 'CoinExchanges', 'TradeIndicatorCompare', 'Indicator', 'Strategy',
                  'BitmexStrategy', 'BitmexNetworkStrategy', 'HistoryTrade']

for apps_name in settings.LOCAL_APPS + settings.THIRD_PARTY_APPS:

    for model in apps.get_app_config(apps_name).get_models():
        if model.__name__ not in exclude_models:
            admin.site.register(model)
