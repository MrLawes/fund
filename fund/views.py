from rest_framework.viewsets import ModelViewSet

from fund.models import Fund
from fund.serializers import FundSerializer


class FundViewSet(ModelViewSet):
    permission_classes = ()
    authentication_classes = ()
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
