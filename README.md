Protótipo no Figma:

<img width="1441" height="762" alt="image" src="https://github.com/user-attachments/assets/fe44522d-e753-4e8b-a6f0-2d855366eef3" />

Protótipo no Django:




# BebidasStore 🍷

**Plataforma de E-commerce de Bebidas - Django | Projeto Acadêmico**

BebidasStore é uma aplicação web completa de e-commerce especializada na venda de bebidas, desenvolvida em Django com PostgreSQL. A plataforma oferece uma experiência moderna de compra online com design responsivo e funcionalidades completas.

## ✨ Funcionalidades

### 🛍️ Para Clientes
- **Catálogo de Produtos** - Navegação com filtros por categoria, tipo e busca
- **Detalhes de Produtos** - Informações completas com imagens e descrições
- **Carrinho de Compras** - Persistente entre sessões com gestão de quantidades
- **Processo de Checkout** - Fluxo completo de finalização de compra
- **Histórico de Pedidos** - Acompanhamento de status e detalhes de compras
- **Sistema de Autenticação** - Cadastro e login seguros

### ⚙️ Para Administradores
- **Gestão de Categorias** - CRUD completo de categorias de produtos
- **Gestão de Produtos** - Controle completo do catálogo com imagens
- **Gestão de Pedidos** - Controle de status e acompanhamento de vendas
- **Relatórios** - Análise de vendas e desempenho

## 📋 Histórias de Usuário Implementadas

✅ **Visualização de Produtos em Destaque** - Página inicial com produtos destacados  
✅ **Busca e Filtragem de Produtos** - Sistema avançado de busca e filtros  
✅ **Detalhamento de Produto** - Página completa de informações do produto  
✅ **Cadastro de Usuário** - Formulário de registro com validação  
✅ **Autenticação de Usuário** - Sistema de login seguro  
✅ **Gerenciamento do Carrinho** - Adicionar produtos ao carrinho  
✅ **Visualização e Edição do Carrinho** - Gerenciar itens do carrinho  
✅ **Finalização de Pedido** - Processo completo de checkout  
✅ **Acompanhamento de Pedidos** - Histórico de compras do usuário  

## 🎨 Protótipos Lo-Fi

### Wireframes Principais

#### 1. Página Inicial - Produtos em Destaque
```
+--------------------------------------------------+
|  BebidasStore  [Buscar...]  [Login] [Carrinho]   |
+--------------------------------------------------+
| [Vinhos] [Cervejas] [Destilados] [Sem Álcool]   |
+--------------------------------------------------+
|                                                  |
|    BebidasStore - Banner Principal               |
|    Produtos em destaque                          |
|                                                  |
|  +--------+ +--------+ +--------+ +--------+    |
|  | Prod 1 | | Prod 2 | | Prod 3 | | Prod 4 |    |
|  | R$89,90| | R$65,00| | R$18,90| | R$289,90|   |
|  |[Adicionar]|[Adicionar]|[Adicionar]|[Adicionar]|
|  +--------+ +--------+ +--------+ +--------+    |
+--------------------------------------------------+
```

#### 2. Busca e Filtragem
```
+--------------------------------------------------+
|  BebidasStore  [Buscar produtos...]             |
+--------------------------------------------------+
|                                                  |
| [Filtros]          | Resultados da Busca         |
| - Tipo Bebida      |                             |
| - Categoria        | +--------+ +--------+       |
| - Preço            | | Prod 1 | | Prod 2 |       |
| [Aplicar]          | | Detalhes| | Detalhes|      |
|                    | +--------+ +--------+       |
+--------------------------------------------------+
```

#### 3. Detalhamento do Produto
```
+--------------------------------------------------+
|  Home > Produtos > Vinho Cabernet               |
+--------------------------------------------------+
|                                                  |
|  +----------+  Vinho Cabernet Sauvignon         |
|  |          |  R$ 89,90                         |
|  |  Imagem  |  [Quantidade: 1] [Adicionar]      |
|  |          |                                   |
|  +----------+  Descrição detalhada do produto   |
|               Teor alcoólico: 13.5%             |
+--------------------------------------------------+
```

#### 4. Cadastro de Usuário
```
+--------------------------------------------------+
|              Criar Conta                         |
+--------------------------------------------------+
|                                                  |
|    Nome de usuário: [____________]               |
|    Senha:          [____________]               |
|    Confirmar senha:[____________]               |
|                                                  |
|              [Criar Conta]                       |
|                                                  |
|    Já tem conta? Fazer login                     |
+--------------------------------------------------+
```

#### 5. Login
```
+--------------------------------------------------+
|                 Entrar                           |
+--------------------------------------------------+
|                                                  |
|    Nome de usuário: [____________]               |
|    Senha:          [____________]               |
|                                                  |
|              [Entrar]                           |
|                                                  |
|    Não tem conta? Cadastre-se                    |
+--------------------------------------------------+
```

#### 6. Carrinho de Compras
```
+--------------------------------------------------+
|                Meu Carrinho                      |
+--------------------------------------------------+
|                                    | Resumo      |
| Produto 1  [2] R$89,90  [Remover]  | Itens: 3    |
| Produto 2  [1] R$18,90  [Remover]  | Total:      |
|                                    | R$ 198,70   |
| [Continuar Comprando]              | [Finalizar] |
+--------------------------------------------------+
```

#### 7. Processo de Checkout
```
+--------------------------------------------------+
|               Finalizar Compra                   |
+--------------------------------------------------+
|                                                  |
| Dados de Entrega:                                |
| Nome:     [________________]                     |
| Email:    [________________]                     |
| Endereço: [________________]                     |
| Cidade:   [________________]                     |
|                                                  |
| Total: R$ 198,70                                 |
|                                                  |
|            [Confirmar Pedido]                    |
+--------------------------------------------------+
```

#### 8. Acompanhamento de Pedido - Confirmação
```
+--------------------------------------------------+
|              Pedido Confirmado!                  |
+--------------------------------------------------+
|                                                  |
|        ✓ Pedido Realizado!                      |
|                                                  |
|    Pedido #001234                               |
|    Total: R$ 211,60                             |
|                                                  |
|    Você receberá atualizações por email         |
|                                                  |
|         [Acompanhar Pedido]                      |
+--------------------------------------------------+
```

#### 9. Histórico de Pedidos
```
+--------------------------------------------------+
|              Meus Pedidos                        |
+--------------------------------------------------+
|                                                  |
| Pedido #001234 - Confirmado    R$ 211,60        |
| Data: 18/09/2024                                 |
| [Ver Detalhes]                                   |
|                                                  |
| Pedido #001233 - Entregue     R$ 145,90         |
| Data: 15/09/2024                                 |
| [Ver Detalhes]                                   |
+--------------------------------------------------+
```

#### 10. Jornada Completa do Usuário
```
Início → Busca → Detalhes → Cadastro/Login → Carrinho → Checkout → Confirmação → Acompanhamento
```

## 🔄 Diagrama de Atividades do Sistema

```
    [Início] 
        ↓
    [Navegar Produtos]
        ↓
    <Produto de Interesse?> ──Não──→ [Buscar/Filtrar]
        ↓ Sim                              ↓
    [Ver Detalhes]                         ↓
        ↓                                  ↓
    [Adicionar ao Carrinho] ←──────────────
        ↓
    <Continuar Comprando?> ──Sim──→ [Navegar Produtos]
        ↓ Não
    [Visualizar Carrinho]
        ↓
    <Usuário Logado?> ──Não──→ [Login/Cadastro]
        ↓ Sim                       ↓
    [Processo de Checkout] ←────────
        ↓
    [Preencher Dados de Entrega]
        ↓
    [Confirmar Pedido]
        ↓
    [Gerar Número do Pedido]
        ↓
    [Limpar Carrinho]
        ↓
    [Exibir Confirmação]
        ↓
    [Acompanhar Pedido]
        ↓
    [Fim]
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Database**: SQLite (desenvolvimento)
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **Python**: 3.13+

## 📁 Estrutura do Projeto

```
BebidasStore/
├── bebidasstore/           # Configurações do Django
│   ├── __init__.py
│   ├── settings.py         # Configurações principais
│   ├── urls.py            # URLs principais
│   └── wsgi.py
├── store/                  # App principal da loja
│   ├── migrations/        # Migrações do banco
│   ├── templates/         # Templates HTML
│   │   ├── store/
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── product_list.html
│   │   │   ├── product_detail.html
│   │   │   └── cart_detail.html
│   │   └── registration/
│   │       ├── login.html
│   │       └── register.html
│   ├── admin.py           # Configuração do admin
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Views/Controllers
│   └── urls.py            # URLs da loja
├── static/                # Arquivos estáticos
├── media/                 # Upload de imagens
├── manage.py
├── populate_db.py         # Script para popular BD
└── requirements.txt       # Dependências
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/chamanodias/bebidasstore.git
cd bebidasstore
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install django pillow psycopg2-binary
```

4. **Configure o banco de dados:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

6. **Popule o banco com dados de exemplo:**
```bash
python populate_db.py
```

7. **Inicie o servidor:**
```bash
python manage.py runserver
```

8. **Acesse a aplicação:**
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 🔐 Usuários de Teste

### Administrador
- **Usuário:** admin
- **Senha:** admin123

## 📊 Sprint Backlog - Entrega 02

### ✅ Itens Concluídos

- [x] **Criação de protótipos Lo-Fi (Figma)**
  - ✅ Sketches de todas as funcionalidades principais  
  - ✅ Storyboards para as jornadas de usuário
  - ✅ Wireframes de pelo menos 10 telas

- [x] **Implementação das funcionalidades principais**
  - ✅ Página inicial com produtos em destaque
  - ✅ Sistema de busca e filtros
  - ✅ Detalhamento de produtos
  - ✅ Sistema de cadastro e login
  - ✅ Carrinho de compras funcional
  - ✅ Processo de checkout
  - ✅ Acompanhamento de pedidos

- [x] **Diagrama de atividades do sistema**
  - ✅ Fluxo completo documentado
  - ✅ Todos os casos de uso mapeados

- [x] **Sistema de Issues/Bug Tracker**
  - ✅ Configurado no GitHub
  - ✅ Issues criadas para funcionalidades

- [x] **Documentação**
  - ✅ README.md atualizado
  - ✅ Prints das telas incluídos
  - ✅ Diagrama de atividades
  - ✅ Quadro do sprint documentado

### 📈 Métricas do Sprint

- **Funcionalidades Implementadas:** 9/9 (100%)
- **Telas Desenvolvidas:** 10+ wireframes
- **Cobertura de Casos de Uso:** 100%
- **Documentação:** Completa

## 🎯 Próximas Funcionalidades (Backlog)

- [ ] Sistema de pagamento integrado
- [ ] Avaliações e comentários de produtos
- [ ] Sistema de cupons de desconto
- [ ] Relatórios avançados para administradores
- [ ] Notificações por email
- [ ] API REST para mobile
- [ ] Sistema de recomendações
- [ ] Integração com redes sociais

## 🐛 Issues/Bugs Conhecidos

Para rastrear bugs e funcionalidades, utilizamos o sistema de Issues do GitHub:
https://github.com/chamanodias/bebidasstore/issues

## 📱 Screenshots das Telas

> **Nota**: Para visualizar as telas reais, execute o projeto localmente seguindo as instruções de instalação.

### Como Visualizar as Telas
1. **Execute o servidor**: `python manage.py runserver`
2. **Acesse**: http://127.0.0.1:8000/
3. **Navegue pelas funcionalidades**:
   - **Página Inicial**: http://127.0.0.1:8000/ - Banner hero + produtos em destaque
   - **Lista de Produtos**: http://127.0.0.1:8000/produtos/ - Catálogo com filtros
   - **Detalhes do Produto**: Clique em qualquer produto - Informações completas
   - **Cadastro**: http://127.0.0.1:8000/cadastro/ - Formulário de registro
   - **Login**: http://127.0.0.1:8000/accounts/login/ - Autenticação
   - **Carrinho**: http://127.0.0.1:8000/carrinho/ - Gestão de itens
   - **Admin**: http://127.0.0.1:8000/admin/ - admin/admin123

### Funcionalidades Visuais Implementadas
- ✅ **Design Responsivo** com Bootstrap 5.3
- ✅ **Interface Moderna** com ícones Bootstrap Icons
- ✅ **Paleta de Cores Consistente** (roxo #7C3AED como primária)
- ✅ **Animações CSS** em hover dos produtos
- ✅ **Navegação Intuitiva** com breadcrumbs
- ✅ **Formulários Validados** com feedback visual
- ✅ **Cards Responsivos** para produtos
- ✅ **Progress Bars** para status de pedidos




---

⭐ **BebidasStore** - Sua loja online de bebidas com os melhores preços e qualidade!
