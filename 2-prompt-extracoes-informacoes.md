# 🔍 ETAPA 2: EXTRAÇÕES DE INFORMAÇÕES - MENTOR DE LÍDERES

## 🎯 OBJETIVO
Realizar extrações estratégicas e inteligência de mercado usando múltiplas ferramentas MCP para coletar dados de redes sociais, sites, tendências e concorrência, criando uma base rica de informações para fundamentar a criação de conteúdo de alta performance.

---

## 📊 FERRAMENTAS NECESSÁRIAS

### 🔧 MCPs Principais:
- `Instagram Video Analyzer MCP` - Transcrições e análise de vídeos
- `Apify Actors` - Scrapers especializados do Instagram
- `imageFetch_fetch` - Extração de conteúdo web
- `web-search` - Inteligência de mercado
- `browser_navigate_Playwright` - Navegação avançada
- `execute_sql_supabase` - Armazenamento estruturado

---

## 🗂️ FASE 1: EXTRAÇÕES DE REDES SOCIAIS

### 📱 Instagram - Análise Completa do Perfil

#### 1.1 Extração de Perfil Principal
```
APIFY ACTOR: Instagram Profile Scraper
DADOS OBRIGATÓRIOS:
✅ Número exato de seguidores
✅ Número de posts totais
✅ Bio completa e links
✅ Tipo de conta (business/creator/personal)
✅ Status de verificação
✅ Categoria/nicho identificado
✅ Frequência de postagem estimada
✅ Engagement rate médio

COMANDO EXEMPLO:
{
  "usernames": ["@usuario"],
  "resultsType": "details",
  "resultsLimit": 1,
  "addParentData": true
}
```

#### 1.2 Análise de Hashtags Estratégicas
```
APIFY ACTOR: Instagram Hashtag Scraper
HASHTAGS OBRIGATÓRIAS (mínimo 3):
✅ Hashtag principal do nicho
✅ Hashtag de localização (se relevante)
✅ Hashtag de especialidade específica

DADOS EXTRAÍDOS:
✅ Posts recentes usando a hashtag
✅ Volume de posts total
✅ Engagement médio por hashtag
✅ Tendências de crescimento
✅ Hashtags relacionadas
✅ Influenciadores principais

COMANDO EXEMPLO:
{
  "hashtags": ["#nicho", "#especialidade", "#localizacao"],
  "resultsType": "posts",
  "resultsLimit": 50
}
```

#### 1.3 Transcrições de Vídeos (Reels/IGTV)
```
INSTAGRAM VIDEO ANALYZER MCP:
VÍDEOS OBRIGATÓRIOS (mínimo 10):
✅ 3 vídeos com maior performance
✅ 3 vídeos mais recentes
✅ 2 vídeos sobre especialidade principal
✅ 2 vídeos educativos/informativos

ANÁLISE COMPLETA:
✅ Transcrição palavra por palavra
✅ Análise de tom de voz
✅ Estrutura do roteiro
✅ Elementos de persuasão
✅ Call-to-actions utilizados
✅ Temas abordados
✅ Duração e ritmo
✅ Hooks de abertura
✅ Técnicas de engajamento

COMANDO EXEMPLO:
analyze_instagram_video("URL_DO_VIDEO", "comprehensive")
```

---

## 🌐 FASE 2: EXTRAÇÕES WEB E INTELIGÊNCIA DE MERCADO

### 🏢 Análise de Sites e Presença Digital

#### 2.1 Website Principal
```
IMAGEFETCH + WEB-SEARCH:
DADOS OBRIGATÓRIOS:
✅ Serviços oferecidos completos
✅ Preços e pacotes (se disponíveis)
✅ Sobre/história da empresa
✅ Equipe e credenciais
✅ Localização e contato
✅ Tecnologias utilizadas
✅ Diferenciais competitivos
✅ Público-alvo identificado
✅ SEO e palavras-chave
✅ Call-to-actions principais

COMANDO EXEMPLO:
imageFetch_fetch({
  "url": "website_principal",
  "maxLength": 20000,
  "enableFetchImages": false
})
```

#### 2.2 Sites Especializados (se existirem)
```
ANÁLISE POR ESPECIALIDADE:
✅ Portfólio específico por área
✅ Metodologias exclusivas
✅ Casos de sucesso
✅ Certificações e formações
✅ Parcerias estratégicas
✅ Tecnologias diferenciadas
✅ Processos únicos
✅ Garantias oferecidas
```

### 📊 Inteligência de Mercado

#### 2.3 Pesquisa de Tendências
```
WEB-SEARCH ESTRATÉGICO:
BUSCAS OBRIGATÓRIAS:
✅ "[nicho] tendências 2025 Brasil"
✅ "[especialidade] mercado crescimento"
✅ "[localização] [profissão] avaliações"
✅ "melhores [profissão] [cidade]"
✅ "[nicho] preços mercado [região]"

DADOS EXTRAÍDOS:
✅ Tendências emergentes
✅ Tecnologias em alta
✅ Mudanças no comportamento do consumidor
✅ Novos players no mercado
✅ Regulamentações e mudanças legais
✅ Oportunidades de nicho
✅ Gaps de mercado identificados
```

#### 2.4 Análise Competitiva
```
CONCORRENTES IDENTIFICADOS:
✅ Top 5 concorrentes diretos
✅ Análise de posicionamento
✅ Comparação de preços
✅ Diferenciais competitivos
✅ Presença digital
✅ Estratégias de conteúdo
✅ Pontos fortes e fracos
✅ Oportunidades de diferenciação
```

---

## 🗄️ FASE 3: ESTRUTURAÇÃO NO SUPABASE

### 📊 Tabela de Extrações: `extracoes_conteudo_[nome_usuario]`

```sql
CREATE TABLE IF NOT EXISTS extracoes_conteudo_[nome_usuario] (
    id SERIAL PRIMARY KEY,
    
    -- IDENTIFICAÇÃO
    usuario_nome VARCHAR(255) NOT NULL,
    plataforma VARCHAR(50) NOT NULL,
    url_origem TEXT,
    tipo_conteudo VARCHAR(50),
    
    -- CONTEÚDO PRINCIPAL
    titulo TEXT,
    descricao TEXT,
    transcricao_completa TEXT,
    hashtags TEXT,
    mencoes TEXT,
    
    -- ANÁLISE DE CONTEÚDO
    tema_principal VARCHAR(255),
    palavras_chave TEXT,
    sentimento VARCHAR(50),
    call_to_action TEXT,
    
    -- MÉTRICAS DE ENGAJAMENTO
    visualizacoes INTEGER,
    curtidas INTEGER,
    comentarios INTEGER,
    compartilhamentos INTEGER,
    engagement_rate DECIMAL(5,2),
    
    -- INSIGHTS ESTRATÉGICOS
    tendencia_identificada TEXT,
    gap_de_conteudo TEXT,
    oportunidade_estrategica TEXT,
    analise_ia_completa TEXT,
    
    -- CONTROLE DE PROCESSAMENTO
    job_id VARCHAR(255),
    status_analise VARCHAR(50),
    data_publicacao TIMESTAMP,
    data_extracao TIMESTAMP DEFAULT now(),
    ferramenta_extracao VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

### 📊 Tabela de Extrações Web: `extracoes_[nome_usuario]`

```sql
CREATE TABLE IF NOT EXISTS extracoes_[nome_usuario] (
    id SERIAL PRIMARY KEY,
    
    -- IDENTIFICAÇÃO
    tipo_extracao VARCHAR(100) NOT NULL,
    fonte VARCHAR(255) NOT NULL,
    ferramenta_utilizada VARCHAR(100) NOT NULL,
    
    -- CONTEÚDO
    titulo TEXT,
    descricao TEXT,
    conteudo_completo TEXT,
    metadados JSONB,
    
    -- ANÁLISE
    insights_principais TEXT,
    oportunidades_identificadas TEXT,
    gaps_de_conteudo TEXT,
    recomendacoes TEXT,
    
    -- CONTROLE
    status VARCHAR(50) DEFAULT 'extraido',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

---

## 🎯 FASE 4: ANÁLISE E CONSOLIDAÇÃO

### 📊 Framework de Análise de Padrões

#### 4.1 Análise de Tom de Voz
```
ELEMENTOS OBRIGATÓRIOS:
✅ Tom predominante identificado
✅ Variações por tipo de conteúdo
✅ Linguagem técnica vs acessível
✅ Nível de formalidade
✅ Elementos emocionais
✅ Personalidade da marca
✅ Consistência entre plataformas
✅ Adaptação ao público-alvo

CATEGORIZAÇÃO:
- Educativo-Maternal
- Científico-Professoral
- Mentor-Especialista
- Comercial-Transparente
- Inspirador-Motivacional
```

#### 4.2 Estruturas de Conteúdo
```
PADRÕES IDENTIFICADOS:
✅ Estrutura de hooks/aberturas
✅ Desenvolvimento do conteúdo
✅ Técnicas de persuasão
✅ Call-to-actions padrão
✅ Duração média dos vídeos
✅ Frequência de postagem
✅ Temas mais abordados
✅ Elementos de viralização
```

#### 4.3 Estratégias de Engajamento
```
TÉCNICAS DOCUMENTADAS:
✅ Tipos de perguntas utilizadas
✅ Elementos de controvérsia
✅ Storytelling aplicado
✅ Uso de dados e estatísticas
✅ Citação de autoridades
✅ Casos práticos e exemplos
✅ Interação com audiência
✅ Criação de comunidade
```

---

## 📊 FASE 5: INTELIGÊNCIA COMPETITIVA

### 🔍 Análise de Concorrência

#### 5.1 Mapeamento Competitivo
```
CONCORRENTES DIRETOS (3-5):
✅ Análise de posicionamento
✅ Estratégias de conteúdo
✅ Frequência de publicação
✅ Tipos de engajamento
✅ Parcerias e colaborações
✅ Preços e ofertas
✅ Diferenciais únicos
✅ Pontos fracos identificados
```

#### 5.2 Gaps de Mercado
```
OPORTUNIDADES IDENTIFICADAS:
✅ Temas não explorados
✅ Formatos de conteúdo ausentes
✅ Públicos não atendidos
✅ Tecnologias não utilizadas
✅ Parcerias não exploradas
✅ Canais de distribuição livres
✅ Nichos específicos disponíveis
```

---

## ✅ CHECKLIST DE QUALIDADE

### 📋 Verificação Obrigatória:

#### Extrações de Redes Sociais:
- [ ] Perfil Instagram analisado completamente
- [ ] Mínimo 3 hashtags estratégicas extraídas
- [ ] 10+ vídeos transcritos e analisados
- [ ] Tom de voz identificado e categorizado
- [ ] Padrões de conteúdo documentados

#### Extrações Web:
- [ ] Website principal analisado
- [ ] Sites especializados mapeados
- [ ] Inteligência de mercado coletada
- [ ] Análise competitiva realizada
- [ ] Tendências identificadas

#### Estruturação de Dados:
- [ ] Tabelas Supabase criadas
- [ ] Dados inseridos corretamente
- [ ] Análises consolidadas
- [ ] Insights estratégicos documentados
- [ ] Server memory atualizado

---

## 🚀 OUTPUTS ESPERADOS

### 📊 Entregáveis Obrigatórios:

1. **Base de Dados Rica**: 15+ extrações estruturadas
2. **Análise de Tom de Voz**: Padrões identificados
3. **Inteligência de Mercado**: Tendências e oportunidades
4. **Análise Competitiva**: Gaps e diferenciação
5. **Relatório Consolidado**: Insights estratégicos

### 🎯 Critérios de Sucesso:
- **Volume**: 15+ extrações de qualidade
- **Diversidade**: Múltiplas fontes e tipos
- **Profundidade**: Análises detalhadas
- **Estratégia**: Insights acionáveis
- **Tempo**: Processo completo em 60-90 minutos

---

## 🔄 PRÓXIMOS PASSOS

### ➡️ Preparação para Etapa 3:
1. **Base rica de dados** para análise de padrões
2. **Tom de voz definido** para adaptação
3. **Tendências mapeadas** para aproveitamento
4. **Gaps identificados** para exploração

### 🎯 Conexão com Workflow:
- **Etapa 3**: Seleção de modelos baseada nos padrões identificados
- **Etapa 4**: Criação de roteiros usando tom de voz e estruturas
- **Etapa 5**: Validação baseada em benchmarks extraídos

---

**📅 Versão**: 2.0  
**🎯 Programa**: MENTOR DE LÍDERES  
**🔄 Status**: Etapa 2 de 7 do Workflow Completo  
**⏱️ Tempo Estimado**: 60-90 minutos  
**🎯 Próxima Etapa**: Construção de Base de Conteúdos
