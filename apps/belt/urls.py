from django.conf.urls import url
from . import views		   
                 
urlpatterns = [
    url(r'^dashboard/(?P<person_id>\d+)$', views.show_dashboard),
    url(r'^event/(?P<event_id>\d+)$', views.show_one_event),
    url(r'^new_event$', views.show_new_event_form),
    url(r'^add_event$', views.add_event),
    url(r'^event/(?P<event_id>\d+)/edit$', views.edit_event),
    url(r'^event/(?P<event_id>\d+)/update$', views.update_event),
    url(r'^event/(?P<event_id>\d+)/destroy$', views.delete_event),    
    url(r'^event/(?P<event_id>\d+)/join$', views.join_event),    
    url(r'^event/(?P<event_id>\d+)/unjoin$', views.unjoin_event),    

]