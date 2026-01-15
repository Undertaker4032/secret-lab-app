<script lang="ts">
  import { page } from '$app/state';
  import AccessCheck from '$lib/components/ui/AccessCheck.svelte';
  import { api } from '$lib/utils/api';
  import { markdownToHtml, getTableOfContents } from '$lib/utils/markdown';
  import type { ResearchObject } from '$lib/utils/researchObject';

  let { data }: { data: { itemId: number } } = $props();

  let researchData = $state<ResearchObject | null>(null);
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
    researchData?.title 
      ? `${researchData.title} - Исследования` 
      : 'Исследование - RMS Laboratories'
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

  const getStatusColor = (status: string) => {
    const statusColors: Record<string, string> = {
      'Активно': 'bg-rms-mine-shaft text-rms-white',
      'Завершено': 'bg-rms-black text-rms-nobel border border-rms-mine-shaft',
      'Приостановлено': 'bg-rms-black text-rms-nobel border border-rms-mine-shaft',
      'В планах': 'bg-rms-black text-rms-nobel border border-rms-mine-shaft'
    };
    return statusColors[status] || 'bg-rms-black text-rms-nobel border border-rms-mine-shaft';
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

  function getResearchId(): number {
    return data.itemId;
  }

  async function handleAccessGranted(): Promise<void> {
    try {
      isLoading = true;
      researchData = await api.getResearchObject(getResearchId());
      
      // Рендер Markdown
      if (researchData?.content) {
        renderedContent = markdownToHtml(researchData.content);
        tableOfContents = getTableOfContents(renderedContent);
        
        shouldSetupObserver = true;
      }
      
      accessGranted = true;
      showAccessCheck = false;
    } catch (err) {
      console.error('Failed to load research:', err);
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
          <p class="text-rms-nobel mb-6">ID исследования не указан в URL</p>
          <a 
            href="/research" 
            class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded hover:bg-rms-nobel transition-colors"
          >
            ← Вернуться к списку исследований
          </a>
        </div>
      </div>
    {:else}
      <!-- Проверка доступа -->
      {#if showAccessCheck}
        <AccessCheck 
          itemId={getResearchId()} 
          itemType="research"
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
            <p class="text-rms-nobel mb-6">У вас недостаточный уровень допуска для просмотра этого исследования</p>
            <a 
              href="/research" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку исследований
            </a>
          </div>
        </div>
      {/if}

      <!-- Контент исследования -->
      {#if accessGranted && researchData}
        <div class="flex flex-col lg:flex-row gap-8">
          <!-- Боковая панель с оглавлением -->
          {#if tableOfContents.length > 0}
            <div class="lg:w-1/4 order-1 lg:order-2">
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

          <!-- Основной контент -->
          <div class="{tableOfContents.length > 0 ? 'lg:w-3/4 order-2 lg:order-1' : 'w-full'}">
            <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft overflow-hidden">
              <!-- Заголовок исследования -->
              <div class="p-8 border-b border-rms-mine-shaft">
                <div class="flex flex-col lg:flex-row justify-between items-start gap-4 mb-6">
                  <div class="flex-1">
                    <div class="flex flex-wrap items-center gap-2 mb-4">
                      <span class="inline-flex items-center px-3 py-1 bg-rms-mine-shaft text-rms-nobel text-sm rounded border border-rms-dove-gray">
                        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                        </svg>
                        ИССЛЕДОВАНИЕ
                      </span>
                      <span class="inline-flex items-center px-3 py-1 {getStatusColor(researchData.status_name)} text-sm rounded border border-rms-mine-shaft">
                        {researchData.status_name}
                      </span>
                      <span class="inline-flex items-center px-3 py-1 bg-rms-black text-rms-nobel text-sm rounded border border-rms-mine-shaft">
                        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                        </svg>
                        {researchData.required_clearance_name}
                      </span>
                    </div>
                    <h1 class="text-2xl font-bold text-rms-white leading-tight mb-4">{researchData.title}</h1>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-rms-nobel">
                      <div class="flex items-center">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                        </svg>
                        <span class="font-medium text-rms-white mr-2">Руководитель:</span>
                        {researchData.lead_name}
                      </div>
                      <div class="flex items-center">
                        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <span class="font-medium text-rms-white mr-2">Начато:</span>
                        {formatDate(researchData.created_date)}
                      </div>
                      {#if researchData.team_members.length > 0}
                        <div class="md:col-span-2 flex items-start">
                          <svg class="w-4 h-4 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                          </svg>
                          <div>
                            <span class="font-medium text-rms-white mr-2">Команда:</span>
                            {researchData.team_members.join(', ')}
                          </div>
                        </div>
                      {/if}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Содержимое исследования -->
              <div class="p-8 min-h-[400px]">
                {#if !researchData.content || researchData.content.trim() === ''}
                  <div class="text-center py-12">
                    <div class="w-16 h-16 mx-auto mb-4 text-rms-nobel">
                      <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                      </svg>
                    </div>
                    <p class="text-rms-nobel italic">Исследование не содержит описания</p>
                  </div>
                {:else}
                  <div class="markdown-content">
                    {@html renderedContent}
                  </div>
                {/if}
              </div>

              <!-- Футер исследования -->
              <div class="bg-rms-black p-6 border-t border-rms-mine-shaft">
                <div class="flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-rms-nobel">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                    </svg>
                    <span class="font-medium text-rms-white">RMS Laboratories</span>
                    <span class="mx-2">•</span>
                    <span>Научно-исследовательский отдел</span>
                  </div>
                  <div class="text-center sm:text-right">
                    <div>ID исследования: <span class="font-mono text-rms-white">{researchData.id}</span></div>
                    <div>Уровень доступа: <span class="text-rms-white">{researchData.required_clearance_name}</span></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Кнопка возврата -->
            <div class="mt-8 text-center">
              <a 
                href="/research" 
                class="inline-flex items-center px-6 py-3 bg-rms-cod-gray text-rms-white rounded hover:bg-rms-mine-shaft transition-colors border border-rms-mine-shaft"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
                </svg>
                Вернуться к списку исследований
              </a>
            </div>
          </div>
        </div>
      {:else if accessGranted && !researchData && !isLoading}
        <!-- Загрузка данных -->
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-rms-mine-shaft p-8 max-w-md mx-auto">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rms-white mx-auto mb-4"></div>
            <h2 class="text-xl font-bold text-rms-white mb-2">Загрузка исследования</h2>
            <p class="text-rms-nobel">Получение данных исследования...</p>
          </div>
        </div>
      {/if}
    {/if}
  </div>
</div>