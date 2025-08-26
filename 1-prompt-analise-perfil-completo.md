# 📋 ETAPA 1: ANÁLISE DE PERFIL COMPLETO - MENTOR DE LÍDERES

## 🎯 OBJETIVO
Criar um perfil 360° completo e estratégico de um influenciador/mentor, consolidando informações de múltiplas fontes (Google Sheets, PDFs, redes sociais, sites) em uma base de dados estruturada no Supabase para fundamentar todas as etapas subsequentes do workflow de criação de conteúdo.

---

## 📊 FERRAMENTAS NECESSÁRIAS

### 🔧 MCPs Principais:
- `googledrivesheets` - Acesso às planilhas do programa
- `execute_sql_supabase` - Criação e manipulação de dados
- `browser_navigate_Playwright` - Navegação web avançada
- `imageFetch_fetch` - Extração de conteúdo web
- `web-search` - Pesquisa complementar
- `create_entities_servermemory` - Armazenamento permanente

---

## 🗂️ FASE 1: EXTRAÇÃO DE DADOS DAS PLANILHAS

### 📝 Procedimento Detalhado:

#### 1.1 Acesso às 4 Planilhas Principais
```
PLANILHAS OBRIGATÓRIAS:
✅ Google_Sheets_googledrivesheets (INFLUENCIADOR DIGITAL)
✅ Google_Sheets1_googledrivesheets (MENTOR LIVRO)  
✅ Google_Sheets2_googledrivesheets (MENTORIA)
✅ Google_Sheets3_googledrivesheets (PALESTRAS)

COMANDO:
Para cada planilha, executar:
- Extrair todos os dados usando MCP
- Buscar pelo nome completo do usuário
- Identificar linha/row de localização
- Anotar em qual planilha foi encontrado
```

#### 1.2 Estratégia de Busca
```
BUSCA PRIMÁRIA:
- Nome completo exato
- Variações com/sem acentos
- Abreviações comuns
- Nomes artísticos/profissionais

BUSCA SECUNDÁRIA (se não encontrado):
- Usar Playwright para busca manual
- Ctrl+F nas planilhas
- Verificar colunas B e C especificamente
- Documentar links encontrados
```

#### 1.3 Validação de Dados
```
VERIFICAÇÕES OBRIGATÓRIAS:
✅ Nome encontrado em pelo menos 1 planilha
✅ Links do Instagram funcionais
✅ Dados de contato válidos
✅ Informações de arquétipo presentes
✅ Links de recursos acessíveis
```

---

## 🗄️ FASE 2: CRIAÇÃO DA ESTRUTURA NO SUPABASE

### 📊 Tabela Principal: `perfil_completo_[nome_usuario]`

```sql
CREATE TABLE IF NOT EXISTS perfil_completo_[nome_usuario] (
    id SERIAL PRIMARY KEY,
    
    -- INFORMAÇÕES PESSOAIS E PROFISSIONAIS
    nome_completo VARCHAR(255) NOT NULL,
    profissao VARCHAR(255),
    especialidade VARCHAR(255),
    tempo_atuacao VARCHAR(100),
    segmento VARCHAR(100),
    
    -- DADOS DIGITAIS (influenciador_digital)
    instagram_principal TEXT,
    instagram_empresa TEXT,
    seguidores_instagram VARCHAR(50),
    perfil_aberto_fechado VARCHAR(20),
    frequencia_postagem TEXT,
    posicionamento_digital_0_10 INTEGER,
    linkedin TEXT,
    
    -- NÍVEIS DE DESENVOLVIMENTO (mentor_lideres)
    nivel_estruturou_mentoria_0_10 INTEGER,
    experiencia_mentoria TEXT,
    nivel_palestrou_0_10 INTEGER,
    experiencia_palestras TEXT,
    nivel_livro_mentor INTEGER,
    experiencia_livro TEXT,
    nivel_aluno INTEGER,
    descricao_nivel_aluno TEXT,
    
    -- ARQUÉTIPO COMPLETO (enriquecido)
    arquetipo_id INTEGER,
    arquetipo_nome TEXT,
    arquetipo_nome_ingles VARCHAR(100),
    arquetipo_descricao_resumida TEXT,
    arquetipo_descricao_detalhada TEXT,
    arquetipo_caracteristicas_principais TEXT,
    arquetipo_pontos_fortes TEXT,
    arquetipo_desafios TEXT,
    arquetipo_missao TEXT,
    arquetipo_motivacao_principal TEXT,
    arquetipo_medo_principal TEXT,
    arquetipo_estrategia TEXT,
    arquetipo_cores_associadas TEXT,
    arquetipo_simbolos TEXT,
    arquetipo_exemplos_marcas TEXT,
    arquetipo_nicho_marketing TEXT,
    arquetipo_tom_voz TEXT,
    
    -- ANÁLISE DE PDF PERSONALIZADO
    pdf_link TEXT,
    pdf_analise_personalizada TEXT,
    pdf_missao_declarada TEXT,
    pdf_objetivos_legado TEXT,
    pdf_futuro_desejado TEXT,
    
    -- WEBSITES E RECURSOS
    website_principal TEXT,
    website_cirurgia_dermatologica TEXT,
    website_medicina_capilar TEXT,
    website_estetica TEXT,
    todos_links_produtos_servicos TEXT,
    
    -- TRAJETÓRIA E OBJETIVOS
    trajetoria_mercado_digital TEXT,
    objetivo_mentoria_mentor_lideres TEXT,
    descricao_profissional_completa TEXT,
    
    -- ANÁLISE ESTRATÉGICA CONSOLIDADA
    pontos_fortes_consolidados TEXT,
    desafios_consolidados TEXT,
    oportunidades_identificadas TEXT,
    recomendacoes_estrategicas TEXT,
    
    -- CONTROLE DE EXTRAÇÕES
    total_extracoes INTEGER DEFAULT 0,
    ultima_extracao TIMESTAMP,
    extracoes_realizadas TEXT,
    data_ultima_extracao TIMESTAMP,
    
    -- TIMESTAMPS
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

---

## 🔍 FASE 3: ENRIQUECIMENTO COM DADOS EXTERNOS

### 🌐 Verificação de Links e Recursos

#### 3.1 Validação de Redes Sociais
```
INSTAGRAM:
✅ Verificar se perfil é público/privado
✅ Extrair número de seguidores atual
✅ Verificar frequência de postagem
✅ Identificar tipo de conteúdo principal
✅ Anotar bio e links na bio

LINKEDIN:
✅ Verificar perfil profissional
✅ Extrair experiência e formação
✅ Identificar conexões relevantes
✅ Anotar artigos e posts recentes
```

#### 3.2 Análise de Websites
```
WEBSITE PRINCIPAL:
✅ Verificar funcionamento
✅ Extrair serviços oferecidos
✅ Identificar público-alvo
✅ Anotar diferenciais competitivos
✅ Verificar SEO e posicionamento

SITES ESPECIALIZADOS:
✅ Mapear portfólio completo
✅ Identificar nichos específicos
✅ Extrair preços e pacotes
✅ Verificar tecnologias utilizadas
```

#### 3.3 Processamento de PDF Personalizado
```
EXTRAÇÃO OBRIGATÓRIA:
✅ Arquétipo identificado completo
✅ Análise personalizada detalhada
✅ Missão declarada específica
✅ Objetivos de legado definidos
✅ Futuro desejado descrito
✅ Pontos fortes únicos
✅ Desafios específicos identificados
```

---

## 📊 FASE 4: ANÁLISE ESTRATÉGICA CONSOLIDADA

### 🎯 Framework de Análise SWOT Adaptado

#### 4.1 Pontos Fortes (Strengths)
```
ANÁLISE OBRIGATÓRIA:
✅ Experiência profissional única
✅ Níveis de desenvolvimento por área
✅ Características positivas do arquétipo
✅ Presença digital estabelecida
✅ Recursos e ferramentas disponíveis
✅ Diferenciais competitivos
✅ Credibilidade e autoridade
✅ Network e conexões
```

#### 4.2 Desafios (Weaknesses)
```
IDENTIFICAÇÃO CRÍTICA:
✅ Áreas com baixo desenvolvimento
✅ Desafios específicos do arquétipo
✅ Limitações na presença digital
✅ Gaps de conhecimento
✅ Recursos limitados
✅ Problemas de posicionamento
✅ Inconsistências na comunicação
```

#### 4.3 Oportunidades (Opportunities)
```
MAPEAMENTO ESTRATÉGICO:
✅ Mercados não explorados
✅ Tendências favoráveis do nicho
✅ Sinergias entre competências
✅ Parcerias potenciais
✅ Tecnologias emergentes
✅ Mudanças no comportamento do público
✅ Gaps da concorrência
```

#### 4.4 Recomendações Estratégicas
```
AÇÕES ESPECÍFICAS:
✅ Prioridades de desenvolvimento
✅ Estratégias de posicionamento
✅ Táticas de crescimento digital
✅ Plano de criação de conteúdo
✅ Cronograma de implementação
✅ Métricas de acompanhamento
✅ Próximos passos concretos
```

---

## ✅ CHECKLIST DE QUALIDADE

### 📋 Verificação Obrigatória Antes de Prosseguir:

#### Dados Básicos:
- [ ] Usuário encontrado em pelo menos 1 das 4 planilhas
- [ ] Dados transferidos para Supabase corretamente
- [ ] Tabela personalizada criada com sucesso
- [ ] Todos os campos obrigatórios preenchidos

#### Validação Externa:
- [ ] Links do Instagram verificados e funcionais
- [ ] Websites acessados e analisados
- [ ] PDF baixado e processado completamente
- [ ] Dados do arquétipo enriquecidos

#### Análise Estratégica:
- [ ] SWOT completa realizada
- [ ] Pontos fortes específicos identificados
- [ ] Desafios reais mapeados
- [ ] Oportunidades concretas listadas
- [ ] Recomendações acionáveis elaboradas

#### Qualidade dos Dados:
- [ ] 90%+ dos campos preenchidos
- [ ] Informações consistentes entre fontes
- [ ] Links testados e funcionais
- [ ] Análise personalizada e específica

---

## 🚀 OUTPUTS ESPERADOS

### 📊 Entregáveis Obrigatórios:

1. **Tabela Supabase Completa**: `perfil_completo_[nome_usuario]`
2. **Relatório de Análise**: Documento markdown consolidado
3. **Server Memory**: Entidades e relações criadas
4. **Validação de Links**: Status de todos os recursos
5. **Análise SWOT**: Framework estratégico completo

### 🎯 Critérios de Sucesso:
- **Completude**: 90%+ dos campos preenchidos
- **Precisão**: Dados verificados e validados
- **Consistência**: Informações alinhadas entre fontes
- **Estratégia**: Análise acionável e específica
- **Tempo**: Processo completo em 30-45 minutos

---

## 🔄 PRÓXIMOS PASSOS

### ➡️ Preparação para Etapa 2:
1. **Base de dados consolidada** pronta para extrações
2. **Perfil estratégico** definido para direcionamento
3. **Oportunidades mapeadas** para exploração
4. **Recomendações** para implementação

### 🎯 Conexão com Workflow:
Esta etapa fundamenta todas as subsequentes:
- **Etapa 2**: Extrações direcionadas baseadas no perfil
- **Etapa 3**: Modelos selecionados conforme arquétipo
- **Etapa 4**: Roteiros personalizados para o público-alvo

---

**📅 Versão**: 2.0  
**🎯 Programa**: MENTOR DE LÍDERES  
**🔄 Status**: Etapa 1 de 7 do Workflow Completo  
**⏱️ Tempo Estimado**: 30-45 minutos  
**🎯 Próxima Etapa**: Extrações de Informações
