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
    p1 = {"title": "asdasdasd", "a_id": "asdasdasd", "artical": "as56d46a1sd6as1d6a"}
    from four import serializers
    serializer = serializers.ArticalSerialzer(data=p1)
    print(serializer.is_valid())
    print(serializer.validated_data)
    # serializer.save()
    return HttpResponse("asdasd")


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