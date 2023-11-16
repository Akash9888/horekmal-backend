from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product
from base.serializer import ProductSerializer


# fetch all products
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# fetch specific products
@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


