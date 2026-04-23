"""
Configuration constants for the API Versioning Demo
"""

from datetime import datetime, timedelta

# API Configuration
API_VERSION_V1 = "1.0"
API_VERSION_V2 = "2.0"

# Deprecation Timeline
DEPRECATION_DAYS_NOTICE = 90
SUNSET_DATE = (datetime.utcnow() + timedelta(days=DEPRECATION_DAYS_NOTICE)).strftime('%a, %d %b %Y %H:%M:%S GMT')

# Supported Currencies in v2
SUPPORTED_CURRENCIES = ['VND', 'USD', 'EUR', 'JPY', 'CNY']

# Currency Symbols
CURRENCY_SYMBOLS = {
    'VND': '₫',
    'USD': '$',
    'EUR': '€',
    'JPY': '¥',
    'CNY': '¥'
}

# Currency Names
CURRENCY_NAMES = {
    'VND': 'Vietnamese Dong',
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'JPY': 'Japanese Yen',
    'CNY': 'Chinese Yuan'
}

# Exchange Rates (mock - VND per unit)
EXCHANGE_RATES = {
    'VND': 1.0,
    'USD': 24500.0,
    'EUR': 27000.0,
    'JPY': 165.0,
    'CNY': 3400.0
}
