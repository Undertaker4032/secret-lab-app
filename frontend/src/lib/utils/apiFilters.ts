// Утилиты для преобразования фильтров в параметры API
import type { EmployeesFilters } from './employee';
import type { DocumentationFilters } from './documentation';
import type { ResearchFilters } from './research';

// Базовый тип для всех фильтров
export interface BaseFilters {
  search?: string;
  ordering?: string;
  [key: string]: any;
}

// Функция для очистки фильтров от undefined/пустых значений
export function cleanFilters<T extends BaseFilters>(filters: T): Partial<T> {
  const cleaned: Partial<T> = {};
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '' && value !== false) {
      cleaned[key as keyof T] = value;
    }
  });
  
  return cleaned;
}

// Функция для преобразования фильтров в URL параметры
export function filtersToParams(filters: BaseFilters): URLSearchParams {
  const params = new URLSearchParams();
  
  Object.entries(cleanFilters(filters)).forEach(([key, value]) => {
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
      params.append(key, value.toString());
    }
  });
  
  return params;
}

// Функция для создания URL с фильтрами
export function buildUrlWithFilters(baseUrl: string, filters: BaseFilters): string {
  const params = filtersToParams(filters);
  const queryString = params.toString();
  return queryString ? `${baseUrl}?${queryString}` : baseUrl;
}