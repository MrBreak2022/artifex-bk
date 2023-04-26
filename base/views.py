
# from .products import products
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import *
from .serializers import *
from accounts.models import *
from accounts.serializers import *

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.utils import timezone

@api_view(['GET'])

def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',
        '/api/products/upload/',
        '/api/products/<id>/',
        '/api/products/delete/<id>/',
        '/api/products/<update>/<id>',
    ]
    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProduct(request):
    seller = request.user
    data = request.data
    bidding = False

    product = Product.objects.create(
            seller=seller,
            name=data['name'],
            description=data['description'],
            image=data['image'],
            price=data['price'],
            stock=data['stock'],
            bidding=bidding,
            selleremail=data['selleremail'],
        )
    serializer = ProductSerializer(product, many=False)
    print(request.data)
    return Response(serializer.data)    
  

@api_view(['PUT'])
def editProduct(request, pk):
    print ('pk ', pk)
    product = get_object_or_404(Product, pk=pk)
    data = request.data
    print ('PRODUCT ', product)
    
    # product.user = data['user']
    if data['name'] != '':
        product.name = data['name']
    # if data['image'] != '':
    #     product.image = data['image']
    if data['price'] != '':
        product.price = data['price']
    if data['selleremail'] != '':
        product.selleremail = data['selleremail']    
    if data['description'] != '':
        product.description = data['description']
    if data['stock'] != '':
        product.stock = data['stock']

    print (request.data)

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

       

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            totalPrice=data['totalPrice']
        )

       
        for i in orderItems:
            product = Product.objects.get(_id=i['product'])

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
                selleremail=product.selleremail
            )

        

            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)    
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not Authorized  to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = timezone.now()
    order.save()

    for order_item in order.orderitem_set.all():
        product = order_item.product
        product.bidding = False
        product.seller = request.user
        product.save()

    return Response('Order was paid on ' + str(timezone.now()))

# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def updateOwner(request, pk):
#     order = Order.objects.get(_id=pk)

#     for order_item in order.orderitem_set.all():
#         product = order_item.product
#         product.seller = request.user
#         product.save()

#     return Response('Order was paid on ' + str(timezone.now()))




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteOrder(request, pk):
    order = Order.objects.get(_id=pk)
    order.delete()
    return Response('Order Deleted')

# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def Product_user(request):
    user = request.user
    products = Product.objects.filter(seller=user.id)
    product_list = []
    for product in products:
        product_list.append({
            '_id' : product._id,
            'name': product.name,
        })
    return Response({'products': product_list})


@api_view(['GET'])
def Product_spec(request, pk):
    user = get_object_or_404(User, id=int(pk))
    products = Product.objects.filter(seller=user.id)
    product_list = []
    for product in products:
        product_list.append({
            '_id' : product._id,
            'name': product.name,
        })
    return Response({'products': product_list})

@api_view(['PUT'])
def sellProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.data
    print ('PRODUCT ', product)
    
    product.bidding = True

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def soldProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = request.data
    print ('PRODUCT ', product)
    
    product.seller = request.user.username
    product.selleremail = request.user.paypalemail

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def set_bidding(request, pk):
    product = Product.objects.get(_id=pk)
    product.bidding = request.data['bidding']
    product.save()
    return Response('Bidding field updated')