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

# APIs gratuitas para imagens
UNSPLASH_ACCESS_KEY = "demo"  # Você pode se cadastrar em unsplash.com/developers para uma chave real
PIXABAY_API_KEY = "demo"      # Você pode se cadastrar em pixabay.com/api/docs/ para uma chave real

def get_unsplash_image(query):
    """Busca imagem no Unsplash"""
    try:
        # API demo do Unsplash - em produção, use uma chave real
        url = f"https://source.unsplash.com/400x400/?{query}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        print(f"Erro ao buscar no Unsplash: {e}")
    return None

def get_product_image_query(product):
    """Gera query de busca baseada no produto"""
    queries = {
        'vinho-cabernet-sauvignon-premium': 'red wine bottle cabernet',
        'vinho-malbec-argentino': 'red wine bottle malbec',
        'vinho-chardonnay-reserve': 'white wine bottle chardonnay',
        'vinho-sauvignon-blanc': 'white wine bottle sauvignon',
        'cerveja-ipa-artesanal': 'craft beer ipa bottle',
        'cerveja-stout-cremosa': 'stout beer dark bottle',
        'cerveja-premium-lager': 'premium beer lager bottle',
        'cerveja-wheat-premium': 'wheat beer bottle',
        'whisky-escoces-12-anos': 'scotch whisky bottle',
        'vodka-premium-russa': 'premium vodka bottle',
        'gin-london-dry': 'gin bottle london dry',
        'suco-de-uva-integral-premium': 'grape juice bottle',
        'agua-tonica-premium': 'tonic water bottle',
        'energetico-natural': 'energy drink bottle natural'
    }
    
    # Se temos uma query específica, usa ela
    if product.slug in queries:
        return queries[product.slug]
    
    # Senão, gera baseado no tipo e nome
    type_mapping = {
        'vinhos': 'wine bottle',
        'cervejas': 'beer bottle',
        'destilados': 'spirits bottle',
        'sem_alcool': 'beverage bottle'
    }
    
    base_query = type_mapping.get(product.alcohol_type, 'beverage bottle')
    return base_query

def download_real_images():
    """Download de imagens reais para todos os produtos"""
    products = Product.objects.all()
    
    print(f"🖼️ Baixando imagens reais para {products.count()} produtos...")
    
    # URLs de imagens reais específicas (Unsplash sources)
    real_images = {
        'vinho-cabernet-sauvignon-premium': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&h=400&fit=crop&crop=center',
        'vinho-malbec-argentino': 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=400&h=400&fit=crop&crop=center',
        'vinho-chardonnay-reserve': 'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=400&h=400&fit=crop&crop=center',
        'vinho-sauvignon-blanc': 'https://images.unsplash.com/photo-1556881286-fc7fa5d14c7c?w=400&h=400&fit=crop&crop=center',
        'cerveja-ipa-artesanal': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400&h=400&fit=crop&crop=center',
        'cerveja-stout-cremosa': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=400&fit=crop&crop=center',
        'cerveja-premium-lager': 'https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=400&h=400&fit=crop&crop=center',
        'cerveja-wheat-premium': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400&h=400&fit=crop&crop=center',
        'whisky-escoces-12-anos': 'https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=400&h=400&fit=crop&crop=center',
        'vodka-premium-russa': 'https://images.unsplash.com/photo-1560963689-b3785ac2a527?w=400&h=400&fit=crop&crop=center',
        'gin-london-dry': 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=400&h=400&fit=crop&crop=center',
        'suco-de-uva-integral-premium': 'https://images.unsplash.com/photo-1613478223719-2ab802602423?w=400&h=400&fit=crop&crop=center',
        'agua-tonica-premium': 'https://images.unsplash.com/photo-1571689743307-2d62d3d82a80?w=400&h=400&fit=crop&crop=center',
        'energetico-natural': 'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=400&h=400&fit=crop&crop=center'
    }
    
    for product in products:
        try:
            print(f"📥 Baixando imagem para: {product.name}")
            
            # Tentar pegar imagem real específica
            image_url = real_images.get(product.slug)
            
            if image_url:
                response = requests.get(image_url, timeout=15)
                
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
                    filename = f"{product.slug}_real_{uuid.uuid4().hex[:8]}.jpg"
                    product.image.save(
                        filename,
                        ContentFile(img_io.getvalue()),
                        save=True
                    )
                    
                    print(f"✅ Imagem real baixada para {product.name}")
                else:
                    print(f"❌ Falha ao baixar imagem para {product.name} (Status: {response.status_code})")
            else:
                print(f"⚠️ URL não encontrada para {product.name}, mantendo imagem atual")
            
            # Pausa entre downloads para não sobrecarregar o servidor
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Erro ao processar {product.name}: {e}")

def main():
    print("🌐 Baixando imagens reais dos produtos...")
    download_real_images()
    print("\n✅ Download de imagens concluído!")
    
    # Estatísticas
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")

if __name__ == '__main__':
    main()
