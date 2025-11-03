<script lang="ts">
	import '../app.css';
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
	
	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}
	
	function closeMenu() {
		isMenuOpen = false;
	}
	
	// Инициализация аутентификации
	onMount(async () => {
		try {
			await initializeAuth();
		} catch (error) {
			console.error('Auth initialization failed:', error);
		} finally {
			authLoading.set(false);
		}
	});
	
	// Блокировка скролла
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
	<div class="flex items-center justify-center min-h-screen bg-gray-100">
		<div class="text-center">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
			<p class="mt-4 text-gray-600">Загрузка...</p>
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