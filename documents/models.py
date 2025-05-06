from django.db import models


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    rubrics = models.JSONField()
    text = models.TextField()
    created_date = models.DateTimeField()

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"Document {self.id} - {self.created_date}"
