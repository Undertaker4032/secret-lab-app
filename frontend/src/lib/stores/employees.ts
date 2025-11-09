import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import { cleanFilters, buildUrlWithFilters } from '$lib/utils/apiFilters';
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

// Основная функция загрузки сотрудников
export async function fetchEmployees(filters: EmployeesFilters = {}) {
  employeesLoading.set(true);
  employeesError.set(null);
  
  try {
    // Используем нашу утилиту для построения URL
    const url = buildUrlWithFilters('/api/employees/', filters);
    
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

// Функция обновления фильтров
export function updateFilters(newFilters: Partial<EmployeesFilters>) {
  const currentFilters = get(employeesFilters);
  const mergedFilters = { ...currentFilters, ...cleanFilters(newFilters) };
  
  employeesFilters.set(mergedFilters);
  fetchEmployees(mergedFilters);
}

// Функция сброса фильтров
export function clearFilters() {
  employeesFilters.set({});
  fetchEmployees();
}

// Вспомогательная функция для получения текущего значения store
function get(store: any) {
  let value: any;
  store.subscribe((v: any) => value = v)();
  return value;
}

// Инициализация
export function initEmployeesStore() {
  fetchEmployees();
}