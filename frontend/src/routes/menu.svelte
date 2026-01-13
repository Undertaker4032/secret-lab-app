<script lang="ts">
  import menuIcon from "$lib/assets/Menu.svg";
  import { fade, fly } from "svelte/transition";
  import logo from "$lib/assets/NewLogoW.png";
  import avatar from "$lib/assets/avatar.svg";
  import { cubicOut } from "svelte/easing";
  import { isAuthenticated, user, employee } from '$lib/stores/auth';
  import { api } from '$lib/utils/api';

  let { open, onClose } = $props();

  function handleClose(): void {
    onClose?.();
  }

  function handleKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleClose();
    }
  }

  async function handleLogout(): Promise<void> {
    await api.logout();
    onClose?.();
  }

  let touchStartX = 0;
  let touchEndX = 0;
  let touchStartY = 0;
  let touchEndY = 0;
  let isSwiping = false;
  const SWIPE_THRESHOLD = 50;
  let menuTransform = $state('translateX(0)');

  function handleTouchStart(event: TouchEvent) {
    touchStartX = event.touches[0].clientX;
    touchStartY = event.touches[0].clientY;
    isSwiping = false;
  }

  function handleTouchMove(event: TouchEvent) {
    if (!open) return;
    
    const touchX = event.touches[0].clientX;
    const touchY = event.touches[0].clientY;
    const deltaX = touchX - touchStartX;
    const deltaY = touchY - touchStartY;
    
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
      isSwiping = true;
      event.preventDefault();
      
      if (deltaX < 0) {
        menuTransform = `translateX(${Math.max(deltaX, -100)}px)`;
      }
    }
  }

  function handleTouchEnd() {
    if (!isSwiping || !open) return;
    
    const swipeDistance = touchEndX - touchStartX;
    
    if (swipeDistance < -SWIPE_THRESHOLD) {
      handleClose();
    }
    
    menuTransform = 'translateX(0)';
    isSwiping = false;
  }

  function handleTouchCancel() {
    menuTransform = 'translateX(0)';
    isSwiping = false;
  }
</script>

{#if open}
  <!-- Оверлей -->
  <button
    in:fade={{ duration: 200 }}
    out:fade={{ duration: 150 }}
    class="fixed inset-0 bg-black opacity-70 z-40 border-none w-full h-full cursor-pointer"
    onclick={handleClose}
    onkeydown={handleKeydown}
    aria-label="Закрыть меню"
    type="button"
  ></button>

  <!-- Боковое меню -->
  <aside
    style="transform: {menuTransform}; transition: {isSwiping ? 'none' : 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)'}"
    class="flex flex-col w-80 sm:w-96 z-50 fixed top-0 left-0 h-screen px-4 py-4 overflow-y-auto bg-rms-cod-gray border-r border-rms-mine-shaft shadow-xl"
    ontouchstart={handleTouchStart}
    ontouchmove={handleTouchMove}
    ontouchend={handleTouchEnd}
    ontouchcancel={handleTouchCancel}
  >
    <!-- Верхняя часть с кнопкой закрытия и лого -->
    <div class="flex justify-between items-center mb-8">
      <button 
        class="cursor-pointer hover:bg-rms-mine-shaft rounded-2xl p-3 transition-all duration-200"
        onclick={handleClose}
        aria-label="Закрыть меню"
      >
        <img src={menuIcon} alt="Закрыть меню" class="h-8 w-8">
      </button>
      
      <a href="/" class="mx-auto">
        <img class="w-auto h-10" src={logo} alt="RMS Laboratories">
      </a>
      
      <div class="w-12"></div>
    </div>

    <!-- Блок профиля -->
    <div class="flex flex-col items-center mb-8 p-4 bg-rms-black rounded-xl border border-rms-mine-shaft">
      {#if $isAuthenticated}
        <div class="flex flex-col items-center">
          <img 
            class="object-cover w-24 h-24 rounded-full border-4 border-rms-dove-gray"
            src={$employee?.profile_picture || avatar}
            alt="Аватар сотрудника"
          />
          <h4 class="mt-4 font-medium text-rms-white text-lg text-center">
            {$employee?.name || $user?.username || 'Сотрудник'}
          </h4>
          <p class="mt-2 text-base font-medium text-rms-nobel text-center">
            {$employee?.position?.name || 'Должность не указана'}
          </p>
          
          {#if $employee?.clearance_level}
            <div class="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-700">
              {$employee.clearance_level.name}
            </div>
          {/if}
          
          {#if $employee?.division?.name}
            <div class="mt-3 space-y-1 text-center">
              <p class="text-sm text-rms-nobel">{$employee.division.name}</p>
              {#if $employee.department?.name}
                <p class="text-sm text-rms-nobel">{$employee.department.name}</p>
              {/if}
              {#if $employee.cluster?.name}
                <p class="text-sm text-rms-nobel">{$employee.cluster.name}</p>
              {/if}
            </div>
          {/if}
        </div>
      {:else}
        <div class="flex flex-col items-center">
          <img 
            class="object-cover w-24 h-24 rounded-full border-4 border-rms-mine-shaft"
            src={avatar}
            alt="Гость"
          />
          <h4 class="mt-4 font-medium text-rms-white text-lg">Гость</h4>
          <p class="mt-2 text-base font-medium text-rms-nobel">Пожалуйста, войдите в систему</p>
        </div>
      {/if}
    </div>
    
    <!-- Навигация -->
    <div class="flex flex-col justify-between flex-1">
      <nav class="space-y-2">
        <a class="flex items-center px-4 py-3 text-rms-nobel transition-all duration-200 rounded-lg hover:bg-rms-mine-shaft hover:text-rms-white text-lg border border-transparent hover:border-rms-dove-gray"
          href="/"
          onclick={handleClose}>
          <svg class="w-6 h-6 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          <span class="font-medium">Главная</span>
        </a>

        <a class="flex items-center px-4 py-3 text-rms-nobel transition-all duration-200 rounded-lg hover:bg-rms-mine-shaft hover:text-rms-white text-lg border border-transparent hover:border-rms-dove-gray" 
          href="/employees" 
          onclick={handleClose}>
          <svg class="w-6 h-6 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <span class="font-medium">Сотрудники</span>
        </a>

        <a class="flex items-center px-4 py-3 text-rms-nobel transition-all duration-200 rounded-lg hover:bg-rms-mine-shaft hover:text-rms-white text-lg border border-transparent hover:border-rms-dove-gray"
          href="/documentation"
          onclick={handleClose}>
          <svg class="w-6 h-6 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span class="font-medium">Документация</span>
        </a>

        <a class="flex items-center px-4 py-3 text-rms-nobel transition-all duration-200 rounded-lg hover:bg-rms-mine-shaft hover:text-rms-white text-lg border border-transparent hover:border-rms-dove-gray"
          href="/research"
          onclick={handleClose}>
          <svg class="w-6 h-6 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          <span class="font-medium">Исследования</span>
        </a>
      </nav>

      <!-- Кнопка выхода -->
      {#if $isAuthenticated}
        <div class="mt-auto pt-4 border-t border-rms-mine-shaft">
          <button
            onclick={handleLogout}
            class="flex items-center w-full px-4 py-3 text-red-400 hover:text-red-300 hover:bg-red-900/20 rounded-lg transition-all duration-200 border border-transparent hover:border-red-700 text-lg"
          >
            <svg class="w-6 h-6 mr-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="font-medium">Выйти</span>
          </button>
        </div>
      {/if}
    </div>
  </aside>
{/if}