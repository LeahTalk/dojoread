from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^add_book_and_review$', views.add_book_and_review),
    url(r'^$', views.index),
    url(r'^add$', views.add_book),
    url(r'^delete/(?P<review_id>\d+)$', views.delete_review),
    url(r'^(?P<book_id>\d+)$', views.show_book),
]
