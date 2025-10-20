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

def get_real_product_images():
    """Baixar imagens reais específicas para cada produto"""
    
    # Mapeamento de produtos para imagens reais específicas
    real_product_images = {
        # VINHOS ESPECÍFICOS
        'vinho-cabernet-sauvignon-premium': 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&h=400&fit=crop',
        'vinho-malbec-argentino': 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=400&h=400&fit=crop',
        'vinho-chardonnay-reserve': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=400&fit=crop',
        'vinho-sauvignon-blanc': 'https://images.unsplash.com/photo-1574870111867-089730e5a72e?w=400&h=400&fit=crop',
        'barolo-italiano-docg': 'https://images.unsplash.com/photo-1586370434639-0fe43b2d32d6?w=400&h=400&fit=crop',
        'bordeaux-frances-chateau': 'https://images.unsplash.com/photo-1596142332133-327f9d48db8a?w=400&h=400&fit=crop',
        'rioja-reserva-espanhol': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop',
        'sauvignon-blanc-chileno': 'https://images.unsplash.com/photo-1595813967359-da0ea5373cd7?w=400&h=400&fit=crop',
        'albarino-espanhol': 'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=400&h=400&fit=crop',
        'pinot-grigio-italiano': 'https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=400&h=400&fit=crop',
        
        # ESPUMANTES
        'espumante-brut-nacional': 'https://images.unsplash.com/photo-1513618827672-0d7c5ad591b1?w=400&h=400&fit=crop',
        'prosecco-moscatel-nacional': 'https://images.unsplash.com/photo-1560963689-b3785ac2a527?w=400&h=400&fit=crop',
        
        # CERVEJAS ESPECÍFICAS
        'cerveja-ipa-artesanal': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400&h=400&fit=crop',
        'ipa-american-hoppy': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf6d2c?w=400&h=400&fit=crop',
        'ipa-session-tropical': 'https://images.unsplash.com/photo-1612528443702-f6741f70a049?w=400&h=400&fit=crop',
        'double-ipa-imperial': 'https://images.unsplash.com/photo-1596449584503-98bb50a52e6e?w=400&h=400&fit=crop',
        'cerveja-stout-cremosa': 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=400&fit=crop',
        'stout-imperial-coffee': 'https://images.unsplash.com/photo-1634128252737-5b87b1b7094c?w=400&h=400&fit=crop',
        'porter-chocolate-artesanal': 'https://images.unsplash.com/photo-1571613316887-6f8d5cbf6d2c?w=400&h=400&fit=crop',
        'cerveja-premium-lager': 'https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=400&h=400&fit=crop',
        'pilsner-tcheca-premium': 'https://images.unsplash.com/photo-1572888224297-13c0e8f0d7b6?w=400&h=400&fit=crop',
        'pilsner-alema-puro-malte': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=400&fit=crop',
        'cerveja-wheat-premium': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400&h=400&fit=crop',
        
        # DESTILADOS ESPECÍFICOS
        'whisky-escoces-12-anos': 'https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=400&h=400&fit=crop',
        'single-malt-escoces-18-anos': 'https://images.unsplash.com/photo-1569275808161-2d29a4d6c2d1?w=400&h=400&fit=crop',
        'bourbon-americano-premium': 'https://images.unsplash.com/photo-1634658932003-1b09db671764?w=400&h=400&fit=crop',
        'irish-whiskey-triple-destilado': 'https://images.unsplash.com/photo-1552743838-ffe1f00928f5?w=400&h=400&fit=crop',
        'vodka-premium-russa': 'https://images.unsplash.com/photo-1615332579937-523d95c451c4?w=400&h=400&fit=crop',
        'gin-london-dry': 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=400&h=400&fit=crop',
        'gin-brasileiro-amazonico': 'https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=400&fit=crop',
        'gin-london-dry-premium': 'https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=400&fit=crop',
        'cachaca-artesanal-envelhecida': 'https://images.unsplash.com/photo-1593969939792-ca54f6fb0018?w=400&h=400&fit=crop',
        'cachaca-premium-ouro': 'https://images.unsplash.com/photo-1593969939792-ca54f6fb0018?w=400&h=400&fit=crop',
        
        # BEBIDAS SEM ÁLCOOL ESPECÍFICAS
        'suco-de-uva-integral-premium': 'https://images.unsplash.com/photo-1613478223719-2ab802602423?w=400&h=400&fit=crop',
        'suco-de-acai-integral': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
        'suco-de-cupuacu-natural': 'https://images.unsplash.com/photo-1570831739435-6601aa3fa4fb?w=400&h=400&fit=crop',
        'suco-detox-verde-organico': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop',
        'agua-tonica-premium': 'https://images.unsplash.com/photo-1571689743307-2d62d3d82a80?w=400&h=400&fit=crop',
        'energetico-natural': 'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=400&h=400&fit=crop',
        'energy-drink-acai-guarana': 'https://images.unsplash.com/photo-1625772299848-391b8a87d7b9?w=400&h=400&fit=crop',
        'isotonico-coco-natural': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
        'guarana-artesanal-amazonico': 'https://images.unsplash.com/photo-1581006852262-e4307cf6283a?w=400&h=400&fit=crop',
        'cola-artesanal-bourbon': 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=400&h=400&fit=crop',
        'kombucha-gengibre-limao': 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=400&h=400&fit=crop',
        'cha-verde-gelado-organico': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400&h=400&fit=crop',
    }
    
    # Adicionar produtos famosos conhecidos
    famous_products = {
        # Se você quiser adicionar produtos famosos específicos
        'heineken': 'https://images.unsplash.com/photo-1572888224297-13c0e8f0d7b6?w=400&h=400&fit=crop',
        'corona': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400&h=400&fit=crop',
        'stella-artois': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400&h=400&fit=crop',
    }
    
    products = Product.objects.all()
    
    print(f"🖼️ Baixando imagens reais para {products.count()} produtos...")
    
    success_count = 0
    
    for product in products:
        try:
            print(f"📥 Buscando imagem real para: {product.name}")
            
            # Tentar encontrar URL específica para o produto
            image_url = real_product_images.get(product.slug)
            
            if not image_url:
                # Se não encontrar, tentar buscar por palavras-chave no nome
                product_name_lower = product.name.lower()
                for key, url in famous_products.items():
                    if key in product_name_lower:
                        image_url = url
                        break
                
                # Se ainda não encontrar, usar busca genérica mais específica
                if not image_url:
                    if 'whisky' in product_name_lower or 'whiskey' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1527281400683-1aae777175f8?w=400&h=400&fit=crop'
                    elif 'vodka' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1615332579937-523d95c451c4?w=400&h=400&fit=crop'
                    elif 'gin' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?w=400&h=400&fit=crop'
                    elif 'ipa' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400&h=400&fit=crop'
                    elif 'stout' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400&h=400&fit=crop'
                    elif 'vinho' in product_name_lower or 'wine' in product_name_lower:
                        if 'tinto' in product_name_lower or 'red' in product_name_lower:
                            image_url = 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=400&h=400&fit=crop'
                        else:
                            image_url = 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400&h=400&fit=crop'
                    elif 'cerveja' in product_name_lower or 'beer' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=400&h=400&fit=crop'
                    elif 'suco' in product_name_lower or 'juice' in product_name_lower:
                        image_url = 'https://images.unsplash.com/photo-1613478223719-2ab802602423?w=400&h=400&fit=crop'
                    else:
                        print(f"⚠️ Sem imagem específica para {product.name}, mantendo atual")
                        continue
            
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
                    success_count += 1
                else:
                    print(f"❌ Falha ao baixar imagem para {product.name} (Status: {response.status_code})")
            
            # Pausa entre downloads para não sobrecarregar o servidor
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Erro ao processar {product.name}: {e}")
    
    return success_count

def main():
    print("🌐 Baixando imagens reais específicas dos produtos...")
    success_count = get_real_product_images()
    print(f"\n✅ Download concluído! {success_count} imagens baixadas com sucesso!")
    
    # Estatísticas finais
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas Finais:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")
    print(f"   Imagens reais específicas: {success_count}")

if __name__ == '__main__':
    main()
