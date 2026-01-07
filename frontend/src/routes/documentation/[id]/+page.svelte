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
                  <div class="markdown-content">
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
  .markdown-content {
    color: #ffffff;
    line-height: 1.8;
    font-size: 17px;
    font-family: "Times New Roman", Times, serif;
    text-align: justify;
    text-justify: inter-word;
    letter-spacing: 0.01em;
  }
  
  /* Заголовки с более выраженной иерархией */
  .markdown-content h1 {
    font-family: "Times New Roman", Times, serif;
    font-size: 2.5em;
    font-weight: 700;
    margin-top: 2.5em;
    margin-bottom: 0.8em;
    padding-bottom: 0.4em;
    border-bottom: 2px solid #444;
    color: #f0f0f0;
    line-height: 1.3;
    letter-spacing: 0.02em;
  }
  
  .markdown-content h2 {
    font-family: "Times New Roman", Times, serif;
    font-size: 2em;
    font-weight: 700;
    margin-top: 2.2em;
    margin-bottom: 0.7em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid #444;
    color: #f0f0f0;
    line-height: 1.3;
    letter-spacing: 0.02em;
  }
  
  .markdown-content h3 {
    font-family: "Times New Roman", Times, serif;
    font-size: 1.6em;
    font-weight: 600;
    margin-top: 2em;
    margin-bottom: 0.6em;
    color: #f0f0f0;
    line-height: 1.4;
    letter-spacing: 0.01em;
  }
  
  .markdown-content h4 {
    font-family: "Times New Roman", Times, serif;
    font-size: 1.4em;
    font-weight: 600;
    margin-top: 1.8em;
    margin-bottom: 0.5em;
    color: #f0f0f0;
    line-height: 1.4;
  }
  
  .markdown-content h5, .markdown-content h6 {
    font-family: "Times New Roman", Times, serif;
    font-size: 1.2em;
    font-weight: 600;
    margin-top: 1.6em;
    margin-bottom: 0.5em;
    color: #f0f0f0;
    line-height: 1.4;
  }
  
  .markdown-content p {
    margin-bottom: 1.5em;
    text-align: justify;
    text-justify: inter-word;
    line-height: 1.8;
    hyphens: auto;
    -webkit-hyphens: auto;
    -moz-hyphens: auto;
    -ms-hyphens: auto;
  }
  
  .markdown-content ul, .markdown-content ol {
    margin-bottom: 1.5em;
    margin-top: 0.5em;
    padding-left: 2.5em;
    line-height: 1.8;
  }
  
  .markdown-content li {
    margin-bottom: 0.8em;
    line-height: 1.8;
  }
  
  .markdown-content li > p {
    margin-bottom: 0.5em;
  }
  
  .markdown-content blockquote {
    font-family: "Times New Roman", Times, serif;
    border-left: 4px solid #666;
    padding-left: 1.5em;
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    margin: 1.5em 0;
    color: #d4d4d4;
    font-style: italic;
    background-color: rgba(255, 255, 255, 0.05);
    line-height: 1.7;
  }
  
  .markdown-content blockquote p {
    margin-bottom: 0.5em;
  }
  
  .markdown-content code {
    font-family: 'Courier New', Courier, monospace;
    background-color: #2a2a2a;
    padding: 0.25em 0.5em;
    border-radius: 4px;
    font-size: 0.9em;
    color: #f8f8f2;
    border: 1px solid #3a3a3a;
  }
  
  .markdown-content pre {
    font-family: 'Courier New', Courier, monospace;
    background-color: #2a2a2a;
    padding: 1.2em;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1.5em 0;
    border: 1px solid #3a3a3a;
    line-height: 1.5;
  }
  
  .markdown-content pre code {
    background-color: transparent;
    padding: 0;
    border: none;
    font-size: 0.95em;
  }
  
  .markdown-content a {
    color: #6ea8fe;
    text-decoration: none;
    border-bottom: 1px solid #6ea8fe;
    transition: all 0.2s ease;
  }
  
  .markdown-content a:hover {
    color: #93c5fd;
    border-bottom: 2px solid #93c5fd;
    text-decoration: none;
  }
  
  .markdown-content table {
    font-family: "Times New Roman", Times, serif;
    border-collapse: collapse;
    width: 100%;
    margin: 1.5em 0;
    background-color: #2a2a2a;
    border: 1px solid #3a3a3a;
  }
  
  .markdown-content th, .markdown-content td {
    border: 1px solid #3a3a3a;
    padding: 0.9em;
    text-align: left;
    line-height: 1.5;
  }
  
  .markdown-content th {
    background-color: #333;
    font-weight: 600;
    color: #fff;
  }
  
  .markdown-content tr:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.03);
  }
  
  .markdown-content img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 1.5em 0;
    display: block;
    border: 1px solid #3a3a3a;
  }
  
  .markdown-content hr {
    border: none;
    border-top: 2px solid #444;
    margin: 2.5em 0;
    height: 0;
  }
  
  .markdown-content strong {
    font-weight: 700;
    color: #f0f0f0;
  }
  
  .markdown-content em {
    font-style: italic;
    color: #e0e0e0;
  }
  
  .markdown-content del {
    color: #999;
    text-decoration: line-through;
  }
  
  .markdown-content sup, .markdown-content sub {
    font-size: 0.8em;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
  }
  
  .markdown-content sup {
    top: -0.5em;
  }
  
  .markdown-content sub {
    bottom: -0.25em;
  }
  
  .toc-item {
    display: block;
    padding: 0.6em 0;
    color: #aaa;
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: all 0.2s ease;
    font-family: "Times New Roman", Times, serif;
    font-size: 0.95em;
    line-height: 1.5;
  }
  
  .toc-item:hover {
    color: #ffffff;
    border-left-color: #666;
    background-color: rgba(255, 255, 255, 0.05);
    padding-left: 0.5em;
  }
  
  .toc-item.active {
    color: #ffffff;
    border-left-color: #6ea8fe;
    font-weight: 600;
    background-color: rgba(110, 168, 254, 0.1);
    padding-left: 0.5em;
  }
  
  .toc-item.level-2 { padding-left: 1.2em; }
  .toc-item.level-3 { padding-left: 2.4em; }
  .toc-item.level-4 { padding-left: 3.6em; }
  .toc-item.level-5 { padding-left: 4.8em; }
  .toc-item.level-6 { padding-left: 6em; }
</style>