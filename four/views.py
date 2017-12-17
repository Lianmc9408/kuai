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
