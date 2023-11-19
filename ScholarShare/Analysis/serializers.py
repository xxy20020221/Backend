from rest_framework import serializers
from .models import User
from .models import Analysis
from .models import Work


class AnalysisSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField("%Y-%m-%d %H:%M:%S", read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    works = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all())

    class Meta:
        model = Analysis
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user']= {

        }
        return representation


