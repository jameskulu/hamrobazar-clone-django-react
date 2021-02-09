from django.shortcuts import render
from .serializer import ProductSerializer
from ..models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_products_view(request):
  try:
      posts = Product.objects.all()
  except Product.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  serializer = ProductSerializer(posts,many=True)
  return Response(serializer.data)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_add_product_view(request):
  user = request.user
  product = Product(user=user)
  if request.method == 'POST':
      serializer = ProductSerializer(product, data=request.data)
      data = {}
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_product_view(request, pk):
    try:
        post = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if post.user.user != user:
        return Response({'response': 'You dont have permission to edit this product.'})
    if request.method == 'PUT':
        serializer = ProductSerializer(post, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = 'update successfully'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_product_view(request, pk):
    try:
        post = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if post.user.user != user:
        return Response({'response': 'You dont have permission to delete this product.'})
    if request.method == 'DELETE':
        operation = post.delete()
        if operation:
            data['success'] = 'Deleted Successfully'
        else:
            data['failure'] = 'Delete failed'
        return Response(data=data)

