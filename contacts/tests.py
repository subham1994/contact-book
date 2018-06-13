from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from contacts.models import Contact


class ContactModelTestCase(TestCase):
	def setUp(self):
		self.name = 'test'
		self.email = 'test@test.com'

	def test_can_create_a_contact(self):
		old_count = Contact.objects.count()
		contact = Contact(name=self.name, email=self.email)
		contact.save()
		new_count = Contact.objects.count()
		self.assertEqual(old_count + 1, new_count)


class ContactsListViewTestCase(TestCase):
	def setUp(self):
		self.url = "/"
		self.user = User.objects.create(username="test")
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_can_post_a_contact(self):
		name, email = "admin", "test@admin.com"
		contact = dict(name=name, email=email)
		response = self.client.post(self.url, contact, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_can_fetch_all_contacts(self):
		name, email = "test", "test@test.com"
		contact = Contact(name=name, email=email)
		contact.save()

		response = self.client.get(self.url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]["name"], name)


class ContactsDetailViewTestCase(TestCase):
	def setUp(self):
		self.name = 'test'
		self.email = 'test@test.com'
		self.url = "/contacts/1/"
		self.contact = Contact(name=self.name, email=self.email)
		self.user = User.objects.create(username="test")
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		self.contact.save()

	def test_can_fetch_a_contact(self):
		response = self.client.get(self.url, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], self.name)

	def test_can_update_a_contact(self):
		update = dict(name="test123", email="test@test.com")
		response = self.client.put(self.url, update, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], update["name"])

	def test_can_delete_a_contact(self):
		response = self.client.delete(self.url, format='json', follow=True)
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class ContactsSearchViewTestCase(TestCase):
	def setUp(self):
		self.url = "/search/?q={}"

		user = User.objects.create(username="test")
		self.client = APIClient()
		self.client.force_authenticate(user=user)

		self.first_contact = Contact(name="test abc", email="test@test.com")
		self.second_contact = Contact(name="admin", email="test@email.com")

		self.first_contact.save()
		self.second_contact.save()

	def test_can_search_by_name(self):
		q = "abc"
		response = self.client.get(self.url.format(q), format='json', follow=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]["name"], self.first_contact.name)

	def test_can_search_by_email(self):
		q = "email"
		response = self.client.get(self.url.format(q), format='json', follow=True)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]["email"], self.second_contact.email)
