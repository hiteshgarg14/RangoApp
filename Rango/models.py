from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

"""
"how do i create a slug in django" turns into "how-do-i-create-a-slug-in-django"
User object (located at django.contrib.auth.models.User ) is considered to be the core of
Djangos authentication system
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes =  models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

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
