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

    @action(methods=['get'], detail=False, )  # todo 暂时用不到
    def user_id_by_douyin_no(self, request, pk, version):
        return Response({'id': 3})
