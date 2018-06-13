from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Contact
from .serializers import ContactSerializer


def paginate(data, page, items_per_page=3):
	paginator = Paginator(data, items_per_page)
	try:
		data = paginator.page(page)
	except (PageNotAnInteger, EmptyPage):
		data = paginator.page(1)
	return data.object_list


class ContactSearch(APIView):
	# noinspection PyMethodMayBeStatic
	def get(self, request):
		q = request.GET.get('q', '')
		contacts = Contact.objects.filter(
			Q(name__icontains=q) | Q(email__icontains=q)
		)
		page = request.GET.get("page", 1)
		current_page_contacts = paginate(contacts, page)

		context = dict(request=request)
		serializer = ContactSerializer(current_page_contacts, context=context, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


# noinspection PyMethodMayBeStatic
class ContactList(APIView):
	def get(self, request):
		contacts = Contact.objects.all()
		context = dict(request=request)
		serializer = ContactSerializer(contacts, context=context, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = ContactSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class ContactDetail(APIView):
	def get(self, request, pk):
		contact = get_object_or_404(Contact, pk=pk)
		serializer = ContactSerializer(contact)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request, pk):
		contact = get_object_or_404(Contact, pk=pk)
		serializer = ContactSerializer(contact, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		contact = get_object_or_404(Contact, pk=pk)
		contact.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
