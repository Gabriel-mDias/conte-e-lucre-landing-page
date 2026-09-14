---
name: landing-page-builder
description: >-
  Especialista na concepção, planejamento hiper-detalhado, busca de referências de mercado e desenvolvimento de landing pages premium e cinematográficas de alta conversão. Conduz entrevistas exaustivas de briefing, busca referências automáticas na web via search_web e implementa landing pages com Vite, Lenis, GSAP, Swiper e automação de mídias e logos SVG.
---

# Skill: Landing Page Builder (Alta Conversão & Design Cinematográfico)

Esta skill orienta o agente na construção de landing pages profissionais, sofisticadas e de alto padrão visual, baseadas na arquitetura de excelência do template (Vite, Lenis Smooth Scroll, GSAP ScrollTrigger, Swiper Carrossel, CSS Modular com tokens e automação de mídias).

---

## Filosofia de Design e Padrão de Qualidade

1. **Impacto Visual Imediato**: A primeira impressão (Hero) deve transmitir exclusividade e autoridade máxima, utilizando fundos escuros refinados, vídeo cinematográfico de background, tipografia fluida e badges douradas/metalizadas.
2. **Rolagem Suavizada & Micro-interações**: Uso obrigatório de rolagem inercial com Lenis, transições suaves com curvas bezier e revelações graduais de elementos ao scroll via GSAP.
3. **Nenhum Placeholder Genérico**: Cada imagem, logo SVG e texto deve refletir a identidade real do cliente ou um conceito altamente fiel e contextualizado.
4. **Alimentação Descomplicada**: Logos SVG e mídias tratadas de forma automatizada através do script `scripts/process_media.py`.

---

## Fluxo de Trabalho em 4 Etapas

```
[1. Entrevista & Mapeamento Minucioso] 
                 │
                 ▼
[2. Benchmarking Automático com search_web]
                 │
                 ▼
[3. Consolidação do briefing.md & Validação]
                 │
                 ▼
[4. Implementação Técnica, Otimização & Deploy]
```

---

## Etapa 1: Entrevista Estratégica & Mapeamento Minucioso

Ao iniciar o planejamento de uma nova landing page, o agente deve entrevistar o usuário/cliente de forma faseada, cobrindo todos os detalhes cruciais divididos em **6 Blocos Estratégicos**:

### Bloco 1: Negócio, Posicionamento & Proposta de Valor (UVP)
- **Identificação Básica**:
  - Razão social e nome fantasia da marca/empresa.
  - Slogan principal e subtítulo institucional.
  - Endereço físico completo, cidade, estado e referências de localização.
  - Telefones de contato e WhatsApp comercial principal.
- **Proposta Única de Valor (UVP)**:
  - Qual é a transformação definitiva que o seu serviço entrega? Em que você é substancialmente diferente dos concorrentes da região?
  - Qual o arquétipo da marca? (Ex: O Cuidador / Acolhedor, O Mago / Transformador, O Especialista / Científico, O Soberano / Alto Luxo).
- **Público-Alvo & Objeções**:
  - Quem é o cliente ideal (faixa etária, gênero, classe socioeconômica, profissão)?
  - Quais são as dores e angústias mais frequentes que o fazem procurar seu atendimento?
  - Quais são as 3 principais objeções que o impedem de agendar imediatamente (ex: medo de procedimento, percepção de preço, falta de tempo, falta de clareza sobre o resultado)?
  - Qual o ticket médio do atendimento/serviço?

### Bloco 2: Identidade Visual, Cores & Atmosfera Sensorial
- **Paleta de Cores**:
  - Cor de destaque principal (Hexadecimal) — ex: Dourado `#b08a5a`, Verde Esmeralda `#1b4332`, Azul Royal `#1a365d`.
  - Cores secundárias de apoio (tons amadeirados, bronze, grafite, champagne).
  - Distribuição visual das seções:
    - *Opção Recomendada (Híbrida Cinematográfica)*: Hero e Rodapé escuros (`--bg-dark: #0e0d0c`) com seções de conteúdo claras e arejadas (`--bg-light: #f9f8f5`).
    - *Opção Total Dark Mode*: Estilo ultra-luxuoso e intimista.
    - *Opção Total Light Mode*: Estilo clínico hospitalar ou corporativo clássico.
- **Tipografia**:
  - Combinação preferida de fontes do Google Fonts:
    - Editorial Clássica: `Cormorant Garamond` (Títulos) + `Plus Jakarta Sans` (Corpo).
    - Moderna Contemporânea: `Playfair Display` + `Inter`.
    - Minimalista Tecnológica: `Outfit` + `DM Sans`.
- **Sensações Desejadas**:
  - Quais adjetivos devem resumir a experiência do visitante ao abrir a página? (Ex: Acolhimento, serenidade, sofisticação, precisão, segurança).

### Bloco 3: Ativos Visuais, Logos SVG & Mídias
- **Logomarca**:
  - O cliente possui os logos vetorizados em `.svg`?
  - Devem ser depositados em `media/logo/` nas variações:
    - `logo-full.svg` (Logomarca completa para cabeçalho)
    - `logo-symbol.svg` (Símbolo isolado para favicon e marcas d'água)
    - `logo-horizontal.svg` (Variação horizontal se aplicável)
- **Imagens do Espaço / Instalações**:
  - Existem fotos de alta resolução do ambiente, recepção e consultórios/escritórios? (Devem ser inseridas em `media/espaco/`).
- **Equipe & Profissionais**:
  - Há fotos dos especialistas?
  - Fotos de meio-corpo recortadas sem fundo (PNG com transparência) são o ideal para o carrossel (`media/equipe/`).
- **Vídeo de Background**:
  - O cliente possui vídeo institucional de 10 a 30 segundos em `.mp4`? (Inserir em `media/video/`). Se não possuir, selecionar imagem de altíssimo impacto com overlay suave.

### Bloco 4: Arquitetura de Conteúdo & Seções
- **Hero Section**:
  - Headline principal impactante (com quebra de linha elegante).
  - Subtítulo explicativo com benefício direto.
  - Frase ou badge de destaque sobre o título ("Viva a sua essência").
  - Botão principal (CTA primário direto para WhatsApp).
  - Botão secundário ("Conhecer o Espaço" com âncora suave `#sobre`).
- **Apresentação / Sobre Nós**:
  - História da empresa, valores e razão de existir.
  - Composição de imagem dupla (foto principal vertical + foto secundária de detalhe).
  - Badges de destaque (ex: "Multidisciplinar", "Privacidade Total").
- **Pilares de Atendimento / Especialidades**:
  - Quais são os 3 ou 4 grandes eixos de serviços oferecidos?
  - Título, descrição concisa e lista de sub-especialidades com ícones de check para cada pilar.
- **Corpo Clínico / Especialistas (Carrossel Horizontal)**:
  - Lista completa dos profissionais/integrantes:
    - Nome completo com titulação.
    - Especialidade / Função.
    - Conselho e número de registro (ex: CRM, CRO, CRP, OAB, CREA).
    - Descrição do método de atuação (2 a 3 linhas).
    - Link para Instagram ou LinkedIn particular.
- **Localização & Acessibilidade**:
  - Endereço com ponto de referência.
  - Coordenadas geográficas ou link direto do Google Maps para incorporação via iframe.
  - Botão de rota rápida ("Traçar Rota no Google Maps").
- **Prova Social & Avaliações (Opcional)**:
  - Depoimentos reais de clientes ou nota média no Google Meu Negócio.
- **FAQ / Dúvidas Frequentes (Opcional)**:
  - Principais perguntas sobre convênios, formas de pagamento, agendamento e estacionamento.

### Bloco 5: Canais de Conversão & CTAs
- **WhatsApp Principal**:
  - Número com DDD no formato internacional `5527999999999`.
  - Mensagem inicial pré-formatada para o WhatsApp:
    `"Olá, conheci a clínica pelo site e gostaria de agendar uma consulta."`
- **Redes Sociais & Links**:
  - Perfil oficial do Instagram.
  - Linktree ou página de links rápidos.
  - E-mail institucional e telefone fixo (se houver).

### Bloco 6: Parâmetros Técnicos & SEO
- **Title Tag**: Título otimizado de até 65 caracteres contendo marca + especialidade + cidade (ex: `Essenza — Saúde Personalizada | Viva a sua essência em Santa Teresa - ES`).
- **Meta Description**: Resumo magnético de até 160 caracteres com chamada para ação.
- **Open Graph**: Imagem de pré-visualização para links compartilhados em redes sociais e WhatsApp.

---

## Etapa 2: Benchmarking Automatizado com `search_web`

Durante a entrevista (após os Blocos 1 e 2), o agente deve proativamente realizar buscas na web para identificar referências reais do mesmo nicho e cidade/região:

1. **Executar buscas estratégicas**:
   - `[nicho] landing page alta conversao referencia visual awwwards`
   - `melhores clinicas de [especialidade] design premium`
   - Exemplos reais de concorrentes diretos no mesmo estado/cidade.
2. **Curadoria de 3 a 5 referências**:
   - Selecionar páginas com arquitetura inspiradora.
   - Analisar: paleta de cores dominante, tom de voz da cópia, disposição do hero e uso de fotos reais vs ilustrações.
3. **Documentar em `requisitos/referencias.md`**:
   - Registrar links clicáveis e notas de design que serão adotadas no projeto atual.

---

## Etapa 3: Consolidação do Briefing

Antes de realizar alterações no código, a Skill instrui o agente a criar o arquivo `requisitos/briefing.md` consolidando todas as respostas da entrevista e decisões de design para aprovação do usuário.

---

## Etapa 4: Implementação Técnica & Otimização de Mídias

Após aprovação do briefing, o agente executa os passos práticos:

### 1. Atualizar Design Tokens em `src/styles/variables.css`
Ajustar as variáveis conforme a identidade acordada:
```css
:root {
  --color-primary: #b08a5a;
  --color-primary-hover: #c49d6c;
  --color-secondary: #755535;
  --bg-dark: #0e0d0c;
  --bg-light: #f9f8f5;
  --font-serif: 'Cormorant Garamond', serif;
  --font-sans: 'Plus Jakarta Sans', sans-serif;
}
```

### 2. Alimentar e Processar Mídias com o Script Python
1. O usuário ou agente deposita os arquivos nas pastas correspondentes em `media/`:
   - `media/logo/`: arquivos `.svg` ou `.png`
   - `media/espaco/`: fotos do local
   - `media/equipe/`: fotos dos profissionais
   - `media/video/`: vídeo em `.mp4`
2. Executar o processador automatizado:
   ```bash
   python scripts/process_media.py
   # ou via npm
   npm run process-media
   ```
   *O script automaticamente gera WebP otimizado, redimensionamento Lanczos, unsharp mask, sincroniza o favicon.svg e gera o poster do vídeo.*

### 3. Atualizar Conteúdo Semântico em `index.html`
- Atualizar meta tags de SEO e título.
- Atualizar logos e imagens apontando para `assets/...`.
- Substituir títulos, descrições dos pilares e dados dos profissionais no carrossel.
- Atualizar links do WhatsApp, Instagram, Linktree e coordenadas do Google Maps iframe.

### 4. Validar e Compilar
```bash
npm install
npm run build
npm run preview
```
Garantir que a pasta `dist/` seja gerada sem erros e os assets carreguem com fidelidade.

### 5. Deploy no GitHub Pages
O workflow `.github/workflows/deploy.yml` já está pré-configurado.
Ao realizar o commit e push para a branch `main`:
1. O GitHub Actions compila o projeto.
2. A página é publicada automaticamente no GitHub Pages sob a URL:
   `https://<usuario>.github.io/<nome-do-repositorio>/`
3. A demonstração fica imediatamente acessível para envio gratuito e de alta velocidade ao cliente!
