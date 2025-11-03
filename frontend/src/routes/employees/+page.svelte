<script lang="ts">
  import { onMount } from 'svelte';
  import {
    employees,
    employeesLoading,
    employeesError,
    employeesFilters,
    employeesCount,
    activeEmployees,
    inactiveEmployees,
    fetchEmployees,
    updateFilters,
    clearFilters
  } from '$lib/stores/employees';
  import EmployeeCard from '$lib/components/employees/EmployeeCard.svelte';
  import EmployeesFilter from '$lib/components/employees/EmployeesFilter.svelte';
  
  let activeTab: 'all' | 'active' | 'inactive' = 'all';
  
  onMount(() => {
    fetchEmployees();
  });
  
  function handleFilterChange(event: CustomEvent) {
    updateFilters(event.detail);
  }
  
  function handleClearFilters() {
    clearFilters();
  }
  
  $: displayedEmployees = activeTab === 'all' 
    ? $employees 
    : activeTab === 'active' 
      ? $activeEmployees 
      : $inactiveEmployees;
</script>

<svelte:head>
  <title>Сотрудники лаборатории</title>
  <meta name="description" content="Список сотрудников секретной лаборатории" />
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-rms-white">Сотрудники лаборатории</h1>
      <p class="mt-2 text-sm text-rms-nobel">
        Всего сотрудников: {$employeesCount}
        {#if $employeesFilters.search}
          • Поиск: "{$employeesFilters.search}"
        {/if}
      </p>
    </div>

    <!-- Фильтры -->
    <div class="mb-6">
      <EmployeesFilter 
        on:filterChange={handleFilterChange}
        on:clearFilters={handleClearFilters}
      />
    </div>

    <!-- Табы и управление -->
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <!-- Табы -->
      <div class="flex space-x-1 rounded-lg bg-rms-mine-shaft p-1">
        <button
          class="px-3 py-2 text-sm font-medium rounded-md transition-all duration-200"
          class:bg-rms-white={activeTab === 'all'}
          class:text-rms-black={activeTab === 'all'}
          class:text-rms-nobel={activeTab !== 'all'}
          class:shadow={activeTab === 'all'}
          on:click={() => activeTab = 'all'}
        >
          Все ({$employees.length})
        </button>
        <button
          class="px-3 py-2 text-sm font-medium rounded-md transition-all duration-200"
          class:bg-rms-white={activeTab === 'active'}
          class:text-rms-black={activeTab === 'active'}
          class:text-rms-nobel={activeTab !== 'active'}
          class:shadow={activeTab === 'active'}
          on:click={() => activeTab = 'active'}
        >
          Активные ({$activeEmployees.length})
        </button>
        <button
          class="px-3 py-2 text-sm font-medium rounded-md transition-all duration-200"
          class:bg-rms-white={activeTab === 'inactive'}
          class:text-rms-black={activeTab === 'inactive'}
          class:text-rms-nobel={activeTab !== 'inactive'}
          class:shadow={activeTab === 'inactive'}
          on:click={() => activeTab = 'inactive'}
        >
          Неактивные ({$inactiveEmployees.length})
        </button>
      </div>
    </div>

    <!-- Состояние загрузки -->
    {#if $employeesLoading}
      <div class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white"></div>
      </div>
    {:else if $employeesError}
      <!-- Ошибка -->
      <div class="rounded-md bg-red-900/30 border border-red-700 p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-300">Ошибка загрузки</h3>
            <p class="text-sm text-red-200 mt-1">{$employeesError}</p>
            <button
              class="mt-2 text-sm text-red-300 hover:text-red-100 underline transition-colors"
              on:click={() => fetchEmployees()}
            >
              Попробовать снова
            </button>
          </div>
        </div>
      </div>
    {:else if displayedEmployees.length === 0}
      <!-- Пустой список -->
      <div class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-rms-dove-gray" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-rms-white">Сотрудники не найдены</h3>
        <p class="mt-1 text-sm text-rms-nobel">
          {#if Object.keys($employeesFilters).length > 0}
            Попробуйте изменить параметры фильтрации
          {:else}
            В системе пока нет сотрудников
          {/if}
        </p>
      </div>
    {:else}
      <!-- Список сотрудников в виде плиток -->
      <div class="space-y-3">
        {#each displayedEmployees as employee (employee.id)}
          <EmployeeCard {employee} />
        {/each}
      </div>
    {/if}
  </div>
</div>