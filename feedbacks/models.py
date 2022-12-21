from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models


class Feedback(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(validators=(MaxValueValidator(5),))

    def __str__(self):
        return f"{self.text} | {self.user} | {self.rating}"