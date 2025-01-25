from django.urls import path
from crime_app.views import (query1, query2, query3, query4, query5, 
                             query6, query7, query8, query9, query10,
                             GetPoliceOfficer, GetCrimeReport, 
                             AddCrimeReportView, AddPoliceOfficerView, AddOfficerUpvoteView
                            )

urlpatterns = [
    path('query1/', query1.as_view(), name='query1'),
    path('query2/', query2.as_view(), name='query2'),
    path('query3/', query3.as_view(), name='query3'),
    path('query4/', query4.as_view(), name='query4'),
    path('query5/', query5.as_view(), name='query5'),
    path('query6/', query6.as_view(), name='query6'),
    path('query7/', query7.as_view(), name='query7'),
    path('query8/', query8.as_view(), name='query8'),
    path('query9/', query9.as_view(), name='query9'),
    path('query10/', query10.as_view(), name='query10'),
    path('get_police_officer/', GetPoliceOfficer.as_view(), name='get_police_officer'),
    path('get_crime_report/', GetCrimeReport.as_view(), name='get_crime_report'),
    path('add_crime_report/', AddCrimeReportView.as_view(), name='add_crime_report'),
    path('add_police_officer/', AddPoliceOfficerView.as_view(), name='add_police_officer'),
    path('add_officer_upvote/', AddOfficerUpvoteView.as_view(), name='add_officer_upvote')
]