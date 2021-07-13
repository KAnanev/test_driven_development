from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
	""" Тест домашней страницы. """

	def test_uses_home_template(self):
		""" Тест: Используется домашний шаблон. """

		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):
	""" Тест нового списка """

	def test_can_save_a_POST_request(self):
		""" Тест: Можно сохранить post-запрос. """

		self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		""" Тест: переадресует после post-запроса.  """

		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
	""" Тест нового элемента списка """

	def test_can_save_a_POST_request_to_an_existing_list(self):
		""" Тест: Можно сохранить post-запрос в существующий список """

		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		""" Тест: Переадресуется в представление списка. """

		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListViewTest(TestCase):
	""" Тест: Представление списка. """

	def test_uses_list_templates(self):
		""" Тест: Используется шаблон списка. """

		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_passes_correct_list_to_template(self):
		""" Тест: Передается правильный шаблон списка. """

		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_displays_all_items(self):
		""" Тест: Отображаются все элементы списка. """
		correct_list = List.objects.create()
		Item.objects.create(text='item 1', list=correct_list)
		Item.objects.create(text='item 2', list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text='другой элемент 1 списка', list=other_list)
		Item.objects.create(text='другой элемент 2 списка', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'item 1')
		self.assertContains(response, 'item 2')
		self.assertNotContains(response, 'другой элемент 1 списка')
		self.assertNotContains(response, 'другой элемент 2 списка')


class ListAndItemModelTest(TestCase):
	""" Тест модели элемента списка """

	def test_saving_and_retrieving_item(self):
		""" Тест: Сохранение и получение элементов списка """

		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'Первый (самый) элемент списка'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Элемент второй'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'Первый (самый) элемент списка')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Элемент второй')
		self.assertEqual(second_saved_item.list, list_)
