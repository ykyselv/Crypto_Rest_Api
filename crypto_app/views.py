from django.forms import model_to_dict
from rest_framework import generics, viewsets
from .models import Crypto, Comment
from rest_framework.response import Response
from .serializers import CryptoSerializer, CommentSerializer, UserSerializer
from rest_framework.views import APIView
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User




class UserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CryptoAPIView(generics.ListAPIView):
    serializer_class = CryptoSerializer

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        curr = self.request.query_params.get("curr")
        crypt = self.request.query_params.get("crypt")
        year_created = self.request.query_params.get("year")
        month_created = self.request.query_params.get("month")
        day_created = self.request.query_params.get("day")
        hour_created = self.request.query_params.get("hour")
        minute_created = self.request.query_params.get("min")

        if curr or crypt:
            if year_created and not month_created and not day_created and not hour_created and not minute_created:
                    return (Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created))

            elif year_created and month_created and not day_created and not hour_created and not minute_created:
                return(Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                            time_create__month=month_created))

            elif year_created and month_created and day_created and not hour_created and not minute_created:
                return (Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                              time_create__month=month_created,
                                              time_create__day=day_created))

            elif year_created and month_created and day_created and hour_created and not minute_created:
                return (Crypto.objects.filter(curr=curr, cp_curr=crypt,time_create__year=year_created,
                                              time_create__month=month_created,
                                              time_create__day=day_created, time_create__hour=hour_created))

            elif year_created and month_created and day_created and hour_created and minute_created:
                return (Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                                  time_create__month=month_created,
                                                  time_create__day=day_created, time_create__hour=hour_created,
                                                  time_create__minute=minute_created))

            else:
                return (Crypto.objects.filter(curr=curr, cp_curr=crypt))

        else:
            return (Crypto.objects.all())



class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if pk:
            return Response({'post': "Method POST not allowed"})
        if not pk:
            new_comment = Comment.objects.create(
                title=request.data['title'],
                content=request.data['content'],
                cat_id=request.user.id
            )
            return Response({'post': model_to_dict(new_comment)})


    def update(self, request, *args, **kwargs):

        pk = kwargs.get("pk", None)

        if not pk:
            return Response({'put': "Method PUT not allowed"})
        else:
            try:
                update_comment = Comment.objects.get(id=pk)
                if update_comment.cat_id == request.user.id:
                    update_comment.title = request.data['title']
                    update_comment.content = request.data['content']
                    update_comment.cat_id = request.user.id
                    update_comment.save()
                    return Response({'put': model_to_dict(update_comment)})
                else:
                    return Response({'error': "You can update only your comments"})
            except:
                return Response({'error': "Object does not exists"})


    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'put': "Method DELETE not allowed"})
        else:
            try:
                update_comment = Comment.objects.get(id=pk)
                if update_comment.cat_id == request.user.id:
                    update_comment.delete()
                    return Response({'delete': "Объект успешно удалён"})
                else:
                    return Response({'error': "You can delete only your comments"})
            except:
                return Response({'error': "Object does not exists"})



class AverageAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        curr = request.GET.get("curr")
        crypt = request.GET.get("crypt")
        year_created = request.GET.get("year")
        month_created = request.GET.get("month")
        day_created = request.GET.get("day")
        hour_created = request.GET.get("hour")

        if curr and crypt:
            # среднее за всё время:
            if not year_created and not month_created and not day_created:
                return Response(Crypto.objects.filter(curr=curr, cp_curr=crypt).aggregate(Avg('price')))

            # среднее за год:
            elif year_created and not month_created and not day_created:
                return Response(Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created).aggregate(Avg('price')))

            # среднее за месяц:
            elif year_created and month_created and not day_created:
                return Response(Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                                      time_create__month=month_created).aggregate(Avg('price')))
            # среднее за день:
            elif year_created and month_created and day_created:
                return Response(Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                                      time_create__month=month_created,
                                                      time_create__day=day_created).aggregate(Avg('price')))

            # среднее за час:
            elif year_created and month_created and day_created and hour_created:
                return Response(Crypto.objects.filter(curr=curr, cp_curr=crypt, time_create__year=year_created,
                                                      time_create__month=month_created,
                                                      time_create__day=day_created,
                                                      time_create__hour=hour_created).aggregate(Avg('price')))

        else:
            return Response({"error": "Please, enter currency and cryptocurrency for find the average"})






