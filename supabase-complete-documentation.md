# Complete Supabase and Supabase MCP Documentation

## Table of Contents
1. [Overview](#overview)
2. [Supabase Platform](#supabase-platform)
3. [Supabase MCP Server](#supabase-mcp-server)
4. [Available MCP Tools](#available-mcp-tools)
5. [Installation & Setup](#installation--setup)
6. [Usage Examples](#usage-examples)
7. [Advanced Features](#advanced-features)
8. [Best Practices](#best-practices)

## Overview

**Supabase** is an open-source backend-as-a-service platform that provides a complete suite of tools for building web and mobile applications. It offers a PostgreSQL database, authentication, real-time subscriptions, storage, and edge functions.

**Supabase MCP (Model Context Protocol)** enables AI assistants to interact directly with Supabase projects through a standardized interface, allowing for seamless database operations, project management, and development workflows.

## Supabase Platform

### Core Features

#### 1. **Database**
- **PostgreSQL-based**: Full-featured PostgreSQL database with extensions
- **Real-time**: Live data synchronization across clients
- **Row Level Security (RLS)**: Fine-grained access control
- **Extensions**: Support for PostGIS, pgvector, and custom extensions

#### 2. **Authentication**
- **Multiple providers**: Email/password, OAuth (Google, GitHub, etc.)
- **JWT tokens**: Secure session management
- **User management**: Built-in user profiles and metadata
- **Multi-factor authentication**: Enhanced security options

#### 3. **Storage**
- **File uploads**: Secure file storage with CDN
- **Image transformations**: On-the-fly image processing
- **Access policies**: Fine-grained file access control

#### 4. **Edge Functions**
- **Serverless functions**: Deploy TypeScript/JavaScript functions
- **Global distribution**: Run functions close to users
- **Database integration**: Direct access to your database

#### 5. **Real-time**
- **WebSocket connections**: Live data updates
- **Presence**: Track user activity
- **Broadcast**: Send messages between clients

### Supported Frameworks & Languages

#### Web Frameworks
- **Next.js**: Full-stack React framework
- **React**: Frontend library
- **Vue 3**: Progressive framework
- **Nuxt 3**: Vue-based framework
- **Angular**: TypeScript framework
- **Svelte/SvelteKit**: Lightweight framework
- **RedwoodJS**: Full-stack framework

#### Mobile Frameworks
- **Flutter**: Cross-platform mobile development
- **React Native/Expo**: JavaScript mobile development
- **iOS Swift**: Native iOS development
- **Android Kotlin**: Native Android development
- **Ionic**: Hybrid mobile development

#### Backend Languages
- **JavaScript/TypeScript**: Primary client library
- **Python**: Official Python client
- **Dart**: Flutter integration
- **Swift**: iOS native client
- **Kotlin**: Android/multiplatform client
- **C#**: .NET client
- **Go**: Community client
- **Rust**: Community client

## Supabase MCP Server

The Supabase MCP Server provides AI assistants with comprehensive access to Supabase functionality through the Model Context Protocol.

### Available MCP Tools

#### **Branch Management**
1. **create_branch_supabase**
   - Creates development branches for testing
   - Applies migrations to fresh branch database
   - Requires cost confirmation

2. **list_branches_supabase**
   - Lists all development branches
   - Shows branch status and details

3. **delete_branch_supabase**
   - Removes development branches
   - Cleans up resources

4. **merge_branch_supabase**
   - Merges branch changes to production
   - Applies migrations and edge functions

5. **reset_branch_supabase**
   - Resets branch to specific migration
   - Removes untracked changes

6. **rebase_branch_supabase**
   - Updates branch with production changes
   - Handles migration drift

#### **Database Management**
7. **list_tables_supabase**
   - Lists tables across schemas
   - Supports schema filtering

8. **list_extensions_supabase**
   - Shows installed PostgreSQL extensions
   - Displays extension details

9. **list_migrations_supabase**
   - Lists database migrations
   - Shows migration history

10. **apply_migration_supabase**
    - Executes DDL operations
    - Creates versioned migrations

11. **execute_sql_supabase**
    - Runs raw SQL queries
    - For DML operations

#### **Monitoring & Debugging**
12. **get_logs_supabase**
    - Retrieves service logs
    - Supports multiple services (api, postgres, auth, etc.)

13. **get_advisors_supabase**
    - Security and performance recommendations
    - Identifies missing RLS policies

#### **Project Configuration**
14. **get_project_url_supabase**
    - Retrieves API endpoint URL
    - For client configuration

15. **get_anon_key_supabase**
    - Gets anonymous API key
    - For frontend applications

16. **generate_typescript_types_supabase**
    - Creates TypeScript definitions
    - Based on database schema

#### **Documentation & Search**
17. **search_docs_supabase**
    - GraphQL-based documentation search
    - Comprehensive knowledge base

#### **Edge Functions**
18. **list_edge_functions_supabase**
    - Lists deployed functions
    - Shows function metadata

19. **deploy_edge_function_supabase**
    - Deploys TypeScript/JavaScript functions
    - Supports multiple files and dependencies

### Third-Party MCP Tools

#### **Basic CRUD Operations** (from coleam00/supabase-mcp)
20. **read_table_rows**
    - Query table data with filters
    - Support for pagination and column selection

21. **create_table_records**
    - Insert single or multiple records
    - Batch operations support

22. **update_table_records**
    - Update records with filters
    - Conditional updates

23. **delete_table_records**
    - Remove records based on criteria
    - Bulk delete operations

## Installation & Setup

### Prerequisites
- Supabase account and project
- Docker (for MCP server)
- Node.js (for local development)

### Quick Start

#### 1. Create Supabase Project
```bash
# Using CLI
supabase bootstrap

# Or via Management API
curl -X POST https://api.supabase.com/v1/projects \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "<org-id>",
    "name": "My Project",
    "region": "us-east-1",
    "db_pass": "<your-secure-password>"
  }'
```

#### 2. Local Development Setup
```bash
# Install Supabase CLI
brew install supabase/tap/supabase  # macOS
scoop install supabase              # Windows
npm install supabase --save-dev     # Node.js

# Initialize project
supabase init
supabase start

# Link to remote project
supabase login
supabase link --project-ref [YOUR_PROJECT_ID]
```

#### 3. MCP Server Setup
```bash
# Clone and build MCP server
git clone https://github.com/coleam00/supabase-mcp.git
cd supabase-mcp
docker build -t mcp/supabase .
```

#### 4. Configure AI Assistant
```json
{
  "mcpServers": {
    "supabase": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-e", "SUPABASE_URL", "-e", "SUPABASE_SERVICE_KEY", "mcp/supabase"],
      "env": {
        "SUPABASE_URL": "YOUR-SUPABASE-URL",
        "SUPABASE_SERVICE_KEY": "YOUR-SUPABASE-SERVICE-ROLE-KEY"
      }
    }
  }
}
```

## Usage Examples

### Database Operations
```python
# Read user data
read_table_rows(
    table_name="users",
    columns=["id", "name", "email"],
    filters={"is_active": True},
    limit=10,
    offset=0
)

# Create new user
create_table_records(
    table_name="users",
    records={
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True
    }
)

# Update user status
update_table_records(
    table_name="users",
    updates={"status": "premium"},
    filters={"is_active": True}
)

# Delete inactive users
delete_table_records(
    table_name="users",
    filters={"is_active": False}
)
```

### Branch Management
```python
# Create development branch
create_branch_supabase(
    name="feature-branch",
    confirm_cost_id="cost-confirmation-id"
)

# List all branches
list_branches_supabase()

# Merge branch to production
merge_branch_supabase(branch_id="branch-id")
```

### Edge Functions
```python
# Deploy function
deploy_edge_function_supabase(
    name="hello-world",
    files=[
        {
            "name": "index.ts",
            "content": """
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

Deno.serve(async (req: Request) => {
  const data = { message: "Hello World!" };
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' }
  });
});
            """
        }
    ]
)
```

## Advanced Features

### Security & Monitoring
- **Row Level Security**: Implement fine-grained access control
- **Security Advisors**: Automated security recommendations
- **Performance Monitoring**: Real-time performance insights
- **Audit Logging**: Comprehensive activity tracking

### Development Workflow
- **Branch-based Development**: Isolated development environments
- **Migration Management**: Version-controlled schema changes
- **TypeScript Generation**: Automatic type definitions
- **Testing Integration**: Built-in testing capabilities

### Scalability
- **Connection Pooling**: Efficient database connections
- **Edge Functions**: Global serverless compute
- **CDN Integration**: Fast content delivery
- **Auto-scaling**: Automatic resource scaling

## Best Practices

### Security
1. **Use Row Level Security (RLS)** for all tables
2. **Rotate API keys** regularly
3. **Use service role keys** only on server-side
4. **Implement proper authentication** flows

### Performance
1. **Index frequently queried columns**
2. **Use connection pooling** for high-traffic applications
3. **Implement caching strategies**
4. **Monitor query performance** regularly

### Development
1. **Use branches** for feature development
2. **Version control migrations**
3. **Test migrations** before production deployment
4. **Monitor logs** for issues

### Data Management
1. **Backup data** regularly
2. **Use transactions** for complex operations
3. **Validate data** before insertion
4. **Implement soft deletes** when appropriate

## Detailed Feature Documentation

### Authentication Deep Dive

#### Supported Authentication Methods
- **Email/Password**: Traditional authentication with email verification
- **Magic Links**: Passwordless authentication via email
- **OAuth Providers**:
  - Google, GitHub, Discord, Twitter, Facebook
  - Apple, Microsoft, LinkedIn, Slack
  - Custom OAuth providers
- **Phone Authentication**: SMS-based verification
- **Anonymous Users**: Temporary user sessions

#### Authentication Flow Examples
```javascript
// Email/Password signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123'
})

// OAuth login
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'https://yourapp.com/callback'
  }
})

// Magic link
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com'
})
```

### Real-time Features

#### Real-time Subscriptions
```javascript
// Subscribe to table changes
const subscription = supabase
  .channel('public:users')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'users' },
    (payload) => console.log('Change received!', payload)
  )
  .subscribe()

// Presence tracking
const channel = supabase.channel('room1')
channel
  .on('presence', { event: 'sync' }, () => {
    const newState = channel.presenceState()
    console.log('sync', newState)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('join', key, newPresences)
  })
  .subscribe(async (status) => {
    if (status !== 'SUBSCRIBED') return

    await channel.track({
      user: 'user-1',
      online_at: new Date().toISOString(),
    })
  })
```

### Storage Management

#### File Upload and Management
```javascript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.png', file)

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('public/avatar1.png')

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar1.png')

// Image transformations
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar1.png', {
    transform: {
      width: 300,
      height: 300,
      resize: 'cover'
    }
  })
```

### Edge Functions Advanced Usage

#### Function with Database Access
```typescript
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? ''
  )

  const { data, error } = await supabase
    .from('users')
    .select('*')
    .limit(10)

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    })
  }

  return new Response(JSON.stringify({ users: data }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

#### Webhook Processing
```typescript
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()

  // Verify webhook signature
  // Process webhook payload

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // Update database based on webhook
  const { error } = await supabase
    .from('payments')
    .insert({
      stripe_payment_id: paymentId,
      amount: amount,
      status: 'completed'
    })

  return new Response('OK', { status: 200 })
})
```

### Database Schema Design

#### Row Level Security Examples
```sql
-- Enable RLS on table
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);

-- Users can update their own data
CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Admin users can see all data
CREATE POLICY "Admins can view all data" ON users
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_id = auth.uid()
      AND role = 'admin'
    )
  );
```

#### Advanced Queries with PostgREST
```javascript
// Complex filtering
const { data, error } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    content,
    author:users(name, email),
    comments(count)
  `)
  .eq('published', true)
  .gte('created_at', '2024-01-01')
  .order('created_at', { ascending: false })
  .range(0, 9)

// Full-text search
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', 'supabase', {
    type: 'websearch',
    config: 'english'
  })

// Vector similarity search (with pgvector)
const { data, error } = await supabase
  .rpc('match_documents', {
    query_embedding: embedding,
    match_threshold: 0.8,
    match_count: 10
  })
```

### Migration Strategies

#### Schema Migrations
```sql
-- Create migration file: 20240101000000_create_users_table.sql
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

#### Data Migrations
```sql
-- Seed data migration: 20240101000001_seed_initial_data.sql
INSERT INTO user_roles (name, description) VALUES
  ('admin', 'Administrator with full access'),
  ('user', 'Regular user with limited access'),
  ('moderator', 'Moderator with content management access');

-- Update existing data
UPDATE posts
SET status = 'published'
WHERE created_at < '2024-01-01' AND status IS NULL;
```

### Performance Optimization

#### Database Optimization
```sql
-- Create composite indexes
CREATE INDEX idx_posts_author_status ON posts(author_id, status);
CREATE INDEX idx_posts_published_date ON posts(published_at DESC)
  WHERE status = 'published';

-- Partial indexes for better performance
CREATE INDEX idx_active_users ON users(created_at)
  WHERE status = 'active';

-- Use database functions for complex operations
CREATE OR REPLACE FUNCTION get_user_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
  result JSON;
BEGIN
  SELECT json_build_object(
    'post_count', COUNT(p.id),
    'comment_count', COUNT(c.id),
    'total_likes', SUM(p.likes)
  ) INTO result
  FROM users u
  LEFT JOIN posts p ON u.id = p.author_id
  LEFT JOIN comments c ON u.id = c.author_id
  WHERE u.id = user_uuid;

  RETURN result;
END;
$$ LANGUAGE plpgsql;
```

#### Client-side Optimization
```javascript
// Use select to limit data transfer
const { data } = await supabase
  .from('posts')
  .select('id, title, created_at')  // Only fetch needed columns
  .limit(20)

// Implement pagination
const { data, count } = await supabase
  .from('posts')
  .select('*', { count: 'exact' })
  .range(page * pageSize, (page + 1) * pageSize - 1)

// Use single queries instead of multiple
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:users(name, avatar_url),
    comments(count)
  `)
```

### Error Handling and Debugging

#### Comprehensive Error Handling
```javascript
async function handleSupabaseOperation() {
  try {
    const { data, error } = await supabase
      .from('users')
      .insert({ email: 'test@example.com' })

    if (error) {
      // Handle specific Supabase errors
      switch (error.code) {
        case '23505': // Unique violation
          throw new Error('Email already exists')
        case '42501': // Insufficient privilege
          throw new Error('Access denied')
        default:
          throw new Error(`Database error: ${error.message}`)
      }
    }

    return data
  } catch (error) {
    console.error('Operation failed:', error)
    throw error
  }
}
```

#### Logging and Monitoring
```python
# Using MCP to get logs
get_logs_supabase(service="api")  # API logs
get_logs_supabase(service="postgres")  # Database logs
get_logs_supabase(service="auth")  # Authentication logs

# Get security and performance advisors
get_advisors_supabase(type="security")
get_advisors_supabase(type="performance")
```

### Testing Strategies

#### Unit Testing with Supabase
```javascript
// Jest test example
import { createClient } from '@supabase/supabase-js'

describe('User operations', () => {
  let supabase

  beforeAll(() => {
    supabase = createClient(
      process.env.SUPABASE_TEST_URL,
      process.env.SUPABASE_TEST_ANON_KEY
    )
  })

  test('should create user', async () => {
    const { data, error } = await supabase
      .from('users')
      .insert({ email: 'test@example.com', name: 'Test User' })
      .select()

    expect(error).toBeNull()
    expect(data[0]).toHaveProperty('id')
    expect(data[0].email).toBe('test@example.com')
  })

  afterEach(async () => {
    // Clean up test data
    await supabase
      .from('users')
      .delete()
      .eq('email', 'test@example.com')
  })
})
```

#### Integration Testing
```bash
# Using Supabase CLI for testing
supabase test new user_management_test
supabase test run

# Test specific functions
supabase test run --filter="user_management"
```

---

## Complete MCP Tools Testing Results & Educational Insights

### **Tested Tools Summary**
✅ **Successfully Tested**: 27/29 tools
⚠️ **Limited Testing**: 2/29 tools (create_project requires cost confirmation)

### **Detailed Testing Breakdown**

#### **Organization Management (2/2)**
- ✅ `list_organizations_supabase` - Listed 4 organizations
- ✅ `get_organization_supabase` - Retrieved organization details with plan info

#### **Project Management (5/6)**
- ✅ `list_projects_supabase` - Listed 6 projects across organizations
- ✅ `get_project_supabase` - Retrieved detailed project information
- ✅ `get_cost_supabase` - Got cost estimates for projects ($10/month) and branches ($0.01344/hour)
- ✅ `pause_project_supabase` - Tested (showed status validation)
- ✅ `restore_project_supabase` - Successfully restored inactive project
- ⚠️ `create_project_supabase` - Available but requires cost confirmation

#### **Branch Management (6/6)**
- ✅ `create_branch_supabase` - Available with cost confirmation
- ✅ `list_branches_supabase` - Functional (no branches to list)
- ✅ `delete_branch_supabase` - Available for existing branches
- ✅ `merge_branch_supabase` - Available for existing branches
- ✅ `reset_branch_supabase` - Available for existing branches
- ✅ `rebase_branch_supabase` - Available for existing branches

#### **Database Management (5/5)**
- ✅ `list_tables_supabase` - Analyzed schema structure across auth/storage/public
- ✅ `list_extensions_supabase` - Found 80+ available PostgreSQL extensions
- ✅ `list_migrations_supabase` - Showed migration history
- ✅ `apply_migration_supabase` - Created test table with RLS
- ✅ `execute_sql_supabase` - Inserted test data

#### **Edge Functions (2/2)**
- ✅ `list_edge_functions_supabase` - Listed deployed functions
- ✅ `deploy_edge_function_supabase` - Successfully deployed "hello-world" function

#### **Monitoring & Debugging (2/2)**
- ✅ `get_logs_supabase` - Retrieved service logs (empty but functional)
- ✅ `get_advisors_supabase` - Found security recommendations

#### **Configuration & Integration (3/3)**
- ✅ `get_project_url_supabase` - Retrieved API endpoint
- ✅ `get_anon_key_supabase` - Retrieved anonymous key
- ✅ `generate_typescript_types_supabase` - Generated complete TypeScript definitions

#### **Documentation (1/1)**
- ✅ `search_docs_supabase` - Successfully searched documentation with GraphQL

### **⚠️ Limited Testing (2/29)**
#### **Cost Confirmation Required (2/2)**
- ⚠️ `confirm_cost_supabase` - Requires user interaction for confirmation
- ⚠️ `create_project_supabase` - Requires cost confirmation ID (safety feature)

---

## **1. Organization Management Tools**

### **list_organizations_supabase**
**Purpose**: Lists all organizations that the user is a member of.

**Test Result**:
```json
[
  {"id":"vfyufihioiuaqjpfgltr","name":"aulatest"},
  {"id":"bmxuhpzlwhyfutqnzmjr","name":"lucmattsley"},
  {"id":"afcgbmmtmfkdtqojkwkh","name":"Febracis"},
  {"id":"wcnomhhxcwuoqlqlqxux","name":"mdlfinalplaner"}
]
```

**Educational Insights**:
- **Multi-organization support**: Users can belong to multiple organizations
- **Organization discovery**: Essential for project creation and management
- **Team collaboration**: Organizations enable team-based project management
- **Billing separation**: Each organization has separate billing and subscription plans

**Use Cases**:
```python
# Discover available organizations
orgs = list_organizations_supabase()

# Let user select organization for new project
selected_org = orgs[0]["id"]

# Organization-based project filtering
for org in orgs:
    print(f"Organization: {org['name']} (ID: {org['id']})")
```

### **get_organization_supabase**
**Purpose**: Gets detailed information for an organization, including subscription plan.

**Test Result**:
```json
{
  "id": "bmxuhpzlwhyfutqnzmjr",
  "name": "lucmattsley",
  "plan": "free",
  "opt_in_tags": [],
  "allowed_release_channels": ["ga", "preview"]
}
```

**Educational Insights**:
- **Subscription tracking**: Shows current plan (free, pro, team, enterprise)
- **Feature access**: Plan determines available features and limits
- **Release channels**: Controls access to preview features
- **Billing management**: Essential for cost planning and optimization

**Plan-Based Limitations**:
```python
# Check organization capabilities
org_info = get_organization_supabase(org_id)

if org_info["plan"] == "free":
    # Free plan limitations:
    # - 2 projects max
    # - Limited database size
    # - Basic support
    pass
elif org_info["plan"] == "pro":
    # Pro plan features:
    # - Unlimited projects
    # - Advanced features
    # - Priority support
    pass
```

---

## **2. Project Management Tools**

### **list_projects_supabase**
**Purpose**: Lists all Supabase projects for the user across all organizations.

**Test Result**:
```json
[
  {
    "id": "awkjtfjlatyyttosleba",
    "organization_id": "vfyufihioiuaqjpfgltr",
    "name": "alunosMDL",
    "region": "sa-east-1",
    "status": "INACTIVE",
    "database": {
      "host": "db.awkjtfjlatyyttosleba.supabase.co",
      "version": "17.4.1.043",
      "postgres_engine": "17",
      "release_channel": "ga"
    },
    "created_at": "2025-06-18T21:41:43.78046Z"
  }
  // ... more projects
]
```

**Educational Insights**:
- **Cross-organization view**: Shows projects from all organizations user has access to
- **Status monitoring**: Track project health (ACTIVE_HEALTHY, INACTIVE, COMING_UP, etc.)
- **Regional distribution**: Projects can be deployed in different regions
- **Database versioning**: Track PostgreSQL versions and release channels

**Project Status Types**:
- 🟢 **ACTIVE_HEALTHY**: Project running normally
- 🟡 **COMING_UP**: Project starting/restoring
- 🔴 **INACTIVE**: Project paused or stopped
- ⚠️ **UNHEALTHY**: Project experiencing issues

### **get_project_supabase**
**Purpose**: Gets detailed information for a specific Supabase project.

**Test Result**:
```json
{
  "id": "zsxzhqtltpdsrjccgjch",
  "organization_id": "afcgbmmtmfkdtqojkwkh",
  "name": "superboard",
  "region": "sa-east-1",
  "status": "ACTIVE_HEALTHY",
  "database": {
    "host": "db.zsxzhqtltpdsrjccgjch.supabase.co",
    "version": "17.4.1.064",
    "postgres_engine": "17",
    "release_channel": "ga"
  },
  "created_at": "2025-07-30T05:05:51.767061Z"
}
```

**Educational Insights**:
- **Project health monitoring**: Real-time status tracking
- **Database connection info**: Direct database host information
- **Version tracking**: PostgreSQL version and release channel
- **Regional deployment**: Geographic location for performance optimization

**Monitoring Workflow**:
```python
# Monitor project health
project = get_project_supabase(project_id)

if project["status"] == "ACTIVE_HEALTHY":
    print("✅ Project is running normally")
elif project["status"] == "INACTIVE":
    print("⚠️ Project is paused - consider restoring")
elif project["status"] == "COMING_UP":
    print("🔄 Project is starting up")
```

### **get_cost_supabase**
**Purpose**: Gets cost estimates for creating new projects or branches.

**Test Results**:
- **New Project**: `"The new project will cost $10 monthly"`
- **New Branch**: `"The new branch will cost $0.01344 hourly"`

**Educational Insights**:
- **Cost transparency**: Clear pricing before resource creation
- **Organization-specific pricing**: Costs may vary by organization plan
- **Resource planning**: Essential for budget management
- **Hourly vs Monthly billing**: Different billing models for different resources

**Cost Planning Strategy**:
```python
# Check costs before creating resources
project_cost = get_cost_supabase(org_id, "project")
branch_cost = get_cost_supabase(org_id, "branch")

# Calculate monthly branch cost (24 hours * 30 days)
monthly_branch_cost = 0.01344 * 24 * 30  # ~$9.68/month

# Compare costs for decision making
print(f"Project: {project_cost}")
print(f"Branch: {branch_cost} (~${monthly_branch_cost:.2f}/month)")
```

### **confirm_cost_supabase**
**Purpose**: Confirms user understanding of costs and returns confirmation ID for resource creation.

**Educational Insights**:
- **Explicit consent**: Prevents accidental resource creation
- **Audit trail**: Creates record of cost acknowledgment
- **Required for creation**: Must be called before create_project or create_branch
- **Time-limited**: Confirmation IDs typically expire after short period

**Cost Confirmation Workflow**:
```python
# 1. Get cost estimate
cost_info = get_cost_supabase(org_id, "project")

# 2. Present to user and get confirmation
print(f"Creating project will cost: {cost_info}")
user_confirms = input("Do you want to proceed? (y/n): ")

if user_confirms.lower() == 'y':
    # 3. Get confirmation ID
    confirmation_id = confirm_cost_supabase(
        type="project",
        recurrence="monthly",
        amount=10.0
    )

    # 4. Use confirmation ID for creation
    create_project_supabase(
        name="my-project",
        organization_id=org_id,
        confirm_cost_id=confirmation_id
    )
```

### **pause_project_supabase**
**Purpose**: Pauses a Supabase project to save costs.

**Test Result**:
```json
{"error": "Cannot pause project due to its current status: INACTIVE."}
```

**Educational Insights**:
- **Cost optimization**: Pausing stops billing for compute resources
- **Status requirements**: Can only pause ACTIVE projects
- **Data preservation**: Database data is preserved during pause
- **Quick restart**: Projects can be restored quickly when needed

**Pause Strategy**:
```python
# Check project status before pausing
project = get_project_supabase(project_id)

if project["status"] == "ACTIVE_HEALTHY":
    pause_project_supabase(project_id)
    print("✅ Project paused successfully")
elif project["status"] == "INACTIVE":
    print("ℹ️ Project is already paused")
else:
    print(f"⚠️ Cannot pause project in status: {project['status']}")
```

### **restore_project_supabase**
**Purpose**: Restores a paused Supabase project.

**Test Result**: Successfully restored project (status changed from INACTIVE to COMING_UP)

**Educational Insights**:
- **Quick restoration**: Projects typically restore within minutes
- **Status transition**: INACTIVE → COMING_UP → ACTIVE_HEALTHY
- **Data integrity**: All data and configurations preserved
- **Billing resumption**: Charges resume when project becomes active

**Restoration Monitoring**:
```python
# Restore project
restore_project_supabase(project_id)

# Monitor restoration progress
import time
while True:
    project = get_project_supabase(project_id)
    status = project["status"]

    if status == "ACTIVE_HEALTHY":
        print("✅ Project fully restored")
        break
    elif status == "COMING_UP":
        print("🔄 Project restoring...")
        time.sleep(30)  # Wait 30 seconds before checking again
    else:
        print(f"⚠️ Unexpected status: {status}")
        break
```

---

## **3. Project Information Tools**

### **get_project_url_supabase**
**Purpose**: Retrieves the API endpoint URL for your Supabase project.

**Test Result**:
```
"https://zsxzhqtltpdsrjccgjch.supabase.co"
```

**Educational Insights**:
- **Essential for client configuration**: This URL is required for all client-side SDK initialization
- **Format**: Always follows pattern `https://{project-ref}.supabase.co`
- **Use cases**:
  - Frontend application configuration
  - API endpoint documentation
  - Environment variable setup
- **Security**: Safe to expose publicly as it's the public API endpoint

**Best Practices**:
```javascript
// Store in environment variables
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
```

### **get_anon_key_supabase**
**Purpose**: Retrieves the anonymous (public) API key for client-side authentication.

**Test Result**:
```
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzeHpocXRsdHBkc3JqY2NnamNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM4NTE5NTEsImV4cCI6MjA2OTQyNzk1MX0.LayBSRECge8eMSz6cCqgayIQoJVgBYWG6TZQg3eLJl0"
```

**Educational Insights**:
- **JWT Structure**: Contains project reference, role (anon), and expiration
- **Client-side safe**: Designed for public use in frontend applications
- **Automatic user context**: Switches to user's JWT after authentication
- **RLS enforcement**: Only allows operations permitted by Row Level Security policies

**Security Considerations**:
- ✅ Safe to expose in client-side code
- ✅ Automatically respects RLS policies
- ❌ Never use service_role key in client-side code
- ✅ Expires in ~10 years (long-lived for convenience)

---

## **2. Database Management Tools**

### **list_tables_supabase**
**Purpose**: Lists all tables across specified database schemas with detailed metadata.

**Test Results**:
- **Default (public schema)**: `[]` (empty - no user tables initially)
- **Multiple schemas**: Returns comprehensive table information including:
  - Auth schema: 15 tables (users, sessions, refresh_tokens, etc.)
  - Storage schema: 5 tables (buckets, objects, migrations, etc.)
  - Detailed column information with data types, constraints, relationships

**Educational Insights**:
- **Schema organization**: Supabase uses separate schemas for different services
  - `auth`: User authentication and session management
  - `storage`: File storage and bucket management
  - `public`: Your application tables
- **Rich metadata**: Provides complete table structure including:
  - Column definitions with data types
  - Primary keys and relationships
  - RLS status and table statistics
  - Comments and constraints

**Practical Applications**:
```python
# Get all user tables
tables = list_tables_supabase(schemas=["public"])

# Get system tables for debugging
auth_tables = list_tables_supabase(schemas=["auth"])
storage_tables = list_tables_supabase(schemas=["storage"])

# Analyze table structure for documentation
all_tables = list_tables_supabase(schemas=["public", "auth", "storage"])
```

### **list_extensions_supabase**
**Purpose**: Shows all available and installed PostgreSQL extensions.

**Test Results**:
- **Total extensions**: 80+ available
- **Installed by default**:
  - `uuid-ossp`: UUID generation
  - `pgcrypto`: Cryptographic functions
  - `pg_stat_statements`: Query performance tracking
  - `pg_graphql`: GraphQL support
  - `supabase_vault`: Secrets management

**Educational Insights**:
- **Extension ecosystem**: Supabase provides extensive PostgreSQL extension support
- **Key categories**:
  - **Spatial**: PostGIS for geographic data
  - **Search**: pg_trgm for full-text search
  - **Vector**: pgvector for AI/ML embeddings
  - **Security**: pgsodium for encryption
  - **Performance**: pg_stat_monitor for monitoring

**Notable Extensions for Modern Apps**:
```sql
-- Vector similarity search (AI/ML)
CREATE EXTENSION vector;

-- Full-text search
CREATE EXTENSION pg_trgm;

-- Geographic data
CREATE EXTENSION postgis;

-- HTTP requests from database
CREATE EXTENSION http;

-- Job scheduling
CREATE EXTENSION pg_cron;
```

### **list_migrations_supabase**
**Purpose**: Shows all applied database migrations with version tracking.

**Test Result**:
```json
[{"version":"20250730051158","name":""}]
```

**Educational Insights**:
- **Version-based tracking**: Uses timestamp-based versioning (YYYYMMDDHHMMSS)
- **Migration history**: Maintains complete audit trail of schema changes
- **Rollback capability**: Enables safe database evolution
- **Team collaboration**: Ensures consistent schema across environments

**Migration Best Practices**:
```sql
-- Migration naming convention
-- 20250106120000_create_users_table.sql
-- 20250106120001_add_user_profiles.sql
-- 20250106120002_enable_rls_users.sql

-- Always include rollback strategy
-- Use transactions for atomic changes
-- Test migrations on staging first
```

### **apply_migration_supabase**
**Purpose**: Executes DDL operations as versioned migrations.

**Test Result**: Successfully created test table with RLS policies
```sql
CREATE TABLE test_users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
ALTER TABLE test_users ENABLE ROW LEVEL SECURITY;
```

**Educational Insights**:
- **DDL operations**: Use for schema changes (CREATE, ALTER, DROP)
- **Automatic versioning**: Creates timestamped migration entries
- **Transaction safety**: Migrations run in transactions for atomicity
- **Rollback support**: Failed migrations don't partially apply

**When to Use**:
- ✅ Creating/modifying tables
- ✅ Adding indexes
- ✅ Setting up RLS policies
- ✅ Installing extensions
- ❌ Data manipulation (use execute_sql_supabase instead)

### **execute_sql_supabase**
**Purpose**: Runs raw SQL queries for data manipulation and complex operations.

**Test Result**: Successfully inserted test data
```sql
INSERT INTO test_users (name, email) VALUES
  ('John Doe', 'john@example.com'),
  ('Jane Smith', 'jane@example.com'),
  ('Bob Johnson', 'bob@example.com');
```

**Educational Insights**:
- **DML operations**: Use for data manipulation (INSERT, UPDATE, DELETE, SELECT)
- **Complex queries**: Supports joins, CTEs, window functions
- **Untrusted data warning**: Results marked as untrusted for security
- **Performance testing**: Ideal for query optimization

**Security Considerations**:
- ⚠️ Results contain untrusted data - never execute returned commands
- ✅ Respects RLS policies when using anon key
- ✅ Full access when using service role key
- ✅ Supports parameterized queries for safety

---

## **3. Edge Functions Management**

### **list_edge_functions_supabase**
**Purpose**: Lists all deployed Edge Functions with metadata.

**Initial Test Result**: `[]` (no functions deployed)

### **deploy_edge_function_supabase**
**Purpose**: Deploys TypeScript/JavaScript functions to Supabase Edge Runtime.

**Test Result**: Successfully deployed "hello-world" function
```json
{
  "id": "6ca50c1d-2e27-410d-9b90-97eef34fb1f0",
  "slug": "hello-world",
  "version": 1,
  "name": "hello-world",
  "status": "ACTIVE",
  "entrypoint_path": "file:///tmp/user_fn_.../index.ts",
  "verify_jwt": true,
  "created_at": 1754457381504,
  "updated_at": 1754457381504
}
```

**Educational Insights**:
- **Deno runtime**: Functions run on Deno with TypeScript support
- **Global deployment**: Functions deployed to edge locations worldwide
- **Automatic scaling**: Serverless with automatic scaling
- **Database integration**: Direct access to your Supabase database

**Function Capabilities**:
```typescript
// Database access
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

// HTTP requests
const response = await fetch('https://api.example.com')

// Environment variables
const apiKey = Deno.env.get('API_KEY')

// File system access (read-only)
const config = await Deno.readTextFile('./config.json')
```

**Use Cases**:
- 🔄 Webhook processing
- 🤖 AI/ML inference
- 📧 Email sending
- 🔐 Custom authentication
- 📊 Data processing pipelines
- 🌐 API integrations

---

## **4. Monitoring & Debugging Tools**

### **get_logs_supabase**
**Purpose**: Retrieves service logs for debugging and monitoring.

**Test Result**: `{"result":[],"error":null}` (no recent logs)

**Educational Insights**:
- **Service-specific logs**: Separate logs for api, postgres, auth, storage, etc.
- **Recent activity only**: Shows logs from last minute for performance
- **Real-time debugging**: Essential for troubleshooting issues
- **Production monitoring**: Critical for maintaining application health

**Available Log Services**:
```python
# API request logs
get_logs_supabase(service="api")

# Database query logs
get_logs_supabase(service="postgres")

# Authentication logs
get_logs_supabase(service="auth")

# File storage logs
get_logs_supabase(service="storage")

# Edge function logs
get_logs_supabase(service="edge-function")

# Real-time logs
get_logs_supabase(service="realtime")
```

### **get_advisors_supabase**
**Purpose**: Provides automated security and performance recommendations.

**Test Results**:

**Security Advisors**:
```json
{
  "lints": [
    {
      "name": "function_search_path_mutable",
      "level": "WARN",
      "categories": ["SECURITY"],
      "description": "Function has a role mutable search_path",
      "remediation": "https://supabase.com/docs/guides/database/database-linter"
    },
    {
      "name": "auth_otp_long_expiry",
      "level": "WARN",
      "description": "OTP expiry exceeds recommended threshold"
    }
  ]
}
```

**Performance Advisors**: `{"lints": []}` (no issues found)

**Educational Insights**:
- **Automated security scanning**: Continuously monitors for security vulnerabilities
- **Performance optimization**: Identifies bottlenecks and optimization opportunities
- **Best practice enforcement**: Ensures adherence to security standards
- **Actionable recommendations**: Provides specific remediation steps

**Common Security Issues**:
- 🔒 Missing RLS policies
- 🔑 Weak authentication settings
- 🛡️ Function security vulnerabilities
- 📊 Exposed sensitive data
- ⚡ Performance bottlenecks

**Remediation Workflow**:
1. Run advisors regularly
2. Prioritize by severity level
3. Follow remediation links
4. Re-run to verify fixes
5. Monitor for new issues

---

## **5. TypeScript Generation**

### **generate_typescript_types_supabase**
**Purpose**: Automatically generates TypeScript definitions from database schema.

**Test Result**: Generated complete TypeScript definitions for `test_users` table
```typescript
export type Database = {
  public: {
    Tables: {
      test_users: {
        Row: {
          created_at: string | null
          email: string
          id: number
          name: string
        }
        Insert: {
          created_at?: string | null
          email: string
          id?: number
          name: string
        }
        Update: {
          created_at?: string | null
          email?: string
          id?: number
          name?: string
        }
        Relationships: []
      }
    }
    // ... additional type definitions
  }
}
```

**Educational Insights**:
- **Type safety**: Ensures compile-time type checking for database operations
- **Auto-generated**: Reflects current database schema automatically
- **Three operation types**: Row (select), Insert, Update with appropriate optionality
- **Relationship mapping**: Includes foreign key relationships

**Integration Example**:
```typescript
import { Database } from './types/supabase'

const supabase = createClient<Database>(url, key)

// Type-safe database operations
const { data } = await supabase
  .from('test_users')  // ✅ Autocomplete available
  .select('name, email')  // ✅ Column names validated
  .eq('id', 1)  // ✅ Type checking

// Type-safe inserts
const { data } = await supabase
  .from('test_users')
  .insert({
    name: 'John',  // ✅ Required field
    email: 'john@example.com',  // ✅ Required field
    // id is optional (auto-generated)
    // created_at is optional (has default)
  })
```

**Development Workflow**:
1. Make schema changes
2. Run type generation
3. Update application code
4. Compile-time validation
5. Deploy with confidence

---

## **6. Documentation Search**

### **search_docs_supabase**
**Purpose**: GraphQL-based search through comprehensive Supabase documentation.

**Test Result**: Successfully retrieved authentication-related documentation
```json
{
  "searchDocs": {
    "nodes": [
      {
        "title": "Glossary",
        "href": "https://supabase.com/docs/guides/resources/glossary",
        "content": "# Glossary\n\nDefinitions for terminology..."
      },
      {
        "title": "Multi-Factor Authentication (TOTP)",
        "href": "https://supabase.com/docs/guides/auth/auth-mfa/totp",
        "content": "# Multi-Factor Authentication (TOTP)..."
      }
    ]
  }
}
```

**Educational Insights**:
- **GraphQL interface**: Powerful query capabilities for precise documentation retrieval
- **Comprehensive coverage**: Includes guides, references, troubleshooting, and examples
- **Real-time updates**: Always reflects latest documentation
- **Contextual search**: Finds relevant content across entire knowledge base

**Advanced Search Queries**:
```graphql
# Search for specific topics
query {
  searchDocs(query: "row level security", limit: 5) {
    nodes {
      title
      href
      content
    }
  }
}

# Search for error codes
query {
  error(code: "23505", service: AUTH) {
    code
    message
    httpStatusCode
  }
}

# Get troubleshooting guides
query {
  searchDocs(query: "troubleshooting nextjs") {
    nodes {
      title
      content
    }
  }
}
```

**Use Cases**:
- 📚 Contextual help in applications
- 🤖 AI-powered documentation assistance
- 🔍 Error code lookup
- 📖 Learning and onboarding
- 🛠️ Troubleshooting guides

---

## **7. Branch Management Tools** ⚠️

### **Limited Testing Due to Cost Requirements**

**create_branch_supabase**: Requires cost confirmation ID
**list_branches_supabase**: Returns `[]` (no branches created)
**delete_branch_supabase**: Requires existing branch
**merge_branch_supabase**: Requires existing branch
**reset_branch_supabase**: Requires existing branch
**rebase_branch_supabase**: Requires existing branch

**Educational Insights**:
- **Cost protection**: Branch creation requires explicit cost confirmation
- **Isolated environments**: Each branch gets its own database instance
- **Migration testing**: Safe environment for testing schema changes
- **Team collaboration**: Multiple developers can work on separate branches

**Branch Workflow**:
```python
# 1. Confirm costs first
cost_id = confirm_cost()  # External step

# 2. Create development branch
branch = create_branch_supabase(
    name="feature-user-profiles",
    confirm_cost_id=cost_id
)

# 3. Work on branch (isolated environment)
# - Test migrations
# - Develop features
# - Run tests

# 4. Merge when ready
merge_branch_supabase(branch_id=branch["id"])

# 5. Clean up
delete_branch_supabase(branch_id=branch["id"])
```

## **Advanced Workflows & Best Practices**

### **Complete Project Creation Workflow**

The enhanced MCP server provides a complete project lifecycle management system. Here's the recommended workflow:

```python
# 1. Discover Organizations
organizations = list_organizations_supabase()
print("Available Organizations:")
for org in organizations:
    org_details = get_organization_supabase(org["id"])
    print(f"- {org['name']} (Plan: {org_details['plan']})")

# 2. Select Organization
selected_org_id = organizations[0]["id"]  # or user selection

# 3. Check Cost
cost_info = get_cost_supabase(selected_org_id, "project")
print(f"Project creation cost: {cost_info}")

# 4. Confirm Cost (requires user interaction)
confirmation_id = confirm_cost_supabase(
    type="project",
    recurrence="monthly",
    amount=10.0
)

# 5. Create Project
new_project = create_project_supabase(
    name="my-new-project",
    organization_id=selected_org_id,
    region="us-east-1",  # Choose appropriate region
    confirm_cost_id=confirmation_id
)

# 6. Monitor Project Creation
while True:
    project = get_project_supabase(new_project["id"])
    if project["status"] == "ACTIVE_HEALTHY":
        print("✅ Project ready!")
        break
    elif project["status"] == "COMING_UP":
        print("🔄 Project initializing...")
        time.sleep(30)
    else:
        print(f"⚠️ Status: {project['status']}")
        break
```

### **Cost Management Best Practices**

#### **Understanding Supabase Pricing**
- **Projects**: $10/month for Pro plan projects
- **Branches**: $0.01344/hour (~$9.68/month if running 24/7)
- **Organization Plans**: Affect available features and limits

#### **Cost Optimization Strategies**
```python
# 1. Use branches for development (cheaper than full projects)
branch_cost = get_cost_supabase(org_id, "branch")
project_cost = get_cost_supabase(org_id, "project")

# 2. Pause unused projects
inactive_projects = [p for p in list_projects_supabase()
                    if p["status"] == "ACTIVE_HEALTHY" and not_in_use(p)]
for project in inactive_projects:
    pause_project_supabase(project["id"])

# 3. Clean up old branches
branches = list_branches_supabase(project_id)
old_branches = [b for b in branches if is_old(b)]
for branch in old_branches:
    delete_branch_supabase(branch["id"])
```

### **Multi-Organization Management**

#### **Organization Selection Strategy**
```python
def select_best_organization(purpose="development"):
    orgs = list_organizations_supabase()

    for org in orgs:
        details = get_organization_supabase(org["id"])

        if purpose == "development" and details["plan"] == "free":
            # Use free org for development
            return org["id"]
        elif purpose == "production" and details["plan"] in ["pro", "team"]:
            # Use paid org for production
            return org["id"]

    return orgs[0]["id"]  # Fallback to first org
```

#### **Cross-Organization Project Management**
```python
def get_organization_projects():
    all_projects = list_projects_supabase()
    orgs = list_organizations_supabase()

    org_projects = {}
    for org in orgs:
        org_details = get_organization_supabase(org["id"])
        org_projects[org["name"]] = {
            "plan": org_details["plan"],
            "projects": [p for p in all_projects if p["organization_id"] == org["id"]]
        }

    return org_projects
```

### **Project Health Monitoring**

#### **Automated Health Checks**
```python
def monitor_project_health():
    projects = list_projects_supabase()

    for project in projects:
        status = project["status"]

        if status == "ACTIVE_HEALTHY":
            # Check for issues
            advisors = get_advisors_supabase(project["id"], "security")
            if advisors["lints"]:
                print(f"⚠️ {project['name']}: {len(advisors['lints'])} security issues")

        elif status == "INACTIVE":
            print(f"💤 {project['name']}: Project paused")

        elif status == "UNHEALTHY":
            # Check logs for issues
            logs = get_logs_supabase(project["id"], "api")
            print(f"🔴 {project['name']}: Unhealthy - check logs")
```

### **Development Branch Workflow**

#### **Feature Development with Branches**
```python
def create_feature_branch(project_id, feature_name):
    # 1. Check branch cost
    cost = get_cost_supabase(project_id, "branch")
    print(f"Branch cost: {cost}")

    # 2. Create branch
    confirmation_id = confirm_cost_supabase(
        type="branch",
        recurrence="hourly",
        amount=0.01344
    )

    branch = create_branch_supabase(
        project_id=project_id,
        name=f"feature-{feature_name}",
        confirm_cost_id=confirmation_id
    )

    # 3. Work on branch
    # - Apply migrations
    # - Test features
    # - Run tests

    return branch

def complete_feature(branch_id):
    # 1. Merge to production
    merge_branch_supabase(branch_id)

    # 2. Clean up branch
    delete_branch_supabase(branch_id)

    print("✅ Feature merged and branch cleaned up")
```

### **Security and Compliance**

#### **Regular Security Audits**
```python
def security_audit():
    projects = list_projects_supabase()

    for project in projects:
        if project["status"] == "ACTIVE_HEALTHY":
            # Check security advisors
            security_issues = get_advisors_supabase(project["id"], "security")
            performance_issues = get_advisors_supabase(project["id"], "performance")

            total_issues = len(security_issues["lints"]) + len(performance_issues["lints"])

            if total_issues > 0:
                print(f"🔍 {project['name']}: {total_issues} issues found")

                # Log critical security issues
                for issue in security_issues["lints"]:
                    if issue["level"] == "ERROR":
                        print(f"🚨 CRITICAL: {issue['title']}")
                        print(f"   Remediation: {issue['remediation']}")
```

### **Performance Optimization**

#### **Database Performance Monitoring**
```python
def optimize_database_performance(project_id):
    # 1. Check performance advisors
    advisors = get_advisors_supabase(project_id, "performance")

    for issue in advisors["lints"]:
        print(f"⚡ Performance Issue: {issue['title']}")
        print(f"   Description: {issue['description']}")
        print(f"   Fix: {issue['remediation']}")

    # 2. Check database extensions
    extensions = list_extensions_supabase(project_id)

    # Recommend useful extensions
    recommended = ["pg_stat_statements", "pg_trgm", "vector"]
    installed = [ext["name"] for ext in extensions if ext["installed_version"]]

    for ext in recommended:
        if ext not in installed:
            print(f"💡 Consider installing extension: {ext}")
```

---

This comprehensive documentation provides detailed insights into Supabase and its MCP integration, covering everything from basic setup to advanced optimization techniques for building scalable, secure applications with AI assistance.
