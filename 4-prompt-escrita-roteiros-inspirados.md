# ✍️ ETAPA 4: ESCRITA DE ROTEIROS INSPIRADOS - MENTOR DE LÍDERES

## 🎯 OBJETIVO
Criar roteiros de conteúdo de alta performance adaptando os padrões de sucesso identificados nos modelos de referência para o perfil específico do usuário, mantendo autenticidade enquanto aplica estruturas comprovadamente eficazes para maximizar engajamento e conversão.

---

## 📊 FERRAMENTAS NECESSÁRIAS

### 🔧 MCPs Principais:
- `execute_sql_supabase` - Consulta de modelos e criação de conteúdos
- `create_entities_servermemory` - Armazenamento de padrões adaptados
- `sequentialthinking` - Planejamento estratégico de conteúdos
- `web-search` - Validação de informações científicas/técnicas
- `imageFetch_fetch` - Pesquisa de referências adicionais

---

## 🗂️ FASE 1: PLANEJAMENTO ESTRATÉGICO

### 🎯 Análise de Compatibilidade

#### 1.1 Mapeamento Perfil vs Modelos
```
ANÁLISE OBRIGATÓRIA:
✅ Tom de voz do usuário vs influenciador de referência
✅ Público-alvo: sobreposição e adaptações necessárias
✅ Nicho: transferibilidade de conceitos
✅ Recursos disponíveis vs recursos necessários
✅ Nível de expertise: adaptação de complexidade
✅ Objetivos comerciais: alinhamento estratégico
✅ Valores e posicionamento: compatibilidade ética
✅ Formato preferido: adequação ao canal

MATRIZ DE COMPATIBILIDADE:
- Alta (90-100%): Replicação direta possível
- Média (70-89%): Adaptação moderada necessária
- Baixa (50-69%): Adaptação significativa requerida
- Incompatível (<50%): Buscar outros modelos
```

#### 1.2 Seleção de Padrões Aplicáveis
```
CRITÉRIOS DE SELEÇÃO:
✅ Efetividade comprovada (métricas altas)
✅ Replicabilidade (recursos disponíveis)
✅ Autenticidade (alinhamento com personalidade)
✅ Diferenciação (oportunidade de destaque)
✅ Escalabilidade (sustentabilidade a longo prazo)
✅ Compliance (adequação legal/ética)
✅ Timing (relevância atual)
✅ ROI potencial (retorno esperado)
```

---

## 🗄️ FASE 2: ESTRUTURAÇÃO DE CONTEÚDOS

### 📊 Tabela de Conteúdos: `[nome_usuario]_conteudos`

```sql
CREATE TABLE IF NOT EXISTS [nome_usuario]_conteudos (
    id SERIAL PRIMARY KEY,
    
    -- IDENTIFICAÇÃO DO CONTEÚDO
    numero_conteudo INTEGER,
    titulo VARCHAR(255),
    tema_principal VARCHAR(255),
    subtema VARCHAR(255),
    
    -- BASEADO NOS PADRÕES DE REFERÊNCIA
    padrao_base VARCHAR(255),
    influenciador_referencia VARCHAR(255),
    estrutura_adaptada TEXT,
    
    -- CONTEÚDO COMPLETO
    roteiro_completo TEXT,
    hook_abertura TEXT,
    desenvolvimento TEXT,
    aplicacao_pratica TEXT,
    filosofia_marca TEXT,
    call_to_action TEXT,
    
    -- ANÁLISE DO CONTEÚDO
    duracao_estimada_segundos INTEGER,
    palavras_totais INTEGER,
    nivel_tecnico VARCHAR(50),
    nivel_controversia VARCHAR(50),
    
    -- ELEMENTOS PERSUASIVOS
    autoridade_utilizada TEXT,
    estudos_citados TEXT,
    casos_praticos TEXT,
    dados_especificos TEXT,
    
    -- TOM DE VOZ E LINGUAGEM
    tom_de_voz VARCHAR(100),
    linguagem_utilizada VARCHAR(100),
    emocoes_evocadas TEXT,
    publico_alvo_especifico TEXT,
    
    -- ESTRATÉGIA DE ENGAJAMENTO
    tipo_hook VARCHAR(100),
    elementos_viralizacao TEXT,
    expectativa_performance VARCHAR(50),
    palavra_chave_cta VARCHAR(50),
    
    -- DIFERENCIAÇÃO ESPECÍFICA
    diferencial_nicho BOOLEAN DEFAULT FALSE,
    tecnologias_mencionadas TEXT,
    protocolo_proprio BOOLEAN DEFAULT FALSE,
    abordagem_integrativa BOOLEAN DEFAULT FALSE,
    
    -- METADADOS
    baseado_em_shortcode VARCHAR(50),
    criado_para_programa VARCHAR(100) DEFAULT 'MENTOR DE LÍDERES',
    status_conteudo VARCHAR(50) DEFAULT 'criado',
    
    -- CONTROLE
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

---

## 🎬 FASE 3: PROCESSO DE ADAPTAÇÃO

### 📊 Framework de Adaptação Estrutural

#### 3.1 Adaptação de Hooks
```
PROCESSO OBRIGATÓRIO:
✅ Identificar hook original do modelo
✅ Extrair elemento central de impacto
✅ Adaptar para nicho específico do usuário
✅ Manter intensidade emocional
✅ Ajustar linguagem ao público-alvo
✅ Validar relevância cultural/temporal
✅ Testar compreensibilidade
✅ Garantir autenticidade

EXEMPLO DE ADAPTAÇÃO:
Original (Rafael Gratta): "Se você toma creatina e liga pra queda de cabelo..."
Adaptado (Dermatologista): "Se você usa protetor solar todo dia e se preocupa com vitamina D..."

ELEMENTOS MANTIDOS:
- Estrutura condicional "Se você..."
- Controvérsia científica
- Preocupação comum do público
- Promessa de esclarecimento
```

#### 3.2 Desenvolvimento de Conteúdo
```
ESTRUTURA UNIVERSAL ADAPTADA:
1. HOOK ESPECÍFICO (3-5 segundos)
   - Adaptado ao nicho
   - Mantém impacto emocional
   - Relevante para público-alvo

2. DESENVOLVIMENTO COM AUTORIDADE (30-50 segundos)
   - Estudos/casos do nicho específico
   - Linguagem técnica adaptada
   - Credenciais relevantes
   - Dados específicos do setor

3. APLICAÇÃO PRÁTICA (10-20 segundos)
   - Soluções específicas do usuário
   - Processos/protocolos próprios
   - Tecnologias disponíveis
   - Metodologias exclusivas

4. FILOSOFIA/MARCA (5-10 segundos)
   - Valores do usuário
   - Posicionamento único
   - Missão pessoal/profissional
   - Diferencial competitivo

5. CALL-TO-ACTION CONSISTENTE (3-5 segundos)
   - Específico para estratégia do usuário
   - Consistente entre conteúdos
   - Mensurável e rastreável
   - Alinhado com objetivos comerciais
```

#### 3.3 Personalização de Tom de Voz
```
HIBRIDIZAÇÃO ESTRATÉGICA:
✅ Tom base do modelo de referência
✅ Personalidade autêntica do usuário
✅ Expectativas do público-alvo
✅ Contexto cultural/regional
✅ Nível de formalidade adequado
✅ Elementos emocionais específicos
✅ Linguagem técnica do nicho
✅ Diferenciação competitiva

EXEMPLO DE HIBRIDIZAÇÃO:
Base (Científico-Professoral) + Usuário (Maternal-Acolhedor) = Científico-Maternal
- Mantém autoridade científica
- Adiciona acolhimento e cuidado
- Preserva credibilidade técnica
- Humaniza a comunicação
```

---

## 🎯 FASE 4: CRIAÇÃO DE MÚLTIPLOS CONTEÚDOS

### 📊 Estratégia de Diversificação

#### 4.1 Categorização por Objetivo
```
CONTEÚDOS EDUCATIVOS (40%):
- Desmistificação de mitos
- Explicação de processos
- Apresentação de estudos
- Tendências e inovações
- Comparações técnicas

CONTEÚDOS DE AUTORIDADE (30%):
- Protocolos próprios
- Metodologias exclusivas
- Casos de sucesso
- Experiência profissional
- Certificações e formações

CONTEÚDOS COMERCIAIS (20%):
- Apresentação de serviços
- Parcerias transparentes
- Ofertas especiais
- Depoimentos de clientes
- Calls comerciais éticos

CONTEÚDOS INSPIRACIONAIS (10%):
- Histórias pessoais
- Filosofia de trabalho
- Valores e missão
- Transformações pessoais
- Visão de futuro
```

#### 4.2 Planejamento de Série
```
ESTRUTURA RECOMENDADA (10 CONTEÚDOS):
1. Conteúdo Polêmico/Viral (maior alcance)
2. Protocolo/Metodologia Própria (diferenciação)
3. Educativo Científico (autoridade)
4. Nicho Específico (especialização)
5. Desmistificação (valor educativo)
6. Protocolo Avançado (expertise)
7. Fundamentos (acessibilidade)
8. Casos Reais (social proof)
9. Abordagem Integrativa (holística)
10. Conceito Inovador (thought leadership)
```

---

## 📊 FASE 5: OTIMIZAÇÃO E REFINAMENTO

### 🎯 Checklist de Qualidade por Roteiro

#### 5.1 Estrutura e Fluxo
```
VERIFICAÇÕES OBRIGATÓRIAS:
✅ Hook impactante nos primeiros 3 segundos
✅ Transições fluidas entre seções
✅ Ritmo adequado (não muito rápido/lento)
✅ Clímax bem posicionado (meio/final)
✅ Resolução satisfatória
✅ CTA claro e específico
✅ Duração otimizada (45-90 segundos)
✅ Linguagem consistente
```

#### 5.2 Conteúdo e Valor
```
CRITÉRIOS DE APROVAÇÃO:
✅ Informação nova ou perspectiva única
✅ Valor prático imediato
✅ Autoridade científica/técnica
✅ Relevância para público-alvo
✅ Diferenciação da concorrência
✅ Alinhamento com marca pessoal
✅ Potencial de viralização
✅ Oportunidade de conversão
```

#### 5.3 Autenticidade e Ética
```
VALIDAÇÕES ÉTICAS:
✅ Informações factualmente corretas
✅ Fontes confiáveis citadas
✅ Transparência sobre limitações
✅ Disclosure de parcerias/interesses
✅ Respeito ao público-alvo
✅ Conformidade legal/regulatória
✅ Alinhamento com valores pessoais
✅ Sustentabilidade a longo prazo
```

---

## 📊 FASE 6: DOCUMENTAÇÃO E ANÁLISE

### 🎯 Relatório de Criação

#### 6.1 Análise Comparativa
```
DOCUMENTAÇÃO OBRIGATÓRIA:
✅ Modelo original vs versão adaptada
✅ Elementos mantidos e modificados
✅ Justificativas para adaptações
✅ Expectativas de performance
✅ Recursos necessários para produção
✅ Cronograma de implementação
✅ Métricas de acompanhamento
✅ Planos de otimização
```

#### 6.2 Previsão de Performance
```
ESTIMATIVAS BASEADAS EM:
✅ Performance do modelo original
✅ Tamanho da audiência atual
✅ Engajamento histórico
✅ Relevância do tema
✅ Timing de publicação
✅ Qualidade da adaptação
✅ Recursos de produção
✅ Estratégia de distribuição

CATEGORIAS DE EXPECTATIVA:
- Viral (100k+ visualizações)
- Alto (50k-100k visualizações)
- Médio (20k-50k visualizações)
- Baixo (5k-20k visualizações)
```

---

## ✅ CHECKLIST DE QUALIDADE

### 📋 Verificação Obrigatória:

#### Planejamento:
- [ ] Análise de compatibilidade realizada
- [ ] Padrões aplicáveis selecionados
- [ ] Estratégia de diversificação definida
- [ ] Cronograma de criação estabelecido

#### Criação:
- [ ] 10+ roteiros completos criados
- [ ] Estrutura universal aplicada
- [ ] Tom de voz hibridizado
- [ ] Autenticidade preservada

#### Qualidade:
- [ ] Todos os roteiros validados
- [ ] Informações verificadas
- [ ] Ética e compliance confirmados
- [ ] Performance estimada

---

## 🚀 OUTPUTS ESPERADOS

### 📊 Entregáveis Obrigatórios:

1. **10+ Roteiros Completos**: Prontos para produção
2. **Tabela Estruturada**: Base de dados organizada
3. **Análise Comparativa**: Modelos vs adaptações
4. **Previsão de Performance**: Expectativas fundamentadas
5. **Cronograma de Implementação**: Plano de execução

### 🎯 Critérios de Sucesso:
- **Qualidade**: Roteiros profissionais e detalhados
- **Diversidade**: Múltiplos tipos e objetivos
- **Autenticidade**: Alinhamento com marca pessoal
- **Viabilidade**: Recursos disponíveis adequados
- **Tempo**: Processo completo em 120-180 minutos

---

## 🔄 PRÓXIMOS PASSOS

### ➡️ Preparação para Etapa 5:
1. **Roteiros finalizados** prontos para validação
2. **Cronograma definido** para implementação
3. **Métricas estabelecidas** para acompanhamento
4. **Recursos mapeados** para produção

### 🎯 Conexão com Workflow:
- **Etapa 5**: Validação e teste dos roteiros criados
- **Etapa 6**: Monitoramento de performance pós-publicação
- **Etapa 7**: Otimização baseada em resultados reais

---

**📅 Versão**: 2.0  
**🎯 Programa**: MENTOR DE LÍDERES  
**🔄 Status**: Etapa 4 de 7 do Workflow Completo  
**⏱️ Tempo Estimado**: 120-180 minutos  
**🎯 Próxima Etapa**: Validação e Teste de Conteúdos
