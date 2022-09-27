import datetime  # noqa
import time

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from mv.models import Mv


class MvViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Mv.objects.all()
    serializer_class = ModelSerializer

    # download_url = models.CharField(verbose_name='下载地址', max_length=1024)
    # # 需要下载 -》下载中 -》下载完成修改文件名 -》下载完成
    # action = models.CharField(verbose_name='行为', default='需要下载',  max_length=200)

    @action(methods=['get'], detail=False, )
    def get_download_url(self, request, version):
        mv = Mv.objects.filter(action='下载中').first()
        if mv:
            return Response({'msg': f'正在下载：{mv.download_url}', 'download_url': None, })
        mv = Mv.objects.filter(action='需要下载').first()
        if mv:
            return Response({'id': mv.id, 'download_url': mv.download_url, })
        return Response({})

    @action(methods=['put'], detail=True, )
    def set_downloading(self, request, *args, **kargs):
        mv = self.get_object()
        mv.action = '下载中'
        mv.save()

        while 1:
            time.sleep(3)

        return Response({})
