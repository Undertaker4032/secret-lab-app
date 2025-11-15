<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import { employeeSortOptions } from '$lib/utils/employee';
  import { cleanFilters } from '$lib/utils/apiFilters';
  import { api } from '$lib/utils/api';
  import type { EmployeeFiltersData } from '$lib/utils/api';

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let selectedCluster: string | number = '';
  let selectedDepartment: string | number = '';
  let selectedDivision: string | number = '';
  let selectedClearance: string | number = '';
  let activeStatus = '';
  let selectedSort = '';

  let filtersData: EmployeeFiltersData = {
    clusters: [],
    departments: [],
    divisions: [],
    positions: [],
    clearance_levels: []
  };

  let isLoading = true;

  onMount(async () => {
    try {
      filtersData = await api.getEmployeeFilters();
    } catch (error) {
      console.error('Failed to load filters:', error);
    } finally {
      isLoading = false;
    }
  });

  function handleSubmit() {
    const filters = cleanFilters({
      search: searchTerm,
      is_active: activeStatus,
      cluster: selectedCluster,
      department: selectedDepartment,
      division: selectedDivision,
      clearance_level: selectedClearance,
      ordering: selectedSort
    });
    
    dispatch('filterChange', filters);
  }

  function handleClear() {
    searchTerm = '';
    selectedCluster = '';
    selectedDepartment = '';
    selectedDivision = '';
    selectedClearance = '';
    activeStatus = '';
    selectedSort = '';
    
    dispatch('clearFilters');
  }
</script>

<div class="bg-rms-cod-gray p-6 rounded-lg border border-rms-mine-shaft">
  <h3 class="text-lg font-semibold text-rms-white mb-6">Фильтры сотрудников</h3>
  
  {#if isLoading}
    <div class="text-center py-4">
      <p class="text-rms-white">Загрузка фильтров...</p>
    </div>
  {:else}
    <form on:submit|preventDefault={handleSubmit}>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <div class="space-y-2">
          <label for="search" class="block text-sm font-medium text-rms-white">
            Поиск по имени
          </label>
          <input
            id="search"
            type="text"
            bind:value={searchTerm}
            placeholder="Введите имя сотрудника..."
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          />
        </div>

        <div class="space-y-2">
          <label for="sort" class="block text-sm font-medium text-rms-white">
            Сортировка
          </label>
          <select
            id="sort"
            bind:value={selectedSort}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Без сортировки</option>
            {#each employeeSortOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="space-y-2">
          <label for="status" class="block text-sm font-medium text-rms-white">
            Статус
          </label>
          <select
            id="status"
            bind:value={activeStatus}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все сотрудники</option>
            <option value="true">Только активные</option>
            <option value="false">Только неактивные</option>
          </select>
        </div>

        <div class="space-y-2">
          <label for="clearance" class="block text-sm font-medium text-rms-white">
            Уровень допуска
          </label>
          <select
            id="clearance"
            bind:value={selectedClearance}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все уровни</option>
            {#each filtersData.clearance_levels as level}
              <option value={level.id}>{level.name}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="space-y-2">
          <label for="cluster" class="block text-sm font-medium text-rms-white">
            Кластер
          </label>
          <select
            id="cluster"
            bind:value={selectedCluster}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все кластеры</option>
            {#each filtersData.clusters as cluster}
              <option value={cluster.id}>{cluster.name}</option>
            {/each}
          </select>
        </div>

        <div class="space-y-2">
          <label for="department" class="block text-sm font-medium text-rms-white">
            Департамент
          </label>
          <select
            id="department"
            bind:value={selectedDepartment}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все департаменты</option>
            {#each filtersData.departments as department}
              <option value={department.id}>{department.name}</option>
            {/each}
          </select>
        </div>

        <div class="space-y-2">
          <label for="division" class="block text-sm font-medium text-rms-white">
            Отдел
          </label>
          <select
            id="division"
            bind:value={selectedDivision}
            class="w-full px-3 py-2.5 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white/50 focus:border-rms-white/30 transition-all duration-300"
          >
            <option value="">Все отделы</option>
            {#each filtersData.divisions as division}
              <option value={division.id}>{division.name}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="flex justify-end space-x-3 pt-4 border-t border-rms-mine-shaft">
        <button
          type="button"
          on:click={handleClear}
          class="px-5 py-2.5 text-sm font-medium text-rms-white bg-rms-mine-shaft border border-rms-dove-gray rounded-lg hover:bg-rms-dove-gray hover:text-rms-black focus:outline-none focus:ring-2 focus:ring-rms-white/50 transition-all duration-300"
        >
          Сбросить всё
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