from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time

class NewVisitorTest(LiveServerTestCase):
    ''' Тест нового посетителя. '''

    def setUp(self):
        ''' Установка. '''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        ''' Демонтаж. '''
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        ''' Подтверждение строки в таблице списка. '''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrive_it_later(self):
        ''' Тест: Можно начать список и получить его позже. '''
        # Эдит слышала про крутое онлайн-приложение со списком
        # неотложных дел. Она решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        # Она набирает в текстовом поле "Купить павлиньи перья" (её хобби -
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлинья перьи" в качестве элемента списка.
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Купить павлиньи перья')


        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обнавляется и теперь показывает оба элемента ее списка
        self.check_for_row_in_list_table('1: Купить павлиньи перья')
        self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')


        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что сайт
        # сгенерировал для неё уникальный URL-адрес - об этом
        # выводится небольшой текст с объяснениями.
        self.fail('Закончить тест')

        # Она посещает этот URL-адрес - ее список по-прежнему там.

        # Удовлетворенная, он снова ложится спать