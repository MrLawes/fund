from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from douyin.models import DouYinUser
from douyin.serializers import DouYinUserSerializer


class DouYinUserViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = DouYinUser.objects.all()
    serializer_class = DouYinUserSerializer

    @action(methods=['get'], detail=False, )
    def get_user_by_href(self, request, version):
        print(request.query_params)
        href = request.query_params.get('href')
        if href:
            douyinuser = DouYinUser.objects.filter(href__contains=href).last()
            if douyinuser:
                return Response({'id': douyinuser.id})

        return Response({})
