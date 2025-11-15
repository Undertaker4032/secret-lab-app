import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import { cleanFilters, buildUrlWithFilters } from '$lib/utils/apiFilters';
import type { Employee, EmployeesResponse, EmployeesFilters } from '$lib/utils/employee';

export const employees = writable<Employee[]>([]);
export const employeesLoading = writable<boolean>(false);
export const employeesError = writable<string | null>(null);
export const employeesFilters = writable<EmployeesFilters>({});
export const employeesCount = writable<number>(0);

export const activeEmployees = derived(employees, $employees => 
  $employees.filter(emp => emp.is_active)
);

export const inactiveEmployees = derived(employees, $employees => 
  $employees.filter(emp => !emp.is_active)
);

export async function fetchEmployees(filters: EmployeesFilters = {}) {
  employeesLoading.set(true);
  employeesError.set(null);
  
  try {
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

export function updateFilters(newFilters: Partial<EmployeesFilters>) {
  const currentFilters = get(employeesFilters);
  const mergedFilters = { ...currentFilters, ...cleanFilters(newFilters) };
  
  employeesFilters.set(mergedFilters);
  fetchEmployees(mergedFilters);
}

export function clearFilters() {
  employeesFilters.set({});
  fetchEmployees();
}

function get(store: any) {
  let value: any;
  store.subscribe((v: any) => value = v)();
  return value;
}

export function initEmployeesStore() {
  fetchEmployees();
}