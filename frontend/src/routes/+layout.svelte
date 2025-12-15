<script lang="ts">
	import "../App.css"
	import icon from '$lib/assets/logo-eye1.svg';
	import Header from './header.svelte';
	import Footer from './footer.svelte';
	import Menu from './menu.svelte';
	import { onMount } from 'svelte';
	import { initializeAuth } from '$lib/utils/api';
	import { authLoading } from '$lib/stores/auth';

	let { children } = $props();

	let isMenuOpen = $state(false);
	let scrollbarWidth = $state(0);
	let authError = $state(false);
	let backendAvailable = $state(true);
	
	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}
	
	function closeMenu() {
		isMenuOpen = false;
	}
	
	onMount(async () => {
		try {
			console.log('Initializing auth...');
			
			// Сначала проверяем доступность бэкенда
			try {
				const healthResponse = await fetch('/api/health/', {
					credentials: 'include',
					method: 'GET'
				});
				backendAvailable = healthResponse.ok;
				console.log('Backend health check:', backendAvailable);
			} catch (error) {
				console.warn('Backend health check failed:', error);
				backendAvailable = false;
			}

			if (!backendAvailable) {
				console.log('Backend not available, skipping auth initialization');
				authError = false; // Не показываем ошибку, просто пропускаем аутентификацию
				authLoading.set(false);
				return;
			}
			
			// Получаем CSRF токен с retry логикой
			let csrfSuccess = false;
			let retries = 5;
			
			while (retries > 0 && !csrfSuccess) {
				try {
					const csrfResponse = await fetch('/api/auth/csrf/', {
						credentials: 'include',
						method: 'GET'
					});
					
					if (csrfResponse.ok) {
						csrfSuccess = true;
						console.log('CSRF token obtained');
					} else {
						throw new Error(`CSRF request failed: ${csrfResponse.status}`);
					}
				} catch (error) {
					retries--;
					if (retries === 0) throw error;
					console.warn(`CSRF fetch failed, ${retries} retries left`);
					await new Promise(resolve => setTimeout(resolve, 2000));
				}
			}
			
			await initializeAuth();
			console.log('Auth initialized successfully');
			authError = false;
			
		} catch (error) {
			console.error('Auth initialization failed:', error);
			// Не показываем ошибку если бэкенд недоступен или нет активной сессии
			if (error instanceof Error && 
				(error.message.includes('Failed to fetch') || 
				 error.message.includes('401'))) {
				authError = false;
			} else {
				authError = true;
			}
		} finally {
			console.log('Setting authLoading to false');
			authLoading.set(false);
		}
	});
	
	$effect(() => {
		if (isMenuOpen) {
			scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
			
			document.body.style.overflow = 'hidden';
			document.body.style.paddingRight = `${scrollbarWidth}px`;
		} else {
			document.body.style.overflow = '';
			document.body.style.paddingRight = '';
		}
		
		return () => {
			document.body.style.overflow = '';
			document.body.style.paddingRight = '';
		};
	});

</script>

<svelte:head>
	<link rel="icon" href={icon} />
	<title>RMS Laboratories</title>
</svelte:head>

<svelte:window onkeydown={(e) => {
    if (e.key === 'Escape' && isMenuOpen) closeMenu();
}} />

{#if $authLoading}
	<div class="flex items-center justify-center min-h-screen bg-rms-black">
		<div class="text-center">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
			<p class="mt-4 text-rms-nobel">
				{backendAvailable ? 'Инициализация системы безопасности...' : 'Загрузка сервисов...'}
			</p>
		</div>
	</div>
{:else if authError}
  <div class="flex items-center justify-center min-h-screen bg-rms-black">
    <div class="text-center bg-rms-cod-gray rounded-lg border border-red-700 p-8 max-w-md mx-4">
      <div class="text-red-400 text-4xl mb-4">⚠️</div>
      <h2 class="text-xl font-bold text-rms-white mb-2">Ошибка инициализации</h2>
      <p class="text-rms-nobel mb-4">Не удалось загрузить систему безопасности</p>
      <button 
        onclick={() => location.reload()} 
        class="px-4 py-2 bg-red-600 text-rms-white rounded hover:bg-red-700 transition-colors"
      >
        Перезагрузить
      </button>
    </div>
  </div>
{:else}
	<div class="font-roboto min-h-screen flex flex-col">
		<Menu open={isMenuOpen} onClose={closeMenu} />
		<Header onToggleMenu={toggleMenu} />
		<div class:blur={isMenuOpen} class="flex-1 mt-[80px]">
			{@render children?.()}
		</div>
		<Footer />
	</div>
{/if}

<style>
	.blur {
		filter: blur(2px);
		transition: filter 0.3s ease;
	}
</style>