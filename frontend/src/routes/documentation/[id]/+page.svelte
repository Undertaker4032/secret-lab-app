<script lang="ts">
  import { page } from '$app/state';
  import AccessCheck from '$lib/components/ui/AccessCheck.svelte';
  import { api } from '$lib/utils/api';
  import type { DocumentObject } from '$lib/utils/documentObject';

  let { data }: { data: { itemId: number } } = $props();

  let documentData = $state<DocumentObject | null>(null);
  let accessGranted = $state(false);
  let accessDenied = $state(false);
  let showAccessCheck = $state(true);
  let isLoading = $state(false);

  const pageTitle = $derived(
    documentData?.title 
      ? `${documentData.title} - Документация` 
      : 'Документ - RMS Laboratories'
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

  function getDocumentId(): number {
    return data.itemId;
  }

  async function handleAccessGranted(): Promise<void> {
    try {
      isLoading = true;
      documentData = await api.getDocumentationObject(getDocumentId());
      accessGranted = true;
      showAccessCheck = false;
    } catch (err) {
      console.error('Failed to load document:', err);
      accessDenied = true;
      showAccessCheck = false;
    } finally {
      isLoading = false;
    }
  }

  function handleAccessDenied(): void {
    accessDenied = true;
    showAccessCheck = false;
  }
</script>

<svelte:head>
  <title>{pageTitle}</title>
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
    {#if !page.params.id}
      <div class="text-center py-16">
        <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft p-8 max-w-md mx-auto">
          <div class="w-12 h-12 mx-auto mb-4 text-rms-nobel">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.35 16.5c-.77.833.192 2.5 1.732 2.5z"/>
            </svg>
          </div>
          <h2 class="text-xl font-bold text-rms-white mb-2">Ошибка</h2>
          <p class="text-rms-nobel mb-6">ID документа не указан в URL</p>
          <a 
            href="/documentation" 
            class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded hover:bg-rms-nobel transition-colors"
          >
            ← Вернуться к списку документов
          </a>
        </div>
      </div>
    {:else}
      <!-- Проверка доступа -->
      {#if showAccessCheck}
        <AccessCheck 
          itemId={getDocumentId()} 
          itemType="document"
          onAccessGranted={handleAccessGranted}
          onAccessDenied={handleAccessDenied}
        />
      {/if}

      <!-- Сообщение об отказе в доступе -->
      {#if accessDenied}
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft p-8 max-w-md mx-auto">
            <div class="w-12 h-12 mx-auto mb-4 text-rms-nobel">
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
            <h2 class="text-xl font-bold text-rms-white mb-2">Доступ запрещен</h2>
            <p class="text-rms-nobel mb-6">У вас недостаточный уровень допуска для просмотра этого документа</p>
            <a 
              href="/documentation" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку документов
            </a>
          </div>
        </div>
      {/if}

      <!-- Контент документа -->
      {#if accessGranted && documentData}
        <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft overflow-hidden">
          <!-- Заголовок документа -->
          <div class="p-8 border-b border-rms-mine-shaft">
            <div class="flex flex-col lg:flex-row justify-between items-start gap-4 mb-6">
              <div class="flex-1">
                <div class="flex flex-wrap items-center gap-2 mb-4">
                  <span class="inline-flex items-center px-3 py-1 bg-rms-mine-shaft text-rms-nobel text-sm rounded border border-rms-dove-gray">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    {documentData.type_name}
                  </span>
                  <span class="inline-flex items-center px-3 py-1 bg-rms-black text-rms-nobel text-sm rounded border border-rms-mine-shaft">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    {documentData.required_clearance_name}
                  </span>
                </div>
                <h1 class="text-2xl font-bold text-rms-white leading-tight mb-4">{documentData.title}</h1>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-rms-nobel">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                    <span class="font-medium text-rms-white mr-2">Автор:</span>
                    {documentData.author_name}
                  </div>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    <span class="font-medium text-rms-white mr-2">Создан:</span>
                    {formatDate(documentData.created_date)}
                  </div>
                  {#if documentData.updated_date !== documentData.created_date}
                    <div class="md:col-span-2 flex items-center">
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 4a2 2 0 114 0v1a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-1a2 2 0 100 4h1a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-1a2 2 0 10-4 0v1a1 1 0 01-1 1H7a1 1 0 01-1-1v-3a1 1 0 00-1-1H4a2 2 0 110-4h1a1 1 0 001-1V7a1 1 0 011-1h3a1 1 0 001-1V4z"/>
                      </svg>
                      <span class="font-medium text-rms-white mr-2">Обновлен:</span>
                      {formatDate(documentData.updated_date)}
                    </div>
                  {/if}
                </div>
              </div>
            </div>
          </div>

          <!-- Содержимое документа -->
          <div class="p-8 min-h-[400px]">
            <div class="prose prose-invert max-w-none">
              {#if documentData.content.trim() === ''}
                <div class="text-center py-12">
                  <div class="w-16 h-16 mx-auto mb-4 text-rms-nobel">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <p class="text-rms-nobel italic">Документ не содержит текста</p>
                </div>
              {:else}
                <div class="space-y-6 text-rms-white leading-relaxed">
                  {#each documentData.content.split('\n') as paragraph, i}
                    {#if paragraph.trim()}
                      <p class="text-justify">{paragraph}</p>
                    {:else if i < documentData.content.split('\n').length - 1}
                      <div class="h-4"></div>
                    {/if}
                  {/each}
                </div>
              {/if}
            </div>
          </div>

          <!-- Футер документа -->
          <div class="bg-rms-black p-6 border-t border-rms-mine-shaft">
            <div class="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-rms-nobel">
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                </svg>
                <span class="font-medium text-rms-white">RMS Laboratories</span>
                <span class="mx-2">•</span>
                <span>Конфиденциально</span>
              </div>
              <div class="text-center sm:text-right">
                <div>ID документа: <span class="font-mono text-rms-white">{documentData.id}</span></div>
                <div>Уровень доступа: <span class="text-rms-white">{documentData.required_clearance_name}</span></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Кнопка возврата -->
        <div class="mt-8 text-center">
          <a 
            href="/documentation" 
            class="inline-flex items-center px-6 py-3 bg-rms-cod-gray text-rms-white rounded hover:bg-rms-mine-shaft transition-colors border border-rms-mine-shaft"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            Вернуться к списку документов
          </a>
        </div>
      {:else if accessGranted && !documentData && !isLoading}
        <!-- Загрузка данных -->
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft p-8 max-w-md mx-auto">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white mx-auto mb-4"></div>
            <h2 class="text-xl font-bold text-rms-white mb-2">Загрузка документа</h2>
            <p class="text-rms-nobel">Получение данных документа...</p>
          </div>
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  .prose-invert {
    color: #ffffff;
  }
  
  .prose-invert p {
    margin-bottom: 1rem;
    text-align: justify;
    line-height: 1.7;
  }
</style>