<script lang="ts">
  import type { Documentation } from '$lib/utils/documentation';

  export let document: Documentation;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };
</script>

<a 
  href="/documentation/{document.id}" 
  class="block bg-rms-cod-gray border border-rms-mine-shaft hover:border-rms-white/30 hover:bg-rms-mine-shaft/50 transition-all duration-300 p-6 group"
>
  <div class="flex items-start justify-between">
    <div class="flex-1 min-w-0">
      <div class="flex flex-wrap items-start gap-3 mb-3">
        <h3 class="text-lg font-semibold text-rms-white group-hover:text-rms-white/90 break-words min-w-0 flex-1">
          {document.title}
        </h3>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/40 text-red-200 border border-red-600/50 whitespace-nowrap flex-shrink-0">
          {document.required_clearance_name}
        </span>
      </div>
      
      <div class="flex flex-wrap items-center gap-4 text-sm text-rms-nobel">
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>{document.type_name}</span>
        </div>
        
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span>{document.author_name}</span>
        </div>
        
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{formatDate(document.created_date)}</span>
        </div>
      </div>
    </div>

    <div class="ml-4 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <svg class="w-5 h-5 text-rms-dove-gray group-hover:text-rms-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </div>
</a>