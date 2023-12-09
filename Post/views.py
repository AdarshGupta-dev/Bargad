from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.views import APIView

from Post.Serializers import PostSerializer


class PostCreateView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.student)
            return redirect(reverse('social-media:homepage'))

        # todo: add error message
