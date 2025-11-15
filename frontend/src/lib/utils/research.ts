export interface ResearchStatus {
  id: number;
  name: string;
}

export interface Division {
  id: number;
  name: string;
}

export interface ResearchStatus {
  id: number;
  name: string;
}

export interface ResearchStatusesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ResearchStatus[];
}

export interface Research {
  id: number;
  title: string;
  lead: number;
  lead_name: string;
  status: number;
  status_name: string;
  required_clearance: number;
  required_clearance_name: string;
  created_date: string;
  updated_date: string;
}

export interface ResearchResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Research[];
}

export interface ResearchFilters {
  lead__division__name?: string;
  status__name?: string;
  required_clearance__number?: string;
  created_date?: string;
  search?: string;
  ordering?: string;
}

export interface ResearchSortOption {
  value: string;
  label: string;
}

export const researchSortOptions: ResearchSortOption[] = [
  { value: 'title', label: 'По названию (А-Я)' },
  { value: '-title', label: 'По названию (Я-А)' },
  { value: 'lead__division__name', label: 'По отделу руководителя (А-Я)' },
  { value: '-lead__division__name', label: 'По отделу руководителя (Я-А)' },
  { value: 'status__name', label: 'По статусу (А-Я)' },
  { value: '-status__name', label: 'По статусу (Я-А)' },
  { value: 'required_clearance__number', label: 'По уровню допуска (возр.)' },
  { value: '-required_clearance__number', label: 'По уровню допуска (убыв.)' },
  { value: 'created_date', label: 'По дате создания (сначала старые)' },
  { value: '-created_date', label: 'По дате создания (сначала новые)' },
  { value: 'updated_date', label: 'По дате обновления (сначала старые)' },
  { value: '-updated_date', label: 'По дате обновления (сначала новые)' },
];
