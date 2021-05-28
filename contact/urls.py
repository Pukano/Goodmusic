from django.conf.urls import url
from . import views # import views so we can use them in urls

urlpatterns = [
    url(r'^$', views.send_mail, name="send_mail"), # "/about" will call the method "index" in "views.py"
    url(r'^success/$', views.success, name="success"),
]
