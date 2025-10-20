import os
import django
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import uuid
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Product
from django.core.files.base import ContentFile

def create_realistic_product_image(product, width=400, height=400):
    """Criar uma imagem mais realista baseada no produto específico"""
    
    # Definir estilos específicos por produto
    product_styles = {
        # CERVEJAS ESPECÍFICAS
        'heineken': {
            'bg_color': '#066A47',  # Verde Heineken
            'bottle_color': '#0D8B2F',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'bottle'
        },
        'corona': {
            'bg_color': '#F4E4A6',  # Amarelo Corona
            'bottle_color': '#FFF8DC',
            'label_color': '#1E3A8A',
            'text_color': '#1E3A8A',
            'container': 'bottle'
        },
        'stella-artois': {
            'bg_color': '#C41E3A',  # Vermelho Stella
            'bottle_color': '#228B22',
            'label_color': '#FFD700',
            'text_color': '#FFFFFF',
            'container': 'bottle'
        },
        'budweiser': {
            'bg_color': '#DC143C',  # Vermelho Budweiser
            'bottle_color': '#8B0000',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'skol': {
            'bg_color': '#1E90FF',  # Azul Skol
            'bottle_color': '#4169E1',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'brahma': {
            'bg_color': '#B22222',  # Vermelho Brahma
            'bottle_color': '#CD5C5C',
            'label_color': '#FFD700',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        
        # DESTILADOS ESPECÍFICOS
        'johnnie-walker': {
            'bg_color': '#000000',  # Preto JW
            'bottle_color': '#2F4F4F',
            'label_color': '#FFD700',
            'text_color': '#FFD700',
            'container': 'bottle'
        },
        'jack-daniels': {
            'bg_color': '#1C1C1C',  # Preto JD
            'bottle_color': '#2F2F2F',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'bottle'
        },
        'smirnoff': {
            'bg_color': '#DC143C',  # Vermelho Smirnoff
            'bottle_color': '#FFFFFF',
            'label_color': '#DC143C',
            'text_color': '#DC143C',
            'container': 'bottle'
        },
        'absolut': {
            'bg_color': '#4169E1',  # Azul Absolut
            'bottle_color': '#FFFFFF',
            'label_color': '#4169E1',
            'text_color': '#4169E1',
            'container': 'bottle'
        },
        
        # REFRIGERANTES ESPECÍFICOS
        'coca-cola': {
            'bg_color': '#DC143C',  # Vermelho Coca
            'bottle_color': '#8B0000',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'pepsi': {
            'bg_color': '#1E3A8A',  # Azul Pepsi
            'bottle_color': '#1E40AF',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'guarana-antarctica': {
            'bg_color': '#228B22',  # Verde Guaraná
            'bottle_color': '#32CD32',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'fanta': {
            'bg_color': '#FF8C00',  # Laranja Fanta
            'bottle_color': '#FF7F50',
            'label_color': '#FFFFFF',
            'text_color': '#FFFFFF',
            'container': 'can'
        },
        'sprite': {
            'bg_color': '#32CD32',  # Verde Sprite
            'bottle_color': '#90EE90',
            'label_color': '#1E40AF',
            'text_color': '#1E40AF',
            'container': 'can'
        }
    }
    
    # Determinar estilo baseado no nome do produto
    product_name_lower = product.name.lower().replace(' ', '-')
    style_key = None
    
    for key in product_styles.keys():
        if key in product_name_lower:
            style_key = key
            break
    
    # Se não encontrou estilo específico, usar genérico baseado no tipo
    if not style_key:
        if product.alcohol_type == 'cervejas':
            style_key = 'generic_beer'
            product_styles['generic_beer'] = {
                'bg_color': '#FFD700',
                'bottle_color': '#8B4513',
                'label_color': '#FFFFFF',
                'text_color': '#8B4513',
                'container': 'bottle'
            }
        elif product.alcohol_type == 'vinhos':
            style_key = 'generic_wine'
            product_styles['generic_wine'] = {
                'bg_color': '#722F37',
                'bottle_color': '#2F4F2F',
                'label_color': '#FFD700',
                'text_color': '#FFFFFF',
                'container': 'bottle'
            }
        elif product.alcohol_type == 'destilados':
            style_key = 'generic_spirits'
            product_styles['generic_spirits'] = {
                'bg_color': '#8B4513',
                'bottle_color': '#2F4F4F',
                'label_color': '#FFD700',
                'text_color': '#FFD700',
                'container': 'bottle'
            }
        else:  # sem_alcool
            style_key = 'generic_soft'
            product_styles['generic_soft'] = {
                'bg_color': '#1E90FF',
                'bottle_color': '#87CEEB',
                'label_color': '#FFFFFF',
                'text_color': '#1E3A8A',
                'container': 'can'
            }
    
    style = product_styles[style_key]
    
    # Criar imagem base
    img = Image.new('RGB', (width, height), color=style['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Tentar usar fontes melhores
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_brand = ImageFont.truetype("arialbd.ttf", 32)
        font_price = ImageFont.truetype("arialbd.ttf", 36)
        font_volume = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_brand = ImageFont.load_default()
        font_price = ImageFont.load_default()
        font_volume = ImageFont.load_default()
    
    # Desenhar container (garrafa ou lata)
    if style['container'] == 'bottle':
        # Desenhar garrafa
        bottle_width = 80
        bottle_height = 200
        bottle_x = (width - bottle_width) // 2
        bottle_y = 50
        
        # Corpo da garrafa
        draw.rectangle([bottle_x, bottle_y, bottle_x + bottle_width, bottle_y + bottle_height], 
                      fill=style['bottle_color'], outline='#000000', width=2)
        
        # Gargalo
        neck_width = 30
        neck_height = 40
        neck_x = bottle_x + (bottle_width - neck_width) // 2
        draw.rectangle([neck_x, bottle_y - neck_height, neck_x + neck_width, bottle_y], 
                      fill=style['bottle_color'], outline='#000000', width=2)
        
        # Tampa
        cap_width = 35
        cap_height = 15
        cap_x = bottle_x + (bottle_width - cap_width) // 2
        draw.rectangle([cap_x, bottle_y - neck_height - cap_height, cap_x + cap_width, bottle_y - neck_height], 
                      fill='#2F2F2F', outline='#000000', width=1)
        
        # Label da garrafa
        label_height = 60
        label_y = bottle_y + 40
        draw.rectangle([bottle_x + 5, label_y, bottle_x + bottle_width - 5, label_y + label_height], 
                      fill=style['label_color'], outline='#000000', width=1)
        
        text_y_start = 280
        
    else:  # can
        # Desenhar lata
        can_width = 70
        can_height = 120
        can_x = (width - can_width) // 2
        can_y = 80
        
        # Corpo da lata
        draw.rectangle([can_x, can_y, can_x + can_width, can_y + can_height], 
                      fill=style['bottle_color'], outline='#000000', width=2)
        
        # Tampa da lata
        draw.ellipse([can_x, can_y - 5, can_x + can_width, can_y + 10], 
                    fill='#C0C0C0', outline='#000000', width=1)
        
        # Label principal
        label_height = 50
        label_y = can_y + 20
        draw.rectangle([can_x + 5, label_y, can_x + can_width - 5, label_y + label_height], 
                      fill=style['label_color'], outline='#000000', width=1)
        
        text_y_start = 220
    
    # Extrair marca do nome do produto
    brand_name = product.name.split()[0]
    if len(brand_name) > 12:
        brand_name = brand_name[:12]
    
    # Desenhar nome da marca no container
    if style['container'] == 'bottle':
        # Na label da garrafa
        bbox = draw.textbbox((0, 0), brand_name, font=font_brand)
        text_width = bbox[2] - bbox[0]
        text_x = bottle_x + (bottle_width - text_width) // 2
        draw.text((text_x, label_y + 15), brand_name, fill=style['text_color'], font=font_brand)
    else:
        # Na label da lata
        bbox = draw.textbbox((0, 0), brand_name, font=font_brand)
        text_width = bbox[2] - bbox[0]
        text_x = can_x + (can_width - text_width) // 2
        draw.text((text_x, label_y + 10), brand_name, fill=style['text_color'], font=font_brand)
    
    # Desenhar nome completo do produto embaixo
    product_words = product.name.split()
    if len(product_words) > 2:
        line1 = ' '.join(product_words[:2])
        line2 = ' '.join(product_words[2:4]) if len(product_words) > 3 else product_words[2]
    else:
        line1 = product.name
        line2 = ''
    
    # Linha 1
    bbox = draw.textbbox((0, 0), line1, font=font_title)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, text_y_start), line1, fill='#FFFFFF', font=font_title)
    
    # Linha 2
    if line2:
        bbox = draw.textbbox((0, 0), line2, font=font_title)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, text_y_start + 30), line2, fill='#FFFFFF', font=font_title)
        text_y_start += 30
    
    # Desenhar preço
    price_text = f"R$ {product.price}"
    bbox = draw.textbbox((0, 0), price_text, font=font_price)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, text_y_start + 40), price_text, fill='#FFD700', font=font_price)
    
    # Desenhar volume
    if product.volume:
        bbox = draw.textbbox((0, 0), product.volume, font=font_volume)
        text_width = bbox[2] - bbox[0]
        text_x = (width - text_width) // 2
        draw.text((text_x, text_y_start + 85), product.volume, fill='#FFFFFF', font=font_volume)
    
    return img

def update_product_images_realistic():
    """Atualizar imagens com versões mais realistas"""
    
    # Focar nos produtos de marcas famosas primeiro
    from django.db.models import Q
    
    famous_products = Product.objects.filter(
        Q(name__icontains='Heineken') |
        Q(name__icontains='Corona') |
        Q(name__icontains='Stella') |
        Q(name__icontains='Budweiser') |
        Q(name__icontains='Skol') |
        Q(name__icontains='Brahma') |
        Q(name__icontains='Johnnie') |
        Q(name__icontains='Jack') |
        Q(name__icontains='Smirnoff') |
        Q(name__icontains='Absolut') |
        Q(name__icontains='Coca-Cola') |
        Q(name__icontains='Pepsi') |
        Q(name__icontains='Guaraná') |
        Q(name__icontains='Fanta') |
        Q(name__icontains='Sprite')
    )
    
    print(f"🎨 Criando imagens realistas para {famous_products.count()} produtos famosos...")
    
    success_count = 0
    for product in famous_products:
        try:
            print(f"🖼️ Criando imagem realista para: {product.name}")
            
            # Criar imagem realista
            img = create_realistic_product_image(product, 400, 400)
            
            # Converter para bytes
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=95)
            img_io.seek(0)
            
            # Remover imagem anterior
            if product.image:
                product.image.delete(save=False)
            
            # Salvar nova imagem
            filename = f"{product.slug}_realistic_{uuid.uuid4().hex[:8]}.jpg"
            product.image.save(
                filename,
                ContentFile(img_io.getvalue()),
                save=True
            )
            
            print(f"✅ Imagem realista criada para {product.name}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Erro ao criar imagem para {product.name}: {e}")
    
    return success_count

def main():
    print("🎨 Criando imagens mais realistas dos produtos...")
    success_count = update_product_images_realistic()
    
    print(f"\n✅ Processo concluído!")
    print(f"   Imagens realistas criadas: {success_count}")
    
    # Estatísticas
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")

if __name__ == '__main__':
    main()
