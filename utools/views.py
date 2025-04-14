# Create your views here.

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class UToolsViewSet(ViewSet):
    permission_classes = ()
    authentication_classes = ()

    @action(methods=['get'], detail=False, )
    def mp(self, request, *args, **kwargs):
        return Response('ffffff')
