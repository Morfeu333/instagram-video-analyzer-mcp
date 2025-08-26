# 📋 INSTRUÇÕES PARA ANÁLISE COMPLETA DE PERFIL DE USUÁRIO

## 🎯 OBJETIVO
Criar um perfil completo e detalhado de um usuário do programa MENTOR DE LÍDERES, consolidando informações de múltiplas fontes (Google Sheets, PDFs, redes sociais) em uma tabela abrangente no Supabase.

---

## 📊 PASSO 1: EXTRAÇÃO DE DADOS DO GOOGLE SHEETS

### 🔧 Ferramentas Necessárias:
- `googledrivesheets` MCP
- `imageFetch_fetch` MCP  
- `browser_navigate_Playwright` MCP

### 📝 Procedimento:

#### 1.1 Acesso às Planilhas
```
Usar googledrivesheets MCP para acessar as 4 planilhas principais:
- Google_Sheets_googledrivesheets (INFLUENCIADOR DIGITAL)
- Google_Sheets1_googledrivesheets (MENTOR LIVRO) 
- Google_Sheets2_googledrivesheets (MENTORIA)
- Google_Sheets3_googledrivesheets (PALESTRAS)
```

#### 1.2 Busca do Usuário
```
Para cada planilha:
1. Extrair todos os dados usando o MCP
2. Buscar pelo nome completo do usuário
3. Identificar a linha/row onde o usuário está localizado
4. Anotar em qual planilha o usuário foi encontrado
```

#### 1.3 Verificação com Playwright (se necessário)
```
Se o usuário não for encontrado via MCP:
1. Usar browser_navigate_Playwright para acessar a planilha
2. Usar Ctrl+F para buscar o nome do usuário
3. Navegar pelas células para extrair informações específicas
4. Anotar links e dados das colunas B e C especificamente
```

---

## 📤 PASSO 2: TRANSFERÊNCIA PARA SUPABASE

### 🔧 Ferramentas Necessárias:
- `execute_sql_supabase`

### 📝 Procedimento:

#### 2.1 Verificação de Tabelas Existentes
```sql
-- Verificar se o usuário já existe nas 4 tabelas principais
SELECT * FROM influenciador_digital WHERE nome_completo ILIKE '%NOME_USUARIO%';
SELECT * FROM mentoria WHERE nome_completo ILIKE '%NOME_USUARIO%';
SELECT * FROM palestras WHERE nome_completo ILIKE '%NOME_USUARIO%';
SELECT * FROM mentor_livro WHERE nome_completo ILIKE '%NOME_USUARIO%';
```

#### 2.2 Inserção ou Atualização de Dados
```sql
-- Para cada tabela onde o usuário foi encontrado no Google Sheets:
-- Se não existir: INSERT
-- Se existir: UPDATE

-- Exemplo para influenciador_digital:
INSERT INTO influenciador_digital (nome_completo, instagram, arquetipo, ...)
VALUES ('NOME_USUARIO', 'links_instagram', 'arquetipo_info', ...)
ON CONFLICT (nome_completo) DO UPDATE SET
instagram = EXCLUDED.instagram,
arquetipo = EXCLUDED.arquetipo;
```

---

## 🔗 PASSO 3: VERIFICAÇÃO DE LINKS E TRANSCRIÇÃO DE PDF

### 🔧 Ferramentas Necessárias:
- `browser_navigate_Playwright`
- `imageFetch_fetch`

### 📝 Procedimento:

#### 3.1 Verificação de Links do Instagram
```
1. Navegar para os links do Instagram usando Playwright
2. Verificar se os links estão ativos
3. Extrair informações básicas (seguidores, posts, bio)
4. Atualizar dados no Supabase se necessário
```

#### 3.2 Download e Análise do PDF
```
1. Acessar o link do Google Drive do PDF usando Playwright
2. Fazer download ou visualizar o PDF no browser
3. Extrair informações chave:
   - Arquétipo identificado
   - Descrição personalizada
   - Missão declarada
   - Objetivos de legado
   - Futuro desejado
   - Pontos fortes específicos
   - Desafios identificados
```

#### 3.3 Atualização com Dados do PDF
```sql
-- Atualizar tabelas com informações extraídas do PDF
UPDATE influenciador_digital 
SET arquetipo = 'INFORMAÇÕES_COMPLETAS_DO_PDF'
WHERE nome_completo = 'NOME_USUARIO';
```

---

## 🗃️ PASSO 4: CRIAÇÃO DA TABELA PERSONALIZADA

### 🔧 Ferramentas Necessárias:
- `execute_sql_supabase`

### 📝 Procedimento:

#### 4.1 Estrutura da Tabela
```sql
CREATE TABLE IF NOT EXISTS perfil_completo_[nome_usuario] (
    id SERIAL PRIMARY KEY,
    
    -- INFORMAÇÕES PESSOAIS
    nome_completo VARCHAR(255) NOT NULL,
    profissao VARCHAR(255),
    especialidade VARCHAR(255),
    tempo_atuacao VARCHAR(100),
    segmento VARCHAR(100),
    
    -- DADOS DIGITAIS (do influenciador_digital)
    instagram_principal TEXT,
    instagram_empresa TEXT,
    seguidores_instagram VARCHAR(50),
    perfil_aberto_fechado VARCHAR(20),
    frequencia_postagem TEXT,
    posicionamento_digital_0_10 INTEGER,
    linkedin TEXT,
    
    -- DADOS DE MENTORIA (do mentoria)
    nivel_estruturou_mentoria_0_10 INTEGER,
    experiencia_mentoria TEXT,
    
    -- DADOS DE PALESTRAS (do palestras)
    nivel_palestrou_0_10 INTEGER,
    experiencia_palestras TEXT,
    
    -- DADOS DE LIVRO/MENTOR (do mentor_livro)
    nivel_livro_mentor INTEGER,
    experiencia_livro TEXT,
    
    -- NÍVEL GERAL
    nivel_aluno INTEGER,
    descricao_nivel_aluno TEXT,
    
    -- ARQUÉTIPO COMPLETO
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
    
    -- ANÁLISE DO PDF
    pdf_link TEXT,
    pdf_analise_personalizada TEXT,
    pdf_missao_declarada TEXT,
    pdf_objetivos_legado TEXT,
    pdf_futuro_desejado TEXT,
    
    -- LINKS E RECURSOS
    website_principal TEXT,
    website_cirurgia_dermatologica TEXT,
    website_medicina_capilar TEXT,
    website_estetica TEXT,
    todos_links_produtos_servicos TEXT,
    
    -- TRAJETÓRIA E OBJETIVOS
    trajetoria_mercado_digital TEXT,
    objetivo_mentoria_mentor_lideres TEXT,
    
    -- DESCRIÇÃO PROFISSIONAL COMPLETA
    descricao_profissional_completa TEXT,
    
    -- ANÁLISE CONSOLIDADA
    pontos_fortes_consolidados TEXT,
    desafios_consolidados TEXT,
    oportunidades_identificadas TEXT,
    recomendacoes_estrategicas TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 📊 PASSO 5: ANÁLISE COMPLETA E INSERÇÃO DE DADOS

### 🔧 Ferramentas Necessárias:
- `execute_sql_supabase`
- `resolve-library-id_Context_7` (se necessário para pesquisa de arquétipos)

### 📝 Procedimento:

#### 5.1 Consolidação de Informações
```
Reunir dados de todas as fontes:
1. Dados das 4 tabelas do Supabase
2. Informações extraídas do PDF
3. Dados dos links verificados
4. Informações detalhadas do arquétipo da tabela arquetipos
```

#### 5.2 Análise Estratégica
```
Criar análises consolidadas:

PONTOS FORTES:
- Experiência profissional
- Níveis de desenvolvimento em cada área
- Características do arquétipo
- Presença digital
- Recursos disponíveis

DESAFIOS:
- Áreas com baixo desenvolvimento
- Desafios específicos do arquétipo
- Problemas identificados na trajetória
- Limitações atuais

OPORTUNIDADES:
- Potencial de crescimento
- Mercados não explorados
- Sinergias entre competências
- Tendências favoráveis

RECOMENDAÇÕES:
- Ações específicas por área
- Prioridades de desenvolvimento
- Estratégias de posicionamento
- Próximos passos concretos
```

#### 5.3 Inserção Final
```sql
INSERT INTO perfil_completo_[nome_usuario] (
    -- Todos os campos com dados consolidados
    nome_completo,
    profissao,
    especialidade,
    -- ... todos os outros campos
    pontos_fortes_consolidados,
    desafios_consolidados,
    oportunidades_identificadas,
    recomendacoes_estrategicas
) VALUES (
    -- Valores extraídos e analisados de todas as fontes
);
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### 📋 Antes de Finalizar:
- [ ] Usuário encontrado em pelo menos uma das 4 planilhas
- [ ] Dados transferidos para tabelas correspondentes no Supabase
- [ ] Links do Instagram verificados e funcionais
- [ ] PDF baixado e analisado completamente
- [ ] Informações do arquétipo enriquecidas com dados da tabela arquetipos
- [ ] Tabela personalizada criada com estrutura completa
- [ ] Análise estratégica realizada (SWOT)
- [ ] Recomendações específicas elaboradas
- [ ] Todos os links e recursos catalogados
- [ ] Dados consolidados inseridos na tabela final

### 🎯 Resultado Final:
Uma tabela `perfil_completo_[nome_usuario]` contendo:
- **Informações pessoais e profissionais completas**
- **Dados de todas as 4 áreas do programa (digital, mentoria, palestras, livro)**
- **Análise detalhada do arquétipo com enriquecimento**
- **Informações extraídas do PDF personalizado**
- **Links e recursos verificados**
- **Análise estratégica consolidada (pontos fortes, desafios, oportunidades)**
- **Recomendações específicas e acionáveis**

---

## 🚀 PRÓXIMOS PASSOS SUGERIDOS

1. **Monitoramento**: Configurar atualizações periódicas dos dados
2. **Dashboard**: Criar visualizações dos dados consolidados
3. **Automação**: Implementar processo automatizado para novos usuários
4. **Relatórios**: Gerar relatórios personalizados baseados na análise
5. **Integração**: Conectar com outras ferramentas do programa MENTOR DE LÍDERES

---

## 🛠️ COMANDOS E CÓDIGOS DE EXEMPLO

### 📊 Comandos MCP Essenciais:
```
# Acesso às planilhas
Google_Sheets_googledrivesheets()
Google_Sheets1_googledrivesheets()
Google_Sheets2_googledrivesheets()
Google_Sheets3_googledrivesheets()

# Navegação com Playwright
browser_navigate_Playwright(url="https://docs.google.com/spreadsheets/...")
browser_press_key_Playwright(key="Control+f")
browser_type_Playwright(text="NOME_USUARIO")

# Fetch de conteúdo
imageFetch_fetch(url="https://drive.google.com/...", enableFetchImages=true)
```

### 🗄️ Queries SQL Essenciais:
```sql
-- Busca em todas as tabelas
SELECT 'influenciador_digital' as tabela, * FROM influenciador_digital WHERE nome_completo ILIKE '%NOME%'
UNION ALL
SELECT 'mentoria' as tabela, * FROM mentoria WHERE nome_completo ILIKE '%NOME%'
UNION ALL
SELECT 'palestras' as tabela, * FROM palestras WHERE nome_completo ILIKE '%NOME%'
UNION ALL
SELECT 'mentor_livro' as tabela, * FROM mentor_livro WHERE nome_completo ILIKE '%NOME%';

-- Busca de arquétipo
SELECT * FROM arquetipos WHERE nome = 'O Criador';

-- Atualização de campo longo
ALTER TABLE perfil_completo_usuario ALTER COLUMN campo_nome TYPE TEXT;
```

---

## ⚠️ PROBLEMAS COMUNS E SOLUÇÕES

### 🔧 Troubleshooting:

#### Problema: Usuário não encontrado nas planilhas
**Solução**:
1. Verificar variações do nome (com/sem acentos, abreviações)
2. Usar Playwright para busca manual
3. Verificar se está em planilhas adicionais

#### Problema: Links do Instagram não funcionam
**Solução**:
1. Verificar se o perfil é público/privado
2. Testar links alternativos
3. Documentar status dos links

#### Problema: PDF não acessível
**Solução**:
1. Verificar permissões do Google Drive
2. Tentar acesso via browser autenticado
3. Solicitar novo link se necessário

#### Problema: Campo muito longo para VARCHAR
**Solução**:
```sql
ALTER TABLE tabela ALTER COLUMN campo TYPE TEXT;
```

#### Problema: Dados duplicados
**Solução**:
```sql
-- Usar UPSERT
INSERT INTO tabela (...) VALUES (...)
ON CONFLICT (nome_completo) DO UPDATE SET campo = EXCLUDED.campo;
```

---

## 📈 MÉTRICAS DE QUALIDADE

### ✅ Indicadores de Sucesso:
- **Completude**: 90%+ dos campos preenchidos
- **Precisão**: Links funcionais e dados verificados
- **Consistência**: Dados alinhados entre todas as tabelas
- **Análise**: Recomendações específicas e acionáveis
- **Tempo**: Processo completo em menos de 30 minutos

### 📊 KPIs por Etapa:
1. **Extração**: 4/4 planilhas verificadas
2. **Transferência**: 100% dos dados encontrados transferidos
3. **Verificação**: Links testados e funcionais
4. **Análise**: SWOT completa realizada
5. **Consolidação**: Tabela final criada com sucesso

---

## 🔄 PROCESSO DE ATUALIZAÇÃO

### 📅 Manutenção Periódica:
1. **Semanal**: Verificar links e atualizações nas redes sociais
2. **Mensal**: Revisar dados das planilhas Google Sheets
3. **Trimestral**: Atualizar análise estratégica e recomendações
4. **Anual**: Revisão completa do perfil e arquétipo

### 🔄 Versionamento:
```sql
-- Adicionar campo de versão
ALTER TABLE perfil_completo_usuario ADD COLUMN versao INTEGER DEFAULT 1;
ALTER TABLE perfil_completo_usuario ADD COLUMN data_ultima_atualizacao TIMESTAMP DEFAULT NOW();

-- Histórico de mudanças
CREATE TABLE historico_perfil (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    campo_alterado VARCHAR(100),
    valor_anterior TEXT,
    valor_novo TEXT,
    data_alteracao TIMESTAMP DEFAULT NOW()
);
```

---

## 📚 REFERÊNCIAS E RECURSOS

### 🔗 Links Úteis:
- [Documentação Supabase](https://supabase.com/docs)
- [Playwright Documentation](https://playwright.dev/)
- [Teoria dos 12 Arquétipos](https://example.com/arquetipos)
- [Google Sheets API](https://developers.google.com/sheets/api)

### 📖 Materiais de Apoio:
- Guia de Arquétipos de Marca
- Manual do Programa MENTOR DE LÍDERES
- Templates de Análise SWOT
- Checklist de Verificação de Dados

---

*Documento criado para padronizar o processo de análise completa de perfil de usuários do programa MENTOR DE LÍDERES.*

**Versão**: 1.0
**Data**: 2025-08-06
**Autor**: Sistema de Análise MENTOR DE LÍDERES
**Última Atualização**: Processo NATHALIA MATOS GOMES
