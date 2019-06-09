from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db.models import F
from .serializers import ExportSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from .models import Meeting, User, Thought, MeetingUser
from drf_renderer_xlsx.renderers import XLSXRenderer
from drf_renderer_xlsx.mixins import XLSXFileMixin
import json
# Create your views here.


class MeetingExportAPIView(XLSXFileMixin, ListAPIView):

    serializer_class = ExportSerializer

    parser_classes = (JSONParser, )

    renderer_classes = (XLSXRenderer, JSONRenderer)
    column_header = {
        'titles': [
            "NAME",
            "KEEP",
            "PROBLEM",
            "TRY"
        ],
        'column_width': [17, 30, 30, 30],
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            }
        },
        'height': 40,
    }

    def _auth(self, key):
        try:
            self.request._access_user = User.objects.get(
                skey=key
            )
        except User.DoesNotExist:
            raise PermissionDenied

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        access_key = self.kwargs.get('key')
        self._auth(access_key if access_key else self.request.data.get('AUTH-KEY', None))
        request._export_meeting_user = self._validate_meeting_user()
        super().initial(request, *args, **kwargs)

    def _get_request_meeting_key(self):
        meeting_key = self.request.query_params.get('meeting_key', None)
        meeting_key = meeting_key if meeting_key else self.request.data.get('meeting_key', None)

        if not meeting_key:
            raise ValidationError('need meeting key')
        return meeting_key

    def _validate_meeting_user(self):
        try:
            meeting_key = self._get_request_meeting_key()
            meeting = MeetingUser.objects.get(
                user=self.request._access_user,
                meeting__skey=meeting_key
            )
            return meeting
        except MeetingUser.DoesNotExist:
            raise ValidationError('Meeting not exists')

    def get_queryset(self):
        thoughts = Thought.objects.filter(
            meeting_id=self.request._export_meeting_user.meeting_id
        ).annotate(name=F('user__name'))
        response_dict = dict()
        target_list = ['_keep', '_problem', '_try']
        for thought in thoughts:
            if thought.name not in response_dict:
                response_dict[thought.name] = dict(
                    _keep=[],
                    _problem=[],
                    _try=[]
                )
            response_dict[thought.name][target_list[thought.ttype - 1]].append('#' + thought.content)
        response_list = []
        for k, v in response_dict.items():
            response_list.append(dict(
                name=k,
                _keep='\n'.join(v.get('_keep', [])),
                _problem='\n'.join(v.get('_problem', [])),
                _try='\n'.join(v.get('_try', []))
            ))
        return response_list
