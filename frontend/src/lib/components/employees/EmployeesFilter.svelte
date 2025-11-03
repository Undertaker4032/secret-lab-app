<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { employeeSortOptions } from '$lib/utils/employee';

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let selectedCluster = '';
  let selectedDepartment = '';
  let selectedDivision = '';
  let selectedClearance = '';
  let activeStatus = '';
  let selectedSort = '';

  function handleSubmit() {
    const filters: any = {};
    
    if (searchTerm) filters.search = searchTerm;
    if (activeStatus) filters.is_active = activeStatus;
    if (selectedCluster) filters.cluster = selectedCluster;
    if (selectedDepartment) filters.department = selectedDepartment;
    if (selectedDivision) filters.division = selectedDivision;
    if (selectedClearance) filters.clearance_level__number = selectedClearance;
    if (selectedSort) filters.ordering = selectedSort;
    
    console.log('Applying filters:', filters);
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

  const clearanceLevels = [
    { value: '6', label: '6-У.Д.' },
    { value: '5', label: '5-У.Д.' },
    { value: '4', label: '4-У.Д.' },
    { value: '3', label: '3-У.Д.' },
    { value: '2', label: '2-У.Д.' },
    { value: '1', label: '1-У.Д.' },
  ];
</script>

<div class="bg-rms-cod-gray p-6 rounded-lg border border-rms-mine-shaft">
  <h3 class="text-lg font-medium text-rms-white mb-6">Фильтры сотрудников</h3>
  
  <form on:submit|preventDefault={handleSubmit}>
    <!-- Первая строка: Поиск и сортировка -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
      <!-- Поиск -->
      <div class="space-y-2">
        <label for="search" class="block text-sm font-medium text-rms-white">
          Поиск по имени
        </label>
        <input
          id="search"
          type="text"
          bind:value={searchTerm}
          placeholder="Введите имя сотрудника..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>

      <!-- Сортировка -->
      <div class="space-y-2">
        <label for="sort" class="block text-sm font-medium text-rms-white">
          Сортировка
        </label>
        <select
          id="sort"
          bind:value={selectedSort}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Без сортировки</option>
          {#each employeeSortOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Вторая строка: Статус и уровень допуска -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <!-- Статус -->
      <div class="space-y-2">
        <label for="status" class="block text-sm font-medium text-rms-white">
          Статус
        </label>
        <select
          id="status"
          bind:value={activeStatus}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Все сотрудники</option>
          <option value="true">Только активные</option>
          <option value="false">Только неактивные</option>
        </select>
      </div>

      <!-- Уровень допуска -->
      <div class="space-y-2">
        <label for="clearance" class="block text-sm font-medium text-rms-white">
          Уровень допуска
        </label>
        <select
          id="clearance"
          bind:value={selectedClearance}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Все уровни</option>
          {#each clearanceLevels as level}
            <option value={level.value}>{level.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Третья строка: Кластер, Департамент, Отдел -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <!-- Кластер -->
      <div class="space-y-2">
        <label for="cluster" class="block text-sm font-medium text-rms-white">
          Кластер
        </label>
        <input
          id="cluster"
          type="text"
          bind:value={selectedCluster}
          placeholder="Название кластера..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>

      <!-- Департамент -->
      <div class="space-y-2">
        <label for="department" class="block text-sm font-medium text-rms-white">
          Департамент
        </label>
        <input
          id="department"
          type="text"
          bind:value={selectedDepartment}
          placeholder="Название департамента..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>

      <!-- Отдел -->
      <div class="space-y-2">
        <label for="division" class="block text-sm font-medium text-rms-white">
          Отдел
        </label>
        <input
          id="division"
          type="text"
          bind:value={selectedDivision}
          placeholder="Название отдела..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>
    </div>

    <!-- Кнопки -->
    <div class="flex justify-end space-x-3 pt-4 border-t border-rms-mine-shaft">
      <button
        type="button"
        on:click={handleClear}
        class="px-6 py-2.5 text-sm font-medium text-rms-white bg-rms-mine-shaft border border-rms-dove-gray rounded-lg hover:bg-rms-dove-gray hover:text-rms-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rms-white transition-colors"
      >
        Сбросить всё
      </button>
      <button
        type="submit"
        class="px-6 py-2.5 text-sm font-medium text-rms-black bg-rms-white border border-transparent rounded-lg hover:bg-rms-nobel focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rms-white transition-colors"
      >
        Применить фильтры
      </button>
    </div>
  </form>
</div>