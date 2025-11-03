<script lang="ts">
  import logo from "$lib/assets/NewLogoW.png";
  import menu from "$lib/assets/Menu.svg";
  import avatar from "$lib/assets/avatar.svg";
  import { isAuthenticated, user, employee } from '$lib/stores/auth';
  import { api } from '$lib/utils/api';
  import LoginModal from '$lib/components/LoginModal.svelte';
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  let { onToggleMenu }: { onToggleMenu?: () => void } = $props();

  let showLoginModal = $state(false);
  let showUserMenu = $state(false);

  async function handleLogout(): Promise<void> {
    await api.logout();
    showUserMenu = false;
  }

  // Закрываем меню пользователя при клике вне его
  function handleClickOutside(event: MouseEvent): void {
    if (!(event.target as HTMLElement).closest('.user-menu')) {
      showUserMenu = false;
    }
  }

  $effect(() => {
    if (showUserMenu) {
      document.addEventListener('click', handleClickOutside);
      return () => {
        document.removeEventListener('click', handleClickOutside);
      };
    }
  });
</script>

<header class="bg-rms-black border-b border-rms-mine-shaft shadow-lg">
  <div class="w-full mx-auto px-4 py-3 flex items-center justify-between">
    <!-- Левая часть: кнопка меню -->
    <button 
      class="cursor-pointer hover:bg-rms-mine-shaft rounded-2xl p-3 transition-all duration-200"
      onclick={() => onToggleMenu?.()}
      aria-label="Открыть меню"
    >
      <img src={menu} alt="Открыть меню" class="h-8 w-8">
    </button>
    
    <!-- Центр: логотип -->
    <a href="/" class="absolute left-1/2 transform -translate-x-1/2 flex items-center">
      <img src={logo} alt="RMS Laboratories" class="h-10 hover:opacity-90 transition-opacity">
    </a>
    
    <!-- Правая часть: пользователь или кнопка входа -->
    <div class="relative user-menu">
      {#if $isAuthenticated}
        <!-- Аватар и меню пользователя -->
        <button
          class="flex items-center space-x-3 p-2 rounded-lg hover:bg-rms-mine-shaft transition-all duration-200 border border-transparent hover:border-rms-dove-gray"
          onclick={() => showUserMenu = !showUserMenu}
          aria-label="Меню пользователя"
        >
          <img
            src={$employee?.profile_picture || avatar}
            alt="Аватар"
            class="w-10 h-10 rounded-full object-cover border-2 border-rms-dove-gray"
          />
          <div class="text-left hidden sm:block">
            <div class="font-medium text-rms-white text-sm">{$employee?.name || $user?.username}</div>
            <div class="text-rms-nobel text-xs">{$employee?.position?.name || 'Сотрудник'}</div>
          </div>
        </button>

        <!-- Выпадающее меню пользователя -->
        {#if showUserMenu}
          <div
            class="absolute right-0 mt-2 w-64 bg-rms-cod-gray rounded-lg shadow-xl py-2 z-50 border border-rms-mine-shaft"
            in:fly={{ duration: 200, easing: cubicOut, y: -10 }}
            out:fly={{ duration: 150, easing: cubicOut, y: -10 }}
          >
            <!-- Заголовок профиля -->
            <div class="px-4 py-3 border-b border-rms-mine-shaft">
              <div class="font-medium text-rms-white text-sm">{$employee?.name || $user?.username}</div>
              <div class="text-rms-nobel text-xs mt-1">{$employee?.position?.name || 'Сотрудник'}</div>
              {#if $employee?.clearance_level}
                <div class="inline-flex items-center mt-2 px-2 py-1 rounded-full text-xs font-medium bg-red-900/30 text-red-300 border border-red-700">
                  {$employee.clearance_level.name}
                </div>
              {/if}
            </div>

            <!-- Навигация профиля -->
            <div class="py-1">
              <a href="/" class="flex items-center px-4 py-2 text-sm text-rms-nobel hover:text-rms-white hover:bg-rms-mine-shaft transition-colors">
                <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                В разработке
              </a>
              <a href="/" class="flex items-center px-4 py-2 text-sm text-rms-nobel hover:text-rms-white hover:bg-rms-mine-shaft transition-colors">
                <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                В разработке
              </a>
            </div>

            <!-- Выход -->
            <div class="pt-1 border-t border-rms-mine-shaft">
              <button
                onclick={handleLogout}
                class="flex items-center w-full px-4 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-red-900/20 transition-colors"
              >
                <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Выйти
              </button>
            </div>
          </div>
        {/if}
      {:else}
        <!-- Кнопка входа -->
        <button
          class="bg-rms-white hover:bg-rms-nobel text-rms-black px-6 py-2.5 rounded-lg font-medium transition-all duration-200 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-rms-white focus:ring-offset-2 focus:ring-offset-rms-black"
          onclick={() => showLoginModal = true}
        >
          Войти
        </button>
      {/if}
    </div>
  </div>
</header>

<LoginModal bind:isOpen={showLoginModal} />