// utils/api.ts
import { 
  accessToken, 
  refreshToken, 
  user, 
  employee, 
  clearAuth,
  authLoading 
} from '$lib/stores/auth';
import type { Employee, AuthTokens, LoginResponse, User } from '$lib/stores/auth'; 
import type { EmployeesFilters, EmployeesResponse } from './employee';
import type { DocumentationFilters, DocumentationResponse } from './documentation';
import type { ResearchFilters, ResearchResponse} from './research';
import type { DocumentObject } from './documentObject';
import type { ResearchObject } from './researchObject';


const API_BASE = 'http://localhost:8000';

// Переменные для текущих значений
let currentAccessToken: string | null = null;
let currentRefreshToken: string | null = null;

// Подписываемся на изменения
accessToken.subscribe(value => currentAccessToken = value);
refreshToken.subscribe(value => currentRefreshToken = value);

// Флаг для избежания повторного обновления токена
let isRefreshing = false;

// Функция обновления access token
async function refreshAccessToken(): Promise<string | null> {
  if (!currentRefreshToken) {
    clearAuth();
    return null;
  }

  try {
    const response = await fetch(`${API_BASE}/api/auth/refresh/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: currentRefreshToken
      })
    });

    if (response.ok) {
      const data = await response.json() as AuthTokens;
      accessToken.set(data.access);
      return data.access;
    } else {
      // Refresh token невалиден - полный логаут
      throw new Error('Token refresh failed');
    }
  } catch (error) {
    console.error('Refresh token failed:', error);
    clearAuth();
    return null;
  }
}

// Базовый запрос с обработкой ошибок
async function makeRequest<T>(url: string, options: RequestInit = {}): Promise<T> {
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options
  };

  // Добавляем access token если есть
  if (currentAccessToken) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${currentAccessToken}`
    };
  }

  const response = await fetch(`${API_BASE}${url}`, config);
  
  if (response.ok) {
    return await response.json() as T;
  }

  // Обработка 401 ошибки (только если есть refresh token и не в процессе обновления)
  if (response.status === 401 && currentRefreshToken && !isRefreshing) {
    try {
      isRefreshing = true;
      const newToken = await refreshAccessToken();
      
      if (newToken) {
        // Повторяем оригинальный запрос с новым токеном
        config.headers = {
          ...config.headers,
          Authorization: `Bearer ${newToken}`
        };
        const retryResponse = await fetch(`${API_BASE}${url}`, config);
        
        if (retryResponse.ok) {
          return await retryResponse.json() as T;
        }
      }
      else {
        clearAuth();
      }
    } finally {
      isRefreshing = false;
    }
  }
  
  // Если дошли сюда - ошибка не исправлена
  const errorData = await response.json().catch(() => ({}));
  throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
}

// API функции
export const api = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const data = await makeRequest<LoginResponse>('/api/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    
    accessToken.set(data.access);
    refreshToken.set(data.refresh);
    user.set(data.user);

    // Запрашиваем данные сотрудника
    await this.getEmployeeData();
    
    return data;
  },

  async logout(): Promise<void> {
    try {
      if (currentRefreshToken) {
        await makeRequest('/api/auth/logout/', {
          method: 'POST',
          body: JSON.stringify({ refresh_token: currentRefreshToken })
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuth();
    }
  },

  async getUserProfile(): Promise<User> {
    try {
      const userData = await makeRequest<User>('/api/auth/profile/');
      user.set(userData);
      return userData;
    } catch (error) {
      console.error('Failed to get user profile:', error);
      throw error;
    }
  },

  async getEmployeeData(): Promise<Employee | null> {
    try {
      // ✅ Правильный endpoint для данных сотрудника
      const employeeData = await makeRequest<Employee>('/api/employees/my_profile/');
      employee.set(employeeData);
      return employeeData;
    } catch (error) {
      console.error('Failed to get employee data:', error);
      
      // ✅ Создаем fallback только если пользователь авторизован
      if (currentAccessToken) {
        const fallbackEmployee: Employee = {
          id: 0,
          name: 'Сотрудник',
          is_active: true,
          clearance_level: null,
          cluster: null,
          department: null,
          division: null,
          position: null,
          profile_picture: null
        };
        employee.set(fallbackEmployee);
        return fallbackEmployee;
      }
      
      employee.set(null);
      return null;
    }
  },

  async getEmployees(filters: EmployeesFilters = {}): Promise<EmployeesResponse> {
  const params = new URLSearchParams();
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  const queryString = params.toString();
  const url = queryString ? `/api/employees/?${queryString}` : '/api/employees/';
  
  return await this.get<EmployeesResponse>(url);
},

  // Базовые методы для безопасных запросов (GET)
  get<T>(url: string): Promise<T> {
    return makeRequest<T>(url);
  },

  // POST/PUT/DELETE могут понадобиться для будущего функционала
  post<T>(url: string, data: unknown): Promise<T> {
    return makeRequest<T>(url, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  },

  // Добавьте эти функции в объект api:

async getDocumentation(filters: DocumentationFilters = {}): Promise<DocumentationResponse> {
  const params = new URLSearchParams();
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  const queryString = params.toString();
  const url = queryString ? `/api/documentation/?${queryString}` : '/api/documentation/';
  
  return await this.get<DocumentationResponse>(url);
},

async getResearch(filters: ResearchFilters = {}): Promise<ResearchResponse> {
  const params = new URLSearchParams();
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  const queryString = params.toString();
  const url = queryString ? `/api/research/?${queryString}` : '/api/research/';
  
  return await this.get<ResearchResponse>(url);
},

async getDocumentationObject(id: number): Promise<DocumentObject> {
  return await this.get<DocumentObject>(`/api/documentation/${id}/`);
},

async getResearchObject(id: number): Promise<ResearchObject> {
  return await this.get<ResearchObject>(`/api/research/${id}/`);
},
};

export async function initializeAuth(): Promise<void> {
  if (!currentAccessToken) {
    authLoading.set(false);
    return;
  }

  try {
    // ✅ Сначала проверяем профиль пользователя
    await api.getUserProfile();
    // ✅ Затем получаем данные сотрудника
    await api.getEmployeeData();
  } catch (error) {
    console.error('Auth initialization failed:', error);
    clearAuth();
  } finally {
    authLoading.set(false);
  }
}