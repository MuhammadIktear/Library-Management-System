from django.db import models
from account.models import UserAccount

class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return f'{self.amount} deposited to {self.account.user.username}'

