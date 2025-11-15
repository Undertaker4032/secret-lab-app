// Утилиты для преобразования фильтров в параметры API
import type { EmployeesFilters } from './employee';
import type { DocumentationFilters } from './documentation';
import type { ResearchFilters } from './research';

export interface BaseFilters {
  search?: string;
  ordering?: string;
  [key: string]: any;
}

export function cleanFilters<T extends BaseFilters>(filters: T): Partial<T> {
  const cleaned: Partial<T> = {};
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '' && value !== false) {
      cleaned[key as keyof T] = value;
    }
  });
  
  return cleaned;
}

export function filtersToParams(filters: BaseFilters): URLSearchParams {
  const params = new URLSearchParams();
  
  Object.entries(cleanFilters(filters)).forEach(([key, value]) => {
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
      params.append(key, value.toString());
    }
  });
  
  return params;
}

export function buildUrlWithFilters(baseUrl: string, filters: BaseFilters): string {
  const params = filtersToParams(filters);
  const queryString = params.toString();
  return queryString ? `${baseUrl}?${queryString}` : baseUrl;
}