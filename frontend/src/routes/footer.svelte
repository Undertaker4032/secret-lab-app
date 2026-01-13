<script lang="ts">
    import logo from "$lib/assets/NewLogo1W.png";
</script>

<footer class="bg-rms-black border-t border-rms-mine-shaft text-rms-white">
    <div class="w-full max-w-7xl mx-auto px-4 py-6 sm:py-8">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <a href="/" class="flex items-center mb-4 sm:mb-0 space-x-3 rtl:space-x-reverse group">
                <img src={logo} class="h-8 group-hover:opacity-80 transition-opacity" alt="RMS Laboratories" />
            </a>
            <ul class="flex flex-wrap items-center mb-6 text-sm font-medium text-rms-nobel sm:mb-0">
                <li>
                    <a href="/about" class="hover:text-rms-white me-4 md:me-6 transition-colors">О лаборатории</a>
                </li>
                <li>
                    <a href="/careers" class="hover:text-rms-white me-4 md:me-6 transition-colors">Карьера</a>
                </li>
                <li>
                    <a href="/contact" class="hover:text-rms-white me-4 md:me-6 transition-colors">Контакты</a>
                </li>
                <li>
                    <a href="/security" class="hover:text-rms-white transition-colors">Безопасность</a>
                </li>
            </ul>
        </div>
        <hr class="my-6 border-rms-mine-shaft sm:mx-auto lg:my-8" />
        <div class="sm:flex sm:items-center sm:justify-between">
            <span class="text-sm text-rms-dove-gray sm:text-center">
                © 2025 <a href="/" class="hover:text-rms-white transition-colors">RMS Laboratories</a>. Все права защищены.
            </span>
            <div class="flex mt-4 space-x-5 sm:justify-center sm:mt-0">
                <a href="https://t.me/RMSLabs" class="text-rms-dove-gray hover:text-rms-white transition-colors" target="_blank">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"/>
                </svg>
                <span class="sr-only">Telegram канал</span>
                </a>
                <a href="/privacy" class="text-rms-dove-gray hover:text-rms-white transition-colors text-sm">
                    Конфиденциальность
                </a>
                <a href="/terms" class="text-rms-dove-gray hover:text-rms-white transition-colors text-sm">
                    Условия использования
                </a>
            </div>
        </div>
    </div>
</footer>