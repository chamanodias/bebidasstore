import os
import django
import requests
from PIL import Image
from io import BytesIO
import uuid
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Product
from django.core.files.base import ContentFile

def download_famous_brand_images():
    """Baixar imagens reais de marcas famosas específicas"""
    
    # URLs de imagens reais de produtos famosos
    famous_brand_images = {
        # CERVEJAS FAMOSAS - URLs mais estáveis
        'heineken-lager-330ml': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=400&fit=crop&q=80',
        'corona-extra-355ml': 'https://images.unsplash.com/photo-1572888224297-13c0e8f0d7b6?w=400&h=400&fit=crop&q=80',
        'stella-artois-330ml': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400&h=400&fit=crop&q=80',
        'budweiser-lata-350ml': 'https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=400&h=400&fit=crop&q=80',
        'skol-pilsen-lata-269ml': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400&h=400&fit=crop&q=80',
        'brahma-duplo-malte-350ml': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf6d2c?w=400&h=400&fit=crop&q=80',
        
        # DESTILADOS FAMOSOS
        'johnnie-walker-red-label-1l': 'https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=400&h=400&fit=crop&q=80',
        'jack-daniels-old-no7-750ml': 'https://images.unsplash.com/photo-1569275808161-2d29a4d6c2d1?w=400&h=400&fit=crop&q=80',
        'smirnoff-vodka-998ml': 'https://images.unsplash.com/photo-1560963689-b3785ac2a527?w=400&h=400&fit=crop&q=80',
        'absolut-vodka-original-750ml': 'https://images.unsplash.com/photo-1615332579937-523d95c451c4?w=400&h=400&fit=crop&q=80',
        
        # REFRIGERANTES FAMOSOS
        'coca-cola-original-350ml': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400&h=400&fit=crop&q=80',
        'pepsi-cola-350ml': 'https://images.unsplash.com/photo-1581006852262-e4307cf6283a?w=400&h=400&fit=crop&q=80',
        'guarana-antarctica-350ml': 'https://images.unsplash.com/photo-1625772299848-391b8a87d7b9?w=400&h=400&fit=crop&q=80',
        'fanta-laranja-350ml': 'https://images.unsplash.com/photo-1571689743307-2d62d3d82a80?w=400&h=400&fit=crop&q=80',
        'sprite-lima-limao-350ml': 'https://images.unsplash.com/photo-1564758564527-73ea13c65d56?w=400&h=400&fit=crop&q=80',
    }
    
    print("🏷️ Baixando imagens de marcas famosas...")
    success_count = 0
    
    for slug, image_url in famous_brand_images.items():
        try:
            # Buscar o produto pelo slug
            product = Product.objects.filter(slug=slug).first()
            
            if not product:
                print(f"⚠️ Produto não encontrado: {slug}")
                continue
            
            print(f"📥 Baixando imagem para: {product.name}")
            
            # Baixar a imagem
            response = requests.get(image_url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                # Processar imagem
                img_data = BytesIO(response.content)
                
                # Abrir e processar
                img = Image.open(img_data)
                
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar mantendo proporção
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                
                # Converter para bytes
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=90)
                img_io.seek(0)
                
                # Remover imagem anterior
                if product.image:
                    product.image.delete(save=False)
                
                # Salvar nova imagem
                filename = f"{product.slug}_brand_{uuid.uuid4().hex[:8]}.jpg"
                product.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                print(f"✅ Imagem baixada para {product.name}")
                success_count += 1
            else:
                print(f"❌ Falha ao baixar imagem para {product.name} (Status: {response.status_code})")
            
            # Pausa entre downloads
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Erro ao processar {slug}: {e}")
    
    return success_count

def main():
    print("🌐 Iniciando download de imagens de marcas famosas...")
    success_count = download_famous_brand_images()
    
    print(f"\n✅ Download concluído!")
    print(f"   Imagens de marcas famosas baixadas: {success_count}")
    
    # Estatísticas gerais
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas Gerais:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")

if __name__ == '__main__':
    main()
