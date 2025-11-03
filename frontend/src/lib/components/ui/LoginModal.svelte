<script lang="ts">
  import { api } from '$lib/utils/api';
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  import { onMount } from 'svelte';
  import lottie from 'lottie-web';

  let { isOpen = $bindable(false), onClose = () => {} }: { isOpen?: boolean; onClose?: () => void } = $props();
  
  let username: string = $state('');
  let password: string = $state('');
  let error: string = $state('');
  let loading: boolean = $state(false);
  
  let animationContainer: HTMLDivElement = $state() as HTMLDivElement;
  let currentAnimation: any = $state(null);
  let animationStep: 'idle' | 'start' | 'loading' | 'success' | 'fail' = $state('idle');

  // ФИКС: Сохраняем данные формы даже во время анимации
  let savedUsername: string = $state('');
  let savedPassword: string = $state('');

  // Функции для управления анимациями
  function loadAnimation(animationName: string, loop: boolean = false): Promise<void> {
    return new Promise((resolve, reject) => {
      if (currentAnimation) {
        currentAnimation.destroy();
        currentAnimation = null;
      }

      if (!animationContainer) {
        console.error('Animation container not found');
        reject(new Error('Animation container not found'));
        return;
      }

      try {
        currentAnimation = lottie.loadAnimation({
          container: animationContainer,
          renderer: 'svg',
          loop: loop,
          autoplay: true,
          path: `/animations/login/${animationName}.json`
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

  async function playLoginSequence(): Promise<void> {
    try {
      animationStep = 'start';
      await loadAnimation('LoginStart', false);
      
      animationStep = 'loading';
      await loadAnimation('Login', true);
      
    } catch (err) {
      console.error('Ошибка загрузки анимации:', err);
      // Если анимация не загрузилась, продолжаем без нее
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
        await loadAnimation('LoginAccept', false);
      } else {
        animationStep = 'fail';
        await loadAnimation('LoginFail', false);
      }
    } catch (err) {
      console.error('Ошибка загрузки финальной анимации:', err);
    }
  }

  async function handleLogin(event: Event): Promise<void> {
    event.preventDefault();
    
    if (loading) return;
    
    // ФИКС: Сохраняем данные перед началом анимации
    savedUsername = username;
    savedPassword = password;
    
    error = '';
    loading = true;

    try {
      await playLoginSequence();
      
      // ФИКС: Используем сохраненные данные
      await api.login(savedUsername, savedPassword);
      
      await playResultAnimation(true);
      
      setTimeout(() => {
        isOpen = false;
        resetForm();
      }, 1000);
      
    } catch (err) {
      await playResultAnimation(false);
      error = err instanceof Error ? err.message : 'Ошибка входа. Проверьте логин и пароль.';
      
      // ФИКС: Возвращаем к форме через 2 секунды после анимации ошибки
      setTimeout(() => {
        animationStep = 'idle';
      }, 2000);
    } finally {
      loading = false;
    }
  }

  function resetForm(): void {
    username = '';
    password = '';
    savedUsername = '';
    savedPassword = '';
    animationStep = 'idle';
    error = '';
    if (currentAnimation) {
      currentAnimation.destroy();
      currentAnimation = null;
    }
  }

  function handleClose(): void {
    resetForm();
    isOpen = false;
  }

  // Обработчик клавиатуры для оверлея
  function handleOverlayKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClose();
    }
  }

  // Закрываем по ESC
  function handleKeydown(event: KeyboardEvent): void {
    if (event.key === 'Escape') {
      handleClose();
    }
  }

  $effect(() => {
    if (isOpen) {
      document.addEventListener('keydown', handleKeydown);
      
      return () => {
        document.removeEventListener('keydown', handleKeydown);
      };
    }
  });

  // Эффект для очистки анимации при размонтировании
  $effect(() => {
    return () => {
      if (currentAnimation) {
        currentAnimation.destroy();
        currentAnimation = null;
      }
    };
  });
</script>

{#if isOpen}
  <!-- Затемненный фон -->
  <button
    in:fade={{ duration: 200 }}
    out:fade={{ duration: 150 }}
    class="fixed inset-0 bg-black opacity-80 z-40 border-none w-full h-full cursor-pointer"
    onclick={handleClose}
    onkeydown={handleOverlayKeydown}
    aria-label="Закрыть модальное окно"
    type="button"
  ></button>

  <!-- Основной контейнер модального окна -->
  <div
    class="fixed inset-0 z-50 flex items-center justify-center p-4"
    in:fade={{ duration: 200 }}
    out:fade={{ duration: 150 }}
  >
    <div
      class="bg-rms-cod-gray rounded-2xl shadow-xl w-full max-w-md border border-rms-mine-shaft"
      in:fly={{ duration: 300, easing: cubicOut, y: -50 }}
      out:fly={{ duration: 200, easing: cubicOut, y: -50 }}
    >
      <div class="p-6">
        {#if animationStep === 'idle'}
          <!-- Показываем форму только когда нет активной анимации -->
          <form onsubmit={handleLogin}>
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-rms-white">Вход в систему</h2>
              <button
                type="button"
                onclick={handleClose}
                class="text-rms-nobel hover:text-rms-white text-2xl font-bold transition-colors p-1 rounded-full hover:bg-rms-mine-shaft"
                aria-label="Закрыть"
              >
                ×
              </button>
            </div>

            {#if error}
              <div class="mb-4 p-3 bg-red-900/30 border border-red-700 text-red-300 rounded-lg">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {error}
                </div>
              </div>
            {/if}

            <div class="space-y-4">
              <div>
                <label for="username" class="block text-sm font-medium text-rms-nobel mb-2">
                  Логин
                </label>
                <input
                  id="username"
                  type="text"
                  bind:value={username}
                  required
                  placeholder="Введите ваш логин"
                  class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
                />
              </div>

              <div>
                <label for="password" class="block text-sm font-medium text-rms-nobel mb-2">
                  Пароль
                </label>
                <input
                  id="password"
                  type="password"
                  bind:value={password}
                  required
                  placeholder="Введите ваш пароль"
                  class="w-full px-3 py-2 border border-rms-mine-shaft rounded-lg bg-rms-black text-rms-white placeholder-rms-dove-gray focus:outline-none focus:ring-2 focus:ring-rms-white focus:border-rms-white transition-colors"
                />
              </div>
            </div>

            <button
              type="submit"
              class="w-full mt-6 bg-rms-white hover:bg-rms-nobel text-rms-black font-medium py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-rms-white focus:ring-offset-2 focus:ring-offset-rms-cod-gray"
              disabled={loading}
            >
              {loading ? 'Вход...' : 'Войти'}
            </button>

            <div class="mt-4 text-center text-sm text-rms-nobel">
              <p>Нет аккаунта? Обратитесь к администратору</p>
            </div>
          </form>
        {:else}
          <!-- Показываем анимацию во время процесса логина -->
          <div class="flex flex-col items-center justify-center py-8">
            <div 
              bind:this={animationContainer}
              class="w-48 h-48"
            ></div>
            <div class="mt-4 text-center">
              {#if animationStep === 'start'}
                <p class="text-rms-white">Инициализация системы...</p>
              {:else if animationStep === 'loading'}
                <p class="text-rms-white">Проверка учетных данных...</p>
                <p class="text-rms-nobel text-sm mt-1">Пожалуйста, подождите</p>
              {:else if animationStep === 'success'}
                <p class="text-green-400 font-medium">Доступ предоставлен</p>
                <p class="text-rms-nobel text-sm mt-1">Перенаправление в систему</p>
              {:else if animationStep === 'fail'}
                <p class="text-red-400 font-medium">Доступ запрещен</p>
                <p class="text-rms-nobel text-sm mt-1">Возвращаемся к форме...</p>
              {/if}
            </div>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}