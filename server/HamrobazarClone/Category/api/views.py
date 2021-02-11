from .serializer import CategorySerializer
from ..models import Category
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', ])
def api_caregories_view(request):
  try:
      catogories = Category.objects.all()
  except Category.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  serializer = CategorySerializer(catogories,many=True)
  return Response(serializer.data)


@api_view(['GET', ])
def api_single_category_view(request,pk):
  try:
      category = Category.objects.get(pk=pk)
  except Category.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

  serializer = CategorySerializer(category)
  return Response(serializer.data)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_add_category_view(request):
  user = request.user
  if request.method == 'POST':
      serializer = CategorySerializer(data=request.data)
      data = {}
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_update_category_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if category.user != user:
        return Response({'response': 'You dont have permission to edit this category.'})

    serializer = CategorySerializer(category, data=request.data,partial=True)
    data = {}
    if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_category_view(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {}
    user = request.user
    if category.user != user:
        return Response({'response': 'You dont have permission to delete this category.'})
   
    operation = category.delete()
    if operation:
        data['success'] = 'Deleted Successfully'
    else:
        data['failure'] = 'Delete failed'
    return Response(data=data)


