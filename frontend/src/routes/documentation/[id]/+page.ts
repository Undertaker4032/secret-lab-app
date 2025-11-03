import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import type { DocumentObject } from '$lib/utils/documentObject';

export const load: PageLoad = async ({ params, fetch }) => {
  try {
    const response = await fetch(`http://localhost:8000/api/documentation/${params.id}/`);
    
    if (!response.ok) {
      throw error(response.status, 'Документ не найден');
    }
    
    const documentData: DocumentObject = await response.json();
    
    return {
      documentData,
      meta: {
        title: `${documentData.title} - Документация`
      }
    };
  } catch (err) {
    throw error(404, 'Документ не найден');
  }
};