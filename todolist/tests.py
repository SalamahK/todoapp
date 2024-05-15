from django.test import TestCase
from django.urls import reverse
from .models import TodoList, Category
from .forms import CategoryForm

class CategoryFormTestCase(TestCase):
    def test_category_form_valid(self):
        form_data = {'name': 'New Category'}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form_data = {}  # Empty data, should be invalid
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())

class TodoListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some test categories
        cls.category1 = Category.objects.create(name='Category 1')
        cls.category2 = Category.objects.create(name='Category 2')

        # Create some test todos
        cls.todo1 = TodoList.objects.create(title='Todo 1', content='Content 1', due_date='2024-05-01')
        cls.todo2 = TodoList.objects.create(title='Todo 2', content='Content 2', due_date='2024-05-02')
        cls.todo3 = TodoList.objects.create(title='Todo 3', content='Content 3', due_date='2024-05-03')

        # Associate categories with todos
        cls.todo1.categories.add(cls.category1)
        cls.todo1.categories.add(cls.category2)
        cls.todo2.categories.add(cls.category2)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Convert queryset to list of strings for comparison
        todos_str = [str(todo) for todo in response.context['todos']]
        self.assertListEqual(todos_str, ['Todo 1', 'Todo 2', 'Todo 3'])

    def test_category_view(self):
        response = self.client.get(reverse('category'))
        self.assertEqual(response.status_code, 200)
        # Compare queryset against list of primary keys
        category_pks = list(Category.objects.values_list('pk', flat=True))
        self.assertListEqual(list(response.context['categories'].values_list('pk', flat=True)), category_pks)
