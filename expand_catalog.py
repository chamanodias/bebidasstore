import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Category, Product
from django.utils.text import slugify

def create_expanded_categories():
    """Criar categorias mais específicas"""
    categories = [
        # Vinhos
        {'name': 'Vinhos Tintos Nacionais', 'description': 'Vinhos tintos produzidos no Brasil'},
        {'name': 'Vinhos Tintos Importados', 'description': 'Vinhos tintos internacionais premium'},
        {'name': 'Vinhos Brancos Secos', 'description': 'Vinhos brancos secos e frescos'},
        {'name': 'Vinhos Brancos Suaves', 'description': 'Vinhos brancos suaves e aromáticos'},
        {'name': 'Vinhos Rosé', 'description': 'Vinhos rosé elegantes e refrescantes'},
        {'name': 'Espumantes Nacionais', 'description': 'Espumantes brasileiros de qualidade'},
        {'name': 'Champagnes Importados', 'description': 'Champagnes franceses autênticos'},
        
        # Cervejas
        {'name': 'Cervejas Pilsner', 'description': 'Cervejas Pilsner leves e refrescantes'},
        {'name': 'Cervejas IPA', 'description': 'India Pale Ales lupuladas'},
        {'name': 'Cervejas Stout e Porter', 'description': 'Cervejas escuras encorpadas'},
        {'name': 'Cervejas Wheat', 'description': 'Cervejas de trigo suaves'},
        {'name': 'Cervejas Especiais', 'description': 'Cervejas com ingredientes especiais'},
        {'name': 'Cervejas Importadas', 'description': 'Cervejas internacionais premium'},
        
        # Destilados
        {'name': 'Whiskies Nacionais', 'description': 'Whiskies brasileiros de qualidade'},
        {'name': 'Whiskies Importados', 'description': 'Whiskies escoceses, irlandeses e americanos'},
        {'name': 'Cachaças Artesanais', 'description': 'Cachaças artesanais premium'},
        {'name': 'Vodkas Premium', 'description': 'Vodkas internacionais de alta qualidade'},
        {'name': 'Gins Artesanais', 'description': 'Gins com botânicos especiais'},
        {'name': 'Rum e Cachaças', 'description': 'Rums caribenhos e cachaças brasileiras'},
        
        # Sem Álcool
        {'name': 'Sucos Naturais', 'description': 'Sucos 100% naturais sem conservantes'},
        {'name': 'Refrigerantes Premium', 'description': 'Refrigerantes artesanais e importados'},
        {'name': 'Energéticos', 'description': 'Bebidas energéticas e isotônicos'},
        {'name': 'Águas Especiais', 'description': 'Águas minerais e saborizadas premium'},
        {'name': 'Chás e Kombucha', 'description': 'Chás gelados e kombucha probiótica'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'slug': slugify(cat_data['name']),
                'description': cat_data['description']
            }
        )
        if created:
            print(f"Categoria criada: {category.name}")

def create_expanded_products():
    """Criar catálogo expandido de produtos"""
    
    # Obter categorias
    categories = {cat.name: cat for cat in Category.objects.all()}
    
    products = [
        # VINHOS TINTOS NACIONAIS
        {
            'name': 'Vinho Tannat Uruguaio Premium',
            'category': categories['Vinhos Tintos Nacionais'],
            'alcohol_type': 'vinhos',
            'description': 'Tannat uruguaio com taninos firmes e sabor encorpado, ideal para carnes vermelhas grelhadas.',
            'price': Decimal('95.90'),
            'stock': 15,
            'featured': True,
            'alcohol_content': 14.5,
            'volume': '750ml'
        },
        {
            'name': 'Vinho Merlot Vale dos Vinhedos',
            'category': categories['Vinhos Tintos Nacionais'],
            'alcohol_type': 'vinhos',
            'description': 'Merlot brasileiro do Vale dos Vinhedos com notas de frutas vermelhas e chocolate.',
            'price': Decimal('78.50'),
            'stock': 25,
            'featured': False,
            'alcohol_content': 13.0,
            'volume': '750ml'
        },
        {
            'name': 'Vinho Cabernet Franc Nacional',
            'category': categories['Vinhos Tintos Nacionais'],
            'alcohol_type': 'vinhos',
            'description': 'Cabernet Franc brasileiro com perfil elegante e final persistente.',
            'price': Decimal('82.90'),
            'stock': 18,
            'featured': False,
            'alcohol_content': 13.5,
            'volume': '750ml'
        },
        
        # VINHOS TINTOS IMPORTADOS
        {
            'name': 'Barolo Italiano DOCG',
            'category': categories['Vinhos Tintos Importados'],
            'alcohol_type': 'vinhos',
            'description': 'Barolo italiano autêntico da região do Piemonte, envelhecido em carvalho francês.',
            'price': Decimal('289.90'),
            'stock': 8,
            'featured': True,
            'alcohol_content': 14.0,
            'volume': '750ml'
        },
        {
            'name': 'Bordeaux Francês Château',
            'category': categories['Vinhos Tintos Importados'],
            'alcohol_type': 'vinhos',
            'description': 'Bordeaux francês clássico com blend de Cabernet Sauvignon e Merlot.',
            'price': Decimal('195.50'),
            'stock': 12,
            'featured': True,
            'alcohol_content': 13.5,
            'volume': '750ml'
        },
        {
            'name': 'Rioja Reserva Espanhol',
            'category': categories['Vinhos Tintos Importados'],
            'alcohol_type': 'vinhos',
            'description': 'Rioja Reserva espanhol com 3 anos de envelhecimento, complexo e elegante.',
            'price': Decimal('145.90'),
            'stock': 20,
            'featured': False,
            'alcohol_content': 14.0,
            'volume': '750ml'
        },
        
        # VINHOS BRANCOS SECOS
        {
            'name': 'Sauvignon Blanc Chileno',
            'category': categories['Vinhos Brancos Secos'],
            'alcohol_type': 'vinhos',
            'description': 'Sauvignon Blanc chileno com acidez vibrante e notas cítricas refrescantes.',
            'price': Decimal('52.90'),
            'stock': 35,
            'featured': False,
            'alcohol_content': 12.5,
            'volume': '750ml'
        },
        {
            'name': 'Albariño Espanhol',
            'category': categories['Vinhos Brancos Secos'],
            'alcohol_type': 'vinhos',
            'description': 'Albariño da região de Rías Baixas, mineral e com grande frescor.',
            'price': Decimal('89.90'),
            'stock': 22,
            'featured': True,
            'alcohol_content': 12.0,
            'volume': '750ml'
        },
        {
            'name': 'Pinot Grigio Italiano',
            'category': categories['Vinhos Brancos Secos'],
            'alcohol_type': 'vinhos',
            'description': 'Pinot Grigio italiano leve e aromático, perfeito para aperitivos.',
            'price': Decimal('67.50'),
            'stock': 28,
            'featured': False,
            'alcohol_content': 11.5,
            'volume': '750ml'
        },
        
        # ESPUMANTES NACIONAIS
        {
            'name': 'Espumante Brut Nacional',
            'category': categories['Espumantes Nacionais'],
            'alcohol_type': 'vinhos',
            'description': 'Espumante brut brasileiro método tradicional com perlage fina e persistente.',
            'price': Decimal('72.90'),
            'stock': 25,
            'featured': True,
            'alcohol_content': 12.0,
            'volume': '750ml'
        },
        {
            'name': 'Prosecco Moscatel Nacional',
            'category': categories['Espumantes Nacionais'],
            'alcohol_type': 'vinhos',
            'description': 'Espumante moscatel brasileiro suave e aromático, ideal para sobremesas.',
            'price': Decimal('48.90'),
            'stock': 30,
            'featured': False,
            'alcohol_content': 11.0,
            'volume': '750ml'
        },
        
        # CERVEJAS IPA
        {
            'name': 'IPA American Hoppy',
            'category': categories['Cervejas IPA'],
            'alcohol_type': 'cervejas',
            'description': 'IPA americana com lúpulos Cascade e Centennial, amargor intenso e aroma cítrico.',
            'price': Decimal('18.90'),
            'stock': 60,
            'featured': True,
            'alcohol_content': 6.5,
            'volume': '355ml'
        },
        {
            'name': 'IPA Session Tropical',
            'category': categories['Cervejas IPA'],
            'alcohol_type': 'cervejas',
            'description': 'Session IPA com lúpulos tropicais, baixo teor alcoólico e alto sabor.',
            'price': Decimal('16.50'),
            'stock': 45,
            'featured': False,
            'alcohol_content': 4.8,
            'volume': '355ml'
        },
        {
            'name': 'Double IPA Imperial',
            'category': categories['Cervejas IPA'],
            'alcohol_type': 'cervejas',
            'description': 'Double IPA com duplo malte e lúpulo, para os amantes de cervejas intensas.',
            'price': Decimal('24.90'),
            'stock': 35,
            'featured': True,
            'alcohol_content': 8.2,
            'volume': '355ml'
        },
        
        # CERVEJAS PILSNER
        {
            'name': 'Pilsner Tcheca Premium',
            'category': categories['Cervejas Pilsner'],
            'alcohol_type': 'cervejas',
            'description': 'Pilsner tcheca autêntica com lúpulo Saaz e malte Pilsner tradicional.',
            'price': Decimal('12.90'),
            'stock': 80,
            'featured': False,
            'alcohol_content': 4.4,
            'volume': '330ml'
        },
        {
            'name': 'Pilsner Alemã Puro Malte',
            'category': categories['Cervejas Pilsner'],
            'alcohol_type': 'cervejas',
            'description': 'Pilsner alemã seguindo a lei da pureza, refrescante e equilibrada.',
            'price': Decimal('14.50'),
            'stock': 70,
            'featured': False,
            'alcohol_content': 4.8,
            'volume': '500ml'
        },
        
        # CERVEJAS STOUT
        {
            'name': 'Stout Imperial Coffee',
            'category': categories['Cervejas Stout e Porter'],
            'alcohol_type': 'cervejas',
            'description': 'Stout imperial com café brasileiro torrado, cremosa e intensa.',
            'price': Decimal('26.90'),
            'stock': 30,
            'featured': True,
            'alcohol_content': 9.0,
            'volume': '355ml'
        },
        {
            'name': 'Porter Chocolate Artesanal',
            'category': categories['Cervejas Stout e Porter'],
            'alcohol_type': 'cervejas',
            'description': 'Porter artesanal com cacau brasileiro, doce e encorpada.',
            'price': Decimal('22.50'),
            'stock': 40,
            'featured': False,
            'alcohol_content': 6.8,
            'volume': '355ml'
        },
        
        # WHISKIES IMPORTADOS
        {
            'name': 'Single Malt Escocês 18 Anos',
            'category': categories['Whiskies Importados'],
            'alcohol_type': 'destilados',
            'description': 'Single malt escocês 18 anos das Highlands, complexo e elegante.',
            'price': Decimal('590.00'),
            'stock': 6,
            'featured': True,
            'alcohol_content': 43.0,
            'volume': '750ml'
        },
        {
            'name': 'Bourbon Americano Premium',
            'category': categories['Whiskies Importados'],
            'alcohol_type': 'destilados',
            'description': 'Bourbon americano small batch com notas de baunilha e carvalho.',
            'price': Decimal('189.90'),
            'stock': 15,
            'featured': True,
            'alcohol_content': 45.0,
            'volume': '750ml'
        },
        {
            'name': 'Irish Whiskey Triple Destilado',
            'category': categories['Whiskies Importados'],
            'alcohol_type': 'destilados',
            'description': 'Whiskey irlandês triple destilado, suave e aromático.',
            'price': Decimal('145.90'),
            'stock': 20,
            'featured': False,
            'alcohol_content': 40.0,
            'volume': '750ml'
        },
        
        # CACHAÇAS ARTESANAIS
        {
            'name': 'Cachaça Artesanal Envelhecida',
            'category': categories['Cachaças Artesanais'],
            'alcohol_type': 'destilados',
            'description': 'Cachaça artesanal envelhecida em carvalho brasileiro por 3 anos.',
            'price': Decimal('85.90'),
            'stock': 25,
            'featured': True,
            'alcohol_content': 40.0,
            'volume': '700ml'
        },
        {
            'name': 'Cachaça Premium Ouro',
            'category': categories['Cachaças Artesanais'],
            'alcohol_type': 'destilados',
            'description': 'Cachaça premium com notas de madeira e mel, produção limitada.',
            'price': Decimal('125.50'),
            'stock': 18,
            'featured': True,
            'alcohol_content': 42.0,
            'volume': '700ml'
        },
        
        # GINS ARTESANAIS
        {
            'name': 'Gin Brasileiro Amazônico',
            'category': categories['Gins Artesanais'],
            'alcohol_type': 'destilados',
            'description': 'Gin brasileiro com botânicos da Amazônia, único e exótico.',
            'price': Decimal('128.90'),
            'stock': 22,
            'featured': True,
            'alcohol_content': 42.0,
            'volume': '750ml'
        },
        {
            'name': 'Gin London Dry Premium',
            'category': categories['Gins Artesanais'],
            'alcohol_type': 'destilados',
            'description': 'London Dry Gin premium com zimbro inglês e especiarias selecionadas.',
            'price': Decimal('98.50'),
            'stock': 30,
            'featured': False,
            'alcohol_content': 37.5,
            'volume': '750ml'
        },
        
        # SUCOS NATURAIS
        {
            'name': 'Suco de Açaí Integral',
            'category': categories['Sucos Naturais'],
            'alcohol_type': 'sem_alcool',
            'description': 'Suco de açaí integral sem açúcar, rico em antioxidantes.',
            'price': Decimal('18.90'),
            'stock': 50,
            'featured': False,
            'volume': '500ml'
        },
        {
            'name': 'Suco de Cupuaçu Natural',
            'category': categories['Sucos Naturais'],
            'alcohol_type': 'sem_alcool',
            'description': 'Suco de cupuaçu natural da Amazônia, sabor único e tropical.',
            'price': Decimal('22.50'),
            'stock': 35,
            'featured': True,
            'volume': '500ml'
        },
        {
            'name': 'Suco Detox Verde Orgânico',
            'category': categories['Sucos Naturais'],
            'alcohol_type': 'sem_alcool',
            'description': 'Suco detox com couve, maçã e limão, 100% orgânico.',
            'price': Decimal('16.90'),
            'stock': 40,
            'featured': False,
            'volume': '300ml'
        },
        
        # REFRIGERANTES PREMIUM
        {
            'name': 'Cola Artesanal Bourbon',
            'category': categories['Refrigerantes Premium'],
            'alcohol_type': 'sem_alcool',
            'description': 'Cola artesanal com baunilha bourbon, sabor premium único.',
            'price': Decimal('12.90'),
            'stock': 60,
            'featured': False,
            'volume': '330ml'
        },
        {
            'name': 'Guaraná Artesanal Amazônico',
            'category': categories['Refrigerantes Premium'],
            'alcohol_type': 'sem_alcool',
            'description': 'Guaraná artesanal com extrato natural da Amazônia.',
            'price': Decimal('8.90'),
            'stock': 80,
            'featured': True,
            'volume': '355ml'
        },
        
        # ENERGÉTICOS
        {
            'name': 'Energy Drink Açaí Guaraná',
            'category': categories['Energéticos'],
            'alcohol_type': 'sem_alcool',
            'description': 'Energético natural com açaí, guaraná e vitaminas do complexo B.',
            'price': Decimal('14.50'),
            'stock': 90,
            'featured': True,
            'volume': '355ml'
        },
        {
            'name': 'Isotônico Coco Natural',
            'category': categories['Energéticos'],
            'alcohol_type': 'sem_alcool',
            'description': 'Isotônico natural de coco, hidratação e reposição de eletrólitos.',
            'price': Decimal('9.90'),
            'stock': 75,
            'featured': False,
            'volume': '500ml'
        },
        
        # KOMBUCHA
        {
            'name': 'Kombucha Gengibre Limão',
            'category': categories['Chás e Kombucha'],
            'alcohol_type': 'sem_alcool',
            'description': 'Kombucha artesanal sabor gengibre com limão, probiótica e refrescante.',
            'price': Decimal('19.90'),
            'stock': 45,
            'featured': True,
            'volume': '355ml'
        },
        {
            'name': 'Chá Verde Gelado Orgânico',
            'category': categories['Chás e Kombucha'],
            'alcohol_type': 'sem_alcool',
            'description': 'Chá verde gelado orgânico com antioxidantes naturais.',
            'price': Decimal('12.50'),
            'stock': 55,
            'featured': False,
            'volume': '500ml'
        }
    ]
    
    for product_data in products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'slug': slugify(product_data['name']),
                'category': product_data['category'],
                'alcohol_type': product_data['alcohol_type'],
                'description': product_data['description'],
                'price': product_data['price'],
                'stock': product_data['stock'],
                'available': True,
                'featured': product_data.get('featured', False),
                'alcohol_content': product_data.get('alcohol_content'),
                'volume': product_data.get('volume', ''),
            }
        )
        if created:
            print(f"Produto criado: {product.name}")

def main():
    print("📦 Expandindo catálogo de produtos...")
    create_expanded_categories()
    print("\n" + "="*50 + "\n")
    create_expanded_products()
    print(f"\n✅ Catálogo expandido com sucesso!")
    
    # Estatísticas finais
    print(f"\n📊 Estatísticas do Catálogo:")
    print(f"   Categorias: {Category.objects.count()}")
    print(f"   Total de produtos: {Product.objects.count()}")
    print(f"   Produtos em destaque: {Product.objects.filter(featured=True).count()}")
    
    # Por tipo de bebida
    print(f"\n🍷 Por tipo de bebida:")
    for choice in Product.ALCOHOL_CHOICES:
        count = Product.objects.filter(alcohol_type=choice[0]).count()
        print(f"   {choice[1]}: {count} produtos")

if __name__ == '__main__':
    main()
