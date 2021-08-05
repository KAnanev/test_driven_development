from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class HomePageTest(TestCase):
	"""Тест домашней страницы."""

	def test_uses_home_template(self):
		"""Тест: Используется домашний шаблон."""
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_home_page_uses_item_form(self):
		"""Тест: Домашняя страница страница использует форму для элемента."""
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):
	"""Тест нового списка"""

	def test_can_save_a_POST_request(self):
		"""Тест: Можно сохранить post-запрос."""
		self.client.post('/lists/new', data={'text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		""" Тест: переадресует после post-запроса.  """
		response = self.client.post('/lists/new', data={'text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_for_invalid_input_renders_home_template(self):
		"""Тест на допустимый ввод: отображает домашний шаблон."""
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')

	def test_validation_errors_are_shown_on_home_page(self):
		"""Тест: ошибки валидации выводятся на домашней странице."""
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_invalid_input_passes_form_to_template(self):
		"""Тест на недопустимый ввод: форма передается в шаблон"""
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_invalid_list_items_arent_saved(self):
		"""Тест: Сохраняются недопустимые элементы списка"""
		self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)

	def test_displays_item_form(self):
		"""Тест отображения формы для элемента."""
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertIsInstance(response.context['form'], ItemForm)
		self.assertContains(response, 'name="text"')

class ListViewTest(TestCase):
	"""Тест: Представление списка."""

	def test_uses_list_templates(self):
		"""Тест: Используется шаблон списка."""
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_passes_correct_list_to_template(self):
		""" Тест: Передается правильный шаблон списка. """
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_displays_all_items(self):
		""" Тест: Отображаются все элементы списка. """
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='другой элемент 1 списка', list=other_list)
		Item.objects.create(text='другой элемент 2 списка', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'другой элемент 1 списка')
		self.assertNotContains(response, 'другой элемент 2 списка')

	def test_can_save_a_POST_request_to_an_existing_list(self):
		""" Тест: Можно сохранить post-запрос в существующий список """
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/',
			data={'text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		""" Тест: Переадресуется в представление списка. """

		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/',
			data={'text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')

	def post_invalid_input(self):
		"""Отправляет недопустимый ввод."""
		list_ = List.objects.create()
		return self.client.post(
			f'/lists/{list_.id}/',
			data={'text': ''}
		)

	def test_for_invalid_input_nothing_saved_to_db(self):
		"""Тест недопустимый ввод не сохраняется в БД."""
		self.post_invalid_input()
		self.assertEqual(Item.objects.count(), 0)

	def for_invalid_input_renders_list_template(self):
		"""Тест на недопустимый ввод: отображается шаблон списка."""
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		"""Тест на недопустимый ввод: форма передается в шаблон."""
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_for_invalid_input_shows_error_on_page(self):
		"""Тест на недопустимый ввод: на странице показывается ошибка."""
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

