# 🚀 GUIA COMPLETO PARA INICIANTES - GoHighLevel + Claude

## 📋 O que vamos fazer?
1. ✅ Instalar as ferramentas necessárias
2. ✅ Baixar/criar o projeto 
3. ✅ Configurar suas credenciais do GoHighLevel
4. ✅ Instalar o MCP Server
5. ✅ Conectar com o Claude Desktop

---

## 🔧 PASSO 1: Instalar Ferramentas (Windows)

### 1.1 - Instalar Python
1. **Vá para:** https://python.org/downloads/
2. **Clique em:** "Download Python" (versão mais recente)
3. **Execute o instalador** e **MARQUE**: ☑️ "Add Python to PATH"
4. **Clique:** "Install Now"

### 1.2 - Instalar Git (opcional - para baixar códigos)
1. **Vá para:** https://git-scm.com/download/win
2. **Baixe e instale** (pode usar configurações padrão)

### 1.3 - Verificar se funcionou
1. **Abra o Prompt de Comando** (Windows + R, digite `cmd`)
2. **Digite:**
```bash
python --version
```
**Deve mostrar:** `Python 3.11.x` ou similar

---

## 📁 PASSO 2: Criar o Projeto

### 2.1 - Criar pasta do projeto
```bash
# Abra o Prompt de Comando e digite:
cd C:\
mkdir MeusProjetos
cd MeusProjetos
mkdir gohighlevel-mcp
cd gohighlevel-mcp
```

### 2.2 - Criar arquivos necessários

**Você precisa criar estes arquivos (pode usar Bloco de Notas):**

#### 📝 Arquivo: `pyproject.toml`
**Caminho:** `C:\MeusProjetos\gohighlevel-mcp\pyproject.toml`
```toml
[project]
name = "gohighlevel-mcp"
version = "0.1.0"
description = "MCP server for GoHighLevel API integration"
dependencies = [
    "mcp>=1.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.5.0",
    "python-dotenv>=1.0.0"
]

[project.scripts]
gohighlevel-mcp = "gohighlevel_mcp.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

#### 📝 Arquivo: `.env`
**Caminho:** `C:\MeusProjetos\gohighlevel-mcp\.env`
```env
# Suas credenciais do GoHighLevel (você vai preencher depois)
GHL_API_KEY=sua_api_key_aqui
GHL_LOCATION_ID=seu_location_id_aqui
GHL_API_VERSION=v1
```

---

## 🔑 PASSO 3: Pegar suas Credenciais do GoHighLevel

### 3.1 - Obter API Key
1. **Entre no seu GoHighLevel**
2. **Vá em:** Settings (⚙️) → Integrations → API
3. **Clique:** "Create API Key" 
4. **Copie a API Key** gerada

### 3.2 - Obter Location ID  
1. **Na mesma tela de API**
2. **Procure por:** "Location ID" ou "Agency ID"
3. **Copie o ID**

### 3.3 - Colocar no arquivo `.env`
**Edite o arquivo `.env` que você criou:**
```env
GHL_API_KEY=sua_api_key_real_aqui
GHL_LOCATION_ID=seu_location_id_real_aqui  
GHL_API_VERSION=v1
```

---

## 📦 PASSO 4: Instalar o Projeto

### 4.1 - Instalar dependências
```bash
# No Prompt de Comando, dentro da pasta do projeto:
cd C:\MeusProjetos\gohighlevel-mcp
pip install -e .
```

**Se der erro, tente:**
```bash
pip install mcp httpx pydantic python-dotenv
```

---

## 🖥️ PASSO 5: Conectar com Claude Desktop

### 5.1 - Encontrar arquivo de configuração do Claude
**O arquivo fica em:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Para encontrar:**
1. **Pressione:** Windows + R
2. **Digite:** `%APPDATA%\Claude`
3. **Procure:** `claude_desktop_config.json`

### 5.2 - Editar configuração
**Se o arquivo não existir, crie ele. Conteúdo:**
```json
{
  "mcpServers": {
    "gohighlevel": {
      "command": "python",
      "args": ["-m", "gohighlevel_mcp.server"],
      "cwd": "C:\\MeusProjetos\\gohighlevel-mcp",
      "env": {
        "GHL_API_KEY": "sua_api_key_aqui",
        "GHL_LOCATION_ID": "seu_location_id_aqui"
      }
    }
  }
}
```

### 5.3 - Reiniciar Claude Desktop
1. **Feche completamente** o Claude Desktop
2. **Abra novamente**

---

## ✅ PASSO 6: Testar se Funciona

### 6.1 - No Claude Desktop, teste:
```
Mostre meus contatos do GoHighLevel
```

**Se funcionar, você verá uma lista dos seus contatos!** 🎉

---

## 🆘 PROBLEMAS COMUNS

### ❌ "python não é reconhecido"
**Solução:** Reinstale o Python marcando "Add to PATH"

### ❌ "ModuleNotFoundError: No module named 'mcp'"
**Solução:** 
```bash
pip install mcp httpx pydantic python-dotenv
```

### ❌ "GHL_API_KEY and GHL_LOCATION_ID must be set"
**Solução:** Verifique se o arquivo `.env` tem suas credenciais corretas

### ❌ Claude não mostra os comandos
**Solução:** 
1. Verifique se o arquivo `claude_desktop_config.json` está correto
2. Reinicie o Claude Desktop
3. Verifique se o caminho da pasta está certo

---

## 🎯 COMANDOS QUE FUNCIONARÃO

Depois de configurado, você poderá usar no Claude:

```
"Mostre meus últimos 10 contatos do GoHighLevel"
"Crie um contato novo com nome João Silva e email joao@teste.com"
"Mostre minhas conversas recentes"
"Envie uma mensagem SMS para o contato ID abc123"
"Mostre meus compromissos de hoje"
"Busque contatos com o nome Maria"
"Mostre minhas oportunidades do pipeline de vendas"
```

---

## 📞 PRECISA DE AJUDA?

Se algo não funcionar:
1. **Tire screenshot do erro**
2. **Me mande aqui** que eu te ajudo a resolver
3. **Podemos fazer juntos** passo a passo

**🚀 Você está quase lá! É mais simples do que parece!**