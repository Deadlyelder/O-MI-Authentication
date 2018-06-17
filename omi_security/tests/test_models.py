from django.test import TestCase

# Create your tests here.
from security_node.models import Group

class GroupModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Group.objects.create(group_name='Mygroup')


    def test_group_name_label(self):
        group = Group.objects.get(id=1)
        field_label = group._meta.get_field('group_name').verbose_name
        self.assertEquals(field_label, 'group name')

    def test_group_name_max_length(self):
        group = Group.objects.get(id=1)
        max_length = group._meta.get_field('group_name').max_length
        self.assertEquals(max_length, 200)

