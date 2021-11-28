from django.db import models


# Create your models here.
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    task_type = models.SmallIntegerField()
    obj = models.JSONField(blank=True, null=True)
    priority = models.SmallIntegerField()
    description = models.CharField(max_length=256)
    task_status = models.SmallIntegerField()
    task_progress = models.CharField(max_length=128)
    tmp_info = models.JSONField(blank=True, null=True)
    last_executed_at = models.DateTimeField()
    msg = models.CharField(max_length=256)
    notify = models.IntegerField()
    deleted = models.IntegerField()
    # deleted_at = models.DateTimeField()
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'task'


class TiktokComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.CharField(max_length=32)
    comment_id = models.CharField(unique=True, max_length=32)
    content = models.JSONField(blank=True, null=True)
    comment_at = models.DateTimeField()
    comment_username = models.CharField(max_length=128)
    portrait_url = models.CharField(max_length=512)
    comment_liked_count = models.IntegerField()
    sort_number = models.IntegerField()
    is_author_reply = models.IntegerField()
    is_author_like = models.IntegerField()
    comment_commented_count = models.IntegerField()
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment'
