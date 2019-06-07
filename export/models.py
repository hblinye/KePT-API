from django.db import models


# Create your models here.
class Meeting(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    skey = models.CharField(max_length=100)
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'export'
        db_table = 'meetings'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    skey = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        app_label = 'export'
        db_table = 'users'


class MeetingUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_meeting'
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='meeting_user'
    )

    class Meta:
        app_label = 'export'
        db_table = 'user_meeting_relationships'


class Thought(models.Model):
    content = models.CharField(max_length=100)
    ttype = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_thought'
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='meeting_thought'
    )
    discussing = models.IntegerField()

    class Meta:
        app_label = 'export'
        db_table = 'thoughts'
