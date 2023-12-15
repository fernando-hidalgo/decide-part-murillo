from django.contrib import admin

from .models import Vote
from .models import VoteYN
from .models import VoteByPreference
from .models import VoteMultiChoice


admin.site.register(Vote)
admin.site.register(VoteYN)
admin.site.register(VoteByPreference)
admin.site.register(VoteMultiChoice)
