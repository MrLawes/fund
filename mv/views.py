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

    @action(methods=['get'], detail=False, )
    def sleep(self, request, version):
        time.sleep(6)
        return Response({})

    @action(methods=['put'], detail=True, )
    def set_downloading(self, request, *args, **kargs):
        data = self.request.data
        name = data.get('name', '').split('\n')[0]  # 'F.I.R.飞儿乐团 歌曲选集 - 你的微笑\n\n下载视频视频封面\n\n清空'
        href = data.get('href', '')
        # if not href:
        #     return Response({})
        #
        # with open(f'{str(str(settings.BASE_DIR))}/{name}.mp4', 'wb') as f:
        #     f.write(requests.get(href).content)

        mv = self.get_object()
        mv.action = '下载完成'
        if not mv.name:
            mv.name = name
        mv.save()
        # https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/84/07/170000784/170000784-1-208.mp4?e=ig8euxZM2rNcNbhghbdVhwdlhzNghwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1664306611&gen=playurlv2&os=vcache&oi=1866715013&trid=000181e5e9674df84916b52ee5131e882c94T&mid=0&platform=html5&upsig=c6ec70061bb17240be828558796fbcd9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=5177&bvc=vod&nettype=0&bw=323300&orderid=0,1&logo=80000000
        return Response({})
