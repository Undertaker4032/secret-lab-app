import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import { cleanFilters, buildUrlWithFilters } from '$lib/utils/apiFilters';
import type { Documentation, DocumentationResponse, DocumentationFilters } from '$lib/utils/documentation';

export const documentation = writable<Documentation[]>([]);
export const documentationLoading = writable<boolean>(false);
export const documentationError = writable<string | null>(null);
export const documentationFilters = writable<DocumentationFilters>({});
export const documentationCount = writable<number>(0);

export async function fetchDocumentation(filters: DocumentationFilters = {}) {
  documentationLoading.set(true);
  documentationError.set(null);
  
  try {
    const url = buildUrlWithFilters('/api/documentation/', filters);
    
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

export function updateDocumentationFilters(newFilters: Partial<DocumentationFilters>) {
  const currentFilters = get(documentationFilters);
  const mergedFilters = { ...currentFilters, ...cleanFilters(newFilters) };
  
  documentationFilters.set(mergedFilters);
  fetchDocumentation(mergedFilters);
}

export function clearDocumentationFilters() {
  documentationFilters.set({});
  fetchDocumentation();
}

function get(store: any) {
  let value: any;
  store.subscribe((v: any) => value = v)();
  return value;
}