@echo off
echo Criando estrutura do node n8n...

cd E:\ClaudeCode\Projetos
mkdir n8n-nodes-ghl-mcp 2>nul
cd n8n-nodes-ghl-mcp

mkdir nodes 2>nul
mkdir nodes\GhlMcp 2>nul
mkdir credentials 2>nul

echo Estrutura criada!
echo.
echo Agora execute: cd E:\ClaudeCode\Projetos\n8n-nodes-ghl-mcp
echo Depois: npm install
pause
