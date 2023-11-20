from django.contrib import admin

from .models import Vote
from .models import VoteYN


admin.site.register(Vote)
admin.site.register(VoteYN)
