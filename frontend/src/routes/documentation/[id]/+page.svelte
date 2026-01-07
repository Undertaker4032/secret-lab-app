<script lang="ts">
  import { page } from '$app/state';
  import AccessCheck from '$lib/components/ui/AccessCheck.svelte';
  import { api } from '$lib/utils/api';
  import { markdownToHtml, getTableOfContents } from '$lib/utils/markdown';
  import type { DocumentObject } from '$lib/utils/documentObject';

  let { data }: { data: { itemId: number } } = $props();

  let documentData = $state<DocumentObject | null>(null);
  let accessGranted = $state(false);
  let accessDenied = $state(false);
  let showAccessCheck = $state(true);
  let isLoading = $state(false);
  
  // Новые состояния для Markdown
  let renderedContent = $state('');
  let tableOfContents = $state<Array<{ id: string; text: string; level: number }>>([]);
  let showToc = $state(true);
  let activeHeadingId = $state('');
  let shouldSetupObserver = $state(false);

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

  // Обработчик клика по заголовку в оглавлении
  const scrollToHeading = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      activeHeadingId = id;
    }
  };

  // Наблюдатель за активными заголовками
  const setupIntersectionObserver = () => {
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6[id]');
    if (headings.length === 0) return null;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            activeHeadingId = entry.target.id;
          }
        });
      },
      { 
        rootMargin: '-20% 0px -70% 0px',
        threshold: 0.1
      }
    );

    headings.forEach((heading) => {
      observer.observe(heading);
    });

    return observer;
  };

  function getDocumentId(): number {
    return data.itemId;
  }

  async function handleAccessGranted(): Promise<void> {
    try {
      isLoading = true;
      documentData = await api.getDocumentationObject(getDocumentId());
      
      // Рендер Markdown
      if (documentData?.content) {
        renderedContent = markdownToHtml(documentData.content);
        tableOfContents = getTableOfContents(renderedContent);

        shouldSetupObserver = true;
      }
      
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

  // Отдельный эффект для настройки IntersectionObserver
  $effect(() => {
    if (shouldSetupObserver && renderedContent && accessGranted) {
      const timer = setTimeout(() => {
        const observer = setupIntersectionObserver();
        return () => {
          observer?.disconnect();
        };
      }, 300);
      
      return () => {
        clearTimeout(timer);
      };
    }
  });
</script>

<svelte:head>
  <title>{pageTitle}</title>
</svelte:head>

<div class="min-h-screen bg-rms-black py-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
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
        <div class="flex flex-col lg:flex-row gap-8">
          <!-- Основной контент -->
          <div class="lg:w-3/4">
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
                  <div class="markdown-content override-headers">
                    {@html renderedContent}
                  </div>
                {/if}
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
          </div>

          <!-- Боковая панель с оглавлением -->
          {#if tableOfContents.length > 0}
            <div class="lg:w-1/4">
              <div class="sticky top-8">
                <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft p-6">
                  <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-rms-white flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                      </svg>
                      Содержание
                    </h3>
                    <button
                      on:click={() => showToc = !showToc}
                      class="text-rms-nobel hover:text-rms-white transition-colors"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {#if showToc}
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                        {:else}
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        {/if}
                      </svg>
                    </button>
                  </div>
                  
                  {#if showToc}
                    <nav class="space-y-1">
                      {#each tableOfContents as item}
                        <a
                          href="#{item.id}"
                          class="toc-item level-{item.level} {activeHeadingId === item.id ? 'active' : ''}"
                          on:click|preventDefault={() => scrollToHeading(item.id)}
                        >
                          {item.text}
                        </a>
                      {/each}
                    </nav>
                  {:else}
                    <p class="text-rms-nobel text-sm italic">Нажмите для отображения</p>
                  {/if}
                </div>
              </div>
            </div>
          {/if}
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
.markdown-content.override-headers {
    color: #ffffff;
    line-height: 1.8;
    font-size: 18px;
    font-family: "Times New Roman", Times, serif;
    text-align: justify;
    text-justify: inter-word;
    letter-spacing: 0.01em;
  }
  
  .markdown-content.override-headers h1,
  .markdown-content.override-headers h2,
  .markdown-content.override-headers h3,
  .markdown-content.override-headers h4,
  .markdown-content.override-headers h5,
  .markdown-content.override-headers h6 {
    all: initial;
    font-family: "Times New Roman", Times, serif !important;
    display: block !important;
    unicode-bidi: isolate !important;
    color: #ffffff !important;
    line-height: 1.2 !important;
    letter-spacing: 0.03em !important;
    margin: 0 !important;
    padding: 0 !important;
    border: 0 !important;
    box-sizing: border-box !important;
  }
  
  .markdown-content.override-headers h1 {
    font-size: 2.8em !important;
    font-weight: 900 !important;
    margin-top: 2.8em !important;
    margin-bottom: 1.2em !important;
    padding-bottom: 0.6em !important;
    border-bottom: 3px solid #555 !important;
  }
  
  .markdown-content.override-headers h2 {
    font-size: 2.3em !important;
    font-weight: 900 !important;
    margin-top: 2.5em !important;
    margin-bottom: 1em !important;
    padding-bottom: 0.5em !important;
    border-bottom: 2px solid #555 !important;
    line-height: 1.3 !important;
    letter-spacing: 0.02em !important;
  }
  
  .markdown-content.override-headers h3 {
    font-size: 1.9em !important;
    font-weight: 800 !important;
    margin-top: 2.2em !important;
    margin-bottom: 0.9em !important;
    line-height: 1.3 !important;
    letter-spacing: 0.02em !important;
  }
  
  .markdown-content.override-headers h4 {
    font-size: 1.6em !important;
    font-weight: 700 !important;
    margin-top: 2em !important;
    margin-bottom: 0.8em !important;
    line-height: 1.4 !important;
  }
  
  .markdown-content.override-headers h5 {
    font-size: 1.4em !important;
    font-weight: 700 !important;
    margin-top: 1.8em !important;
    margin-bottom: 0.7em !important;
    line-height: 1.4 !important;
  }
  
  .markdown-content.override-headers h6 {
    font-size: 1.3em !important;
    font-weight: 700 !important;
    margin-top: 1.6em !important;
    margin-bottom: 0.6em !important;
    line-height: 1.4 !important;
  }
  
  .markdown-content.override-headers p {
    margin-bottom: 2em;
    margin-top: 0;
    text-align: justify;
    text-justify: inter-word;
    line-height: 1.8;
    hyphens: auto;
    -webkit-hyphens: auto;
    -moz-hyphens: auto;
    -ms-hyphens: auto;
  }
  
  .markdown-content.override-headers h1 + p,
  .markdown-content.override-headers h2 + p,
  .markdown-content.override-headers h3 + p,
  .markdown-content.override-headers h4 + p,
  .markdown-content.override-headers h5 + p,
  .markdown-content.override-headers h6 + p {
    margin-top: 0.5em;
  }
  
  .markdown-content.override-headers p + h1,
  .markdown-content.override-headers p + h2,
  .markdown-content.override-headers p + h3,
  .markdown-content.override-headers p + h4,
  .markdown-content.override-headers p + h5,
  .markdown-content.override-headers p + h6 {
    margin-top: 3em !important;
  }
  
  .markdown-content.override-headers ul,
  .markdown-content.override-headers ol {
    margin-bottom: 2em;
    margin-top: 1em;
    padding-left: 2.5em;
    line-height: 1.8;
  }
  
  .markdown-content.override-headers li {
    margin-bottom: 0.8em;
    line-height: 1.8;
  }
  
  .markdown-content.override-headers li > p {
    margin-bottom: 0.5em;
  }
  
  .markdown-content.override-headers blockquote {
    font-family: "Times New Roman", Times, serif;
    border-left: 5px solid #777;
    padding-left: 1.8em;
    padding-top: 1em;
    padding-bottom: 1em;
    margin: 2.5em 0;
    color: #e0e0e0;
    font-style: italic;
    background-color: rgba(255, 255, 255, 0.05);
    line-height: 1.7;
    font-size: 1.1em;
  }
  
  .markdown-content.override-headers blockquote p {
    margin-bottom: 0.8em;
    line-height: 1.7;
  }
  
  .markdown-content.override-headers code {
    font-family: 'Courier New', Courier, monospace;
    background-color: #2a2a2a;
    padding: 0.25em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
    color: #f8f8f2;
    border: 1px solid #3a3a3a;
    font-weight: 500;
  }
  
  .markdown-content.override-headers pre {
    font-family: 'Courier New', Courier, monospace;
    background-color: #2a2a2a;
    padding: 1.5em;
    border-radius: 6px;
    overflow-x: auto;
    margin: 2em 0;
    border: 1px solid #3a3a3a;
    line-height: 1.5;
  }
  
  .markdown-content.override-headers pre code {
    background-color: transparent;
    padding: 0;
    border: none;
    font-size: 0.95em;
  }
  
  .markdown-content.override-headers a {
    color: #6ea8fe;
    text-decoration: none;
    border-bottom: 1px solid #6ea8fe;
    transition: all 0.2s ease;
    font-weight: 500;
  }
  
  .markdown-content.override-headers a:hover {
    color: #93c5fd;
    border-bottom: 2px solid #93c5fd;
    text-decoration: none;
  }
  
  .markdown-content.override-headers table {
    font-family: "Times New Roman", Times, serif;
    border-collapse: collapse;
    width: 100%;
    margin: 2em 0;
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
  }
  
  .markdown-content.override-headers th,
  .markdown-content.override-headers td {
    border: 1px solid #3a3a3a;
    padding: 1em;
    text-align: left;
    line-height: 1.5;
  }
  
  .markdown-content.override-headers th {
    background-color: #333;
    font-weight: 700;
    color: #fff;
    font-size: 1.05em;
  }
  
  .markdown-content.override-headers tr:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.03);
  }
  
  .markdown-content.override-headers img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 2.5em 0;
    display: block;
    border: 1px solid #3a3a3a;
  }
  
  .markdown-content.override-headers hr {
    border: none;
    border-top: 3px solid #555;
    margin: 3em 0;
    height: 0;
    opacity: 0.7;
  }
  
  .markdown-content.override-headers strong {
    font-weight: 700;
    color: #f0f0f0;
  }
  
  .markdown-content.override-headers em {
    font-style: italic;
    color: #e0e0e0;
  }
  
  .markdown-content.override-headers del {
    color: #999;
    text-decoration: line-through;
  }
  
  .markdown-content.override-headers sup,
  .markdown-content.override-headers sub {
    font-size: 0.75em;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
  }
  
  .markdown-content.override-headers sup {
    top: -0.6em;
  }
  
  .markdown-content.override-headers sub {
    bottom: -0.3em;
  }
  
  .markdown-content.override-headers p:first-of-type {
    font-size: 1.05em;
    line-height: 1.9;
  }
  
  .toc-item {
    display: block;
    padding: 0.8em 0;
    color: #aaa;
    text-decoration: none;
    border-left: 4px solid transparent;
    transition: all 0.2s ease;
    font-family: "Times New Roman", Times, serif;
    font-size: 0.95em;
    line-height: 1.6;
    margin-bottom: 0.3em;
  }
  
  .toc-item:hover {
    color: #ffffff;
    border-left-color: #777;
    background-color: rgba(255, 255, 255, 0.05);
    padding-left: 0.8em;
  }
  
  .toc-item.active {
    color: #ffffff;
    border-left-color: #6ea8fe;
    font-weight: 700;
    background-color: rgba(110, 168, 254, 0.15);
    padding-left: 0.8em;
  }
  
  .toc-item.level-2 { padding-left: 1.5em; }
  .toc-item.level-3 { padding-left: 3em; }
  .toc-item.level-4 { padding-left: 4.5em; }
  .toc-item.level-5 { padding-left: 6em; }
  .toc-item.level-6 { padding-left: 7.5em; }
  
  @media (max-width: 768px) {
    .markdown-content.override-headers {
      font-size: 17px;
      line-height: 1.8;
    }
    
    .markdown-content.override-headers h1 {
      font-size: 2.3em !important;
      margin-top: 2.5em !important;
      margin-bottom: 1em !important;
    }
    
    .markdown-content.override-headers h2 {
      font-size: 1.9em !important;
      margin-top: 2.2em !important;
    }
    
    .markdown-content.override-headers h3 {
      font-size: 1.6em !important;
    }
    
    .markdown-content.override-headers p {
      margin-bottom: 1.8em;
    }
    
    .toc-item {
      font-size: 0.9em;
      padding: 0.6em 0;
    }
  }
</style>