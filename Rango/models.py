from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes =  models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


"""
ForeignKey , a field type that allows us to create a one-to-many relationship;
OneToOneField , a field type that allows us to define a strict one-to-one relationship; and
ManyToManyField , a field type which allows us to define a many-to-many relationship.
"""
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
