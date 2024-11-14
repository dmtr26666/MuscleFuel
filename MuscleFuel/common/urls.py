from django.urls import path
from MuscleFuel.common import views
from MuscleFuel.common.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]