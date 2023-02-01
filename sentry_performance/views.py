# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


# ssh p1 "cd /var/www/lls_saas_api/;source venv/bin/activate;python manage.py aliyun_sls --settings=settings.production -q e41546bc-0858-4e14-8c80-df7fcfe2f391#3619213"


class SentryUserViewSet(ViewSet):
    permission_classes = ()
    authentication_classes = ()

    @action(methods=['get'], detail=False, )
    def user(self, request, *args, **kwargs):  # noqa
        return Response('ddddddd')
