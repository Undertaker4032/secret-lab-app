export interface DocumentType {
  id: number;
  name: string;
}

export interface ClearanceLevel {
  id: number;
  name: string;
  number: number;
}

export interface DocumentTypesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: DocumentType[];
}

export interface ClearanceLevelsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ClearanceLevel[];
}

export interface Documentation {
  id: number;
  title: string;
  type: number;
  type_name: string;
  content: string;
  author: number;
  author_name: string;
  created_date: string;
  updated_date: string;
  required_clearance: number;
  required_clearance_name: string;
}

export interface DocumentationResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Documentation[];
}

export interface DocumentationFilters {
  type__name?: string;
  author__division__name?: string;
  required_clearance__number?: string;
  created_date?: string;
  search?: string;
  ordering?: string;
}

export interface DocumentationSortOption {
  value: string;
  label: string;
}

export const documentationSortOptions: DocumentationSortOption[] = [
  { value: 'title', label: 'По названию (А-Я)' },
  { value: '-title', label: 'По названию (Я-А)' },
  { value: 'author__division__name', label: 'По отделу автора (А-Я)' },
  { value: '-author__division__name', label: 'По отделу автора (Я-А)' },
  { value: 'type__name', label: 'По типу (А-Я)' },
  { value: '-type__name', label: 'По типу (Я-А)' },
  { value: 'required_clearance__number', label: 'По уровню допуска (возр.)' },
  { value: '-required_clearance__number', label: 'По уровню допуска (убыв.)' },
  { value: 'created_date', label: 'По дате создания (сначала старые)' },
  { value: '-created_date', label: 'По дате создания (сначала новые)' },
  { value: 'updated_date', label: 'По дате обновления (сначала старые)' },
  { value: '-updated_date', label: 'По дате обновления (сначала новые)' },
];