import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import { cleanFilters, buildUrlWithFilters } from '$lib/utils/apiFilters';
import type { Research, ResearchResponse, ResearchFilters } from '$lib/utils/research';

export const research = writable<Research[]>([]);
export const researchLoading = writable<boolean>(false);
export const researchError = writable<string | null>(null);
export const researchFilters = writable<ResearchFilters>({});
export const researchCount = writable<number>(0);

export async function fetchResearch(filters: ResearchFilters = {}) {
  researchLoading.set(true);
  researchError.set(null);
  
  try {
    const url = buildUrlWithFilters('/api/research/', filters);
    
    console.log('Fetching research from:', url);
    const data = await api.get<ResearchResponse>(url);
    
    research.set(data.results);
    researchCount.set(data.count);
    researchFilters.set(filters);
    
  } catch (error) {
    console.error('Error fetching research:', error);
    researchError.set('Не удалось загрузить список исследований');
    research.set([]);
  } finally {
    researchLoading.set(false);
  }
}

export function updateResearchFilters(newFilters: Partial<ResearchFilters>) {
  const currentFilters = get(researchFilters);
  const mergedFilters = { ...currentFilters, ...cleanFilters(newFilters) };
  
  researchFilters.set(mergedFilters);
  fetchResearch(mergedFilters);
}

export function clearResearchFilters() {
  researchFilters.set({});
  fetchResearch();
}

function get(store: any) {
  let value: any;
  store.subscribe((v: any) => value = v)();
  return value;
}