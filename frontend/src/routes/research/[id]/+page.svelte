<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/state';
  import { api } from '$lib/utils/api';
  import AccessCheck from '$lib/components/ui/AccessCheck.svelte';
  import type { ResearchObject } from '$lib/utils/researchObject';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let researchData: ResearchObject | null = $state(null);
  let loading = $state(true);
  let accessGranted = $state(false);
  let accessDenied = $state(false);
  let error = $state('');

  const pageTitle = $derived(
    data.meta?.title || 'Исследование - RMS Laboratories'
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
      'Активно': 'bg-green-600',
      'Завершено': 'bg-blue-600',
      'Приостановлено': 'bg-yellow-600',
      'В планах': 'bg-gray-600'
    };
    return statusColors[status] || 'bg-gray-600';
  };

  // Функция для безопасного получения ID
  function getResearchId(): number {
    const id = page.params.id;
    if (!id) {
      throw new Error('ID исследования не указан');
    }
    return +id;
  }

  async function loadResearch(): Promise<void> {
    try {
      const researchId = getResearchId();
      const data = await api.getResearchObject(researchId);
      researchData = data;
    } catch (err: any) {
      console.error('Error loading research:', err);
      error = err.message || 'Не удалось загрузить исследование';
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
      error = 'ID исследования не указан';
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
          <p class="text-rms-nobel mb-6">ID исследования не указан в URL</p>
          <a 
            href="/research" 
            class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
          >
            ← Вернуться к списку исследований
          </a>
        </div>
      </div>
    {:else}
      <!-- Проверка доступа -->
      {#if !accessGranted && !accessDenied}
        <AccessCheck 
          itemId={getResearchId()} 
          itemType="research"
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
            <p class="text-rms-nobel mb-6">{error || 'У вас недостаточный уровень допуска для просмотра этого исследования'}</p>
            <a 
              href="/research" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку исследований
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
      {#if accessGranted && error && !researchData}
        <div class="text-center py-16">
          <div class="bg-rms-cod-gray rounded-lg border border-red-700 p-8 max-w-md mx-auto">
            <h2 class="text-2xl font-bold text-red-400 mb-2">Ошибка загрузки</h2>
            <p class="text-rms-nobel mb-6">{error}</p>
            <a 
              href="/research" 
              class="inline-flex items-center px-4 py-2 bg-rms-white text-rms-black rounded-lg hover:bg-rms-nobel transition-colors"
            >
              ← Вернуться к списку исследований
            </a>
          </div>
        </div>
      {/if}

      <!-- Контент исследования -->
      {#if accessGranted && researchData}
        <div class="bg-rms-white text-rms-black rounded-lg shadow-2xl overflow-hidden">
          <!-- Заголовок исследования в стиле А4 -->
          <div class="bg-rms-cod-gray text-rms-white p-8 border-b-4 border-blue-600">
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <span class="inline-block px-3 py-1 bg-blue-600 text-white text-sm rounded-full">
                    ИССЛЕДОВАНИЕ
                  </span>
                  <span class="inline-block px-3 py-1 {getStatusColor(researchData.status_name)} text-white text-sm rounded-full">
                    {researchData.status_name}
                  </span>
                </div>
                <h1 class="text-3xl font-bold leading-tight">{researchData.title}</h1>
              </div>
              <span class="inline-flex items-center px-3 py-1 bg-red-900/30 text-red-300 rounded-full text-sm border border-red-700">
                {researchData.required_clearance_name}
              </span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-rms-nobel">
              <div>
                <span class="font-medium text-rms-white">Руководитель:</span> {researchData.lead_name}
              </div>
              <div>
                <span class="font-medium text-rms-white">Начато:</span> {formatDate(researchData.created_date)}
              </div>
              {#if researchData.team_members.length > 0}
                <div class="md:col-span-2">
                  <span class="font-medium text-rms-white">Команда:</span> {researchData.team_members.join(', ')}
                </div>
              {/if}
            </div>
          </div>

          <!-- Содержимое исследования -->
          <div class="p-8 min-h-[calc(210mm-100px)] font-serif text-lg leading-relaxed space-y-8">
            <!-- Описание -->
            {#if researchData.description}
              <section>
                <h2 class="text-2xl font-bold text-rms-cod-gray mb-4 border-b-2 border-blue-200 pb-2">
                  Описание исследования
                </h2>
                <div class="prose prose-lg max-w-none">
                  {#each researchData.description.split('\n') as paragraph}
                    {#if paragraph.trim()}
                      <p class="mb-4 text-justify">{paragraph}</p>
                    {:else}
                      <br />
                    {/if}
                  {/each}
                </div>
              </section>
            {/if}

            <!-- Цели -->
            {#if researchData.objectives}
              <section>
                <h2 class="text-2xl font-bold text-rms-cod-gray mb-4 border-b-2 border-blue-200 pb-2">
                  Цели исследования
                </h2>
                <div class="prose prose-lg max-w-none">
                  {#each researchData.objectives.split('\n') as paragraph}
                    {#if paragraph.trim()}
                      <p class="mb-4 text-justify">{paragraph}</p>
                    {:else}
                      <br />
                    {/if}
                  {/each}
                </div>
              </section>
            {/if}

            <!-- Результаты -->
            {#if researchData.findings}
              <section>
                <h2 class="text-2xl font-bold text-rms-cod-gray mb-4 border-b-2 border-green-200 pb-2">
                  Результаты и выводы
                </h2>
                <div class="prose prose-lg max-w-none">
                  {#each researchData.findings.split('\n') as paragraph}
                    {#if paragraph.trim()}
                      <p class="mb-4 text-justify">{paragraph}</p>
                    {:else}
                      <br />
                    {/if}
                  {/each}
                </div>
              </section>
            {/if}
          </div>

          <!-- Футер исследования -->
          <div class="bg-rms-cod-gray text-rms-nobel p-6 border-t-4 border-blue-600">
            <div class="flex justify-between items-center text-sm">
              <div>
                <span class="text-rms-white font-medium">RMS Laboratories</span> • Научно-исследовательский отдел
              </div>
              <div class="text-right">
                <div>ID исследования: {researchData.id}</div>
                <div>Требуемый уровень: {researchData.required_clearance_name}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Кнопка возврата -->
        <div class="mt-6 text-center">
          <a 
            href="/research" 
            class="inline-flex items-center px-6 py-3 bg-rms-cod-gray text-rms-white rounded-lg border border-rms-mine-shaft hover:border-rms-dove-gray hover:shadow-lg transition-all"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Вернуться к списку исследований
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