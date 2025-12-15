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
</script>

<svelte:head>
	<link rel="icon" href={icon} />
	<title>RMS Laboratories</title>
</svelte:head>

<main class="text-rms-white px-[5%] md:px-[25%] pt-6 text-2xl">
    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">О нас</h1>
        <img src={lab00} alt="Изображение" class="py-3 rounded-4xl">
        <strong>RMS Laboratories</strong> — это глобальная сеть
        научно-исследовательских комплексов, определяющих
        вектор технологического развития всего
        человечества. Наша деятельность охватывает все
        ключевые научные дисциплины, от квантовой
        физики и генной инженерии до искусственного
        интеллекта и исследования пространственных
        аномалий.

        Наша штаб-квартира находится в сердце
        современного мегаполиса Крувер-Сити, а
        флагманский комплекс <strong>RMS-12</strong>, расположенный в
        удаленном горном массиве, служит оплотом для
        самых смелых и секретных экспериментов. Мы
        объединяем гениальные умы со всего мира и
        передовые ресурсы, чтобы превращать
        невозможное в реальность.  
    </section>

    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Наша Миссия</h1>
        Наша миссия — исследование и созидание во имя
        будущего. Мы решаем задачи, которые остальной
        мир считает невозможными, создаем технологии
        завтрашнего дня и раздвигаем границы познания,
        чтобы подарить человечеству новые горизонты.
    </section>
    
    <!-- АДМИНИСТРАЦИЯ -->
    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Руководство</h1>
        <img src={admin01} alt="Административный корпус" class="py-3 px-10 max-w-3/4 flex place-self-center">
        
        <div class="relative">
            <img src={back04} alt="Фон" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0 md:w-full">
            <div class="relative z-10">
                <p class="font-bold text-xl mb-4">Высшее руководство RMS-12:</p>
                <ul class="list-disc list-inside space-y-2 text-lg">
                    <li><strong>Генеральный Директор RMS-12</strong> - верховное руководство комплексом</li>
                    <li><strong>Дирекция Комплекса</strong> - стратегическое планирование и управление</li>
                    <li><strong>Совет Научных Надзоров</strong> - контроль исследовательской деятельности</li>
                </ul>
                <p class="mt-4">Администрация обеспечивает стратегическое видение, распределение ресурсов и поддержку всех направлений деятельности комплекса.</p>
            </div>
        </div>
    </section>

    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Структура комплекса</h1>
        Наша сила в стройной и высокоэффективной
        структуре, где каждый кластер выполняет важную
        роль в достижении общих целей.
    </section>

    <!-- НАУЧНЫЙ КЛАСТЕР -->
    <section class="py-3">
        <h2 class="text-3xl font-bold my-3">Научный Кластер</h2>
        <img src={lab02} alt="Научная лаборатория" class="py-3 px-10 max-w-3/4 flex place-self-center">
        
        <div class="relative">
            <img src={back01} alt="Фон" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0 md:w-full">
            <div class="relative z-10">
                <p class="mb-4">
                    Сердце и ум RMS. Учёные, теоретики и инженеры
                    из различных департаментов работают на передних
                    рубежах науки:
                </p>

                <div class="space-y-4 text-lg">
                    <div>
                        <strong class="text-xl">Департамент Физических Исследований</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Физика высоких энергий и квантовые вычисления</li>
                            <li>Исследование пространственно-временных аномалий</li>
                            <li>Проектная группа "Хронос"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Биологических Наук</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Генетика и биоинженерия</li>
                            <li>Ксенобиология и передовая медицина</li>
                            <li>Проектная группа "Генезис"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Материалов и Энергетики</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Синтез революционных материалов</li>
                            <li>Альтернативная энергетика</li>
                            <li>Проектная группа "Прометей"</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Кибернетических Систем</strong>
                        <ul class="list-disc list-inside ml-4">
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
        <h2 class="text-3xl font-bold my-3">Кластер Безопасности</h2>
        <img src={sec01} alt="Системы безопасности" class="py-3 px-10 max-w-3/4 flex place-self-center">

        <div class="relative">
            <img src={back02} alt="Фон" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0 md:w-full">
            <div class="relative z-10">
                <p class="mb-4">
                    Щит RMS. Элита, обеспечивающая
                    неприкосновенность наших исследований и
                    безопасность персонала.
                </p>

                <div class="space-y-4 text-lg">
                    <div>
                        <strong class="text-xl">Департамент Оперативной Безопасности</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Служба охраны и группа быстрого реагирования</li>
                            <li>Технические системы безопасности</li>
                            <li>Контрразведка и надзор</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Стратегической Защиты</strong>
                        <ul class="list-disc list-inside ml-4">
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
        <h2 class="text-3xl font-bold my-3">Операционный Кластер</h2>
        <img src={it01} alt="Инфраструктура" class="py-3 px-10 max-w-3/4 flex place-self-center">

        <div class="relative">
            <img src={back03} alt="Фон" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0 md:w-full">
            <div class="relative z-10">
                <p class="mb-4">
                    Кровь и нервная система RMS. Специалисты,
                    которые превращают теории в работающую
                    реальность:
                </p>

                <div class="space-y-4 text-lg">
                    <div>
                        <strong class="text-xl">Департамент Инфраструктуры</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Системы жизнеобеспечения комплекса</li>
                            <li>IT и коммуникационные системы</li>
                            <li>Энергоснабжение и техническое обслуживание</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Логистики</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Снабжение и транспортировка</li>
                            <li>Складской комплекс и управление запасами</li>
                            <li>Утилизация особых отходов</li>
                        </ul>
                    </div>

                    <div>
                        <strong class="text-xl">Департамент Персонала</strong>
                        <ul class="list-disc list-inside ml-4">
                            <li>Подбор и обучение специалистов</li>
                            <li>Медицинское обеспечение персонала</li>
                            <li>Архивы и документация</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Карьера в RMS</h1>
        <img src={lab01} alt="Карьера" class="py-3 px-10 max-w-3/4 flex place-self-center">

        Мы всегда находимся в поиске талантливых и
        целеустремлённых специалистов, готовых
        посвятить себя великому делу. Если вы — лучший в
        своей области и ваша жажда открытий превосходит
        общепринятые нормы, ваше место здесь.
        Присоединяйтесь к нам. Исследуйте неизведанное.
        Создавайте будущее.
    </section>

    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Контакты</h1>
        <p>Главный офис: Крувер-Сити, проспект Науки, 1.</p>
        <p>Для связи: <a href="https://t.me/RMSLabs" class="text-blue-300">t.me/RMSLabs</a></p>
    </section>
</main>

<div class="text-rms-nobel pb-6 px-[5%] md:px-[25%]">
    <div class="text-1xl font-roboto font-light pb-3">
        <em>Внимание: Комплекс RMS-12 не отображается на
        публичных картах. Все деловые визиты
        согласовываются исключительно через главный
        офис и сопровождаются нашими офицерами.</em>
    </div>
</div>