from crypto_app.views import GetLatestCryptoDataView, UpdateCryptoDataView
from django.urls import path

urlpatterns = [
    path('update_data/', UpdateCryptoDataView.as_view(), name='update_crypto_data'),
    path('latest_data/', GetLatestCryptoDataView.as_view(), name='get_latest_crypto_data'),
]
