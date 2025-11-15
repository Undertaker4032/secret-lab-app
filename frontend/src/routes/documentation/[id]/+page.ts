import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
  if (!params.id || isNaN(+params.id)) {
    throw error(400, 'Неверный ID документа');
  }

  return {
    itemId: +params.id,
    meta: { title: 'Документ - RMS Laboratories' }
  };
};