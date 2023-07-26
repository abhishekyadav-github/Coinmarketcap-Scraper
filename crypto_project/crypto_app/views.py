import time

from crypto_app.models import CryptoData
from crypto_app.serializers import CryptoDataSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UpdateCryptoDataView(APIView):
    def post(self, request):
        start = time.time()
        data = request.data
        print("in view - ", data[1])
        for coin_data in data:
            # mapping field names to names stored in DB for serialization
            mapped_coin_data = {
                'name': coin_data.get('Name', ''),
                'price': coin_data.get('Price', ''),
                'percent_change_1h': coin_data.get('1h%', ''),
                'percent_change_24h': coin_data.get('24h%', ''),
                'percent_change_7d': coin_data.get('7d%', ''),
                'market_cap': coin_data.get('Market Cap', ''),
                'volume_24h': coin_data.get('Volume(24h)', ''),
                'circulating_supply': coin_data.get('Circulating Supply', ''),
            }
            name = coin_data.get('Name')
            if name:
                # Check if the crypto data already exists then perform update
                try:
                    instance = CryptoData.objects.get(name=name)
                    serializer = CryptoDataSerializer(instance, data=mapped_coin_data)
                except CryptoData.DoesNotExist:
                    # if doesnotexist then perform create
                    serializer = CryptoDataSerializer(data=mapped_coin_data)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        end = time.time()
        print("time taken = ", end-start)
        return Response("Data saved/updated successfully.", status=status.HTTP_201_CREATED)


class GetLatestCryptoDataView(APIView):
    def get(self, request):
        data = CryptoData.objects.order_by('id')
        serializer = CryptoDataSerializer(data, many=True)
        return Response(serializer.data)
