from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    """Форма для элемента списка."""
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(
                attrs={
                    'placeholder': 'Введите элемент списка',
                    'class': 'form-control input-lg',
                }
            )
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
