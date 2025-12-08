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

// ===== TYPES =====
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

// ===== CONSTANTS =====
const API_BASE = '';

// ===== UTILITY FUNCTIONS =====
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

// ===== REQUEST MANAGEMENT =====
let isRefreshing = false;
const refreshSubscribers: ((token: string) => void)[] = [];

function onRefreshed(token: string) {
  refreshSubscribers.forEach(callback => callback(token));
  refreshSubscribers.length = 0;
}

async function makeRequest<T>(url: string, options: RequestInit = {}): Promise<T> {
  const currentToken = get(accessToken);

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>,
  };

  if (currentToken) {
    headers['Authorization'] = `Bearer ${currentToken}`;
  } else {
    console.warn('No access token available for request');
  }

  // Для POST, PUT, PATCH, DELETE добавление CSRF токена
  const method = options.method?.toUpperCase();
  if (method && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const csrfToken = getCSRFToken();
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    } else {
      console.warn('No CSRF token available for request');
    }
  }

  const config: RequestInit = {
    credentials: 'include',
    headers,
    ...options
  };

  console.log(`=== API REQUEST ===`);
  console.log(`URL: ${API_BASE}${url}`);
  console.log(`Method: ${options.method || 'GET'}`);
  console.log(`Headers:`, headers);
  console.log(`Credentials: include`);

  try {
    const response = await fetch(`${API_BASE}${url}`, config);
    
    console.log(`=== API RESPONSE ===`);
    console.log(`Status: ${response.status} ${response.statusText}`);
    console.log(`URL: ${response.url}`);
    console.log(`OK: ${response.ok}`);
    
    if (response.status === 401 && currentToken && !url.includes('/auth/refresh/')) {
      console.log('Received 401, attempting token refresh...');
    }
    
    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: `HTTP error! status: ${response.status}` };
      }
      
      console.log(`=== API ERROR ===`);
      console.log(`Error data:`, errorData);
      
      const errorMessage = errorData.detail || errorData.message || `HTTP error! status: ${response.status}`;
      const error = new Error(errorMessage);
      (error as any).status = response.status;
      (error as any).data = errorData;
      throw error;
    }
    
    const responseData = await response.json();
    console.log(`=== API SUCCESS ===`);
    console.log(`Response data:`, responseData);
    return responseData as T;
    
  } catch (error) {
    console.error(`=== API REQUEST FAILED ===`);
    console.error(`Error:`, error);
    throw error;
  }
}

// ===== CORE API METHODS =====
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

// ===== URL BUILDER =====
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

// ===== API ENDPOINTS =====
export const api = {
  // ===== AUTHENTICATION =====
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
      const errorMessage = errorData.detail || errorData.message || 'Ошибка входа';
      throw new Error(errorMessage);
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
      console.error('Failed to get employee data:', error);
      
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

  // ===== EMPLOYEES =====
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

  // ===== DOCUMENTATION =====
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

  // ===== RESEARCH =====
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

  // ===== FILTER DATA =====
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

  // ===== GENERIC METHODS =====
  get: getApi,
  post: postApi,
  put: putApi,
  patch: patchApi,
  delete: deleteApi
};

// ===== AUTH INITIALIZATION =====
export async function initializeAuth(): Promise<void> {
    try {
        console.log('Initializing auth...');
        
        // Retry логика для CSRF токена
        let retries = 3;
        while (retries > 0) {
            try {
                await fetch('/api/auth/csrf/', {
                    credentials: 'include',
                    method: 'GET'
                });
                break; // Успех, выходим из цикла
            } catch (error) {
                retries--;
                if (retries === 0) throw error;
                console.warn(`CSRF fetch failed, ${retries} retries left`);
                await new Promise(resolve => setTimeout(resolve, 1000)); // Ждем 1 секунду
            }
        }
        
        // Остальная логика без изменений...
        const storedToken = localStorage.getItem('accessToken');
        // ...
        
    } catch (error) {
        console.error('Auth initialization error:', error);
        isAuthenticated.set(false);
        accessToken.set(null);
        user.set(null);
        employee.set(null);
    }
}

async function loadUserProfile(): Promise<void> {
    try {
        console.log('Loading user profile...');
        const response = await fetch('/api/auth/profile/', {
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                ...(get(accessToken) ? { 'Authorization': `Bearer ${get(accessToken)}` } : {})
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Profile data received:', data);
            user.set(data.user || data);
            
            await loadEmployeeData();
        } else {
            console.warn('Profile request failed with status:', response.status);
            throw new Error('Failed to load profile');
        }
    } catch (error) {
        console.error('Failed to load user profile:', error);
        throw error;
    }
}

async function loadEmployeeData(): Promise<void> {
    try {
        const employeeData = await getApi<Employee>('/api/employees/my_profile/');
        employee.set(employeeData);
        console.log('Employee data loaded:', employeeData);
    } catch (error) {
        console.error('Failed to get employee data:', error);
        
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
        } else {
            employee.set(null);
        }
    }
}

async function refreshAccessToken(): Promise<string | null> {
    try {
        console.log('Refreshing access token...');
        const response = await fetch('/api/auth/refresh/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const data = await response.json();
            const newToken = data.access;
            console.log('New access token received');
            return newToken;
        } else {
            console.warn('Token refresh failed with status:', response.status);
            return null;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
        return null;
    }
}