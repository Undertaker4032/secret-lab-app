<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/state';
  import { api } from '$lib/utils/api';
  import AccessCheck from '$lib/components/ui/AccessCheck.svelte';
  import type { DocumentObject } from '$lib/utils/documentObject';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let documentData: DocumentObject | null = $state(data.documentData);
  let loading = $state(false); // Теперь данные уже загружены
  let accessGranted = $state(false);
  let accessDenied = $state(false);
  let error = $state('');

  // Исправляем $derived с правильной типизацией
  const pageTitle = $derived(
    data.meta?.title || 'Документ - RMS Laboratories'
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // Функция для безопасного получения ID
  function getDocumentId(): number {
    const id = page.params.id;
    if (!id) {
      throw new Error('ID документа не указан');
    }
    return +id;
  }

  async function loadDocument(): Promise<void> {
    try {
      const documentId = getDocumentId();
      const data = await api.getDocumentationObject(documentId);
      documentData = data;
    } catch (err: any) {
      console.error('Error loading document:', err);
      error = err.message || 'Не удалось загрузить документ';
    } finally {
      loading = false;
    }
  }

  function handleAccessGranted(): void {
    accessGranted = true;
  }

  function handleAccessDenied(): void {
    accessDenied = true;
  }

  // Проверяем наличие ID при загрузке
  onMount(() => {
    if (!page.params.id) {
      error = 'ID документа не указан';
      loading = false;
      accessDenied = true;
    }
  });
</script>

<svelte:head>
  <title>{pageTitle}</title>
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Проверка наличия ID -->
    {#if !page.params.id}
      <div class="text-center py-16">
        <div class="bg-rms-cod-gray rounded-lg border border-red-700 p-8 max-w-md mx-auto">
          <h2 class="text-2xl font-bold text-red-400 mb-2">Ошибка</h2>
          <p class="text-rms-nobel mb-6">ID документа не указан в URL</p>
          <a 
            href="/documentation" 
            class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
          >
            ← Вернуться к списку документов
          </a>
        </div>
      </div>
    {:else}
      <!-- Проверка доступа -->
      {#if !accessGranted && !accessDenied}
        <AccessCheck 
          itemId={getDocumentId()} 
          itemType="document"
          onAccessGranted={handleAccessGranted}
          onAccessDenied={handleAccessDenied}
        />
      {/if}

      <!-- Сообщение об отказе в доступе -->
      {#if accessDenied && page.params.id}
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-red-700 p-8 max-w-md mx-auto">
            <svg class="mx-auto h-16 w-16 text-red-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <h2 class="text-2xl font-bold text-red-400 mb-2">Доступ запрещен</h2>
            <p class="text-rms-nobel mb-6">{error || 'У вас недостаточный уровень допуска для просмотра этого документа'}</p>
            <a 
              href="/documentation" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку документов
            </a>
          </div>
        </div>
      {/if}

      <!-- Загрузка контента -->
      {#if accessGranted && loading}
        <div class="flex justify-center items-center py-16">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white"></div>
        </div>
      {/if}

      <!-- Ошибка загрузки -->
      {#if accessGranted && error && !documentData}
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-red-700 p-8 max-w-md mx-auto">
            <h2 class="text-2xl font-bold text-red-400 mb-2">Ошибка загрузки</h2>
            <p class="text-rms-nobel mb-6">{error}</p>
            <a 
              href="/documentation" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку документов
            </a>
          </div>
        </div>
      {/if}

      <!-- Контент документа -->
      {#if accessGranted && documentData}
        <div class="bg-rms-white text-rms-black rounded-lg shadow-2xl overflow-hidden">
          <!-- Заголовок документа в стиле А4 -->
          <div class="bg-rms-cod-gray text-rms-white p-8 border-b-4 border-red-600">
            <div class="flex justify-between items-start mb-4">
              <div>
                <span class="inline-block px-3 py-1 bg-red-600 text-white text-sm rounded-full mb-2">
                  {documentData.type_name}
                </span>
                <h1 class="text-3xl font-bold leading-tight">{documentData.title}</h1>
              </div>
              <span class="inline-flex items-center px-3 py-1 bg-red-900/30 text-red-300 rounded-full text-sm border border-red-700">
                {documentData.required_clearance_name}
              </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-rms-nobel">
              <div>
                <span class="font-medium text-rms-white">Автор:</span> {documentData.author_name}
              </div>
              <div>
                <span class="font-medium text-rms-white">Создан:</span> {formatDate(documentData.created_date)}
              </div>
              {#if documentData.updated_date !== documentData.created_date}
                <div class="md:col-span-2">
                  <span class="font-medium text-rms-white">Обновлен:</span> {formatDate(documentData.updated_date)}
                </div>
              {/if}
            </div>
          </div>

          <!-- Содержимое документа -->
          <div class="p-8 min-h-[calc(210mm-100px)] font-serif text-lg leading-relaxed">
            <div class="prose prose-lg max-w-none">
              {#each documentData.content.split('\n') as paragraph}
                {#if paragraph.trim()}
                  <p class="mb-4 text-justify">{paragraph}</p>
                {:else}
                  <br />
                {/if}
              {/each}
            </div>
          </div>

          <!-- Футер документа -->
          <div class="bg-rms-cod-gray text-rms-nobel p-6 border-t-4 border-red-600">
            <div class="flex justify-between items-center text-sm">
              <div>
                <span class="text-rms-white font-medium">RMS Laboratories</span> • Конфиденциально
              </div>
              <div class="text-right">
                <div>ID документа: {documentData.id}</div>
                <div>Требуемый уровень: {documentData.required_clearance_name}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Кнопка возврата -->
        <div class="mt-6 text-center">
          <a 
            href="/documentation" 
            class="inline-flex items-center px-6 py-3 bg-rms-cod-gray text-rms-white rounded-lg border border-rms-mine-shaft hover:border-rms-dove-gray hover:shadow-lg transition-all"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Вернуться к списку документов
          </a>
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  .prose {
    color: #111111;
  }
  
  .prose p {
    margin-bottom: 1rem;
    text-align: justify;
  }
  
  /* Стили для имитации бумаги А4 */
  @media (min-width: 210mm) {
    .bg-rms-white {
      box-shadow: 
        0 0 0 1px rgba(0,0,0,0.1),
        0 10px 30px rgba(0,0,0,0.3);
    }
  }
</style>