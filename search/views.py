from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from export.models import User, Meeting
from .serializer import MeetingSearchSerializer


# Create your views here.
class MeetingSearchAPIView(ListAPIView):

    serializer_class = MeetingSearchSerializer

    def _auth(self, key):
        try:
            self.request._access_user = User.objects.get(
                skey=key
            )
        except User.DoesNotExists:
            raise PermissionDenied

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        self._auth(kwargs['key'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return Meeting.objects.filter(
            meeting_user__user=self.request._access_user
        )
