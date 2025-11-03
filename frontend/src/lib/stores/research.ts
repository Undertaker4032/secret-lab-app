import { writable, derived } from 'svelte/store';
import { api } from '$lib/utils/api';
import type { Research, ResearchResponse, ResearchFilters } from '$lib/utils/research';

// Хранилища
export const research = writable<Research[]>([]);
export const researchLoading = writable<boolean>(false);
export const researchError = writable<string | null>(null);
export const researchFilters = writable<ResearchFilters>({});
export const researchCount = writable<number>(0);

// Обновляем функцию fetchResearch для поддержки всех фильтров
export async function fetchResearch(filters: ResearchFilters = {}) {
  researchLoading.set(true);
  researchError.set(null);
  
  try {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString();
    const url = queryString ? `/api/research/?${queryString}` : '/api/research/';
    
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

// Обновляем функцию updateFilters
export function updateResearchFilters(newFilters: Partial<ResearchFilters>) {
  const cleanFilters: ResearchFilters = {};
  
  Object.entries(newFilters).forEach(([key, value]) => {
    if (key !== 'isTrusted' && value !== undefined && value !== null && value !== '') {
      cleanFilters[key as keyof ResearchFilters] = value;
    }
  });
  
  researchFilters.update(current => ({ ...current, ...cleanFilters }));
  fetchResearch(cleanFilters);
}

export function clearResearchFilters() {
  researchFilters.set({});
  fetchResearch();
}