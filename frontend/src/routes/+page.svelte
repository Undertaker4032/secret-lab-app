<script>
    import '../app.css';
    import icon from '$lib/assets/logo-eye1.svg';
    import lab00 from '$lib/main/Lab00.png';
    import lab02 from '$lib/main/Lab02.svg';
    import lab03 from '$lib/main/Lab03.svg';
    import lab01 from '$lib/main/Lab01.svg';
    import sec01 from '$lib/main/Security01.svg';
    import it01 from '$lib/main/IT01.svg';
    import back01 from "$lib/main/back01.png"
    import back02 from "$lib/main/back02.png"
    import back03 from "$lib/main/back03.png"
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
    
    <section class="py-3">
        <h1 class="text-4xl font-bold my-3">Направления деятельности</h1>

        Наша сила в стройной и высокоэффективной
        структуре, где каждый кластер выполняет важную
        роль в достижении общих целей.
    </section>


    <section class="py-3">
        <h2 class="text-3xl font-bold my-3">Научный Кластер</h2>

        <img src={lab02} alt="Изображение" class="py-3 px-10 max-w-3/4 flex place-self-center">
        
        <div class="relative">
            <img src={back01} alt="Изображение" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0">
            <div class="relative z-10">
                <p>
                    Сердце и ум RMS. Учёные, теоретики и инженеры
                    из различных секторов работают на передних
                    рубежах науки:
                </p>

                <p>
                    <strong>Сектор A:</strong> Физика высоких энергий, квантовые
                    вычисления и исследование пространственно-
                    временных аномалий.
                </p>

                <p>
                    <strong>Сектор B:</strong> Генетика, биоинженерия и передовые
                    медицинские исследования.
                </p>

                <p>
                    <strong>Сектор C:</strong> Синтез новых материалов и
                    революционные энергетические решения.
                </p>
                
                <p>
                    <strong>Сектор D:</strong> Прикладная робототехника и разработка
                    искусственного интеллекта.
                </p>
            </div>
        </div>
    </section>


    <div class="py-3">
        <h2 class="text-3xl font-bold my-3">Кластер Безопасности</h2>

        <img src={sec01} alt="Изображение" class="py-3 px-10 max-w-3/4 flex place-self-center">

        <div class="relative">
            <img src={back02} alt="Изображение" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0">
            <div class="relative z-10">
                <p>
                    Щит RMS. Элита, обеспечивающая
                    неприкосновенность наших исследований и
                    безопасность персонала. В его задачи входит:
                    Круглосуточная охрана периметра и внутренней
                    инфраструктуры.
                </p>

                <p>
                    Проведение специальных операций и
                контрразведывательная деятельность.
                Обеспечение режима максимального сокрытия.
                </p>
            </div>
        </div>
    </div>


    <div class="py-3">
        <h2 class="text-3xl font-bold my-3">Операционный Кластер</h2>

        <img src={it01} alt="Изображение" class="py-3 px-10 max-w-3/4 flex place-self-center">

        <div class="relative">
            <img src={back03} alt="Изображение" class="flex place-self-center absolute inset-0 h-full object-cover opacity-10 z-0">
            <div class="relative z-10">
                <p>
                    Кровь и нервная система RMS. Специалисты,
                    которые превращают теории в работающую
                    реальность:
                </p>
                
                <p>
                    Поддержание систем жизнеобеспечения
                    комплекса.
                </p>
                
                <p>
                    Логистика, снабжение и утилизация.
                </p>
                
                <p>
                    IT, коммуникации и кадровое обеспечение.
                </p>
            </div>
        </div>
    </div>


    <div class="py-3">
        <h1 class="text-4xl font-bold my-3">Карьера в RMS</h1>

        <img src={lab01} alt="Изображение" class="py-3 px-10 max-w-3/4 flex place-self-center">

        Мы всегда находимся в поиске талантливых и
        целеустремлённых специалистов, готовых
        посвятить себя великому делу. Если вы — лучший в
        своей области и ваша жажда открытий превосходит
        общепринятые нормы, ваше место здесь.
        Присоединяйтесь к нам. Исследуйте неизведанное.
        Создавайте будущее.
    </div>


    <div class="py-3">
        <h1 class="text-4xl font-bold my-3">Контакты</h1>

        <p>Главный офис: Крувер-Сити, проспект Науки, 1.</p>
        <p>Для связи: <a href="https://t.me/RMSLabs" class="text-blue-300">t.me/RMSLabs</a></p>
    </div>
</main>


<div class="text-rms-nobel pb-6 px-[5%] md:px-[25%]">
    <div class="text-1xl font-roboto font-light pb-3">
        <em>Внимание: Комплекс RMS-12 не отображается на
        публичных картах. Все деловые визиты
        согласовываются исключительно через главный
        офис и сопровождаются нашими офицерами.</em>
    </div>
</div>