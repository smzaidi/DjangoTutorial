import datetime

from django.db import models
from django.utils import timezone
import binascii
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from polls.rep_settings import INSTALLED_APPS
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def choices(self):
        if not hasattr(self, '_choices'):
            self._choices = self.choice_set.all()
        return self._choices

    def max_voted_choice(self):
        if not hasattr(self, '_max_voted_choice'):
            choices = self.choice_set.order_by('-votes')
            if not choices:
                self._max_voted_choice = None
            else:
                self._max_voted_choice = choices[0]
        return self._max_voted_choice



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True)


    def __str__(self):
        return self.choice_text

# @python_2_unicode_compatible
class StaticToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        User, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'polls.authtoken' not in INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        else:
            self.key = self.key
        return super(StaticToken, self).save(*args, **kwargs)

#    def generate_key(self):
#        return binascii.hexlify(os.urandom(20)).decode()
    def generate_key(self):
        return os.environ.get(SECRET_TOKEN)

    def __str__(self):
        return self.key
