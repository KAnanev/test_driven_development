from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class ItemFormTest(TestCase):
    """Тест: Формы для элемента списка."""

    def test_form_renders_text_input(self):
        """Тест: Форма отображает текстовое поле ввода."""
        form = ItemForm()
        self.assertIn('placeholder="Введите элемент списка"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        """Тест: Валидации формы для пустых элементов."""
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_from_save_handles_saving_to_a_list(self):
        """Тест: метод save формы обрабатывает сохранение в список."""
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list, list_)
