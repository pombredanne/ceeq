from django.conf.urls import patterns, url


urlpatterns = patterns('ceeq.apps.projects.views',
      url(r'^projects/$', 'projects', name='projects'),
      url(r'^project/new/$', 'project_new', name='project_new'),
      url(r'^project/(?P<project_id>\d+)/$', 'project_detail', name='project_detail'),
      url(r'^project/dd/(?P<project_id>\d+)/$', 'project_defects_density', name='project_defects_density'),
      url(r'^project/(?P<project_id>\d+)/edit/$', 'project_edit', name='project_edit'),
      url(r'^project/(?P<project_id>\d+)/delete/$','project_delete', name='project_delete'),
      url(r'^project/(?P<project_id>\d+)/update_scores/$', 'project_update_scores', name='project_update_scores'),
      url(r'^project/(?P<project_id>\d+)/dd_log/$', 'defects_density_log', name='defects_density_log'),

      url(r'^project/score/$', 'fetch_projects_score', name='fetch_projects_score'),
      url(r'^project/dd_score/(?P<project_id>\d+)/$', 'fetch_defects_density_score', name='fetch_defects_density_score'),
      url(r'^project/dd_pie/(?P<project_id>\d+)/$', 'fetch_defects_density_score_pie', name='fetch_defects_density_score_pie'),
      #url(r'^characteristics/$', 'characteristics', name='characteristics'),

      url(r'^project/(?P<project_id>\d+)/Application/$', 'project_sub_apps_piechart', name='project_sub_apps_piechart'),
      url(r'^project/app_sub_pie/(?P<project_id>\d+)/$', 'fetch_apps_subcomponents_pie', name='fetch_apps_subcomponents_pie'),
      )