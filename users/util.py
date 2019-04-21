from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, roll_num, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # if not roll_num:
        #     raise ValueError('The given roll number must be set')
        user = self.model(roll_num=roll_num, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
       


    def create_user(self, roll_num, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(roll_num, password, **extra_fields)

    def create_superuser(self, roll_num, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(roll_num, password, **extra_fields)