from django.conf.urls import url
from api import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^email/', views.EmailViewSet.as_view({'get': 'list', 'post': 'create'})),
]