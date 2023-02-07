from .models import Publisher, BoardGame
from .serializers import PublisherSerializer, BoardGameSerializer
from rest_framework import permissions, generics, views, response, authentication, mixins
from rest_framework.decorators import permission_classes, authentication_classes
from django import http


@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class PublisherList(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class PublisherDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class PublisherGamesList(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         generics.GenericAPIView):
    def get_object(self, pk):
        try:
            return BoardGame.objects.filter(publisher_id=pk)
        except BoardGame.DoesNotExist:
            raise http.Http404

    def get(self, request, pk, format=None):
        board_games = self.get_object(pk)
        serializer = BoardGameSerializer(board_games, many=True)
        return response.Response(serializer.data)


@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class BoardGameList(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = BoardGame.objects.all()
    serializer_class = BoardGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@authentication_classes([authentication.BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
class BoardGameDetail(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = BoardGame.objects.all()
    serializer_class = BoardGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
