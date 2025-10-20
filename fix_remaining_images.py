import os
import django
import requests
from PIL import Image
from io import BytesIO
import uuid

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Product
from django.core.files.base import ContentFile

def fix_remaining_images():
    """Corrigir imagens dos produtos restantes com URLs alternativas"""
    
    # URLs alternativas para produtos que falharam
    alternative_urls = {
        'agua-tonica-premium': 'https://images.unsplash.com/photo-1625772299848-391b8a87d7b9?w=400&h=400&fit=crop&crop=center',
        'vodka-premium-russa': 'https://images.unsplash.com/photo-1569275808161-2d29a4d6c2d1?w=400&h=400&fit=crop&crop=center',
        'vinho-sauvignon-blanc': 'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=400&h=400&fit=crop&crop=center',
    }
    
    print("🔧 Corrigindo imagens dos produtos restantes...")
    
    for slug, url in alternative_urls.items():
        try:
            product = Product.objects.get(slug=slug)
            print(f"📥 Baixando imagem alternativa para: {product.name}")
            
            response = requests.get(url, timeout=15)
            
            if response.status_code == 200:
                # Processar imagem
                img_data = BytesIO(response.content)
                
                # Abrir e redimensionar se necessário
                img = Image.open(img_data)
                
                # Converter para RGB se necessário
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar mantendo proporção
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                
                # Converter de volta para bytes
                img_io = BytesIO()
                img.save(img_io, format='JPEG', quality=85)
                img_io.seek(0)
                
                # Remover imagem anterior se existir
                if product.image:
                    product.image.delete(save=False)
                
                # Salvar nova imagem
                filename = f"{product.slug}_fixed_{uuid.uuid4().hex[:8]}.jpg"
                product.image.save(
                    filename,
                    ContentFile(img_io.getvalue()),
                    save=True
                )
                
                print(f"✅ Imagem corrigida para {product.name}")
            else:
                print(f"❌ Falha ao baixar imagem alternativa para {product.name} (Status: {response.status_code})")
                
        except Product.DoesNotExist:
            print(f"❌ Produto não encontrado: {slug}")
        except Exception as e:
            print(f"❌ Erro ao processar {slug}: {e}")

def main():
    fix_remaining_images()
    print("\n✅ Correção de imagens concluída!")
    
    # Estatísticas finais
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas Finais:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")

if __name__ == '__main__':
    main()
