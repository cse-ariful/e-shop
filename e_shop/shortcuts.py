from account.models import UserModel


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def get_user_or_none(self, **kwargs):
    try:
        return UserModel.objects.get(**kwargs)
    except UserModel.DoesNotExist:
        return None