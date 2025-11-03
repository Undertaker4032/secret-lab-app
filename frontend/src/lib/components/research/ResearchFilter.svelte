<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { researchSortOptions } from '$lib/utils/research';

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let selectedStatus = '';
  let selectedDivision = '';
  let selectedClearance = '';
  let selectedDate = '';
  let selectedSort = '';

  function handleSubmit() {
    const filters = {
      search: searchTerm || undefined,
      status__name: selectedStatus || undefined,
      lead__division__name: selectedDivision || undefined,
      required_clearance__number: selectedClearance || undefined,
      created_date: selectedDate || undefined,
      ordering: selectedSort || undefined
    };
    
    console.log('Applying research filters:', filters);
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

  // В реальном приложении эти данные можно загружать с API
  const researchStatuses = [
    { value: 'Активно', label: 'Активно' },
    { value: 'Завершено', label: 'Завершено' },
    { value: 'Приостановлено', label: 'Приостановлено' },
    { value: 'В планах', label: 'В планах' }
  ];

  const clearanceLevels = [
    { value: '6', label: '5-У.Д.' },
    { value: '5', label: '5-У.Д.' },
    { value: '4', label: '4-У.Д.' },
    { value: '3', label: '3-У.Д.' },
    { value: '2', label: '2-У.Д.' },
    { value: '1', label: '1-У.Д.' },
    { value: '0', label: '0-У.Д.' }
  ];
</script>

<div class="bg-rms-cod-gray p-6 rounded-lg border border-rms-mine-shaft">
  <h3 class="text-lg font-medium text-rms-white mb-4">Фильтры исследований</h3>
  
  <form on:submit|preventDefault={handleSubmit}>
    <!-- Поиск и сортировка -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
      <!-- Поиск -->
      <div>
        <label for="search" class="block text-sm font-medium text-rms-white mb-2">
          Поиск
        </label>
        <input
          id="search"
          type="text"
          bind:value={searchTerm}
          placeholder="Название, руководитель, описание..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>

      <!-- Сортировка -->
      <div>
        <label for="sort" class="block text-sm font-medium text-rms-white mb-2">
          Сортировка
        </label>
        <select
          id="sort"
          bind:value={selectedSort}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Без сортировки</option>
          {#each researchSortOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <!-- Статус исследования -->
      <div>
        <label for="status" class="block text-sm font-medium text-rms-white mb-2">
          Статус
        </label>
        <select
          id="status"
          bind:value={selectedStatus}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Все статусы</option>
          {#each researchStatuses as status}
            <option value={status.value}>{status.label}</option>
          {/each}
        </select>
      </div>

      <!-- Отдел руководителя -->
      <div>
        <label for="division" class="block text-sm font-medium text-rms-white mb-2">
          Отдел руководителя
        </label>
        <input
          id="division"
          type="text"
          bind:value={selectedDivision}
          placeholder="Название отдела..."
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>

      <!-- Уровень допуска -->
      <div>
        <label for="clearance" class="block text-sm font-medium text-rms-white mb-2">
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

      <!-- Дата создания -->
      <div>
        <label for="date" class="block text-sm font-medium text-rms-white mb-2">
          Дата создания
        </label>
        <input
          id="date"
          type="date"
          bind:value={selectedDate}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        />
      </div>
    </div>

    <!-- Кнопки -->
    <div class="flex justify-end space-x-3">
      <button
        type="button"
        on:click={handleClear}
        class="px-4 py-2 text-sm font-medium text-rms-white bg-rms-mine-shaft border border-rms-dove-gray rounded-md shadow-sm hover:bg-rms-dove-gray hover:text-rms-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rms-white transition-colors"
      >
        Сбросить
      </button>
      <button
        type="submit"
        class="px-4 py-2 text-sm font-medium text-rms-black bg-rms-white border border-transparent rounded-md shadow-sm hover:bg-rms-nobel focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rms-white transition-colors"
      >
        Применить фильтры
      </button>
    </div>
  </form>
</div>