import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import type { ResearchObject } from '$lib/utils/researchObject';

export const load: PageLoad = async ({ params, fetch }) => {
  try {
    const response = await fetch(`http://localhost:8000/api/research/${params.id}/`);
    
    if (!response.ok) {
      throw error(response.status, 'Исследование не найдено');
    }
    
    const researchData: ResearchObject = await response.json();
    
    return {
      researchData,
      meta: {
        title: `${researchData.title} - Исследования`
      }
    };
  } catch (err) {
    throw error(404, 'Исследование не найдено');
  }
};