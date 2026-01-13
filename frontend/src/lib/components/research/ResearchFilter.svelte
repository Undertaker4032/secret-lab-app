<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { researchSortOptions } from '$lib/utils/research';
  import { cleanFilters } from '$lib/utils/apiFilters';
  import { api } from '$lib/utils/api';
  import type { ResearchStatus } from '$lib/utils/research';
  import type { ClearanceLevel } from '$lib/utils/documentation';

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let selectedStatus = '';
  let selectedDivision = '';
  let selectedClearance = '';
  let selectedDate = '';
  let selectedSort = '';

  let researchStatuses: ResearchStatus[] = [];
  let clearanceLevels: ClearanceLevel[] = [];
  let divisions: { id: number; name: string }[] = [];
  let loading = true;

  onMount(async () => {
  try {
    await loadFilterData();
  } catch (error) {
    console.error('Error loading research filter data:', error);
  } finally {
    loading = false;
  }
});

  async function loadFilterData() {
    try {
      const divisionsResponse = await api.get('/api/employees/divisions/');
      divisions = divisionsResponse.results;
      
      const typesResponse = await api.get('/api/research/research-statuses/');
      researchStatuses = typesResponse.results;

      const clearanceResponse = await api.get('/api/employees/clearance-level/');
      clearanceLevels = clearanceResponse.results.sort((a, b) => b.number - a.number);
    } catch (error) {
      console.error('Failed to load filter data:', error);
    }

  function handleSubmit() {
    const filters = cleanFilters({
      search: searchTerm,
      status: selectedStatus,
      lead_division: selectedDivision,
      required_clearance: selectedClearance,
      created_date: selectedDate,
      ordering: selectedSort
    });
    
    dispatch('filterChange', filters);
  }


  function handleClear() {
    searchTerm = '';
    selectedStatus = '';
    selectedDivision = '';
    selectedClearance = '';
    selectedDate = '';
    selectedSort = '';
    
    dispatch('clearFilters');
  }
</script>

<div class="bg-rms-cod-gray p-6 rounded-lg border border-rms-mine-shaft">
  <h3 class="text-lg font-semibold text-rms-white mb-6">Фильтры исследований</h3>
  
  {#if loading}
    <div class="text-rms-white text-center py-4">Загрузка фильтров...</div>
  {:else}
    <form on:submit|preventDefault={handleSubmit}>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <label for="search" class="block text-sm font-medium text-rms-white mb-2">
            Поиск
          </label>
          <input
            id="search"
            type="text"
            bind:value={searchTerm}
            placeholder="Название, руководитель, описание..."
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          />
        </div>

        <div>
          <label for="sort" class="block text-sm font-medium text-rms-white mb-2">
            Сортировка
          </label>
          <select
            id="sort"
            bind:value={selectedSort}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Без сортировки</option>
            {#each researchSortOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div>
          <label for="status" class="block text-sm font-medium text-rms-white mb-2">
            Статус
          </label>
          <select
            id="status"
            bind:value={selectedStatus}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все статусы</option>
            {#each researchStatuses as status}
              <option value={status.name}>{status.name}</option>
            {/each}
          </select>
        </div>

        <div>
          <label for="division" class="block text-sm font-medium text-rms-white mb-2">
            Отдел руководителя
          </label>
          <select>
            id="division"
            type="text"
            bind:value={selectedDivision}
            placeholder="Название отдела..."
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          </select>
        </div>

        <div>
          <label for="clearance" class="block text-sm font-medium text-rms-white mb-2">
            Уровень допуска
          </label>
          <select
            id="clearance"
            bind:value={selectedClearance}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все уровни</option>
            {#each clearanceLevels as level}
              <option value={level.number}>{level.name}</option>
            {/each}
          </select>
        </div>

        <div>
          <label for="date" class="block text-sm font-medium text-rms-white mb-2">
            Дата создания
          </label>
          <input
            id="date"
            type="date"
            bind:value={selectedDate}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          />
        </div>
      </div>

      <div class="flex justify-end space-x-3 pt-4 border-t border-rms-mine-shaft">
        <button
          type="button"
          on:click={handleClear}
          class="px-5 py-2.5 text-sm font-medium text-rms-white bg-rms-mine-shaft border border-rms-dove-gray rounded-lg hover:bg-rms-dove-gray hover:text-rms-black focus:outline-none focus:ring-2 focus:ring-rms-white/50 transition-all duration-300"
        >
          Сбросить
        </button>
        <button
          type="submit"
          class="px-5 py-2.5 text-sm font-medium text-rms-black bg-rms-white border border-transparent rounded-lg hover:bg-rms-nobel focus:outline-none focus:ring-2 focus:ring-rms-white/50 transition-all duration-300"
        >
          Применить фильтры
        </button>
      </div>
    </form>
  {/if}
</div>