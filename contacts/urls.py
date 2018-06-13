from django.urls import path, re_path

from .views import ContactList, ContactDetail, ContactSearch

urlpatterns = [
	path('', ContactList.as_view()),
	path('search/', ContactSearch.as_view()),
	re_path(r'^contacts/(?P<pk>[0-9]+)/$', ContactDetail.as_view())
]
