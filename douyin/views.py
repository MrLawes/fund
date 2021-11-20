import datetime
import uuid

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
            douyinuser = DouYinUser.objects.filter(href__contains=href.split('?')[0]).last()
            if not douyinuser:
                douyinuser = DouYinUser.objects.create(username=uuid.uuid4(), href=href)

            return Response({'id': douyinuser.id})

        return Response({})

    def update(self, request, *args, **kwargs):

        # fens_count
        result = super().update(request, *args, *kwargs)
        print(f"results{result=}")
        fens_count = result.data['fens_count']

        if result.data['username'] in (
                'Jiawen222', 'dyop93f17ipm', 'dy28o1b1jy3w', 'Angela141620', 'dy6kdl4mo0vl', 'lianhua17920',):
            return result

        # 10 天内新增加的，不删除
        if datetime.datetime.now() - result.data['create_at'] > datetime.timedelta(days=10):
            return result

        # 粉丝数量超过 1000 的删除
        if not (10 < fens_count < 1000):
            result.data['need_delete'] = True
        # todo 超过两个星期还没有回关我的删除
        return result
