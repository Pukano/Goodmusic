# from django.urls import path
# from . import views

# app_name = 'about'

# urlpatterns = [
#     path('', views.aboutus, name="aboutus"),
# ]

from django.conf.urls import url
from . import views # import views so we can use them in urls

urlpatterns = [
    url(r'^$', views.aboutus, name="aboutus"), # "/about" will call the method "index" in "views.py"
]
