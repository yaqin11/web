from django.db import models


# Create your models here.
class InsLink(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_type = models.SmallIntegerField()
    from_user = models.CharField(max_length=128)
    to_user = models.CharField(max_length=128)
    weight = models.IntegerField()
    last_seen_at = models.DateTimeField()
    deleted = models.IntegerField()
    # deleted_at = models.DateTimeField()
    # created_at = models.DateTimeField()
    # updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ins_link'
        unique_together = (('link_type', 'from_user', 'to_user'),)
