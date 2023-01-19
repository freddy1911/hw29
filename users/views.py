import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
# from psycopg2 import IntegrityError, DatabaseError


from users.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            [{"id": user.pk,
              "first_name": user.first_name,
              "last_name": user.last_name,
              "username": user.username,
              "role": user.role,
              "age": user.age,
              "total_ads": user.total_ads,
              "location": [loc.name for loc in user.location.all()]
              } for user in self.object_list], json_dumps_params={'ensure_ascii': False}, safe=False
        )


class UserDetailView(DetailView):
    model = User

    def get(self, requests, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()],
        }, json_dumps_params={'ensure_ascii': False}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            password=data.get("password"),
            role=data.get("role"),
            age=data.get("age"),
        )

        locations = data.get("locations")

        if locations:
            for loc_name in data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        return JsonResponse(
            {"id": user.pk,
             "first_name": user.first_name,
             "last_name": user.last_name,
             "username": user.username,
             "role": user.role,
             "age": user.age,
             "location": [loc.name for loc in user.location.all()]
             }, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "first_name" in data:
            self.object.first_name = data.get("first_name")
        if "last_name" in data:
            self.object.last_name = data.get("last_name")
        if "username" in data:
            self.object.username = data.get("username")
        if "age" in data:
            self.object.age = data.get("age")

        if "locations" in data:
            self.object.location.all().delete()
            for loc_name in data.get('locations'):
                loc, created = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        return JsonResponse(
            {
                "id": self.object.pk,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "username": self.object.username,
                "role": self.object.role,
                "age": self.object.age,
                "locations": [loc.name for loc in self.object.location.all()]
            }, json_dumps_params={'ensure_ascii': False}, safe=False
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204, safe=False)
