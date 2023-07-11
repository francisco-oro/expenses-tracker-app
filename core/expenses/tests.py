# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.urls import reverse
# from datetime import datetime, timedelta
# from .models import Expense


# class TimelineExpensesTrackerTestCase(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.expense1 = Expense.objects.create(owner=self.user, amount=10, date=datetime.now(), description='Test', category='Test')
#         self.expense2 = Expense.objects.create(owner=self.user, amount=20, date=datetime.now() - timedelta(days=1),description='Test', category='Test')
#         self.expense3 = Expense.objects.create(owner=self.user, amount=30, date=datetime.now() - timedelta(days=2),description='Test', category='Test')

#     def test_weekly_report(self):
#         url = reverse('expenses-tracker',args=[30]) 
#         response = self.client.get(url, follow=True)
        
#         current_date = datetime.now()
#         from_date = current_date - timedelta(days=7)

        

#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             'count': [0, 0, 60],
#             'tags': [datetime.now() , 'Yesterday', '2 days ago']
#         })


#     def test_negative_case(self):
#         url = reverse('expenses-tracker')
#         response = self.client.get(url, {'opt': 'invalid'}, follow=True)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.content.decode(), 'You must provide a valid days count')


#     def test_boundary_case(self):
#         url = reverse('expenses-tracker')
#         response = self.client.get(url, {'opt': 1}, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             'count': [10],
#             'tags': ['Today']
#         })


#     def test_edge_case(self):
#         url = reverse('expenses-tracker')
#         response = self.client.get(url, {'opt': 31}, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             'count': [0, 0, 60, 0],
#             'tags': ['Today', 'Yesterday', '2 days ago', '3 days ago']
#         })

#     def test_corner_case(self):
#         url = reverse('expenses-tracker')
#         response = self.client.get(url, {'opt': 60}, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertJSONEqual(response.content, {
#             'count': [0, 0, 60, 0, 0, 0],
#             'tags': ['Today', 'Yesterday', '2 days ago', '3 days ago', '4 days ago', '5 days ago']
#         })
    
#     def test_last_case(self):
#         url = reverse('expenses-tracker')
#         print(url)