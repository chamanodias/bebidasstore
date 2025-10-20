import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Category, Product
from django.utils.text import slugify

def add_famous_brands():
    """Adicionar produtos de marcas famosas e conhecidas"""
    
    # Obter categorias
    categories = {cat.name: cat for cat in Category.objects.all()}
    
    # Se não tiver as categorias necessárias, criar algumas básicas
    if not categories:
        basic_categories = [
            {'name': 'Cervejas Populares', 'description': 'Cervejas de marcas conhecidas'},
            {'name': 'Vinhos Famosos', 'description': 'Vinhos de marcas reconhecidas'},
            {'name': 'Destilados Clássicos', 'description': 'Destilados de marcas tradicionais'},
            {'name': 'Refrigerantes Famosos', 'description': 'Refrigerantes de marcas conhecidas'},
        ]
        
        for cat_data in basic_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
    
    # Produtos de marcas famosas
    famous_products = [
        # CERVEJAS FAMOSAS
        {
            'name': 'Heineken Lager 330ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Heineken Premium Lager holandesa, refrescante e com sabor único. Garrafa de 330ml.',
            'price': Decimal('8.90'),
            'stock': 150,
            'featured': True,
            'alcohol_content': 5.0,
            'volume': '330ml'
        },
        {
            'name': 'Corona Extra 355ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Corona Extra mexicana, leve e refrescante. Perfeita com limão. Garrafa 355ml.',
            'price': Decimal('7.50'),
            'stock': 120,
            'featured': True,
            'alcohol_content': 4.6,
            'volume': '355ml'
        },
        {
            'name': 'Stella Artois 330ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Stella Artois belga premium, sabor sofisticado e encorpado. Garrafa 330ml.',
            'price': Decimal('9.50'),
            'stock': 100,
            'featured': True,
            'alcohol_content': 5.2,
            'volume': '330ml'
        },
        {
            'name': 'Budweiser Lata 350ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Budweiser americana, o rei das cervejas. Lata gelada 350ml.',
            'price': Decimal('6.90'),
            'stock': 200,
            'featured': False,
            'alcohol_content': 5.0,
            'volume': '350ml'
        },
        {
            'name': 'Skol Pilsen Lata 269ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Skol Pilsen brasileira, leve e refrescante. Lata 269ml.',
            'price': Decimal('3.50'),
            'stock': 300,
            'featured': False,
            'alcohol_content': 4.7,
            'volume': '269ml'
        },
        {
            'name': 'Brahma Duplo Malte 350ml',
            'category': categories.get('Cervejas Populares', list(categories.values())[0]),
            'alcohol_type': 'cervejas',
            'description': 'Cerveja Brahma Duplo Malte, mais sabor e corpo. Lata 350ml.',
            'price': Decimal('4.20'),
            'stock': 250,
            'featured': False,
            'alcohol_content': 4.8,
            'volume': '350ml'
        },
        
        # DESTILADOS FAMOSOS
        {
            'name': 'Johnnie Walker Red Label 1L',
            'category': categories.get('Destilados Clássicos', list(categories.values())[0]),
            'alcohol_type': 'destilados',
            'description': 'Whisky Johnnie Walker Red Label escocês, blend clássico e versátil. Garrafa 1L.',
            'price': Decimal('89.90'),
            'stock': 50,
            'featured': True,
            'alcohol_content': 40.0,
            'volume': '1L'
        },
        {
            'name': 'Jack Daniels Old No.7 750ml',
            'category': categories.get('Destilados Clássicos', list(categories.values())[0]),
            'alcohol_type': 'destilados',
            'description': 'Whiskey Jack Daniels Tennessee, suave e amadeirado. Garrafa 750ml.',
            'price': Decimal('129.90'),
            'stock': 30,
            'featured': True,
            'alcohol_content': 40.0,
            'volume': '750ml'
        },
        {
            'name': 'Smirnoff Vodka 998ml',
            'category': categories.get('Destilados Clássicos', list(categories.values())[0]),
            'alcohol_type': 'destilados',
            'description': 'Vodka Smirnoff premium, pura e cristalina. Garrafa 998ml.',
            'price': Decimal('45.90'),
            'stock': 80,
            'featured': False,
            'alcohol_content': 37.5,
            'volume': '998ml'
        },
        {
            'name': 'Absolut Vodka Original 750ml',
            'category': categories.get('Destilados Clássicos', list(categories.values())[0]),
            'alcohol_type': 'destilados',
            'description': 'Vodka Absolut sueca premium, sabor puro e icônico. Garrafa 750ml.',
            'price': Decimal('79.90'),
            'stock': 40,
            'featured': True,
            'alcohol_content': 40.0,
            'volume': '750ml'
        },
        
        # REFRIGERANTES FAMOSOS
        {
            'name': 'Coca-Cola Original 350ml',
            'category': categories.get('Refrigerantes Famosos', list(categories.values())[0]),
            'alcohol_type': 'sem_alcool',
            'description': 'Coca-Cola Original, o refrigerante mais famoso do mundo. Lata 350ml.',
            'price': Decimal('4.50'),
            'stock': 500,
            'featured': True,
            'volume': '350ml'
        },
        {
            'name': 'Pepsi Cola 350ml',
            'category': categories.get('Refrigerantes Famosos', list(categories.values())[0]),
            'alcohol_type': 'sem_alcool',
            'description': 'Pepsi Cola, sabor único e refrescante. Lata 350ml.',
            'price': Decimal('4.20'),
            'stock': 400,
            'featured': False,
            'volume': '350ml'
        },
        {
            'name': 'Guaraná Antarctica 350ml',
            'category': categories.get('Refrigerantes Famosos', list(categories.values())[0]),
            'alcohol_type': 'sem_alcool',
            'description': 'Guaraná Antarctica, sabor genuinamente brasileiro. Lata 350ml.',
            'price': Decimal('3.80'),
            'stock': 600,
            'featured': True,
            'volume': '350ml'
        },
        {
            'name': 'Fanta Laranja 350ml',
            'category': categories.get('Refrigerantes Famosos', list(categories.values())[0]),
            'alcohol_type': 'sem_alcool',
            'description': 'Fanta Laranja, refrescante sabor de laranja. Lata 350ml.',
            'price': Decimal('4.00'),
            'stock': 300,
            'featured': False,
            'volume': '350ml'
        },
        {
            'name': 'Sprite Lima-Limão 350ml',
            'category': categories.get('Refrigerantes Famosos', list(categories.values())[0]),
            'alcohol_type': 'sem_alcool',
            'description': 'Sprite Lima-Limão, refrescância cítrica. Lata 350ml.',
            'price': Decimal('4.00'),
            'stock': 350,
            'featured': False,
            'volume': '350ml'
        }
    ]
    
    print("🏷️ Adicionando produtos de marcas famosas...")
    
    created_count = 0
    for product_data in famous_products:
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
            print(f"✅ Produto criado: {product.name}")
            created_count += 1
        else:
            print(f"⚠️ Produto já existe: {product.name}")
    
    return created_count

def main():
    created_count = add_famous_brands()
    
    print(f"\n🎉 {created_count} novos produtos de marcas famosas adicionados!")
    
    # Estatísticas finais
    print(f"\n📊 Estatísticas Atualizadas:")
    print(f"   Total de produtos: {Product.objects.count()}")
    print(f"   Produtos em destaque: {Product.objects.filter(featured=True).count()}")
    
    # Por tipo de bebida
    print(f"\n🍷 Por tipo de bebida:")
    for choice in Product.ALCOHOL_CHOICES:
        count = Product.objects.filter(alcohol_type=choice[0]).count()
        print(f"   {choice[1]}: {count} produtos")

if __name__ == '__main__':
    main()
