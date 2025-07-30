#!/usr/bin/env python3
"""
Script de Instalação Completa do Instagram Video Analyzer MCP Server

Este script automatiza a instalação e configuração completa do sistema:
- MCP Server
- Integração com Claude Code
- Templates VibeKanban
- Testes e validação

Execute com: python setup_complete.py
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional

class InstagramAnalyzerSetup:
    """Classe para gerenciar a instalação completa"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.mcp_dir = self.base_dir / "mcp-server"
        self.templates_dir = self.base_dir / "vibekanban-templates"
        self.docs_dir = self.base_dir / "docs"
        
        # Detectar sistema operacional
        self.os_type = platform.system().lower()
        self.is_windows = self.os_type == "windows"
        
        # Configurações
        self.config = {
            "api_url": "http://localhost:8000",
            "mcp_port": 8001,
            "claude_config_path": self._get_claude_config_path(),
            "python_executable": sys.executable
        }
    
    def _get_claude_config_path(self) -> Path:
        """Obtém o caminho do arquivo de configuração do Claude Code"""
        if self.is_windows:
            return Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        elif self.os_type == "darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        else:  # Linux
            return Path.home() / ".config" / "claude" / "claude_desktop_config.json"
    
    def print_step(self, step: str, description: str):
        """Imprime passo da instalação"""
        print(f"\n{'='*60}")
        print(f"🔧 {step}: {description}")
        print(f"{'='*60}")
    
    def run_command(self, command: List[str], cwd: Optional[Path] = None) -> bool:
        """Executa comando e retorna sucesso"""
        try:
            print(f"📝 Executando: {' '.join(command)}")
            result = subprocess.run(
                command,
                cwd=cwd or self.base_dir,
                check=True,
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(f"✅ Saída: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro: {e}")
            if e.stderr:
                print(f"❌ Stderr: {e.stderr}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Verifica pré-requisitos"""
        self.print_step("PASSO 1", "Verificando Pré-requisitos")
        
        # Verificar Python
        python_version = sys.version_info
        if python_version < (3, 11):
            print(f"❌ Python 3.11+ necessário. Versão atual: {python_version.major}.{python_version.minor}")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Verificar uv
        if not self.run_command(["uv", "--version"]):
            print("❌ uv não encontrado. Instalando...")
            if self.is_windows:
                if not self.run_command(["powershell", "-c", "irm https://astral.sh/uv/install.ps1 | iex"]):
                    print("❌ Falha ao instalar uv")
                    return False
            else:
                if not self.run_command(["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]):
                    print("❌ Falha ao instalar uv")
                    return False
        
        # Verificar Node.js (para VibeKanban)
        if not self.run_command(["node", "--version"]):
            print("⚠️ Node.js não encontrado. VibeKanban não será configurado.")
        
        # Verificar se a API está rodando
        try:
            import requests
            response = requests.get(f"{self.config['api_url']}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ Instagram Video Analyzer API rodando em {self.config['api_url']}")
            else:
                print(f"⚠️ API respondeu com status {response.status_code}")
        except Exception as e:
            print(f"⚠️ API não está rodando: {e}")
            print("   Certifique-se de iniciar a API antes de usar o MCP server")
        
        return True
    
    def install_mcp_server(self) -> bool:
        """Instala o MCP Server"""
        self.print_step("PASSO 2", "Instalando MCP Server")
        
        # Criar diretório se não existir
        self.mcp_dir.mkdir(exist_ok=True)
        
        # Instalar dependências
        if not self.run_command(["uv", "sync"], cwd=self.mcp_dir):
            print("❌ Falha ao instalar dependências do MCP server")
            return False
        
        # Testar instalação
        if not self.run_command(["uv", "run", "python", "-c", "import mcp; print('MCP importado com sucesso')"], cwd=self.mcp_dir):
            print("❌ Falha ao importar MCP")
            return False
        
        print("✅ MCP Server instalado com sucesso")
        return True
    
    def configure_claude_code(self) -> bool:
        """Configura integração com Claude Code"""
        self.print_step("PASSO 3", "Configurando Claude Code")
        
        # Verificar se Claude Code está instalado
        claude_config_path = self.config["claude_config_path"]
        
        if not claude_config_path.parent.exists():
            print("⚠️ Claude Code não parece estar instalado")
            print(f"   Diretório esperado: {claude_config_path.parent}")
            return False
        
        # Criar configuração do MCP server
        mcp_config = {
            "mcpServers": {
                "instagram-video-analyzer": {
                    "command": "uv",
                    "args": ["run", "instagram-video-analyzer-mcp"],
                    "cwd": str(self.mcp_dir.absolute()),
                    "env": {
                        "API_BASE_URL": self.config["api_url"],
                        "LOG_LEVEL": "INFO"
                    }
                }
            }
        }
        
        # Ler configuração existente ou criar nova
        existing_config = {}
        if claude_config_path.exists():
            try:
                with open(claude_config_path, 'r') as f:
                    existing_config = json.load(f)
                print("✅ Configuração existente do Claude Code encontrada")
            except Exception as e:
                print(f"⚠️ Erro ao ler configuração existente: {e}")
        
        # Mesclar configurações
        if "mcpServers" not in existing_config:
            existing_config["mcpServers"] = {}
        
        existing_config["mcpServers"]["instagram-video-analyzer"] = mcp_config["mcpServers"]["instagram-video-analyzer"]
        
        # Salvar configuração
        try:
            claude_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(claude_config_path, 'w') as f:
                json.dump(existing_config, f, indent=2)
            print(f"✅ Configuração do Claude Code salva em: {claude_config_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def install_vibekanban(self) -> bool:
        """Instala e configura VibeKanban"""
        self.print_step("PASSO 4", "Configurando VibeKanban")
        
        # Verificar se Node.js está disponível
        if not self.run_command(["node", "--version"]):
            print("⚠️ Node.js não encontrado. Pulando instalação do VibeKanban")
            return True
        
        # Instalar VibeKanban globalmente
        if not self.run_command(["npm", "install", "-g", "@bloop/vibe-kanban"]):
            print("❌ Falha ao instalar VibeKanban")
            return False
        
        # Criar projeto VibeKanban
        vibe_project_dir = self.base_dir / "vibe-project"
        if not vibe_project_dir.exists():
            if not self.run_command(["vibe-kanban", "init", "instagram-analysis"], cwd=self.base_dir):
                print("❌ Falha ao criar projeto VibeKanban")
                return False
            
            # Renomear diretório
            (self.base_dir / "instagram-analysis").rename(vibe_project_dir)
        
        # Copiar templates
        templates_dest = vibe_project_dir / "templates"
        templates_dest.mkdir(exist_ok=True)
        
        for template_file in self.templates_dir.glob("*.yml"):
            dest_file = templates_dest / template_file.name
            dest_file.write_text(template_file.read_text(), encoding='utf-8')
            print(f"✅ Template copiado: {template_file.name}")
        
        print("✅ VibeKanban configurado com sucesso")
        return True
    
    def run_tests(self) -> bool:
        """Executa testes do MCP Server"""
        self.print_step("PASSO 5", "Executando Testes")
        
        # Instalar pytest se necessário
        if not self.run_command(["uv", "add", "--dev", "pytest", "pytest-asyncio"], cwd=self.mcp_dir):
            print("❌ Falha ao instalar pytest")
            return False
        
        # Executar testes
        if not self.run_command(["uv", "run", "pytest", "tests/", "-v"], cwd=self.mcp_dir):
            print("❌ Alguns testes falharam")
            return False
        
        print("✅ Todos os testes passaram")
        return True
    
    def create_startup_scripts(self) -> bool:
        """Cria scripts de inicialização"""
        self.print_step("PASSO 6", "Criando Scripts de Inicialização")
        
        # Script para Windows
        if self.is_windows:
            startup_script = self.base_dir / "start_mcp_server.bat"
            startup_script.write_text(f"""@echo off
echo Iniciando Instagram Video Analyzer MCP Server...
cd /d "{self.mcp_dir}"
uv run instagram-video-analyzer-mcp
pause
""")
            print(f"✅ Script criado: {startup_script}")
        
        # Script para Unix/Linux/macOS
        startup_script = self.base_dir / "start_mcp_server.sh"
        startup_script.write_text(f"""#!/bin/bash
echo "Iniciando Instagram Video Analyzer MCP Server..."
cd "{self.mcp_dir}"
uv run instagram-video-analyzer-mcp
""")
        startup_script.chmod(0o755)
        print(f"✅ Script criado: {startup_script}")
        
        return True
    
    def generate_documentation(self) -> bool:
        """Gera documentação final"""
        self.print_step("PASSO 7", "Gerando Documentação")
        
        # Criar README de instalação
        install_readme = self.base_dir / "INSTALACAO_COMPLETA.md"
        
        readme_content = f"""# 🎉 Instalação Completa - Instagram Video Analyzer MCP

## ✅ Status da Instalação

- **MCP Server**: Instalado em `{self.mcp_dir}`
- **Claude Code**: Configurado em `{self.config['claude_config_path']}`
- **VibeKanban**: Projeto criado em `vibe-project/`
- **Templates**: Disponíveis em `vibekanban-templates/`

## 🚀 Como Usar

### 1. Iniciar MCP Server

**Windows:**
```cmd
{self.base_dir / 'start_mcp_server.bat'}
```

**Linux/macOS:**
```bash
{self.base_dir / 'start_mcp_server.sh'}
```

### 2. Usar com Claude Code

```bash
claude "Analise este vídeo do Instagram: https://www.instagram.com/reel/DMiEEmlMI7J/"
```

### 3. Usar com VibeKanban

```bash
cd vibe-project
vibe-kanban run analise-video-instagram --video_url "https://www.instagram.com/reel/DMiEEmlMI7J/"
```

## 📚 Documentação

- **MCP Server**: `mcp-server/README.md`
- **Claude Code**: `docs/CLAUDE_CODE_INTEGRATION.md`
- **VibeKanban**: `docs/VIBEKANBAN_TEMPLATES_GUIDE.md`

## 🔧 Configurações

- **API URL**: {self.config['api_url']}
- **MCP Port**: {self.config['mcp_port']}
- **Python**: {self.config['python_executable']}

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se a API está rodando: `curl {self.config['api_url']}/health`
2. Teste o MCP server: `cd mcp-server && uv run instagram-video-analyzer-mcp --help`
3. Verifique logs do Claude Code
4. Execute testes: `cd mcp-server && uv run pytest tests/ -v`

## 🎯 Próximos Passos

1. Teste a análise de um vídeo
2. Configure notificações no VibeKanban
3. Personalize templates conforme necessário
4. Configure monitoramento contínuo

**Instalação concluída com sucesso! 🎉**
"""
        
        install_readme.write_text(readme_content, encoding='utf-8')
        print(f"✅ Documentação criada: {install_readme}")
        
        return True
    
    def run_installation(self) -> bool:
        """Executa instalação completa"""
        print("🎬 Instagram Video Analyzer MCP - Instalação Completa")
        print("=" * 60)
        
        steps = [
            ("Pré-requisitos", self.check_prerequisites),
            ("MCP Server", self.install_mcp_server),
            ("Claude Code", self.configure_claude_code),
            ("VibeKanban", self.install_vibekanban),
            ("Testes", self.run_tests),
            ("Scripts", self.create_startup_scripts),
            ("Documentação", self.generate_documentation)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Falha na etapa: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("\n📚 Próximos passos:")
        print("1. Reinicie o Claude Code")
        print("2. Execute: python start_mcp_server.sh (ou .bat no Windows)")
        print("3. Teste: claude 'Analise este vídeo: https://instagram.com/reel/...'")
        print("\n📖 Documentação completa em: INSTALACAO_COMPLETA.md")
        
        return True

def main():
    """Função principal"""
    installer = InstagramAnalyzerSetup()
    
    try:
        success = installer.run_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
