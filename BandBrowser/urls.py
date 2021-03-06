from django.urls import path
from BandBrowser import views

app_name = 'BandBrowser'

urlpatterns = [
    path('', views.index, name='index'),
    path('AddPostUserToBand/', views.AddPostUserToBand, name='AddPostUserToBand'),
    path('AddUserToRequestMembers/', views.AddUserToRequestMembers, name='AddUserToRequestMembers'),

    path('myBandPage/',views.myBandPage, name='myBandPage'),

    path('bandInfoPage/',views.bandInfoPage, name='bandInfoPage'),
    path('updateBandInfo/',views.updateBandInfo, name='updateBandInfo'),
    path('removeCurrentBandMember/',views.removeCurrentBandMember, name='removeCurrentBandMember'),
    path('acceptUserJoinRequest/',views.acceptUserJoinRequest, name='acceptUserJoinRequest'),
    path('declineUserJoinRequest/',views.declineUserJoinRequest, name='declineUserJoinRequest'),

    path('createBandPage/',views.createBandPage, name='createBandPage'),
    path('createBand/',views.createBand, name ='createBand'),
    path('leaveBand/',views.leaveBand, name ='leaveBand'),

    path('createPostPage/',views.createPostPage, name='createPostPage'),
    path('createBandPost/',views.createBandPost, name='createBandPost'),
    path('createUserPost/',views.createUserPost, name='createUserPost'),

    path('viewUserPage/',views.viewUserPage, name='viewUserPage'),
    path('viewBandPage/',views.viewBandPage, name='viewBandPage'),

    path('accountPage/',views.accountPage, name='accountPage'),
    path('uploadUserAvatar/',views.uploadUserAvatar, name='uploadUserAvatar'),
    path('deleteUserAccount/',views.deleteUserAccount, name='deleteUserAccount'),
    path('updateUserAccount/',views.updateUserAccount, name='updateUserAccount'),
    path('createAccountPage/',views.createAccountPage, name='createAccountPage'),

    path('register/',views.registerUser, name='register'),
    path('loginPage/',views.loginPage, name='loginPage'),
    path('login/',views.userLogin, name='login'),
    path('logout/',views.logoutUser, name='logout'),

    path('gitPull/',views.gitPull, name='gitPull'),
]