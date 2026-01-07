from rest_framework import serializers
from ..models import Research, ResearchStatus


class ResearchListSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    required_clearance_name = serializers.CharField(source='required_clearance.name', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title',
                  'status', 'status_name',
                  'lead', 'lead_name',
                  'required_clearance', 'required_clearance_name',
                  'created_date', 'updated_date']
    read_only_fields = ['created_date', 'updated_date']
    

class ResearchObjectSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    team_members = serializers.SerializerMethodField()
    status_name = serializers.CharField(source='status.name', read_only=True)
    required_clearance_name = serializers.CharField(source='required_clearance.name', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title',
                  'status', 'status_name',
                  'content',
                  'lead', 'lead_name',
                  'team', 'team_members',
                  'required_clearance', 'required_clearance_name',
                  'created_date', 'updated_date']
    read_only_fields = ['created_date', 'updated_date']

    def get_team_members(self, obj) -> list:
        return [employee.name for employee in obj.team.all()]
    
class ResearchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchStatus
        fields = ['id', 'name']