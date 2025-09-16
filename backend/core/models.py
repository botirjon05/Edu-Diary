from django.db import models

class Subject(models.Model):
    code = models.CharField(max_length=20, unique = True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, blank = True, null=True)
    description = models.TextField(blank = True)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"