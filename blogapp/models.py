from django.db import models

# Create your models here.
class Author (models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.name


class Category (models.Model):
    name = models.CharField(max_length=40)


class Tag (models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article (models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
