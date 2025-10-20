import os
import django
from PIL import Image
from io import BytesIO
import uuid

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bebidasstore.settings')
django.setup()

from store.models import Product
from django.core.files.base import ContentFile

def create_placeholder_image(product_name, category, width=400, height=400):
    """Cria uma imagem placeholder para o produto"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Cores baseadas na categoria
    colors = {
        'vinhos': ('#7C2D92', '#FFFFFF'),
        'cervejas': ('#F59E0B', '#FFFFFF'),
        'destilados': ('#DC2626', '#FFFFFF'),
        'sem_alcool': ('#059669', '#FFFFFF'),
    }
    
    # Pegar cor baseada no tipo do produto
    bg_color = colors.get(category, ('#64748B', '#FFFFFF'))
    
    # Criar imagem
    img = Image.new('RGB', (width, height), color=bg_color[0])
    draw = ImageDraw.Draw(img)
    
    try:
        # Tentar usar uma fonte padrão
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        # Usar fonte padrão se não encontrar
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Desenhar texto
    # Nome do produto (quebrado em linhas)
    words = product_name.split()
    lines = []
    current_line = []
    
    for word in words:
        if len(' '.join(current_line + [word])) <= 20:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calcular posição central
    total_height = len(lines) * 30 + 40
    start_y = (height - total_height) // 2
    
    # Desenhar cada linha
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_large)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = start_y + i * 30
        draw.text((x, y), line, fill=bg_color[1], font=font_large)
    
    # Adicionar categoria
    category_text = category.upper().replace('_', ' ')
    bbox = draw.textbbox((0, 0), category_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = start_y + len(lines) * 30 + 20
    draw.text((x, y), category_text, fill=bg_color[1], font=font_small)
    
    return img

def add_images_to_products():
    """Adiciona imagens placeholder aos produtos"""
    products_without_images = Product.objects.filter(image='')
    
    print(f"Encontrados {products_without_images.count()} produtos sem imagem")
    
    for product in products_without_images:
        try:
            print(f"Criando imagem para: {product.name}")
            
            # Criar imagem placeholder
            img = create_placeholder_image(
                product.name,
                product.alcohol_type,
                400,
                400
            )
            
            # Converter para bytes
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=85)
            img_io.seek(0)
            
            # Gerar nome do arquivo
            filename = f"{product.slug}_{uuid.uuid4().hex[:8]}.jpg"
            
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
    print("🖼️ Adicionando imagens aos produtos...")
    add_images_to_products()
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
