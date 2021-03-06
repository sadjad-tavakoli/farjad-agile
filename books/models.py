from django.db import models

from farjad.settings import PERIOD, GENRE, AGE
from farjad.utils.utils_view import get_url
from loan.models import LoanState


class Books(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=200, blank=False, null=False)
    pub_date = models.DateField()
    price = models.IntegerField(blank=False, null=False)
    period = models.CharField(max_length=10, choices=PERIOD)
    genre = models.CharField(max_length=10, choices=GENRE)
    reader_age = models.CharField(max_length=10, choices=AGE)
    page_num = models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    jeld_num = models.IntegerField()
    description = models.CharField(max_length=1000)
    summary = models.CharField(max_length=5000)
    owner = models.ForeignKey("members.Member", related_name="books", on_delete=models.CASCADE)

    @property
    def image_url(self):
        return get_url(None, 'books/icons/book_icon.png')

    def loan_state(self, user):
        if user.loans.filter(book=self).exists():
            return user.loans.filter(book=self).last().state.state
        return ""

    def has_not_valid_state(self, user):
        state = self.loan_state(user)
        forbidden = [LoanState.STATE_REJECTED, LoanState.STATE_CANCELED_BY_BORROWER,
                     LoanState.STATE_CANCELED_BY_LENDER, "", LoanState.STATE_FINISHED]
        return state in forbidden
