from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from IFB299app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from forms import LoginForm


urlpatterns = [
	## Home page
	url(r'^$', views.index, name='index'),
	

	## Users
	url(r'^login/$', auth_views.login, {'template_name': 'IFB299app/login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/IFB299app/'}, name='logout'),
	url(r'^register/$', views.register, name='register'),
	

	## Password recovery
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


	## Dashboard
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^location/$', views.location, name='location'),

	## Location page
	url(r'^location/(?P<category_name_slug>[\w\-]+)/$', views.location, name='location'),

	## Admin
	#url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
	url(r'^admin/', admin.site.urls),
]