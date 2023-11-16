

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.models import Order, ShippingAddress, Product, OrderItem
from base.serializer import OrderSerializer
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data
    orderItems = data['orderItems']
    if orderItems and len(orderItems) == 0:
        return Response({'details': "No order items"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        # create order
        order = Order.objects.create(
            # user=user,
            # paymentMethod=data['paymentMethod'],
            # taxPrice=data['taxPrice'],
            # shippingPrice=data['shippingPrice'],
            # totalPrice=data['totalPrice']

            user=user,
            paymentMethod=data['paymentMethod'],
            itemsTotal=data['itemsTotal'],
            vat=data['vat'],
            deliveryFee=data['deliveryFee'],
            totalPayment=data['totalPayment']
        )

        # create shipping address

        shipping = ShippingAddress.objects.create(
            order=order,
            name=data['shippingAddress']['name'],
            email=data['shippingAddress']['email'],
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            phone=data['shippingAddress']['phone'],
            country=data['shippingAddress']['country']
        )

        # create orderItem

        for i in orderItems:
            product = Product.objects.get(_id=i["productId"])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url
            )
            product.stock -= item.qty
            product.save()

        serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):
    user = request.user
    print(user)

    try:
        order = Order.objects.get(order_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response({"details": "Not authorized to view this order"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"details": "Order doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrders(request):
    user = request.user
    try:

        if user.is_staff:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)
        else:
            orders = Order.objects.filter(user__email=user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    except:
        return Response({"details": "Order doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request,pk):
    order=Order.objects.get(order_id=pk)
    order.isPaid=True
    order.paidAt=datetime.now()
    order.save()

    return Response('Order was paid')

