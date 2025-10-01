@echo off
echo 🚀 CRIANDO PROJETO GOHIGHLEVEL-MCP
echo ================================

REM Criar estrutura de pastas
echo 📁 Criando pastas...
mkdir gohighlevel_mcp 2>nul

echo 📝 Criando arquivos Python...

REM Criar __init__.py
echo """GoHighLevel MCP Server - Integrate GHL with Claude via Model Context Protocol."""> gohighlevel_mcp\__init__.py
echo.>> gohighlevel_mcp\__init__.py
echo __version__ = "0.1.0">> gohighlevel_mcp\__init__.py

echo ✅ Projeto criado com sucesso!
echo.
echo 🔧 PRÓXIMOS PASSOS:
echo 1. Edite o arquivo .env com suas credenciais do GoHighLevel
echo 2. Execute: pip install -e .
echo 3. Configure o Claude Desktop
echo.
echo 📖 Leia o arquivo INSTALACAO-INICIANTE.md para instruções completas
echo.
pause