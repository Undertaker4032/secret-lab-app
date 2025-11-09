export interface Cluster {
  id: number;
  name: string;
}

export interface Department {
  id: number;
  name: string;
}

export interface Division {
  id: number;
  name: string;
}

export interface Position {
  id: number;
  name: string;
}

export interface ClearanceLevel {
  id: number;
  name: string;
  number: number;
}

export interface Employee {
  id: number;
  name: string;
  is_active: boolean;
  clearance_level: ClearanceLevel | null;
  cluster: Cluster | null;
  department: Department | null;
  division: Division | null;
  position: Position | null;
  profile_picture: string | null;
}

export interface EmployeesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Employee[];
}

export interface EmployeesFilters {
  is_active?: string;
  cluster?: string | number;
  department?: string | number;
  division?: string | number;
  clearance_level?: string | number;
  search?: string;
  ordering?: string;
}

export interface EmployeeSortOption {
  value: string;
  label: string;
}

export const employeeSortOptions: EmployeeSortOption[] = [
  { value: 'name', label: 'По имени (А-Я)' },
  { value: '-name', label: 'По имени (Я-А)' },
  { value: 'clearance_level__number', label: 'По уровню допуска (возр.)' },
  { value: '-clearance_level__number', label: 'По уровню допуска (убыв.)' },
  { value: 'division__department__cluster__name', label: 'По кластеру (А-Я)' },
  { value: '-division__department__cluster__name', label: 'По кластеру (Я-А)' },
  { value: 'division__name', label: 'По отделу (А-Я)' },
  { value: '-division__name', label: 'По отделу (Я-А)' },
  { value: 'position__name', label: 'По должности (А-Я)' },
  { value: '-position__name', label: 'По должности (Я-А)' },
];
