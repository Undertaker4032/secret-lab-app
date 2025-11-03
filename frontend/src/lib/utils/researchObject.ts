export interface ResearchObject {
  id: number;
  title: string;
  description: string;
  objectives: string;
  lead: number;
  lead_name: string;
  team: number[];
  team_members: string[];
  status: number;
  status_name: string;
  required_clearance: number;
  required_clearance_name: string;
  findings: string;
  created_date: string;
  updated_date: string;
}