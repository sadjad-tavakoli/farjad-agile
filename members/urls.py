from django.urls.conf import include, path

from books.views import AddBookView
from loan.views.borrower_views import BorrowedBooksList, BorrowerLoansRequestList, \
    BorrowerChangeLoanStateView
from loan.views.lender_views import LoanedBooksList, LenderLoansRequestList, \
    LenderChangeLoanStateView
from members.views.authentication_api_views import PhoneValidator
from members.views.authentication_views import LoginView, LogoutView, JoinView, \
    CheckInvitationCode, \
    NewAuthenticationView, AuthenticationCodeCheckingApiView
from members.views.profile_views import ProfileView, EditProfileView, SelfProfileView, \
    InvitationTemplateView
from members.views.user_books_views import UserBooksListView

app_name = "members"
self_books_urlpatterns = ([
                              path(r'', UserBooksListView.as_view(), name="all"),
                              path(r'new/', AddBookView.as_view(), name="new"),
                              path(r'borrowed/', BorrowedBooksList.as_view(), name="borrowed"),
                              path(r'loaned/', LoanedBooksList.as_view(), name="loaned"),

                          ], 'books')
self_loans_urlpatterns = ([

                              path(r'lender', LenderLoansRequestList.as_view(), name="as-lender"),
                              path(r'borrower', BorrowerLoansRequestList.as_view(),
                                   name="as-borrower"),
                              path(r'<int:loan_pk>/lender_change_state/',
                                   LenderChangeLoanStateView.as_view(),
                                   name="lender-change-state"),
                              path(r'<int:loan_pk>/borrower_change_state/',
                                   BorrowerChangeLoanStateView.as_view(),
                                   name="borrower-change-state"),

                          ], 'loans')

api_urlpatterns = ([
    path(r'phone-validator/', PhoneValidator.as_view(), name="phone-validator"),

])
self_urlpatterns = ([
                        path(r'profile/', SelfProfileView.as_view(), name="profile"),
                        path(r'invitation/',
                             InvitationTemplateView.as_view(),
                             name="invitation"),
                        path(r'invitation-checking/',
                             CheckInvitationCode.as_view(),
                             name="invitation-check"),
                        path(r'profile/edit/', EditProfileView.as_view(), name="edit-profile"),
                        path(r'books/', include(self_books_urlpatterns)),
                        path(r'loans/', include(self_loans_urlpatterns)),
                    ], 'self')
authentication_urlpatterns = ([
                                  path(r'', NewAuthenticationView.as_view(),
                                       name="phone"),
                                  path(r'code-checking',
                                       AuthenticationCodeCheckingApiView.as_view(),
                                       name="code"),

                              ], 'authentication')
urlpatterns = [
    path(r'api/', include(api_urlpatterns), name="api"),
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'authentication/', include(authentication_urlpatterns), name="authentication"),
    path(r'join/', JoinView.as_view(), name="join"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'profile/<int:member_id>/', ProfileView.as_view(), name="profile"),
    path(r'self/', include(self_urlpatterns)),
]
