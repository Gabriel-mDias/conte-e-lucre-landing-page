# Sample Landing Page — Boilerplate & Reference Template

> **Template profissional e cinematográfico para desenvolvimento acelerado de landing pages de altíssimo padrão estético, com suporte nativo a Skill do Google Antigravity para planejamento automatizado.**

Este repositório serve como base de excelência e ponto de partida neutro e genérico para a criação de novas landing pages comerciais, institucionais e de serviços de alto padrão, combinando arquitetura moderna, animações suaves, scripts de execução em 1 clique e pipeline automatizada de mídia e deploy.

---

## ⚡ Tecnologias e Recursos

- **Vite**: Bundler ultrarrápido com separação inteligente de chunks para produção.
- **Lenis**: Rolagem inercial e suave (smooth scroll) de padrão Awwwards.
- **GSAP & ScrollTrigger**: Animações fluidas de revelação (`data-reveal`) coordenadas com o ticker do Lenis e efeito parallax no Hero.
- **Swiper 11**: Carrossel responsivo de profissionais/produtos com arraste por toque, suporte a autoplay e pausas inteligentes.
- **CSS Modular com Design Tokens**: Arquitetura CSS por camadas (`variables.css`, `reset.css`, `typography.css`, `components.css`), permitindo alterar toda a paleta visual em segundos através de variáveis CSS fluidas (`clamp()`).
- **Automação de Mídias em Python**: Script inteligente (`scripts/process_media.py`) que varre logos SVG, otimiza fotos com Lanczos e Unsharp Mask, gera arquivos WebP com preservação de canal alfa e sincroniza o `favicon.svg`.
- **Scripts de 1-Clique para Windows**:
  - `iniciar-demo.bat`: Instala dependências, compila e abre o navegador automaticamente na demonstração local.
  - `publicar-demo.bat`: Valida o build e envia as alterações diretamente para publicação no GitHub Pages.
- **Pipeline CI/CD GitHub Pages**: Publicação automática a cada push através de GitHub Actions configurado em `.github/workflows/deploy.yml`.
- **Skill Integrada**: `.agents/skills/landing-page-builder/SKILL.md` pronta para conduzir entrevistas de briefing completas e orquestrar o desenvolvimento via IA.

---

## 🚀 Como Executar a Demonstração Local

### Opção 1: Atalho Rápido de 1-Clique (Windows)
Basta dar um duplo clique no arquivo **`iniciar-demo.bat`** na raiz do projeto. Ele cuidará da instalação, build e abrirá a página automaticamente no seu navegador padrão!

### Opção 2: Via Terminal / NPM
```bash
# Clone o repositório
git clone git@github.com:Gabriel-mDias/sample-landing-page.git
cd sample-landing-page

# Instale as dependências
npm install

# Inicie o servidor local com abertura automática do navegador
npm run serve
# ou para modo de desenvolvimento com HMR:
npm run dev
```

---

## 🎨 Alimentando com Logos SVG e Novas Mídias

Para personalizar as imagens para um novo cliente, você só precisa depositar os arquivos na pasta `media/`:

```
media/
├── logo/        <- Coloque seus logos SVG aqui (ex: logo-full.svg, logo-symbol.svg)
├── espaco/      <- Fotos das instalações ou do escritório (JPG ou PNG)
├── equipe/      <- Fotos dos profissionais recortadas (PNG com transparência)
└── video/       <- Vídeo MP4 curto de background para o Hero (opcional)
```

Em seguida, execute o script de processamento:
```bash
npm run process-media
# ou: python scripts/process_media.py
```

O script automaticamente:
1. Copia e valida os SVGs em `public/assets/logo/`.
2. Sincroniza o símbolo principal como `public/favicon.svg`.
3. Otimiza fotos para formato `.webp` com nitidez e contraste aprimorados.
4. Gera o poster estático `hero-poster.webp` a partir do vídeo ou da foto de capa.

---

## 🧠 Utilizando a Skill no Antigravity (`landing-page-builder`)

Este repositório inclui a skill `.agents/skills/landing-page-builder/SKILL.md`.

Para utilizá-la em um novo projeto:
1. Abra o workspace no Antigravity IDE.
2. Peça ao agente:
   > *"Inicie o planejamento de uma nova landing page utilizando a skill landing-page-builder."*
3. O agente conduzirá uma entrevista estruturada em 6 fases:
   - **Fase 1**: Negócio, Posicionamento, Proposta de Valor (UVP) e Público-Alvo.
   - **Fase 2**: Benchmarking com busca automática de referências na web via `search_web`.
   - **Fase 3**: Definição da Paleta de Cores e Tipografia (Design Tokens).
   - **Fase 4**: Organização de Logos SVG e Mídias.
   - **Fase 5**: Arquitetura de Seções (Hero, Sobre, Serviços, Equipe, Mapa, CTAs).
   - **Fase 6**: Parâmetros de Conversão (WhatsApp formatado, Links, SEO).
4. O agente consolidará um `requisitos/briefing.md` e aplicará as alterações diretamente nos tokens e no código-fonte.

---

## 🌐 Publicação no GitHub Pages para Demonstração Gratuita

Para demonstrar a landing page ao cliente com link público gratuito e ultrarrápido:

### Opção 1: Script de 1-Clique
Execute o arquivo **`publicar-demo.bat`** no terminal ou com duplo clique.

### Opção 2: Git Manual
1. No seu repositório do GitHub, vá em **Settings** > **Pages**.
2. Em **Build and deployment** > **Source**, selecione **GitHub Actions**.
3. Realize um commit e envie para o GitHub:
   ```bash
   git add .
   git commit -m "feat: customize landing page for client"
   git push origin main
   ```
4. A pipeline `.github/workflows/deploy.yml` será disparada automaticamente.
5. Em menos de 1 minuto, seu site estará no ar em:
   `https://<seu-usuario>.github.io/sample-landing-page/`

---

## 📁 Estrutura de Pastas

```
sample-landing-page/
├── .agents/
│   └── skills/
│       └── landing-page-builder/
│           └── SKILL.md                 # Skill oficial do Antigravity
├── .github/
│   └── workflows/
│       └── deploy.yml                   # Pipeline de deploy automático no GitHub Pages
├── media/                               # Diretório para arquivos brutos do cliente
│   ├── logo/
│   ├── espaco/
│   ├── equipe/
│   └── video/
├── public/                              # Arquivos estáticos servidos diretamente
│   ├── favicon.svg
│   └── assets/
│       ├── images/                      # Imagens otimizadas em WebP
│       ├── logo/                        # SVGs sincronizados
│       └── video/                       # Vídeo e posters
├── requisitos/
│   └── briefing_template.md             # Formulário completo para briefing
├── scripts/
│   └── process_media.py                 # Pipeline de otimização de mídias (Python)
├── src/
│   ├── js/
│   │   ├── animations.js                # Setup de Lenis + GSAP ScrollTrigger
│   │   ├── carousel.js                  # Setup de Swiper
│   │   ├── navigation.js                # Navbar dinâmica e rolagem suave
│   │   └── main.js                      # Ponto de entrada JS
│   └── styles/
│       ├── variables.css                # Design tokens (cores, fontes, espaçamentos)
│       ├── reset.css                    # Reset moderno
│       ├── typography.css               # Estilos tipográficos editoriais
│       ├── components.css               # Componentes reutilizáveis
│       └── main.css                     # Importador de estilos
├── index.html                           # HTML semântico e estruturado
├── iniciar-demo.bat                     # Launcher 1-clique para servidor local
├── publicar-demo.bat                    # Script 1-clique para publicação no Pages
├── package.json                         # Dependências e scripts npm
├── vite.config.js                       # Configuração de build para o Pages
└── README.md
```

---

## 📄 Licença

Distribuído sob a licença MIT. Sinta-se livre para utilizar este template em projetos comerciais e pessoais.