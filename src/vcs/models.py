from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=6, primary_key=True)
    lectures = models.ManyToManyField('Lecture')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=250)
    type = models.CharField(max_length=20)
    date_registered = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)

    university_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    teacher_lectures = models.ManyToManyField('Lecture', blank=True)

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    USERNAME_FIELD = 'email'
    object = UserManager()


class Lecture(models.Model):
    text = models.TextField()
    version = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField()
    pack = models.ForeignKey('LecturePack', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    original_lecture = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('version', 'original_lecture')


class LecturePack(models.Model):
    pack_name = models.CharField(max_length=150, primary_key=True)
    description = models.CharField(max_length=150)


class LectureComment(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LectureActivity(models.Model):
    view_count = models.IntegerField(default=0)
    like = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)


class TotalLectureActivities(models.Model):
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
