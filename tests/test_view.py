from laborprotection import app

class TestViews:
    
    def setup(self):
        # print('запуск')
        # app.testing = True
        self.client = app.test_client()
    def test_information(self):
        response = self.client.get('/information')
        assert response.status_code == 200
    
    def test_arm(self):
        response = self.client.get('/arm')
        assert response.status_code == 200   
       
    def test_login(self):
      response = self.client.get('/login')
      assert response.status_code == 200
      
    def test_admin(self):
      response = self.client.get('/admin')
      assert response.status_code == 200  
      
    def test_training(self):
      response = self.client.get('/training')
      assert response.status_code == 200
      
    def test_add_training(self):
      response = self.client.get('/add_training/new/')
      assert response.status_code == 200  
    
    def test_place(self):
      response = self.client.get('/place')
      assert response.status_code == 200 

    def add_place(self):
      response = self.client.get('/place/new/')
      assert response.status_code == 200   
#
    def program(self):
      response = self.client.get('/program')
      assert response.status_code == 200 

    def add_program(self):
      response = self.client.get('/program/new/')
      assert response.status_code == 200 

    def view_report(self):
      response = self.client.get('/view_report')
      assert response.status_code == 200  

       
    def tesrdownelf():
          # print('Конец')
          pass
