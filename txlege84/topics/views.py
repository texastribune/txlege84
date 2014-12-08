from rest_framework.generics import ListAPIView, RetrieveAPIView

from topics.models import Topic
from topics.serializers import TopicSerializer


class TopicList(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicDetail(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
