# services/__init__.py

from .searchServer import search_songs, surf_songs
from .mailServer import send_mail
from .registerServer import Validator, RegisterHandler