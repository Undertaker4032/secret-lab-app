<script>
    import icon from '$lib/assets/logo-eye1.svg';
    import lab00 from '$lib/main/Lab00.webp';
    import lab02 from '$lib/main/Lab02.svg';
    import lab03 from '$lib/main/Lab03.svg';
    import lab01 from '$lib/main/Lab01.svg';
    import sec01 from '$lib/main/Security01.svg';
    import it01 from '$lib/main/IT01.svg';
    import back01 from "$lib/main/back01.png"
    import back02 from "$lib/main/back02.png"
    import back03 from "$lib/main/back03.png"
    import back04 from "$lib/main/back04.svg"
    import admin01 from "$lib/main/Admin01.svg"
    
    import { onMount } from 'svelte';
    
    let imagesLoaded = $state(false);
    
    onMount(() => {
        setTimeout(() => {
            imagesLoaded = true;
        }, 100);
    });
</script>

<svelte:head>
    <link rel="icon" href={icon} />
    <title>RMS Laboratories</title>
    <meta name="description" content="RMS Laboratories — глобальная сеть научно-исследовательских комплексов, определяющих вектор технологического развития человечества.">
</svelte:head>

<main class="text-rms-white px-4 sm:px-[5%] md:px-[25%] pt-6 text-base sm:text-lg md:text-2xl">
    <!-- О НАС -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">О нас</h1>
        <img 
            src={lab00} 
            alt="Главное здание RMS Laboratories" 
            class="py-3 rounded-2xl sm:rounded-3xl md:rounded-4xl w-full h-auto"
            loading="lazy"
            width="1200"
            height="600"
        >
        <div class="space-y-4 text-base sm:text-lg md:text-xl">
            <p>
                <strong>RMS Laboratories</strong> — это глобальная сеть
                научно-исследовательских комплексов, определяющих
                вектор технологического развития всего
                человечества. Наша деятельность охватывает все
                ключевые научные дисциплины, от квантовой
                физики и генной инженерии до искусственного
                интеллекта и исследования пространственных
                аномалий.
            </p>
            <p>
                Наша штаб-квартира находится в сердце
                современного мегаполиса Крувер-Сити, а
                флагманский комплекс <strong>RMS-12</strong>, расположенный в
                удаленном горном массиве, служит оплотом для
                самых смелых и секретных экспериментов. Мы
                объединяем гениальные умы со всего мира и
                передовые ресурсы, чтобы превращать
                невозможное в реальность.
            </p>
        </div>
    </section>

    <!-- НАША МИССИЯ -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">Наша Миссия</h1>
        <div class="text-base sm:text-lg md:text-xl space-y-4">
            <p>
                Наша миссия — исследование и созидание во имя
                будущего. Мы решаем задачи, которые остальной
                мир считает невозможными, создаем технологии
                завтрашнего дня и раздвигаем границы познания,
                чтобы подарить человечеству новые горизонты.
            </p>
        </div>
    </section>
    
    <!-- АДМИНИСТРАЦИЯ -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">Руководство</h1>
        <img 
            src={admin01} 
            alt="Административный корпус RMS-12" 
            class="py-3 px-4 sm:px-10 w-full h-auto max-w-3xl mx-auto"
            loading="lazy"
            width="800"
            height="400"
        >
        
        <div class="bg-image-container mt-6">
            <img 
                src={back04} 
                alt="Фон административного корпуса" 
                class="bg-image"
                loading="lazy"
            >
            <div class="bg-image-content px-4 sm:px-6">
                <p class="font-bold text-lg sm:text-xl md:text-2xl mb-4 md:mb-6">Высшее руководство RMS-12:</p>
                <ul class="list-disc list-inside space-y-2 sm:space-y-3 text-sm sm:text-base md:text-lg">
                    <li><strong>Генеральный Директор RMS-12</strong> - верховное руководство комплексом</li>
                    <li><strong>Дирекция Комплекса</strong> - стратегическое планирование и управление</li>
                    <li><strong>Совет Научных Надзоров</strong> - контроль исследовательской деятельности</li>
                </ul>
                <p class="mt-4 md:mt-6 text-sm sm:text-base md:text-lg">
                    Администрация обеспечивает стратегическое видение, распределение ресурсов и поддержку всех направлений деятельности комплекса.
                </p>
            </div>
        </div>
    </section>

    <!-- СТРУКТУРА КОМПЛЕКСА -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">Структура комплекса</h1>
        <div class="text-base sm:text-lg md:text-xl space-y-4">
            <p>
                Наша сила в стройной и высокоэффективной
                структуре, где каждый кластер выполняет важную
                роль в достижении общих целей.
            </p>
        </div>
    </section>

    <!-- НАУЧНЫЙ КЛАСТЕР -->
    <section class="py-3">
        <h2 class="text-xl sm:text-2xl md:text-3xl font-bold my-3">Научный Кластер</h2>
        <img 
            src={lab02} 
            alt="Научная лаборатория RMS-12" 
            class="py-3 px-4 sm:px-10 w-full h-auto max-w-3xl mx-auto"
            loading="lazy"
            width="800"
            height="400"
        >
        
        <div class="bg-image-container mt-6">
            <img 
                src={back01} 
                alt="Фон научных исследований" 
                class="bg-image"
                loading="lazy"
            >
            <div class="bg-image-content px-4 sm:px-6">
                <p class="mb-4 md:mb-6 text-base sm:text-lg md:text-xl">
                    Сердце и ум RMS. Учёные, теоретики и инженеры
                    из различных департаментов работают на передних
                    рубежах науки:
                </p>

                <div class="space-y-4 sm:space-y-6 text-sm sm:text-base md:text-lg">
                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Физических Исследований</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Физика высоких энергий и квантовые вычисления</li>
                            <li>Исследование пространственно-временных аномалий</li>
                            <li>Проектная группа "Хронос"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Биологических Наук</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Генетика и биоинженерия</li>
                            <li>Ксенобиология и передовая медицина</li>
                            <li>Проектная группа "Генезис"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Материалов и Энергетики</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Синтез революционных материалов</li>
                            <li>Альтернативная энергетика</li>
                            <li>Проектная группа "Прометей"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Кибернетических Систем</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Передовая робототехника</li>
                            <li>Искусственный интеллект нового поколения</li>
                            <li>Проектная группа "Афина"</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- КЛАСТЕР БЕЗОПАСНОСТИ -->
    <section class="py-3">
        <h2 class="text-xl sm:text-2xl md:text-3xl font-bold my-3">Кластер Безопасности</h2>
        <img 
            src={sec01} 
            alt="Системы безопасности RMS-12" 
            class="py-3 px-4 sm:px-10 w-full h-auto max-w-3xl mx-auto"
            loading="lazy"
            width="800"
            height="400"
        >

        <div class="bg-image-container mt-6">
            <img 
                src={back02} 
                alt="Фон систем безопасности" 
                class="bg-image"
                loading="lazy"
            >
            <div class="bg-image-content px-4 sm:px-6">
                <p class="mb-4 md:mb-6 text-base sm:text-lg md:text-xl">
                    Щит RMS. Элита, обеспечивающая
                    неприкосновенность наших исследований и
                    безопасность персонала.
                </p>

                <div class="space-y-4 sm:space-y-6 text-sm sm:text-base md:text-lg">
                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Оперативной Безопасности</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Служба охраны и группа быстрого реагирования</li>
                            <li>Технические системы безопасности</li>
                            <li>Контрразведка и надзор</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Стратегической Защиты</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Внешние операции и маскировка</li>
                            <li>Разработка и испытание вооружения</li>
                            <li>Кибербезопасность и тактическое планирование</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- ОПЕРАЦИОННЫЙ КЛАСТЕР -->
    <section class="py-3">
        <h2 class="text-xl sm:text-2xl md:text-3xl font-bold my-3">Операционный Кластер</h2>
        <img 
            src={it01} 
            alt="Инфраструктура RMS-12" 
            class="py-3 px-4 sm:px-10 w-full h-auto max-w-3xl mx-auto"
            loading="lazy"
            width="800"
            height="400"
        >

        <div class="bg-image-container mt-6">
            <img 
                src={back03} 
                alt="Фон операционной инфраструктуры" 
                class="bg-image"
                loading="lazy"
            >
            <div class="bg-image-content px-4 sm:px-6">
                <p class="mb-4 md:mb-6 text-base sm:text-lg md:text-xl">
                    Кровь и нервная система RMS. Специалисты,
                    которые превращают теории в работающую
                    реальность:
                </p>

                <div class="space-y-4 sm:space-y-6 text-sm sm:text-base md:text-lg">
                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Инфраструктуры</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Системы жизнеобеспечения комплекса</li>
                            <li>IT и коммуникационные системы</li>
                            <li>Энергоснабжение и техническое обслуживание</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Логистики</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Снабжение и транспортировка</li>
                            <li>Складской комплекс и управление запасами</li>
                            <li>Утилизация особых отходов</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-base sm:text-lg md:text-xl block mb-2">Департамент Персонала</strong>
                        <ul class="list-disc list-inside ml-2 sm:ml-4 space-y-1">
                            <li>Подбор и обучение специалистов</li>
                            <li>Медицинское обеспечение персонала</li>
                            <li>Архивы и документация</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- КАРЬЕРА В RMS -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">Карьера в RMS</h1>
        <img 
            src={lab01} 
            alt="Карьерные возможности в RMS Laboratories" 
            class="py-3 px-4 sm:px-10 w-full h-auto max-w-3xl mx-auto"
            loading="lazy"
            width="800"
            height="400"
        >

        <div class="space-y-4 text-base sm:text-lg md:text-xl mt-6">
            <p>
                Мы всегда находимся в поиске талантливых и
                целеустремлённых специалистов, готовых
                посвятить себя великому делу. Если вы — лучший в
                своей области и ваша жажда открытий превосходит
                общепринятые нормы, ваше место здесь.
            </p>
            <p>
                Присоединяйтесь к нам. Исследуйте неизведанное.
                Создавайте будущее.
            </p>
        </div>
    </section>

    <!-- КОНТАКТЫ -->
    <section class="py-3">
        <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold my-3">Контакты</h1>
        <div class="space-y-3 text-base sm:text-lg md:text-xl">
            <p>📌 <strong>Главный офис:</strong> Крувер-Сити, проспект Науки, 1.</p>
            <p>📞 <strong>Для связи:</strong> <a href="https://t.me/RMSLabs" class="text-blue-300 hover:text-blue-400 transition-colors underline" target="_blank" rel="noopener noreferrer">t.me/RMSLabs</a></p>
            <p class="text-sm sm:text-base text-rms-nobel mt-4">
                <em>Часы работы: Пн-Пт 9:00-18:00 (по местному времени)</em>
            </p>
        </div>
    </section>
</main>

<!-- ФУТЕР -->
<div class="text-rms-nobel pb-6 px-4 sm:px-[5%] md:px-[25%] mt-6 sm:mt-8">
    <div class="text-sm sm:text-base font-roboto font-light p-4 sm:p-6 bg-rms-cod-gray/30 rounded-xl border border-rms-mine-shaft/50">
        <em>⚠️ Внимание: Комплекс RMS-12 не отображается на
        публичных картах. Все деловые визиты
        согласовываются исключительно через главный
        офис и сопровождаются нашими офицерами.</em>
    </div>
</div>