# Criar Node n8n - 5 Minutos

## PASSO 1: Criar Estrutura (Cole no Terminal)

```bash
cd E:\ClaudeCode\Projetos
mkdir n8n-nodes-ghl-mcp
cd n8n-nodes-ghl-mcp
mkdir nodes
mkdir nodes\GhlMcp
mkdir credentials
npm init -y
```

## PASSO 2: Instalar Dependências

```bash
npm install --save-dev typescript @types/node n8n-workflow
```

## PASSO 3: Criar Arquivos

Vou te passar o conteúdo de cada arquivo. Crie eles na ordem:

### Arquivo 1: tsconfig.json
(Conteúdo vem a seguir)

### Arquivo 2: credentials/GhlMcpApi.credentials.ts
(Conteúdo vem a seguir)

### Arquivo 3: nodes/GhlMcp/GhlMcp.node.ts
(Conteúdo vem a seguir)

### Arquivo 4: nodes/GhlMcp/GhlMcp.node.json
(Conteúdo vem a seguir)

## PASSO 4: Buildar

```bash
npm run build
```

## PASSO 5: Publicar

```bash
npm login
npm publish
```

## PRONTO!

Agora qualquer cliente instala com:
```bash
npm install n8n-nodes-ghl-mcp
```

E usa no n8n dele só configurando:
- GHL API Key
- GHL Location ID

---

## Para Facilitar Ainda Mais

Criei os arquivos prontos na pasta `gohighlevel-mcp`. 

Você executa os comandos do PASSO 1 e 2, depois COPIA os arquivos que vou criar pra você.

Continua lendo...
