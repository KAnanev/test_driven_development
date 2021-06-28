from django.test import TestCase

class HomePageTest(TestCase):
	''' Тест домашней страницы. '''

	def test_uses_home_template(self):
		''' Тест: Используется домашний шаблон. '''

		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		''' Тест: Можно сохранить post-запрос. '''

		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')