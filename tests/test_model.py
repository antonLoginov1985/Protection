# Задайте URL вашей формы
from laborprotection import app
FORM_URL = '/place/new/'  

# Данные для заполнения формы
valid_data = {

    "name": "ООО Рога и копыта",
    "address": "Комсомольская 10"
    # "is_training": True,
    # "is_certification": False
}

invalid_data = {
    "name": "",
    "address": "Комсомольская 10",
    "is_training": True,
    "is_certification": False
}

class TestPlace:
    
    def setup(self):
        # print('запуск')
        # app.testing = True
        self.client = app.test_client()


    def test_valid_form_submission(self):
        response = self.client.post(FORM_URL, data=valid_data)
                
    # Проверяем, что статус ответа 201 (Создано)
        assert response.status_code == 302
    # Проверяем текст ответа
       


    def test_invalid_form_submission(self):
        response = self.client.post(FORM_URL, data=invalid_data)
    # Проверяем, что статус ответа 400 (Неправильный запрос)
        assert response.status_code == 400
    # Проверяем текст ошибки
        assert response.json.get("error") == "Place name is required"





