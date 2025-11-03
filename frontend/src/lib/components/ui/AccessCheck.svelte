<script lang="ts">
  import { api } from '$lib/utils/api';
  import { onMount } from 'svelte';
  import lottie from 'lottie-web';
  import { fade } from 'svelte/transition';

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
  let animationStep: 'idle' | 'start' | 'loading' | 'success' | 'fail' = $state('idle');
  let errorMessage: string = $state('');

  // Функции для управления анимациями
  function loadAnimation(animationName: string, loop: boolean = false): Promise<void> {
    return new Promise((resolve, reject) => {
      if (currentAnimation) {
        currentAnimation.destroy();
        currentAnimation = null;
      }

      if (!animationContainer) {
        reject(new Error('Animation container not found'));
        return;
      }

      try {
        currentAnimation = lottie.loadAnimation({
          container: animationContainer,
          renderer: 'svg',
          loop: loop,
          autoplay: true,
          path: `/animations/access/${animationName}.json`
        });

        currentAnimation.addEventListener('DOMLoaded', () => {
          console.log(`Анимация ${animationName} загружена`);
        });

        currentAnimation.addEventListener('error', (err: any) => {
          reject(new Error(`Не удалось загрузить анимацию ${animationName}`));
        });

        if (!loop) {
          currentAnimation.addEventListener('complete', () => resolve());
        } else {
          resolve();
        }
      } catch (err) {
        reject(err);
      }
    });
  }

  async function playAccessSequence(): Promise<void> {
    try {
      animationStep = 'start';
      await loadAnimation('AccessStart', false);
      
      animationStep = 'loading';
      await loadAnimation('Access', true);
      
    } catch (err) {
      console.error('Ошибка загрузки анимации:', err);
      animationStep = 'loading';
    }
  }

  async function playResultAnimation(success: boolean): Promise<void> {
    if (currentAnimation) {
      currentAnimation.destroy();
      currentAnimation = null;
    }
    
    try {
      if (success) {
        animationStep = 'success';
        await loadAnimation('AccessGranted', false);
      } else {
        animationStep = 'fail';
        await loadAnimation('AccessLocked', false);
      }
    } catch (err) {
      console.error('Ошибка загрузки финальной анимации:', err);
    }
  }

  async function checkAccess(): Promise<void> {
    errorMessage = '';
    animationStep = 'idle';

    try {
      await playAccessSequence();
      
      const url = itemType === 'document' 
        ? `/api/documentation/${itemId}/`
        : `/api/research/${itemId}/`;
      
      await api.get(url);
      
      await playResultAnimation(true);
      
      setTimeout(() => {
        onAccessGranted();
      }, 1000);
      
    } catch (err: any) {
      await playResultAnimation(false);
      
      if (err.message?.includes('403')) {
        errorMessage = 'Недостаточный уровень допуска для просмотра этого объекта';
      } else if (err.message?.includes('404')) {
        errorMessage = 'Объект не найден';
      } else {
        errorMessage = 'Произошла ошибка при проверке доступа';
      }
      
      setTimeout(() => {
        onAccessDenied();
      }, 2000);
    }
  }

  onMount(() => {
    checkAccess();
  });

  $effect(() => {
    return () => {
      if (currentAnimation) {
        currentAnimation.destroy();
        currentAnimation = null;
      }
    };
  });
</script>

<div class="fixed inset-0 bg-rms-black bg-opacity-90 z-50 flex items-center justify-center p-4">
  <div 
    in:fade={{ duration: 300 }}
    class="bg-rms-cod-gray rounded-2xl shadow-xl border border-rms-mine-shaft p-8 max-w-md w-full"
  >
    <div class="flex flex-col items-center justify-center py-4">
      <div 
        bind:this={animationContainer}
        class="w-64 h-64"
      ></div>
      
      <div class="mt-6 text-center">
        {#if animationStep === 'start'}
          <h3 class="text-xl font-bold text-rms-white mb-2">Инициализация проверки доступа</h3>
          <p class="text-rms-nobel">Подготовка системы безопасности...</p>
        {:else if animationStep === 'loading'}
          <h3 class="text-xl font-bold text-rms-white mb-2">Проверка уровня допуска</h3>
          <p class="text-rms-nobel">Сверяем разрешения...</p>
        {:else if animationStep === 'success'}
          <h3 class="text-xl font-bold text-green-400 mb-2">Доступ предоставлен</h3>
          <p class="text-rms-nobel">Уровень допуска подтвержден</p>
        {:else if animationStep === 'fail'}
          <h3 class="text-xl font-bold text-red-400 mb-2">Доступ запрещен</h3>
          <p class="text-rms-nobel">{errorMessage}</p>
        {:else}
          <h3 class="text-xl font-bold text-rms-white mb-2">Подготовка к проверке</h3>
          <p class="text-rms-nobel">Загрузка системы безопасности...</p>
        {/if}
      </div>
    </div>
  </div>
</div>