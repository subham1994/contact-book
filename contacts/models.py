from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=100, db_index=True)
	email = models.EmailField(db_index=True, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.name} <{self.email}>"
