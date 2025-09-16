from django.db import models

class Subject(models.Model):
    code = models.CharField(max_length=10, unique = True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, blank = True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"