from django.urls import path, include
from .views import stand_detail

urlpatterns = [
    path("h2lab/",  include("projects.stands.h2lab.urls")),
    path("h2race/", include("projects.stands.h2race.urls")),
    path("mechanics/", include("projects.stands.mechanics.urls")),
    path("sofc_streamlit/",  include("projects.stands.sofc_streamlit.urls")),
    path("sofclab/",  include("projects.stands.sofclab.urls")),
    path("solar_streamlit/",  include("projects.stands.solar_streamlit.urls")),
    path("solarlab/",  include("projects.stands.solarlab.urls")),
]

