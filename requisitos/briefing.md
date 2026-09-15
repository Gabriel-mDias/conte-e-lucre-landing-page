# Briefing da Landing Page — Conte & Lucre

Documento de alinhamento estratégico e diretrizes de desenvolvimento para a landing page de alta conversão da **Conte & Lucre**.

## Direção aprovada para a revisão premium — setembro de 2026

- **Direção visual:** editorial híbrida, combinando superfícies claras inspiradas no Instagram com hero, método e conversão em grafite.
- **Política de mídia:** presença autêntica de Vanessa e dos posts oficiais como núcleo da marca; fotos Pexels licenciadas apenas como apoio contextual.
- **Conteúdo:** reestruturação rigorosa da narrativa, sem métricas inventadas, garantias absolutas, prazos rígidos ou resultados financeiros prometidos.
- **Conversão:** diagnóstico inicial pelo WhatsApp, com formulário local e explicação explícita de que os dados só seguem após confirmação do visitante.
- **Identidade preservada:** Cormorant Garamond, Plus Jakarta Sans, teal `#00A896`, grafite `#16191E`, gelo `#F8FAFB` e dourado `#D4AF37` restrito a detalhes.
- **Experiência:** hierarquia mais curta, contraste WCAG AA, movimento reduzido respeitado e mídia responsiva sem deformações.

### Refinamentos de hero, fundadora e rodapé

- **Hero fullscreen:** ocupa a viewport real com `100svh/100dvh`, sem limite máximo no desktop nem altura fixa no mobile. Em telas excepcionalmente baixas, pode crescer para acomodar conteúdo sem cortes.
- **Vídeo da hero:** mantém poster, autoplay silencioso e `object-fit: cover`, agora com opacidade integral. O contraste vem de um scrim localizado atrás do texto e de um degradê inferior suave, com enquadramentos próprios para desktop, tablet, mobile vertical e mobile horizontal.
- **Conteúdo acima da dobra:** tipografia e espaçamentos fluidos mantêm headline, apoio e CTAs na primeira viewport nos tamanhos de referência, preservando a pausa do vídeo em `prefers-reduced-motion`.
- **Retrato da fundadora:** uso exclusivo de `media/equipe/vanessa/vanessa_1.png` na seção de Vanessa. O pipeline preserva transparência e gera `vanessa_1_cutout.webp` com fallback PNG, sem a regra de nomes que sobrescrevia retratos da mesma pasta.
- **Composição da Vanessa:** retrato recortado sobre cenário editorial da paleta Conte & Lucre, com formas discretas e enquadramento responsivo; a hero permanece centrada no vídeo.
- **Rodapé:** grade responsiva com marca, navegação, três soluções e canais de atendimento. WhatsApp, e-mail, Instagram e localização usam ícones SVG lineares acessíveis; a faixa legal preserva copyright, CNPJ e cidade.
- **Crédito de desenvolvimento:** “Desenvolvido por G&Ms Soluções Tecnológicas”, vinculado a `https://gems.tec.br/` e tratado de forma equivalente ao projeto Essenza.

---

## 1. Dados Básicos da Empresa / Marca
- **Razão Social**: CONTE & LUCRE LTDA - ME
- **Nome Fantasia**: Conte & Lucre (Consultoria e Assessoria Financeira)
- **Subtítulo / Especialidade**: Especialista em Processos Financeiros Empresariais & BPO Financeiro
- **Slogan Principal**: *"Gestão com propósito"*
- **Tríade de Valor**: *"Controle | Estratégia | Resultado"*
- **Endereço / Polo**: Venda Nova do Imigrante — ES (Atendimento presencial na Região Serrana e consultoria online para todo o Brasil)
- **WhatsApp Principal**: `(27) 99884-4331` (Formato Internacional: `5527998844331`)
- **E-mail**: `conteelucre@gmail.com`
- **Redes Sociais**: [@conteelucre](https://www.instagram.com/conteelucre/) | [linktr.ee/vanessarezendepianzola](https://linktr.ee/vanessarezendepianzola)

---

## 2. Posicionamento & Público-Alvo
- **Proposta Única de Valor (UVP)**:  
  *"Transformamos desordem financeira em previsibilidade, lucro real e tranquilidade. Cuidamos da rotina contábil e financeira da sua empresa para que você foque no que faz de melhor: fazer o negócio crescer."*
- **Público-Alvo Principal**:
  1. Empresários e donos de PMEs que faturam bem, mas não têm clareza de onde o dinheiro está indo.
  2. Empresas familiares e casais empreendedores que precisam separar finanças pessoais das contas jurídicas e alinhar pró-labore.
  3. Profissionais liberais e prestadores de serviços que perdem horas valiosas fazendo contas a pagar e cobranças manuais.
- **Principais Dores do Cliente**:
  - Mistura constante de conta física e jurídica.
  - Ausência de fluxo de caixa projetado e surpresas negativas no fim do mês.
  - Falta de tempo para rotinas operacionais (conciliação bancária, emissão de boletos, conferência de notas).
  - Medo de crescer e perder o controle das contas.
- **Maiores Objeções**:
  - *"Não sei se meu negócio tem tamanho suficiente para contratar uma consultoria/BPO financeiro."*
  - *"Tenho receio de abrir as contas e números da minha empresa para terceiros."*
  - *"Será que vou perder a autonomia das minhas decisões se terceirizar o financeiro?"*

---

## 3. Identidade Visual & Design System
- **Cor Primária (Destaque & Ação)**: `#00A896` (Teal Lucro / Ciano Estratégico)
- **Cor Primária Hover**: `#028090`
- **Cor de Fundo Escuro**: `#16191E` (Grafite Ônix Nobre)
- **Cor de Fundo Claro**: `#F8FAFB` (Gelo Arejado / Pérola)
- **Acento Secundário**: `#D4AF37` (Dourado Champagne / Prestígio)
- **Estilo Visual das Seções**: Híbrido Cinematográfico (Hero, Prova de Autoridade e Rodapé escuros; Seções explicativas e pilares claras e arejadas para máxima legibilidade).
- **Tipografia**:
  - Títulos: `Cormorant Garamond` (com itálicos nos termos de destaque).
  - Textos & Interface: `Plus Jakarta Sans` / `Inter`.
- **Atmosfera**: Confiança inabalável, alta sofisticação executiva, serenidade e clareza estratégica.

---

## 4. Estrutura de Seções da Landing Page
1. **Header Fixo / Blur Glassmorphism**:
   - Logo Conte & Lucre, links de ancoragem suaves (`#sobre`, `#pilares`, `#metodo`, `#contato`) e botão CTA WhatsApp.
2. **Hero Section (Impacto Imediato)**:
   - Badge: *"Consultoria & Assessoria Financeira Estratégica"*
   - Headline: *"Sua empresa está progredindo ou só movimentando dinheiro?"*
   - Subheadline: *"Estruturamos processos e assumimos a rotina financeira para você decidir com mais clareza, proteger seu tempo e compreender seus números."*
   - CTA Primário: *"Agendar Diagnóstico Gratuito"* (WhatsApp)
   - CTA Secundário: *"Conhecer Nossos Serviços"* (Âncora `#pilares`)
3. **Barra de Métricas & Credibilidade**:
   - Compromissos qualitativos de credibilidade: processos organizados, decisões com contexto e parceria confidencial.
4. **Sobre a Conte & Lucre / Liderança**:
   - Apresentação de Vanessa Rezende Pianzola e sócios.
   - O diferencial de aliar técnica analítica com propósito humano e alinhamento familiar.
5. **Pilares de Atuação (Cards Interativos)**:
   - 1. BPO Financeiro & Gestão Operacional
   - 2. Consultoria & Diagnóstico Estratégico
   - 3. Finanças para Casais & Empresas Familiares
6. **Método Passo a Passo**:
   - 1. Diagnóstico Inicial -> 2. Estruturação dos Processos -> 3. Rotina Operacional BPO -> 4. Acompanhamento & Lucro Estratégico.
7. **Quebra de Objeções / FAQ Acordeon**:
   - Dúvidas sobre sigilo bancário, porte da empresa, transição de sistemas e tempo de implementação.
8. **CTA Final & Rodapé Executivo**:
   - Chamada direta para o WhatsApp com pré-mensagem personalizada, links institucionais e localização em Venda Nova do Imigrante - ES.
