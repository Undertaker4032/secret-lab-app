/* eslint-disable @typescript-eslint/no-explicit-any */
import { get } from 'svelte/store';
import { 
  user, 
  employee, 
  clearAuth,
  authLoading,
  accessToken,
  isAuthenticated
} from '$lib/stores/auth';
import type { Employee, LoginResponse, User } from '$lib/stores/auth'; 

import type { 
  EmployeesFilters, 
  EmployeesResponse,
  Cluster,
  Department, 
  Division,
  Position,
  ClearanceLevel
} from './employee';
import type { 
  DocumentationFilters, 
  DocumentationResponse, 
  DocumentTypesResponse, 
  ClearanceLevelsResponse 
} from './documentation';
import type { 
  ResearchFilters, 
  ResearchResponse, 
  ResearchStatusesResponse
} from './research';
import type { DocumentObject } from './documentObject';
import type { ResearchObject } from './researchObject';

export interface EmployeeFiltersData {
  clusters: Cluster[];
  departments: Department[];
  divisions: Division[];
  positions: Position[];
  clearance_levels: ClearanceLevel[];
}

const API_BASE = '';
let refreshPromise: Promise<string | null> | null = null;

function getCSRFToken(): string | null {
  if (typeof document === 'undefined') return null;
  
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

async function refreshToken(): Promise<string | null> {
  if (refreshPromise) return refreshPromise;
  
  refreshPromise = (async () => {
    try {
      const csrfToken = getCSRFToken();
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };
      
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
      }

      const response = await fetch('/api/auth/refresh/', {
        method: 'POST',
        credentials: 'include',
        headers,
      });

      if (response.ok) {
        const data = await response.json();
        const newToken = data.access;
        accessToken.set(newToken);
        return newToken;
      } else {
        clearAuth();
        return null;
      }
    } catch (error) {
      clearAuth();
      return null;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

async function makeRequest<T>(url: string, options: RequestInit = {}): Promise<T> {
  const currentToken = get(accessToken);

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>,
  };

  if (currentToken) {
    headers['Authorization'] = `Bearer ${currentToken}`;
  }

  const method = options.method?.toUpperCase();
  if (method && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const csrfToken = getCSRFToken();
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }
  }

  const config: RequestInit = {
    credentials: 'include',
    headers,
    ...options
  };

  try {
    const response = await fetch(`${API_BASE}${url}`, config);
    
    if (response.status === 401 && currentToken && !url.includes('/auth/refresh/') && !url.includes('/auth/login/')) {
      const newToken = await refreshToken();
      
      if (newToken) {
        headers['Authorization'] = `Bearer ${newToken}`;
        const retryConfig = { ...config, headers };
        const retryResponse = await fetch(`${API_BASE}${url}`, retryConfig);
        
        if (!retryResponse.ok) {
          const errorData = await retryResponse.json().catch(() => ({}));
          throw new Error(errorData.detail || `HTTP error! status: ${retryResponse.status}`);
        }
        
        return await retryResponse.json() as T;
      }
    }
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json() as T;
    
  } catch (error) {
    console.error(`API request failed: ${url}`, error);
    throw error;
  }
}

function getApi<T>(url: string): Promise<T> {
  return makeRequest<T>(url);
}

function postApi<T>(url: string, data: unknown): Promise<T> {
  return makeRequest<T>(url, {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

function putApi<T>(url: string, data: unknown): Promise<T> {
  return makeRequest<T>(url, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

function patchApi<T>(url: string, data: unknown): Promise<T> {
  return makeRequest<T>(url, {
    method: 'PATCH',
    body: JSON.stringify(data)
  });
}

function deleteApi<T>(url: string): Promise<T> {
  return makeRequest<T>(url, {
    method: 'DELETE'
  });
}

function buildUrlWithParams(baseUrl: string, filters: Record<string, any> = {}): string {
  const params = new URLSearchParams();
  
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, value.toString());
    }
  });
  
  const queryString = params.toString();
  return queryString ? `${baseUrl}?${queryString}` : baseUrl;
}

export const api = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const csrfToken = getCSRFToken();
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }

    const response = await fetch(`${API_BASE}/api/auth/login/`, {
      method: 'POST',
      credentials: 'include',
      headers,
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Ошибка входа');
    }

    const data = await response.json();
    
    accessToken.set(data.access);
    user.set(data.user);
    
    if (data.employee) {
      employee.set(data.employee);
    } else {
      await this.getEmployeeData();
    }
    
    return data;
  },

  async logout(): Promise<void> {
    try {
      const csrfToken = getCSRFToken();
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
      }

      await fetch(`${API_BASE}/api/auth/logout/`, {
        method: 'POST',
        credentials: 'include',
        headers,
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuth();
    }
  },

  async getUserProfile(): Promise<User> {
    const userData = await getApi<User>('/api/auth/profile/');
    user.set(userData);
    return userData;
  },

  async getEmployeeData(): Promise<Employee | null> {
    try {
      const employeeData = await getApi<Employee>('/api/employees/my_profile/');
      employee.set(employeeData);
      return employeeData;
    } catch (error) {
      if (get(user)) {
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
    const url = buildUrlWithParams('/api/employees/', filters);
    return await getApi<EmployeesResponse>(url);
  },

  async getEmployeeById(id: number): Promise<Employee> {
    return await getApi<Employee>(`/api/employees/${id}/`);
  },

  async getEmployeeFilters(): Promise<EmployeeFiltersData> {
    return await getApi<EmployeeFiltersData>('/api/employees/employee-filters/');
  },

  async getDocumentation(filters: DocumentationFilters = {}): Promise<DocumentationResponse> {
    const url = buildUrlWithParams('/api/documentation/', filters);
    return await getApi<DocumentationResponse>(url);
  },

  async getDocumentationObject(id: number): Promise<DocumentObject> {
    return await getApi<DocumentObject>(`/api/documentation/${id}/`);
  },

  async getDocumentTypes(): Promise<DocumentTypesResponse> {
    return await getApi<DocumentTypesResponse>('/api/documentation/document-types/');
  },

  async getResearch(filters: ResearchFilters = {}): Promise<ResearchResponse> {
    const url = buildUrlWithParams('/api/research/', filters);
    return await getApi<ResearchResponse>(url);
  },

  async getResearchObject(id: number): Promise<ResearchObject> {
    return await getApi<ResearchObject>(`/api/research/${id}/`);
  },

  async getResearchStatuses(): Promise<ResearchStatusesResponse> {
    return await getApi<ResearchStatusesResponse>('/api/research/research-statuses/');
  },

  async getClearanceLevels(): Promise<ClearanceLevelsResponse> {
    return await getApi<ClearanceLevelsResponse>('/api/employees/clearance-level/');
  },

  async getClusters(): Promise<Cluster[]> {
    return await getApi<Cluster[]>('/api/employees/clusters/');
  },

  async getDepartments(): Promise<Department[]> {
    return await getApi<Department[]>('/api/employees/departments/');
  },

  async getDivisions(): Promise<Division[]> {
    return await getApi<Division[]>('/api/employees/divisions/');
  },

  async getPositions(): Promise<Position[]> {
    return await getApi<Position[]>('/api/employees/positions/');
  },

  get: getApi,
  post: postApi,
  put: putApi,
  patch: patchApi,
  delete: deleteApi
};

export async function initializeAuth(): Promise<void> {
  try {
    authLoading.set(true);
    
    let retries = 3;
    while (retries > 0) {
      try {
        await fetch('/api/auth/csrf/', {
          credentials: 'include',
          method: 'GET'
        });
        break;
      } catch (error) {
        retries--;
        if (retries === 0) throw error;
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    const storedToken = localStorage.getItem('accessToken');
    
    if (storedToken) {
      accessToken.set(storedToken);
      
      try {
        const profile = await api.getUserProfile();
        
        if (profile) {
          isAuthenticated.set(true);
          await api.getEmployeeData();
        } else {
          clearAuth();
        }
      } catch (error) {
        console.error('Failed to load profile with stored token:', error);
        
        try {
          const newToken = await refreshToken();
          if (newToken) {
            const profile = await api.getUserProfile();
            if (profile) {
              isAuthenticated.set(true);
              await api.getEmployeeData();
            } else {
              clearAuth();
            }
          } else {
            clearAuth();
          }
        } catch (refreshError) {
          clearAuth();
        }
      }
    } else {
      isAuthenticated.set(false);
    }
  } catch (error) {
    console.error('Auth initialization error:', error);
    clearAuth();
  } finally {
    authLoading.set(false);
  }
}