<script lang="ts">
  import type { Research } from '$lib/utils/research';

  export let researchItem: Research;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, string> = {
      'Активно': 'bg-green-900/30 text-green-300 border-green-700',
      'Завершено': 'bg-blue-900/30 text-blue-300 border-blue-700',
      'Приостановлено': 'bg-yellow-900/30 text-yellow-300 border-yellow-700',
      'В планах': 'bg-gray-900/30 text-gray-300 border-gray-700'
    };
    return statusColors[status] || 'bg-gray-900/30 text-gray-300 border-gray-700';
  };
</script>

<a 
  href="/research/{researchItem.id}" 
  class="block bg-rms-cod-gray border border-rms-mine-shaft hover:border-rms-dove-gray hover:bg-rms-mine-shaft/50 transition-all duration-200 p-6 group"
>
  <div class="flex items-start justify-between">
    <!-- Основная информация -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-3 mb-2">
        <h3 class="text-lg font-medium text-rms-white group-hover:text-rms-white truncate">
          {researchItem.title}
        </h3>
        <div class="flex items-center gap-2 flex-shrink-0">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-700">
            {researchItem.required_clearance_name}
          </span>
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {getStatusColor(researchItem.status_name)}">
            {researchItem.status_name}
          </span>
        </div>
      </div>
      
      <div class="flex flex-wrap items-center gap-4 text-sm text-rms-nobel">
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span>{researchItem.lead_name}</span>
        </div>
        
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>{researchItem.status_name}</span>
        </div>
        
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{formatDate(researchItem.created_date)}</span>
        </div>
      </div>
    </div>

    <!-- Стрелка -->
    <div class="ml-4 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
      <svg class="w-5 h-5 text-rms-dove-gray group-hover:text-rms-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </div>
</a>