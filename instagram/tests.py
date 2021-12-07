from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Profile, Comments

# Create your tests here.


class ProfileTestClass(TestCase):

  def setUp(self):
    self.user = User.objects.create_user("Ngetich", "g1234")
    self.profile_test = Profile(
        photo='http://res.cloudinary.com/drroulnbj/image/upload/v1638812127/hb02gqvdifedppgdxeyp.jpg', bio='profile', user=self.user)
    self.profile_test.save()

  def test_instance_true(self):
    self.profile_test.save()
    self.assertTrue(isinstance(self.profile_test, Profile))


class TestCommentsClass(TestCase):

  def setUp(self):
    self.test_user = User(username='Ter')
    self.test_user.save()
    self.photo = Image(image='photo.png', name='Tiger',
                       caption='A vicious tiger', user=self.test_user)
    self.comments = Comments(comment='Beautiful tiger',
                             photo=self.photo, user=self.test_user)


class TestImageClass(TestCase):

  def setUp(self):

    self.test_user = User(username='Ter')
    self.test_user.save()
    self.photo = Image(photo='ter.jpeg', name='Ter',
                       caption='TerPhoto', user=self.test_user)
    self.comments = Comments(
        comment='Awesome', photo=self.photo, user=self.test_user)

  def test_instance(self):
    self.assertTrue(isinstance(self.photo, Image))


def test_display_images(self):
    self.image.save_image()
    self.image1 = Image(image='gidz.png', name='gidz',
                        caption='hello gidz', user=self.test_user)
    self.image1.save_image()
    dt = Image.display_images()
    self.assertEqual(len(dt), 2)

def test_save_image(self):
    self.image.save_image()
    image = Image.objects.all()
    self.assertTrue(len(image)>0)

def test_search(self):
    self.image.save_image()
    self.image1 = Image(image = 'gidz.png',name = 'gidz',caption = 'hello gidz',user = self.test_user)
    self.image1.save_image()
    search_term = "e"
    search1 = Image.search_images(search_term)
    search2 = Image.objects.filter(name__icontains = search_term)
    self.assertEqual(len(search2),len(search1))

def test_delete_photo(self):
    self.image1 = Image(photo = 'gidz.png',name = 'gidz',caption = 'hello gidz',user = self.test_user)
    self.image1.save_image()
    self.image.save_image()
    self.image.delete_image()
    images = Image.objects.all()
    self.assertEqual(len(images),1)