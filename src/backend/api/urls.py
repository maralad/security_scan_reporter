from django.urls import path, include
from rest_framework import routers

from api.views import login, nessus_file

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('nessus_file', nessus_file),
    path('login/', login)
]
