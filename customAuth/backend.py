from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(email=username)
            if user.check_password(password):
                return user
        except my_user_model.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
