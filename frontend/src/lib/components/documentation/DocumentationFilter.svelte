<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { documentationSortOptions } from '$lib/utils/documentation';

  const dispatch = createEventDispatcher();

  let searchTerm = '';
  let selectedType = '';
  let selectedDivision = '';
  let selectedClearance = '';
  let selectedDate = '';
  let selectedSort = '';

  function handleSubmit() {
    const filters = {
      search: searchTerm || undefined,
      type__name: selectedType || undefined,
      author__division__name: selectedDivision || undefined,
      required_clearance__number: selectedClearance || undefined,
      created_date: selectedDate || undefined,
      ordering: selectedSort || undefined
    };
    
    console.log('Applying documentation filters:', filters);
    dispatch('filterChange', filters);
  }

  function handleClear() {
    searchTerm = '';
    selectedType = '';
    selectedDivision = '';
    selectedClearance = '';
    selectedDate = '';
    selectedSort = '';
    
    dispatch('clearFilters');
  }

  // В реальном приложении эти данные можно загружать с API
  const documentTypes = [
    { value: 'Протокол', label: 'Протокол' },
    { value: 'Отчет', label: 'Отчет' },
    { value: 'Инструкция', label: 'Инструкция' },
    { value: 'Руководство', label: 'Руководство' },
    { value: 'Спецификация', label: 'Спецификация' }
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
  <h3 class="text-lg font-medium text-rms-white mb-4">Фильтры документации</h3>
  
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
          placeholder="Название, автор, содержание..."
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
          {#each documentationSortOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <!-- Тип документа -->
      <div>
        <label for="type" class="block text-sm font-medium text-rms-white mb-2">
          Тип документа
        </label>
        <select
          id="type"
          bind:value={selectedType}
          class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
        >
          <option value="">Все типы</option>
          {#each documentTypes as type}
            <option value={type.value}>{type.label}</option>
          {/each}
        </select>
      </div>

      <!-- Отдел автора -->
      <div>
        <label for="division" class="block text-sm font-medium text-rms-white mb-2">
          Отдел автора
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