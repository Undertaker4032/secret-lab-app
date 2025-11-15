import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const accessToken = writable<string | null>(
  browser ? localStorage.getItem('accessToken') : null
);
export const isAuthenticated = writable<boolean>(false);
export const authLoading = writable<boolean>(true);

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

if (browser) {
  accessToken.subscribe((token) => {
    if (token) {
      localStorage.setItem('accessToken', token);
    } else {
      localStorage.removeItem('accessToken');
    }
  });
}

const getStoredItem = <T>(key: string): T | null => {
  if (!browser) return null;
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) as T : null;
  } catch (error) {
    return null;
  }
};

export const user = writable<User | null>(getStoredItem<User>('user'));
export const employee = writable<Employee | null>(getStoredItem<Employee>('employee'));

const setStoredItem = <T>(key: string, value: T): void => {
  if (!browser) return;
  localStorage.setItem(key, JSON.stringify(value));
};

user.subscribe((value) => {
  setStoredItem('user', value);
  isAuthenticated.set(!!value);
});

employee.subscribe((value) => {
  setStoredItem('employee', value);
});

accessToken.subscribe((value) => {
  if (browser) {
    if (value) {
      localStorage.setItem('accessToken', value);
    } else {
      localStorage.removeItem('accessToken');
    }
  }
});

export function clearAuth(): void {
  user.set(null);
  employee.set(null);
  accessToken.set(null);
  isAuthenticated.set(false);
  authLoading.set(false);
  
  if (browser) {
    localStorage.removeItem('user');
    localStorage.removeItem('employee');
    localStorage.removeItem('accessToken');
  }
}