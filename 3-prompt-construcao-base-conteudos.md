# 🎬 ETAPA 3: CONSTRUÇÃO DE BASE DE CONTEÚDOS - MENTOR DE LÍDERES

## 🎯 OBJETIVO
Criar uma biblioteca estruturada de modelos de conteúdo de referência, analisando influenciadores de sucesso comprovado para identificar padrões, estruturas e estratégias replicáveis que servirão como base para criação de conteúdos de alta performance.

---

## 📊 FERRAMENTAS NECESSÁRIAS

### 🔧 MCPs Principais:
- `Instagram Video Analyzer MCP` - Análise de vídeos de referência
- `Apify Actors` - Extração de dados de influenciadores
- `execute_sql_supabase` - Criação de tabelas de modelos
- `imageFetch_fetch` - Análise de sites e recursos
- `web-search` - Pesquisa de influenciadores de referência
- `create_entities_servermemory` - Armazenamento de padrões

---

## 🗂️ FASE 1: SELEÇÃO DE INFLUENCIADORES DE REFERÊNCIA

### 🎯 Critérios de Seleção

#### 1.1 Métricas de Performance
```
REQUISITOS MÍNIMOS:
✅ 1M+ seguidores OU alta taxa de engajamento (>5%)
✅ Nicho relacionado ou transferível
✅ Conteúdo educativo/profissional
✅ Estratégia de monetização clara
✅ Consistência de postagem
✅ Autoridade reconhecida no nicho
✅ Crescimento sustentável
✅ Audiência engajada e qualificada

FONTES DE IDENTIFICAÇÃO:
- Pesquisa web por "top influencers [nicho]"
- Análise de hashtags do nicho
- Recomendações de algoritmo
- Benchmarking competitivo
- Indicações de especialistas
```

#### 1.2 Compatibilidade Estratégica
```
ALINHAMENTO OBRIGATÓRIO:
✅ Tom de voz adaptável ao usuário
✅ Público-alvo similar ou expansível
✅ Estratégias de conteúdo replicáveis
✅ Modelo de negócio compatível
✅ Valores e posicionamento alinhados
✅ Formato de conteúdo transferível
✅ Frequência de postagem viável
✅ Recursos necessários acessíveis
```

---

## 🗄️ FASE 2: CRIAÇÃO DA ESTRUTURA DE MODELOS

### 📊 Tabela Principal: `modelos_[nome_influenciador]`

```sql
CREATE TABLE IF NOT EXISTS modelos_[nome_influenciador] (
    id SERIAL PRIMARY KEY,
    
    -- IDENTIFICAÇÃO DO VÍDEO
    ranking INTEGER,
    shortcode VARCHAR(50) UNIQUE,
    url TEXT,
    titulo VARCHAR(255),
    tema VARCHAR(255),
    
    -- DADOS TEMPORAIS
    data_publicacao TIMESTAMP,
    duracao_segundos DECIMAL(6,3),
    
    -- MÉTRICAS DE PERFORMANCE
    visualizacoes INTEGER,
    curtidas INTEGER,
    comentarios INTEGER,
    taxa_engajamento VARCHAR(10),
    
    -- CONTEÚDO
    caption TEXT,
    transcricao_completa TEXT,
    hashtags TEXT[],
    
    -- PARCERIAS E MONETIZAÇÃO
    parceria VARCHAR(255),
    cupom VARCHAR(50),
    
    -- ANÁLISE DE PADRÕES
    estrutura_roteiro TEXT,
    hook_abertura TEXT,
    desenvolvimento TEXT,
    call_to_action TEXT,
    elementos_persuasao TEXT,
    tecnicas_engajamento TEXT,
    
    -- INSIGHTS ESTRATÉGICOS
    tipo_conteudo VARCHAR(100),
    nivel_controversia VARCHAR(50),
    autoridade_cientifica TEXT,
    fatores_viralizacao TEXT,
    publico_alvo_identificado TEXT,
    
    -- ANÁLISE DE TOM E LINGUAGEM
    tom_de_voz VARCHAR(100),
    linguagem_utilizada VARCHAR(100),
    nivel_tecnico VARCHAR(50),
    emocoes_evocadas TEXT,
    
    -- METADADOS
    job_id VARCHAR(255),
    modelo_ia VARCHAR(100),
    arquivo_origem TEXT,
    tamanho_arquivo_bytes BIGINT,
    
    -- CONTROLE
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

---

## 🔍 FASE 3: ANÁLISE DETALHADA DE PADRÕES

### 📊 Framework de Análise de Conteúdo

#### 3.1 Estrutura de Roteiros
```
ELEMENTOS OBRIGATÓRIOS:
✅ Hook/Abertura (primeiros 3-5 segundos)
✅ Desenvolvimento (corpo principal)
✅ Clímax/Ponto alto (momento de maior impacto)
✅ Resolução/Conclusão (fechamento)
✅ Call-to-Action (direcionamento final)

PADRÕES IDENTIFICADOS:
- Estrutura linear vs não-linear
- Uso de storytelling
- Técnicas de suspense
- Elementos de surpresa
- Repetição estratégica
- Ritmo e timing
- Transições entre seções
```

#### 3.2 Análise de Hooks
```
TIPOS DE ABERTURA:
✅ Controvérsia/Polêmica
✅ Pergunta direta
✅ Estatística impactante
✅ História pessoal
✅ Problema comum
✅ Promessa de benefício
✅ Curiosidade/Mistério
✅ Urgência/Escassez

EFETIVIDADE MEDIDA POR:
- Taxa de retenção nos primeiros 5 segundos
- Comentários gerados
- Compartilhamentos
- Saves/Salvamentos
- Visualizações completas
```

#### 3.3 Elementos de Persuasão
```
TÉCNICAS DOCUMENTADAS:
✅ Autoridade (credenciais, experiência)
✅ Social Proof (depoimentos, números)
✅ Escassez (limitação temporal/quantidade)
✅ Reciprocidade (valor gratuito primeiro)
✅ Consistência (compromisso público)
✅ Simpatia (conexão pessoal)
✅ Consenso (prova social)
✅ Contraste (antes vs depois)
```

---

## 📊 FASE 4: CATEGORIZAÇÃO E TAXONOMIA

### 🎭 Classificação por Tipo de Conteúdo

#### 4.1 Categorias Principais
```
EDUCATIVO-CIENTÍFICO:
- Estudos e pesquisas
- Dados e estatísticas
- Explicações técnicas
- Desmistificação de mitos
- Tendências e inovações

PROTOCOLO-PRÓPRIO:
- Metodologias exclusivas
- Sistemas proprietários
- Processos únicos
- Frameworks pessoais
- Técnicas diferenciadas

SOCIAL PROOF:
- Depoimentos de clientes
- Casos de sucesso
- Transformações reais
- Resultados mensuráveis
- Histórias inspiradoras

COMERCIAL-TRANSPARENTE:
- Parcerias declaradas
- Produtos recomendados
- Ofertas especiais
- Cupons e descontos
- Calls comerciais honestos
```

#### 4.2 Análise de Performance por Categoria
```
MÉTRICAS POR TIPO:
✅ Visualizações médias
✅ Taxa de engajamento
✅ Comentários por visualização
✅ Compartilhamentos
✅ Saves/Salvamentos
✅ Alcance orgânico
✅ Crescimento de seguidores
✅ Conversão para ação
```

---

## 🎯 FASE 5: IDENTIFICAÇÃO DE PADRÕES UNIVERSAIS

### 📊 Framework de Análise Comparativa

#### 5.1 Padrões Estruturais
```
ESTRUTURA UNIVERSAL IDENTIFICADA:
1. Hook Impactante (3-5 segundos)
2. Desenvolvimento com Autoridade (20-40 segundos)
3. Aplicação Prática (10-20 segundos)
4. Filosofia/Inspiração (5-10 segundos)
5. Call-to-Action Consistente (3-5 segundos)

VARIAÇÕES POR NICHO:
- Científico: Mais dados e estudos
- Lifestyle: Mais storytelling pessoal
- Business: Mais casos práticos
- Saúde: Mais autoridade médica
- Educação: Mais didática estruturada
```

#### 5.2 Elementos de Viralização
```
FATORES CRÍTICOS:
✅ Timing perfeito (momento certo)
✅ Relevância cultural (trending topics)
✅ Emoção forte (raiva, alegria, surpresa)
✅ Valor prático (aplicabilidade imediata)
✅ Controvérsia controlada (debate saudável)
✅ Simplicidade (fácil de entender)
✅ Shareability (fácil de compartilhar)
✅ Memorabilidade (fácil de lembrar)
```

#### 5.3 Monetização Ética
```
ESTRATÉGIAS IDENTIFICADAS:
✅ Transparência total sobre parcerias
✅ Valor antes de venda
✅ Produtos alinhados com conteúdo
✅ Cupons personalizados
✅ Recomendações genuínas
✅ Disclosure claro
✅ Benefício mútuo
✅ Confiança como prioridade
```

---

## 📊 FASE 6: ANÁLISE CONSOLIDADA

### 🎯 Relatório de Padrões por Influenciador

#### 6.1 Perfil do Influenciador
```
DADOS OBRIGATÓRIOS:
✅ Nome e handle
✅ Nicho principal
✅ Número de seguidores
✅ Taxa de engajamento média
✅ Frequência de postagem
✅ Principais temas abordados
✅ Estratégia de monetização
✅ Diferencial competitivo único
```

#### 6.2 Análise de Conteúdo
```
PADRÕES IDENTIFICADOS:
✅ Estrutura de roteiro predominante
✅ Tipos de hook mais utilizados
✅ Elementos de persuasão recorrentes
✅ Tom de voz característico
✅ Linguagem e vocabulário
✅ Técnicas de engajamento
✅ Call-to-actions padrão
✅ Fatores de viralização
```

#### 6.3 Aplicabilidade e Adaptação
```
REPLICABILIDADE:
✅ Elementos facilmente adaptáveis
✅ Recursos necessários
✅ Conhecimento técnico requerido
✅ Investimento em produção
✅ Tempo de implementação
✅ Risco de saturação
✅ Potencial de diferenciação
✅ ROI esperado
```

---

## ✅ CHECKLIST DE QUALIDADE

### 📋 Verificação Obrigatória:

#### Seleção de Influenciadores:
- [ ] 3-5 influenciadores de referência identificados
- [ ] Critérios de performance validados
- [ ] Compatibilidade estratégica confirmada
- [ ] Diversidade de abordagens garantida

#### Análise de Conteúdo:
- [ ] 10+ vídeos por influenciador analisados
- [ ] Padrões estruturais identificados
- [ ] Elementos de viralização documentados
- [ ] Estratégias de monetização mapeadas

#### Estruturação de Dados:
- [ ] Tabelas Supabase criadas para cada modelo
- [ ] Dados inseridos e organizados
- [ ] Análises consolidadas documentadas
- [ ] Padrões universais identificados

---

## 🚀 OUTPUTS ESPERADOS

### 📊 Entregáveis Obrigatórios:

1. **Biblioteca de Modelos**: 3-5 influenciadores com 10+ vídeos cada
2. **Análise de Padrões**: Estruturas e estratégias identificadas
3. **Framework de Replicação**: Guia de adaptação
4. **Relatório Consolidado**: Insights estratégicos
5. **Base de Dados Estruturada**: Tabelas Supabase organizadas

### 🎯 Critérios de Sucesso:
- **Diversidade**: Múltiplos estilos e abordagens
- **Qualidade**: Influenciadores de performance comprovada
- **Aplicabilidade**: Padrões facilmente adaptáveis
- **Profundidade**: Análises detalhadas e específicas
- **Tempo**: Processo completo em 90-120 minutos

---

## 🔄 PRÓXIMOS PASSOS

### ➡️ Preparação para Etapa 4:
1. **Modelos de referência** prontos para adaptação
2. **Padrões identificados** para aplicação
3. **Estruturas validadas** para replicação
4. **Estratégias documentadas** para implementação

### 🎯 Conexão com Workflow:
- **Etapa 4**: Criação de roteiros baseados nos modelos
- **Etapa 5**: Validação usando benchmarks dos modelos
- **Etapa 6**: Monitoramento comparativo com referências

---

**📅 Versão**: 2.0  
**🎯 Programa**: MENTOR DE LÍDERES  
**🔄 Status**: Etapa 3 de 7 do Workflow Completo  
**⏱️ Tempo Estimado**: 90-120 minutos  
**🎯 Próxima Etapa**: Escrita de Roteiros Inspirados
