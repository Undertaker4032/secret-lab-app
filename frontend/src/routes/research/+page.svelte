<script lang="ts">
  import { onMount } from 'svelte';
  import {
    research,
    researchLoading,
    researchError,
    researchFilters,
    researchCount,
    fetchResearch,
    updateResearchFilters,
    clearResearchFilters
  } from '$lib/stores/research';
  import ResearchCard from '$lib/components/research/ResearchCard.svelte';
  import ResearchFilter from '$lib/components/research/ResearchFilter.svelte';

  onMount(() => {
    fetchResearch();
  });

  function handleFilterChange(event: CustomEvent) {
    updateResearchFilters(event.detail);
  }

  function handleClearFilters() {
    clearResearchFilters();
  }
</script>

<svelte:head>
  <title>Исследования лаборатории</title>
  <meta name="description" content="Научные исследования и проекты секретной лаборатории" />
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-rms-white">Исследования лаборатории</h1>
      <p class="mt-2 text-sm text-rms-nobel">
        Всего исследований: {$researchCount}
        {#if $researchFilters.search}
          • Поиск: "{$researchFilters.search}"
        {/if}
        {#if $researchFilters.ordering}
          • Сортировка: {$researchFilters.ordering}
        {/if}
      </p>
    </div>

    <!-- Фильтры -->
    <div class="mb-6">
      <ResearchFilter 
        on:filterChange={handleFilterChange}
        on:clearFilters={handleClearFilters}
      />
    </div>

    <!-- Состояние загрузки -->
    {#if $researchLoading}
      <div class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white"></div>
      </div>
    {:else if $researchError}
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
            <p class="text-sm text-red-200 mt-1">{$researchError}</p>
            <button
              class="mt-2 text-sm text-red-300 hover:text-red-100 underline transition-colors"
              on:click={() => fetchResearch()}
            >
              Попробовать снова
            </button>
          </div>
        </div>
      </div>
    {:else if $research.length === 0}
      <!-- Пустой список -->
      <div class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-rms-dove-gray" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-rms-white">Исследования не найдены</h3>
        <p class="mt-1 text-sm text-rms-nobel">
          В системе пока нет исследований
        </p>
      </div>
    {:else}
      <!-- Список исследований в виде плиток -->
      <div class="space-y-3">
        {#each $research as researchItem (researchItem.id)}
          <ResearchCard {researchItem} />
        {/each}
      </div>
    {/if}
  </div>
</div>