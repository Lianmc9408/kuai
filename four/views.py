from django.shortcuts import render, HttpResponse
from four import models


# Create your views here.
def index(request):
    result = models.MVinfo.objects.all()
    return render(request, "index.html", {'result': result})


def tencentindex(request):
    queryset = models.Artical.objects.all()
    # queryset = models.Artical.objects.values_list("a_id", "title", "artical")

    # 方式1：
    # data = []
    # for item in queryset:
    #     p_tmp = {
    #         "title": item.title,
    #         "cover_url": item.cover_url.images_url
    #     }
    #     data.append(p_tmp)

    # 方式2：
    # data = []
    # from django.forms.models import model_to_dict
    # for item in queryset:
    #     data.append(model_to_dict(item))

    # import json
    # return HttpResponse(json.dumps(data), content_type="application/json")

    # 方式3：
    # from django.core import serializers
    # data = serializers.serialize("json", queryset)
    # return HttpResponse(data, content_type="application/json")

    # 方式4： restframework
    from four import serializers
    import json
    serializer = serializers.ArticalSerialzer(queryset, many=True)
    return HttpResponse(json.dumps(serializer.data), content_type="application/json")


def serializers_ind(request):
    p1 = {"title": "asdasdasd", "a_id": "asdasdasd", "artical": "as56d46a1sd6as1d6a",
          "cover_url": "https://asdasd.asdasd.com"}
    from four import serializers
    serializer = serializers.ArticalSerialzer(data=p1)
    print(serializer.is_valid())
    print(serializer.validated_data)
    serializer.save()
    return HttpResponse("asdasd")


# 请求和响应
from rest_framework.decorators import api_view
from rest_framework.response import Response
from four import serializers


@api_view(['GET', 'POST'])
def artical_list(request):
    if request.method == 'GET':
        queryset = models.Artical.objects.all()
        serializer = serializers.ArticalSerialzer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = serializers.ArticalSerialzer(data=request.data)
        from rest_framework import status
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def artical_detail(request, pk):
    from rest_framework import status
    try:
        artical = models.Artical.objects.get(pk=pk)
    except models.Artical.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.ArticalSerialzer(artical)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.ArticalSerialzer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artical.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 视图
from rest_framework.views import APIView


class ArticalList(APIView):
    def get(self, request, format=None):
        artical = models.Artical.objects.all()
        serializer = serializers.ArticalSerialzer(artical, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        from rest_framework import status
        serializer = serializers.ArticalSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticalDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return models.Artical.objects.get(pk=pk)
        except models.Artical.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get(self, request, pk, format=None):
        artical = self.get_object(pk)
        serializer = serializers.ArticalSerialzer(artical)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        artical = self.get_object(pk)
        serializer = serializers.ArticalSerialzer(artical, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        from rest_framework import status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        artical = self.get_object(pk)
        artical.delete()
        from rest_framework import status
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import mixins
from rest_framework import generics


class ListMixin(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    queryset = models.Artical.objects.all()
    serializer_class = serializers.ArticalSerialzer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DetailMixin(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = models.Artical.objects.all()
    serializer_class = serializers.ArticalSerialzer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


from rest_framework import permissions
from four import permissions as per


class ListGenerics(generics.ListCreateAPIView):
    queryset = models.Artical.objects.all()
    serializer_class = serializers.ArticalSerialzer
    # 不需要登录也可以使用api
    permission_classes = ()
    # permission_classes = (permissions.IsAuthenticated)
    # permission_classes = (permissions.IsAuthenticated, per.IsOwnerOrReadOnly)


class DetailGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Artical.objects.all()
    serializer_class = serializers.ArticalSerialzer
    # permission_classes = ()
    # permission_classes = (permissions.IsAuthenticated)
    permission_classes = (permissions.IsAuthenticated, per.IsOwnerOrReadOnly)

# https://q1mi.github.io/Django-REST-framework-documentation