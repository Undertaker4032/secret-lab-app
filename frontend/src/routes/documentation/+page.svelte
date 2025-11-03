<script lang="ts">
  import { onMount } from 'svelte';
  import {
    documentation,
    documentationLoading,
    documentationError,
    documentationFilters,
    documentationCount,
    fetchDocumentation,
    updateDocumentationFilters,
    clearDocumentationFilters
  } from '$lib/stores/documentation';
  import DocumentCard from '$lib/components/documentation/DocumentCard.svelte';
  import DocumentationFilter from '$lib/components/documentation/DocumentationFilter.svelte';

  onMount(() => {
    fetchDocumentation();
  });

  function handleFilterChange(event: CustomEvent) {
    updateDocumentationFilters(event.detail);
  }

  function handleClearFilters() {
    clearDocumentationFilters();
  }
</script>

<svelte:head>
  <title>Документация лаборатории</title>
  <meta name="description" content="Документация и руководства секретной лаборатории" />
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-rms-white">Документация лаборатории</h1>
      <p class="mt-2 text-sm text-rms-nobel">
        Всего документов: {$documentationCount}
        {#if $documentationFilters.search}
          • Поиск: "{$documentationFilters.search}"
        {/if}
        {#if $documentationFilters.ordering}
          • Сортировка: {$documentationFilters.ordering}
        {/if}
      </p>
    </div>

    <!-- Фильтры -->
    <div class="mb-6">
      <DocumentationFilter 
        on:filterChange={handleFilterChange}
        on:clearFilters={handleClearFilters}
      />
    </div>

    <!-- Состояние загрузки -->
    {#if $documentationLoading}
      <div class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white"></div>
      </div>
    {:else if $documentationError}
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
            <p class="text-sm text-red-200 mt-1">{$documentationError}</p>
            <button
              class="mt-2 text-sm text-red-300 hover:text-red-100 underline transition-colors"
              on:click={() => fetchDocumentation()}
            >
              Попробовать снова
            </button>
          </div>
        </div>
      </div>
    {:else if $documentation.length === 0}
      <!-- Пустой список -->
      <div class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-rms-dove-gray" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-rms-white">Документы не найдены</h3>
        <p class="mt-1 text-sm text-rms-nobel">
          В системе пока нет документов
        </p>
      </div>
    {:else}
      <!-- Список документов в виде плиток -->
      <div class="space-y-3">
        {#each $documentation as doc (doc.id)}
          <DocumentCard document={doc} />
        {/each}
      </div>
    {/if}
  </div>
</div>