<script lang="ts">
  import type { Employee } from '$lib/utils/employee';

  export let employee: Employee;
  
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };
</script>

<div class="bg-rms-cod-gray border border-rms-mine-shaft hover:border-rms-dove-gray hover:bg-rms-mine-shaft/50 transition-all duration-200 p-6 group">
  <div class="flex items-center justify-between">
    <!-- Левая часть: аватар и основная информация -->
    <div class="flex items-center gap-4 flex-1 min-w-0">
      <!-- Аватар -->
      {#if employee.profile_picture}
        <img
          src={employee.profile_picture}
          alt={employee.name}
          class="h-14 w-14 rounded-full object-cover border-2 border-rms-mine-shaft group-hover:border-rms-dove-gray transition-colors"
        />
      {:else}
        <div class="h-14 w-14 rounded-full bg-rms-mine-shaft flex items-center justify-center border border-rms-dove-gray group-hover:border-rms-nobel transition-colors">
          <span class="text-rms-white font-semibold text-base">
            {getInitials(employee.name)}
          </span>
        </div>
      {/if}

      <!-- Информация -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-3 mb-1">
          <h3 class="text-lg font-medium text-rms-white group-hover:text-rms-white truncate">
            {employee.name}
          </h3>
          {#if !employee.is_active}
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rms-mine-shaft text-rms-nobel border border-rms-dove-gray whitespace-nowrap flex-shrink-0">
              Неактивен
            </span>
          {/if}
        </div>
        
        <div class="flex flex-wrap items-center gap-4 text-sm text-rms-nobel">
          {#if employee.position}
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>{employee.position.name}</span>
            </div>
          {/if}
          
          {#if employee.division}
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <span>{employee.division.name}</span>
            </div>
          {/if}
          
          {#if employee.department && employee.department.name !== employee.division?.name}
            <div class="flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              <span>{employee.department.name}</span>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Правая часть: уровень допуска и стрелка -->
    <div class="flex items-center gap-3 ml-4">
      {#if employee.is_active && employee.clearance_level}
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-700 whitespace-nowrap">
          {employee.clearance_level.name}
        </span>
      {/if}
      
      <!-- Стрелка -->
      <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
        <svg class="w-5 h-5 text-rms-dove-gray group-hover:text-rms-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </div>
  </div>

  <!-- Дополнительная информация (кластер) -->
  {#if employee.cluster}
    <div class="mt-3 pt-3 border-t border-rms-mine-shaft">
      <div class="flex items-center gap-1 text-sm text-rms-nobel">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Кластер: {employee.cluster.name}</span>
      </div>
    </div>
  {/if}
</div>