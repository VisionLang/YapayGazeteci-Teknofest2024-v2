def categorize_news_type(news_type, types_list, return_type):
    if news_type in types_list:
        return return_type
    else:
        return news_type

def category_reducer(df):

    ##---------Yerel---------
    with open("../Preprocess-Data/iller.txt", 'r', encoding='utf-8') as f:
        cities = f.readlines()

    cities = [city.strip() for city in cities] + [
        'Kayseri Bölge', 'Karadeniz - Doğu Anadolu', 'Egeli Sabah', 'Marmara', 'Ankara Başkent', 'Akdeniz',
        'Güney'
        ]
        
    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=cities, return_type='Yerel')

    ##---------Futbol---------
    sports_teams = [
        "Beşiktaş", "Futbol", "Fenerbahçe",  "Galatasaray", "Trabzonspor", 'Türkiye Kupası', 'Euro 2020',
        'TFF 1. Lig', 'Spor Magazin', 'Transfer Haberleri', 'Uluslararası Futbol Ekonomi Forumu'
    ]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=sports_teams, return_type='Futbol')

    ##---------Dünya---------
    gloabl_list = ['Amerika', "Avrupa"]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=gloabl_list, return_type='Dünya')

    ##---------Yemek Tarifleri---------
    recipes_categories = [
        "Kahvaltılık Tarifler", "Çorbalar", "Sebze Yemekleri", "Vegan Tarifler", "Vejetaryen Tarifler",
        "Makarna Ve Pilav Tarifleri", "Yemek Tarifleri", "Kekler", "Salata ve Mezeler", 
        "Kurabiye Tarifleri", "Yemek", "Tatlılar", "Et Yemekleri", "Sağlıklı Tarifler",
        "Hamur İşi", 'Mutfak Sırları', 'İçecek Tarifleri', 'Tatlı Tarifleri', 'Börekler-Çörekler ve Poğaçalar',
        'Soslar ve İçecekler', 'Diğer Tarifler', 'Çorba Tarifleri', 'Pilav Tarifleri', 'Hamurişi Tarifleri',
        'Salata & Meze & Kanepe', 'Makarna Tarifleri', 'Bakliyat Yemekleri', 'Dolma-Sarma Tarifleri',
        'Sandviç Tarifleri', 'Aperatifler', 'Yumurta Yemekleri', 'Dünya Kupası', 'Diyet Yemekleri'
    ]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=recipes_categories, return_type='Yemek Tarifleri')

    ##---------Sağlık---------
    health_topics = ["Sağlık", "Çocuk Sağlığı", "Ruh Sağlığı", "Kadın Sağlığı", "Erkek Sağlığı"]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=health_topics, return_type='Sağlık')

    ##---------Kişisel Bakım---------
    personal_care_categories = [
        "Makyaj", "Saç Bakımı", "Cilt Bakımı", "Güzellik"
    ]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=personal_care_categories, return_type="Kişisel Bakım")

    ##---------Finans---------
    finans_categories = [
        "Finans Kripto Para Haberleri", "Ekonomi", "Finans Şirket Haberleri", "Finans Altın Haberleri", 
        "Finans Emtia-Döviz Haberleri", "Finans Borsa Haberleri", "Finans Gündem Haberleri", "Finans Ekonomi Haberleri",
    ]

    df['News_type'] = df['News_type'].apply(categorize_news_type, types_list=finans_categories, return_type="Finans")


    return df