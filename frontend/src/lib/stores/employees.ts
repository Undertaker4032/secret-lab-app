import { writable, derived, get } from 'svelte/store';
import { api } from '$lib/utils/api';
import type { Employee, EmployeesResponse, EmployeesFilters } from '$lib/utils/employee';

// Хранилища
export const employees = writable<Employee[]>([]);
export const employeesLoading = writable<boolean>(false);
export const employeesError = writable<string | null>(null);
export const employeesFilters = writable<EmployeesFilters>({});
export const employeesCount = writable<number>(0);

// Дербированные хранилища
export const activeEmployees = derived(employees, $employees => 
  $employees.filter(emp => emp.is_active)
);

export const inactiveEmployees = derived(employees, $employees => 
  $employees.filter(emp => !emp.is_active)
);

// Функции
export async function fetchEmployees(filters: EmployeesFilters = {}) {
  employeesLoading.set(true);
  employeesError.set(null);
  
  try {
    // Строим query string из фильтров
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        // Убедимся, что это не системные свойства (как isTrusted)
        if (key !== 'isTrusted' && typeof value !== 'boolean') {
          params.append(key, value.toString());
        }
      }
    });
    
    const queryString = params.toString();
    const url = queryString ? `/api/employees/?${queryString}` : '/api/employees/';
    
    console.log('Fetching employees from:', url);
    
    const data = await api.get<EmployeesResponse>(url);
    
    employees.set(data.results);
    employeesCount.set(data.count);
    employeesFilters.set(filters);
    
  } catch (error) {
    console.error('Error fetching employees:', error);
    employeesError.set('Не удалось загрузить список сотрудников');
    employees.set([]);
  } finally {
    employeesLoading.set(false);
  }
}

export function updateFilters(newFilters: Partial<EmployeesFilters>) {
  // Очищаем фильтры от системных свойств
  const cleanFilters: EmployeesFilters = {};
  
  Object.entries(newFilters).forEach(([key, value]) => {
    if (key !== 'isTrusted' && value !== undefined && value !== null && value !== '') {
      cleanFilters[key as keyof EmployeesFilters] = value;
    }
  });
  
  employeesFilters.update(current => ({ ...current, ...cleanFilters }));
  fetchEmployees(cleanFilters);
}

export function clearFilters() {
  employeesFilters.set({});
  fetchEmployees();
}

// Инициализация
export function initEmployeesStore() {
  fetchEmployees();
}