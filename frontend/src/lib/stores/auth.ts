import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Добавляем интерфейсы для вложенных объектов
export interface ClearanceLevel {
  id: number;
  name: string;
  number: number;
}

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

// Обновляем интерфейс Employee
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

// User интерфейс с employee_id
export interface User {
  id: number;
  username: string;
  employee_id?: number;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse extends AuthTokens {
  user: User;
  employee?: Employee;
}

// Функции для работы с localStorage
const getStoredItem = <T>(key: string): T | null => {
  if (!browser) return null;
  
  try {
    const item = localStorage.getItem(key);
    if (!item) return null;
    
    // Для строковых значений (токены)
    if (key.includes('Token')) {
      return item as T;
    }
    
    return JSON.parse(item) as T;
  } catch (error) {
    console.error(`Error reading ${key} from localStorage:`, error);
    return null;
  }
};

const setStoredItem = <T>(key: string, value: T): void => {
  if (!browser) return;
  
  if (typeof value === 'object') {
    localStorage.setItem(key, JSON.stringify(value));
  } else {
    localStorage.setItem(key, value as string);
  }
};

const removeStoredItem = (key: string): void => {
  if (browser) {
    localStorage.removeItem(key);
  }
};

// Создаем хранилища
export const user = writable<User | null>(getStoredItem<User>('user'));
export const employee = writable<Employee | null>(getStoredItem<Employee>('employee'));
export const accessToken = writable<string | null>(getStoredItem<string>('accessToken'));
export const refreshToken = writable<string | null>(getStoredItem<string>('refreshToken'));
export const isAuthenticated = writable<boolean>(false);
export const authLoading = writable<boolean>(true);

// Синхронизация с localStorage
user.subscribe((value) => {
  setStoredItem('user', value);
});

employee.subscribe((value) => {
  setStoredItem('employee', value);
});

accessToken.subscribe((value) => {
  setStoredItem('accessToken', value);
  isAuthenticated.set(!!value);
});

refreshToken.subscribe((value) => {
  setStoredItem('refreshToken', value);
});

// Функция для очистки всех данных аутентификации
export function clearAuth(): void {
  user.set(null);
  employee.set(null);
  accessToken.set(null);
  refreshToken.set(null);
  isAuthenticated.set(false);
  authLoading.set(false);
  
  if (browser) {
    removeStoredItem('user');
    removeStoredItem('employee');
    removeStoredItem('accessToken');
    removeStoredItem('refreshToken');
  }
}