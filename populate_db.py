import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Category, Product
from django.utils.text import slugify

def create_categories():
    categories = [
        {'name': 'Vinhos Tintos', 'description': 'Vinhos tintos nacionais e importados'},
        {'name': 'Vinhos Brancos', 'description': 'Vinhos brancos frescos e aromáticos'},
        {'name': 'Cervejas Artesanais', 'description': 'Cervejas artesanais especiais'},
        {'name': 'Cervejas Premium', 'description': 'Cervejas premium importadas'},
        {'name': 'Destilados Premium', 'description': 'Whisky, Vodka, Gin e outros destilados'},
        {'name': 'Bebidas sem Álcool', 'description': 'Sucos, refrigerantes e energéticos'},
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

def create_products():
    # Obter categorias
    vinho_tinto = Category.objects.get(name='Vinhos Tintos')
    vinho_branco = Category.objects.get(name='Vinhos Brancos')
    cerveja_artesanal = Category.objects.get(name='Cervejas Artesanais')
    cerveja_premium = Category.objects.get(name='Cervejas Premium')
    destilados = Category.objects.get(name='Destilados Premium')
    sem_alcool = Category.objects.get(name='Bebidas sem Álcool')
    
    products = [
        # Vinhos Tintos
        {
            'name': 'Vinho Cabernet Sauvignon Premium',
            'category': vinho_tinto,
            'alcohol_type': 'vinhos',
            'description': 'Um excepcional Cabernet Sauvignon com notas de frutas vermelhas maduras, cassis e toques de carvalho. Perfeito para acompanhar carnes vermelhas e queijos curados.',
            'price': 89.90,
            'stock': 25,
            'featured': True,
            'alcohol_content': 13.5,
            'volume': '750ml'
        },
        {
            'name': 'Vinho Malbec Argentino',
            'category': vinho_tinto,
            'alcohol_type': 'vinhos',
            'description': 'Malbec argentino encorpado com aromas intensos de ameixa e especiarias. Ideal para momentos especiais.',
            'price': 65.00,
            'stock': 18,
            'featured': True,
            'alcohol_content': 14.0,
            'volume': '750ml'
        },
        
        # Vinhos Brancos
        {
            'name': 'Vinho Chardonnay Reserve',
            'category': vinho_branco,
            'alcohol_type': 'vinhos',
            'description': 'Chardonnay elegante com passagem por barrica, apresentando notas de frutas tropicais e baunilha.',
            'price': 72.50,
            'stock': 22,
            'featured': True,
            'alcohol_content': 12.5,
            'volume': '750ml'
        },
        {
            'name': 'Vinho Sauvignon Blanc',
            'category': vinho_branco,
            'alcohol_type': 'vinhos',
            'description': 'Sauvignon Blanc fresco e aromático com notas cítricas e herbáceas. Perfeito para dias quentes.',
            'price': 45.90,
            'stock': 30,
            'alcohol_content': 11.5,
            'volume': '750ml'
        },
        
        # Cervejas Artesanais
        {
            'name': 'Cerveja IPA Artesanal',
            'category': cerveja_artesanal,
            'alcohol_type': 'cervejas',
            'description': 'India Pale Ale artesanal com lúpulos selecionados, proporcionando amargor equilibrado e aroma floral.',
            'price': 18.90,
            'stock': 45,
            'featured': True,
            'alcohol_content': 6.2,
            'volume': '355ml'
        },
        {
            'name': 'Cerveja Stout Cremosa',
            'category': cerveja_artesanal,
            'alcohol_type': 'cervejas',
            'description': 'Stout encorpada com notas de café e chocolate, textura cremosa e final prolongado.',
            'price': 22.50,
            'stock': 35,
            'alcohol_content': 5.8,
            'volume': '355ml'
        },
        
        # Cervejas Premium
        {
            'name': 'Cerveja Premium Lager',
            'category': cerveja_premium,
            'alcohol_type': 'cervejas',
            'description': 'Lager premium importada com sabor suave e refrescante, ideal para qualquer ocasião.',
            'price': 8.90,
            'stock': 120,
            'featured': True,
            'alcohol_content': 4.5,
            'volume': '330ml'
        },
        {
            'name': 'Cerveja Wheat Premium',
            'category': cerveja_premium,
            'alcohol_type': 'cervejas',
            'description': 'Cerveja de trigo premium com sabor suave e notas cítricas, perfeita para o verão.',
            'price': 12.50,
            'stock': 80,
            'alcohol_content': 5.0,
            'volume': '500ml'
        },
        
        # Destilados
        {
            'name': 'Whisky Escocês 12 Anos',
            'category': destilados,
            'alcohol_type': 'destilados',
            'description': 'Whisky escocês single malt envelhecido por 12 anos, com notas defumadas e mel.',
            'price': 289.90,
            'stock': 12,
            'featured': True,
            'alcohol_content': 40.0,
            'volume': '750ml'
        },
        {
            'name': 'Vodka Premium Russa',
            'category': destilados,
            'alcohol_type': 'destilados',
            'description': 'Vodka premium russa destilada cinco vezes, pureza cristalina e sabor suave.',
            'price': 145.00,
            'stock': 20,
            'alcohol_content': 40.0,
            'volume': '750ml'
        },
        {
            'name': 'Gin London Dry',
            'category': destilados,
            'alcohol_type': 'destilados',
            'description': 'Gin London Dry clássico com botanicals selecionados, perfeito para drinks sofisticados.',
            'price': 98.50,
            'stock': 25,
            'alcohol_content': 37.5,
            'volume': '750ml'
        },
        
        # Bebidas sem Álcool
        {
            'name': 'Suco de Uva Integral Premium',
            'category': sem_alcool,
            'alcohol_type': 'sem_alcool',
            'description': 'Suco de uva integral premium, 100% natural, rico em antioxidantes.',
            'price': 28.90,
            'stock': 50,
            'featured': True,
            'volume': '1L'
        },
        {
            'name': 'Água Tônica Premium',
            'category': sem_alcool,
            'alcohol_type': 'sem_alcool',
            'description': 'Água tônica premium com quinino natural, ideal para drinks sofisticados.',
            'price': 15.90,
            'stock': 75,
            'volume': '500ml'
        },
        {
            'name': 'Energético Natural',
            'category': sem_alcool,
            'alcohol_type': 'sem_alcool',
            'description': 'Energético natural com guaraná, açaí e vitaminas, sem conservantes artificiais.',
            'price': 12.50,
            'stock': 60,
            'volume': '355ml'
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
    print("Populando banco de dados...")
    create_categories()
    print("\n" + "="*50 + "\n")
    create_products()
    print(f"\nBanco de dados populado com sucesso!")
    print(f"Categorias: {Category.objects.count()}")
    print(f"Produtos: {Product.objects.count()}")
    print(f"Produtos em destaque: {Product.objects.filter(featured=True).count()}")

if __name__ == '__main__':
    main()
