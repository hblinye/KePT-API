from rest_framework.generics import ListAPIView
from .serializers import ExportSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Meeting, User, Thought
# Create your views here.


class MeetingExportAPIView(ListAPIView):

    serializer_class = ExportSerializer

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        query_id = 1
        mt = Meeting.objects.filter(
            pk=query_id
        )
        print(mt)
        meeting_users = User.objects.filter(
            user_meeting__meeting_id=mt.first().pk
        )
        print(meeting_users)
        thoughts = Thought.objects.filter(
            meeting_id=mt.first().pk
        )
        print(thoughts)
        return []
