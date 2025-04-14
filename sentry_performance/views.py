# Create your views here.
import os

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SentryUserViewSet(ViewSet):
    permission_classes = ()
    authentication_classes = ()

    @action(methods=['get'], detail=False, )
    def user(self, request, *args, **kwargs):  # noqa
        x_request_id = self.request.query_params.get('X-Request-Id')
        if ';' in x_request_id or '(' in x_request_id:
            return Response('非法', status=400, )
        p1_command = f'ssh p1 "cd /var/www/lls_saas_api/;source venv/bin/activate;python manage.py aliyun_sls --settings=settings.production -q {x_request_id}"'
        sls_log = os.popen(p1_command).read()
        user = ([log for log in sls_log.split(' - ') if x_request_id in log] + ['', ])[0]
        if 'user-' in user:
            user = user.split('user-')[-1]
        return Response(user)
