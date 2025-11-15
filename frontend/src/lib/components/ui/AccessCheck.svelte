<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import lottie from 'lottie-web';
  import { fade } from 'svelte/transition';
  import { api } from '$lib/utils/api';
  import { authLoading, isAuthenticated, accessToken, user, employee } from '$lib/stores/auth';
  import { get } from 'svelte/store';

  let { 
    itemId, 
    itemType, 
    onAccessGranted = () => {}, 
    onAccessDenied = () => {} 
  } = $props<{
    itemId: number;
    itemType: 'document' | 'research';
    onAccessGranted?: () => void;
    onAccessDenied?: () => void;
  }>();

  let animationContainer: HTMLDivElement = $state() as HTMLDivElement;
  let currentAnimation: any = $state(null);
  let animationStep: 'start' | 'checking' | 'success' | 'fail' = $state('start');
  let errorMessage: string = $state('');
  let accessCheckCompleted = $state(false);
  let accessCheckStarted = $state(false);

  async function loadAnimation(animationName: string, loop: boolean = false): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!animationContainer) {
        reject(new Error('Animation container not found'));
        return;
      }

      if (!document.body.contains(animationContainer)) {
        reject(new Error('Animation container not in DOM'));
        return;
      }

      if (currentAnimation) {
        currentAnimation.destroy();
        currentAnimation = null;
      }

      try {
        console.log(`Loading animation: /animations/access/${animationName}.json`);
        currentAnimation = lottie.loadAnimation({
          container: animationContainer,
          renderer: 'svg',
          loop: loop,
          autoplay: true,
          path: `/animations/access/${animationName}.json`
        });

        currentAnimation.addEventListener('DOMLoaded', () => {
          console.log(`Animation ${animationName} loaded successfully`);
        });

        currentAnimation.addEventListener('error', (err: any) => {
          console.error(`Animation ${animationName} error:`, err);
          reject(err);
        });

        if (!loop) {
          currentAnimation.addEventListener('complete', () => {
            console.log(`Animation ${animationName} completed`);
            resolve();
          });
        } else {
          console.log(`Animation ${animationName} started (loop)`);
          resolve();
        }
      } catch (err) {
        console.error(`Failed to load animation ${animationName}:`, err);
        reject(err);
      }
    });
  }

  async function waitForAnimationContainer(): Promise<void> {
    let attempts = 0;
    const maxAttempts = 10;
    
    while (!animationContainer && attempts < maxAttempts) {
      await tick();
      attempts++;
    }
    
    if (!animationContainer) {
      throw new Error('Animation container never became available');
    }
  }

  function switchAnimation(animationName: string, loop: boolean = false): void {
    if (currentAnimation) {
      currentAnimation.destroy();
      currentAnimation = null;
    }

    if (!animationContainer) return;

    try {
      currentAnimation = lottie.loadAnimation({
        container: animationContainer,
        renderer: 'svg',
        loop: loop,
        autoplay: true,
        path: `/animations/access/${animationName}.json`
      });
    } catch (err) {
      console.warn(`Failed to load animation ${animationName}:`, err);
    }
  }

  async function startAccessCheck(): Promise<void> {
    if (accessCheckCompleted || accessCheckStarted) return;
    
    accessCheckStarted = true;
    errorMessage = '';
    
    try {
      console.log(`=== STARTING ACCESS CHECK ===`);
      
      animationStep = 'checking';
      switchAnimation('Access', true);
      
      console.log(`Making API request for ${itemType} with ID: ${itemId}`);
      
      if (itemType === 'document') {
        await api.getDocumentationObject(itemId);
      } else if (itemType === 'research') {
        await api.getResearchObject(itemId);
      }
      
      console.log('Access granted by API');
      
      animationStep = 'success';
      switchAnimation('AccessGranted', false);
      
      accessCheckCompleted = true;
      
      setTimeout(() => {
        console.log('Calling onAccessGranted');
        onAccessGranted();
      }, 1500);
      
    } catch (err: any) {
      console.error('Access check error:', err);
      
      if (err.status === 403) {
        errorMessage = 'Недостаточный уровень допуска';
      } else if (err.status === 404) {
        errorMessage = 'Объект не найден';
      } else if (err.status === 401) {
        errorMessage = 'Ошибка авторизации';
      } else {
        errorMessage = 'Произошла ошибка при проверке доступа';
      }
      
      animationStep = 'fail';
      switchAnimation('AccessDenied', false);
      
      accessCheckCompleted = true;
      
      setTimeout(() => {
        console.log('Calling onAccessDenied');
        onAccessDenied();
      }, 2000);
    }
  }

  onMount(async () => {
    console.log('AccessCheck mounted');

    if (accessCheckStarted || accessCheckCompleted) return;

    await waitForAnimationContainer();

    try {
      console.log('Playing start animation...');
      await loadAnimation('AccessStart', false);
      console.log('Start animation completed');
    } catch (animError) {
      console.warn('Failed to load AccessStart animation, continuing...');
    }

    const currentToken = get(accessToken);
    const authenticated = get(isAuthenticated);
    const loading = get(authLoading);
    
    if (loading) {
      const unsubscribe = authLoading.subscribe((isLoading) => {
        if (!isLoading) {
          unsubscribe();
          checkAuthAndStartAccessCheck();
        }
      });
    } else {
      checkAuthAndStartAccessCheck();
    }

    function checkAuthAndStartAccessCheck() {
      if (!currentToken || !authenticated) {
        console.log('No auth token or not authenticated');
        errorMessage = 'Требуется авторизация';
        
        animationStep = 'fail';
        switchAnimation('AccessDenied', false);
        
        accessCheckCompleted = true;
        
        setTimeout(() => {
          onAccessDenied();
        }, 2000);
      } else {
        console.log('User authenticated, starting access check');
        startAccessCheck();
      }
    }
  });

  onDestroy(() => {
    console.log('AccessCheck destroyed');
    if (currentAnimation) {
      currentAnimation.destroy();
      currentAnimation = null;
    }
  });
</script>

<div class="fixed inset-0 bg-rms-black bg-opacity-90 z-50 flex items-center justify-center p-4">
  <div 
    in:fade={{ duration: 300 }}
    class="bg-rms-cod-gray rounded-2xl shadow-xl border border-rms-mine-shaft p-8 max-w-md w-full"
  >
    <div class="flex flex-col items-center justify-center py-4">
      <!-- Контейнер только для анимаций -->
      <div 
        bind:this={animationContainer}
        class="w-64 h-64"
      >
        <!-- Только анимации Lottie загружаются сюда -->
      </div>
      
      <!-- Только текстовые сообщения под анимацией -->
      <div class="mt-6 text-center">
        {#if animationStep === 'start'}
          <h3 class="text-xl font-bold text-rms-white mb-2">Инициализация системы безопасности</h3>
          <p class="text-rms-nobel">Запуск процедуры проверки доступа...</p>
        {:else if animationStep === 'checking'}
          <h3 class="text-xl font-bold text-rms-white mb-2">Проверка уровня допуска</h3>
          <p class="text-rms-nobel">Сверяем разрешения с центральным сервером...</p>
        {:else if animationStep === 'success'}
          <h3 class="text-xl font-bold text-green-400 mb-2">Доступ предоставлен</h3>
          <p class="text-rms-nobel">Уровень допуска подтвержден</p>
        {:else if animationStep === 'fail'}
          <h3 class="text-xl font-bold text-red-400 mb-2">Доступ запрещен</h3>
          <p class="text-rms-nobel">{errorMessage}</p>
        {/if}
      </div>
    </div>
  </div>
</div>