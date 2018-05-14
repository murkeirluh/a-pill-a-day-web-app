from rest_framework import serializers
from dashboard.models import Intakes

class IntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intakes
        fields = ('intake_id', 'patient', 'sched', 'time_taken')