import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import type { Documentation, DocumentationResponse, DocumentationFilters } from '$lib/utils/documentation';

// Хранилища
export const documentation = writable<Documentation[]>([]);
export const documentationLoading = writable<boolean>(false);
export const documentationError = writable<string | null>(null);
export const documentationFilters = writable<DocumentationFilters>({});
export const documentationCount = writable<number>(0);

// Обновляем функцию fetchDocumentation для поддержки всех фильтров
export async function fetchDocumentation(filters: DocumentationFilters = {}) {
  documentationLoading.set(true);
  documentationError.set(null);
  
  try {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString();
    const url = queryString ? `/api/documentation/?${queryString}` : '/api/documentation/';
    
    console.log('Fetching documentation from:', url);
    const data = await api.get<DocumentationResponse>(url);
    
    documentation.set(data.results);
    documentationCount.set(data.count);
    documentationFilters.set(filters);
    
  } catch (error) {
    console.error('Error fetching documentation:', error);
    documentationError.set('Не удалось загрузить список документов');
    documentation.set([]);
  } finally {
    documentationLoading.set(false);
  }
}

// Обновляем функцию updateFilters
export function updateDocumentationFilters(newFilters: Partial<DocumentationFilters>) {
  const cleanFilters: DocumentationFilters = {};
  
  Object.entries(newFilters).forEach(([key, value]) => {
    if (key !== 'isTrusted' && value !== undefined && value !== null && value !== '') {
      cleanFilters[key as keyof DocumentationFilters] = value;
    }
  });
  
  documentationFilters.update(current => ({ ...current, ...cleanFilters }));
  fetchDocumentation(cleanFilters);
}

export function clearDocumentationFilters() {
  documentationFilters.set({});
  fetchDocumentation();
}