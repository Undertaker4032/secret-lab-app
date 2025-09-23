from rest_framework import serializers
from ..models import Research

class ResearchSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    team_members = serializers.SerializerMethodField()
    status_name = serializers.CharField(source='status.name', read_only=True)
    required_clearance_number = serializers.CharField(source='required_clearance.number', read_only=True)

    class Meta:
        model = Research
        fields = ['id', 'title',
                  'description', 'objectives',
                  'lead', 'lead_name',
                  'team', 'team_members',
                  'status', 'status_name',
                  'required_clearance', 'required_clearance_number',
                  'findings', 'created_date',
                  'updated_date']
    read_only_fields = ['created_date', 'updated_date']

    def get_team_members(self, obj):
        return [employee.name for employee in obj.team.all()]