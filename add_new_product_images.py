import os
import django
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import uuid

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Product
from django.core.files.base import ContentFile

def create_specific_placeholder(product, width=400, height=400):
    """Cria placeholder específico baseado no tipo de produto"""
    
    # Cores e ícones específicos por categoria
    product_styles = {
        # Vinhos
        'vinho': {
            'bg_color': '#722F37',
            'text_color': '#F8F8F2',
            'icon': '🍷',
        },
        'espumante': {
            'bg_color': '#9D4EDD',
            'text_color': '#FFFFFF',
            'icon': '🥂',
        },
        # Cervejas
        'ipa': {
            'bg_color': '#D4A574',
            'text_color': '#2F1B14',
            'icon': '🍺',
        },
        'pilsner': {
            'bg_color': '#FFD60A',
            'text_color': '#2F1B14',
            'icon': '🍺',
        },
        'stout': {
            'bg_color': '#2F1B14',
            'text_color': '#F8F8F2',
            'icon': '🍺',
        },
        'porter': {
            'bg_color': '#6F4E37',
            'text_color': '#F8F8F2',
            'icon': '🍺',
        },
        # Destilados
        'whisky': {
            'bg_color': '#8B4513',
            'text_color': '#FFD700',
            'icon': '🥃',
        },
        'bourbon': {
            'bg_color': '#CD853F',
            'text_color': '#2F1B14',
            'icon': '🥃',
        },
        'cachaça': {
            'bg_color': '#228B22',
            'text_color': '#FFFFFF',
            'icon': '🥃',
        },
        'gin': {
            'bg_color': '#40E0D0',
            'text_color': '#2F1B14',
            'icon': '🍸',
        },
        # Sem álcool
        'suco': {
            'bg_color': '#FF6B6B',
            'text_color': '#FFFFFF',
            'icon': '🧃',
        },
        'energético': {
            'bg_color': '#00BCD4',
            'text_color': '#FFFFFF',
            'icon': '⚡',
        },
        'kombucha': {
            'bg_color': '#8BC34A',
            'text_color': '#2F1B14',
            'icon': '🫖',
        },
        'refrigerante': {
            'bg_color': '#FF9800',
            'text_color': '#FFFFFF',
            'icon': '🥤',
        }
    }
    
    # Determinar estilo baseado no nome do produto
    product_name_lower = product.name.lower()
    style_key = 'vinho'  # default
    
    if 'espumante' in product_name_lower or 'prosecco' in product_name_lower:
        style_key = 'espumante'
    elif 'ipa' in product_name_lower:
        style_key = 'ipa'
    elif 'pilsner' in product_name_lower:
        style_key = 'pilsner'
    elif 'stout' in product_name_lower:
        style_key = 'stout'
    elif 'porter' in product_name_lower:
        style_key = 'porter'
    elif 'whisky' in product_name_lower or 'whiskey' in product_name_lower:
        style_key = 'whisky'
    elif 'bourbon' in product_name_lower:
        style_key = 'bourbon'
    elif 'cachaça' in product_name_lower:
        style_key = 'cachaça'
    elif 'gin' in product_name_lower:
        style_key = 'gin'
    elif 'suco' in product_name_lower:
        style_key = 'suco'
    elif 'energy' in product_name_lower or 'energético' in product_name_lower or 'isotônico' in product_name_lower:
        style_key = 'energético'
    elif 'kombucha' in product_name_lower or 'chá' in product_name_lower:
        style_key = 'kombucha'
    elif 'cola' in product_name_lower or 'guaraná' in product_name_lower:
        style_key = 'refrigerante'
    
    style = product_styles.get(style_key, product_styles['vinho'])
    
    # Criar imagem
    img = Image.new('RGB', (width, height), color=style['bg_color'])
    draw = ImageDraw.Draw(img)
    
    try:
        # Tentar usar fontes do sistema
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
        font_icon = ImageFont.truetype("seguiemj.ttf", 60)  # Para emojis
    except:
        try:
            font_large = ImageFont.truetype("calibri.ttf", 32)
            font_medium = ImageFont.truetype("calibri.ttf", 24)
            font_small = ImageFont.truetype("calibri.ttf", 18)
            font_icon = ImageFont.load_default()
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_icon = ImageFont.load_default()
    
    # Desenhar ícone no topo
    icon_text = style['icon']
    try:
        icon_bbox = draw.textbbox((0, 0), icon_text, font=font_icon)
        icon_width = icon_bbox[2] - icon_bbox[0]
        icon_x = (width - icon_width) // 2
        draw.text((icon_x, 50), icon_text, fill=style['text_color'], font=font_icon)
    except:
        # Se não conseguir desenhar emoji, desenhar texto alternativo
        icon_text = style_key.upper()
        icon_bbox = draw.textbbox((0, 0), icon_text, font=font_medium)
        icon_width = icon_bbox[2] - icon_bbox[0]
        icon_x = (width - icon_width) // 2
        draw.text((icon_x, 50), icon_text, fill=style['text_color'], font=font_medium)
    
    # Quebrar nome do produto em linhas
    words = product.name.split()
    lines = []
    current_line = []
    max_chars_per_line = 18
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if len(test_line) <= max_chars_per_line:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Palavra muito grande, quebrar ela
                lines.append(word[:max_chars_per_line])
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Limitar a 4 linhas
    if len(lines) > 4:
        lines = lines[:3] + ['...']
    
    # Desenhar nome do produto
    start_y = 140
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * 30
        draw.text((x, y), line, fill=style['text_color'], font=font_medium)
    
    # Desenhar preço
    price_text = f"R$ {product.price}"
    bbox = draw.textbbox((0, 0), price_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = start_y + len(lines) * 30 + 20
    draw.text((x, y), price_text, fill=style['text_color'], font=font_large)
    
    # Desenhar volume se existir
    if product.volume:
        volume_text = product.volume
        bbox = draw.textbbox((0, 0), volume_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + len(lines) * 30 + 60
        draw.text((x, y), volume_text, fill=style['text_color'], font=font_small)
    
    # Desenhar categoria no rodapé
    category_text = product.category.name.upper()
    bbox = draw.textbbox((0, 0), category_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height - 40
    draw.text((x, y), category_text, fill=style['text_color'], font=font_small)
    
    return img

def add_images_to_new_products():
    """Adicionar imagens aos produtos sem imagem"""
    products_without_images = Product.objects.filter(image='')
    
    print(f"🖼️ Encontrados {products_without_images.count()} produtos sem imagem")
    
    for product in products_without_images:
        try:
            print(f"🎨 Criando imagem específica para: {product.name}")
            
            # Criar imagem específica
            img = create_specific_placeholder(product, 400, 400)
            
            # Converter para bytes
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=90)
            img_io.seek(0)
            
            # Gerar nome do arquivo
            filename = f"{product.slug}_custom_{uuid.uuid4().hex[:8]}.jpg"
            
            # Salvar no modelo
            product.image.save(
                filename,
                ContentFile(img_io.getvalue()),
                save=True
            )
            
            print(f"✅ Imagem criada para {product.name}")
            
        except Exception as e:
            print(f"❌ Erro ao criar imagem para {product.name}: {e}")

def main():
    print("🎨 Adicionando imagens específicas aos novos produtos...")
    add_images_to_new_products()
    print("\n✅ Processo concluído!")
    
    # Estatísticas
    total_products = Product.objects.count()
    products_with_images = Product.objects.exclude(image='').count()
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de produtos: {total_products}")
    print(f"   Produtos com imagem: {products_with_images}")
    print(f"   Cobertura: {(products_with_images/total_products*100):.1f}%")

if __name__ == '__main__':
    main()
