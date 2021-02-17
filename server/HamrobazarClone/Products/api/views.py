from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .serializer import ProductSerializer
from ..models import Product
from Category.models import Category
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', ])
def api_products_view(request):
  try:
      posts = Product.objects.all()
  except Product.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  serializer = ProductSerializer(posts,many=True)
  return Response(serializer.data)



@api_view(['GET', ])
def api_single_product_view(request,pk):
  try:
      post = Product.objects.get(pk=pk)
  except Product.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  serializer = ProductSerializer(post)
  return Response(serializer.data)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_add_product_view(request):
  user = request.user
  product = Product(user=user,category=Category.objects.get(pk = request.data['category']))
  serializer = ProductSerializer(instance=product, data=request.data)
  if serializer.is_valid():
     serializer.save()
     return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_product_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if product.user != user:
        return Response({'details': 'You dont have permission to edit this product.'})

    serializer = ProductSerializer(product, data=request.data,partial=True)
    if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_product_view(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if product.user != user:
        return Response({'details': 'You dont have permission to delete this product.'})
   
    operation = product.delete()
    if operation:
        data['success'] = True
    else:
        data['details'] = "Delete failed"
    return Response(data=data)



# class ProductView(GenericAPIView):
#     serializer_class = ProductSerializer

#     def get(self, request):
#         try:
#             posts = Product.objects.all()
#         except Product.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = ProductSerializer(posts,many=True)
#         return Response(serializer.data)


# class SingleProductView(GenericAPIView):
#     serializer_class = ProductSerializer

#     def get(self, request, pk):
#         try:
#             post = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = ProductSerializer(post)
#         return Response(serializer.data)


# class AddProductView(GenericAPIView,CreateModelMixin):
#     serializer_class = ProductSerializer
#     # permission_classes = [IsAuthenticated,]

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save()
#             data = serializer.data
#             return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
