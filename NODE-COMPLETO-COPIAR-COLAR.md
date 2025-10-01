# Node n8n GoHighLevel MCP - Todos os Arquivos

## INSTRUÇÕES RÁPIDAS

1. Execute no terminal:
```bash
cd E:\ClaudeCode\Projetos
mkdir n8n-nodes-ghl-mcp
cd n8n-nodes-ghl-mcp
mkdir nodes
mkdir nodes\GhlMcp
mkdir credentials
```

2. Crie cada arquivo abaixo copiando o conteúdo

3. Rode:
```bash
npm install --save-dev typescript @types/node n8n-workflow
npm run build
```

4. Publique:
```bash
npm publish
```

---

## ARQUIVO 1: package.json
**Caminho:** `package.json` (raiz)

```json
{
  "name": "n8n-nodes-ghl-mcp",
  "version": "1.0.0",
  "description": "GoHighLevel MCP integration for n8n",
  "keywords": [
    "n8n-community-node-package",
    "gohighlevel",
    "mcp"
  ],
  "license": "MIT",
  "main": "index.js",
  "scripts": {
    "build": "tsc"
  },
  "files": [
    "dist"
  ],
  "n8n": {
    "n8nNodesApiVersion": 1,
    "credentials": [
      "dist/credentials/GhlMcpApi.credentials.js"
    ],
    "nodes": [
      "dist/nodes/GhlMcp/GhlMcp.node.js"
    ]
  },
  "devDependencies": {
    "@types/node": "^18.0.0",
    "n8n-workflow": "^1.0.0",
    "typescript": "^5.0.0"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  }
}
```

---

## ARQUIVO 2: tsconfig.json
**Caminho:** `tsconfig.json` (raiz)

```json
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./",
    "declaration": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["nodes/**/*", "credentials/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

## ARQUIVO 3: credentials/GhlMcpApi.credentials.ts
**Caminho:** `credentials/GhlMcpApi.credentials.ts`

```typescript
import {
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class GhlMcpApi implements ICredentialType {
	name = 'ghlMcpApi';
	displayName = 'GoHighLevel MCP API';
	properties: INodeProperties[] = [
		{
			displayName: 'MCP Server URL',
			name: 'serverUrl',
			type: 'string',
			default: 'https://mcp-github.va1qz0.easypanel.host',
			description: 'URL do servidor MCP',
		},
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
		},
		{
			displayName: 'Location ID',
			name: 'locationId',
			type: 'string',
			default: '',
			required: true,
		},
	];
}
```

---

## ARQUIVO 4: nodes/GhlMcp/GhlMcp.node.json
**Caminho:** `nodes/GhlMcp/GhlMcp.node.json`

```json
{
  "node": "n8n-nodes-base.ghlMcp",
  "nodeVersion": "1.0",
  "codexVersion": "1.0",
  "categories": ["CRM"]
}
```

---

## ARQUIVO 5: nodes/GhlMcp/GhlMcp.node.ts
**Caminho:** `nodes/GhlMcp/GhlMcp.node.ts`

```typescript
import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	IDataObject,
} from 'n8n-workflow';

export class GhlMcp implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'GoHighLevel MCP',
		name: 'ghlMcp',
		group: ['transform'],
		version: 1,
		description: 'GoHighLevel via MCP Server',
		defaults: { name: 'GHL MCP' },
		inputs: ['main'],
		outputs: ['main'],
		credentials: [{ name: 'ghlMcpApi', required: true }],
		properties: [
			{
				displayName: 'Operação',
				name: 'operation',
				type: 'options',
				options: [
					{ name: 'Criar Contato', value: 'createContact' },
					{ name: 'Listar Contatos', value: 'getContacts' },
					{ name: 'Criar Oportunidade', value: 'createOpportunity' },
					{ name: 'Ver Pipelines', value: 'getPipelines' },
					{ name: 'Enviar SMS', value: 'sendSms' },
				],
				default: 'createContact',
			},
			{
				displayName: 'Nome',
				name: 'firstName',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createContact'] } },
			},
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createContact'] } },
			},
			{
				displayName: 'Telefone',
				name: 'phone',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createContact'] } },
			},
			{
				displayName: 'Limite',
				name: 'limit',
				type: 'number',
				default: 10,
				displayOptions: { show: { operation: ['getContacts'] } },
			},
			{
				displayName: 'Nome do Contato',
				name: 'contactName',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createOpportunity'] } },
			},
			{
				displayName: 'Telefone',
				name: 'oppPhone',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createOpportunity'] } },
			},
			{
				displayName: 'Pipeline',
				name: 'pipelineName',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createOpportunity'] } },
			},
			{
				displayName: 'Estágio',
				name: 'stageName',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['createOpportunity'] } },
			},
			{
				displayName: 'Valor',
				name: 'value',
				type: 'number',
				default: 0,
				displayOptions: { show: { operation: ['createOpportunity'] } },
			},
			{
				displayName: 'Contact ID',
				name: 'contactId',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['sendSms'] } },
			},
			{
				displayName: 'Mensagem',
				name: 'message',
				type: 'string',
				default: '',
				displayOptions: { show: { operation: ['sendSms'] } },
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const credentials = await this.getCredentials('ghlMcpApi');
		const serverUrl = credentials.serverUrl as string;

		for (let i = 0; i < items.length; i++) {
			const operation = this.getNodeParameter('operation', i) as string;
			let method = '';
			let params: IDataObject = {};

			if (operation === 'createContact') {
				method = 'create_contact';
				params = {
					firstName: this.getNodeParameter('firstName', i),
					email: this.getNodeParameter('email', i),
					phone: this.getNodeParameter('phone', i),
				};
			} else if (operation === 'getContacts') {
				method = 'get_contacts';
				params = { limit: this.getNodeParameter('limit', i) };
			} else if (operation === 'createOpportunity') {
				method = 'create_opportunity_natural';
				params = {
					nome: this.getNodeParameter('contactName', i),
					telefone: this.getNodeParameter('oppPhone', i),
					pipeline_name: this.getNodeParameter('pipelineName', i),
					stage_name: this.getNodeParameter('stageName', i),
					valor: this.getNodeParameter('value', i),
				};
			} else if (operation === 'getPipelines') {
				method = 'get_pipelines';
				params = {};
			} else if (operation === 'sendSms') {
				method = 'send_sms';
				params = {
					contactId: this.getNodeParameter('contactId', i),
					message: this.getNodeParameter('message', i),
				};
			}

			const response = await this.helpers.request({
				method: 'POST',
				url: `${serverUrl}/mcp`,
				body: { method, params },
				json: true,
			});

			returnData.push(response.data || response);
		}

		return [this.helpers.returnJsonArray(returnData)];
	}
}
```

---

## ARQUIVO 6: README.md
**Caminho:** `README.md` (raiz)

```markdown
# n8n-nodes-ghl-mcp

Node para n8n que conecta ao GoHighLevel via MCP Server.

## Instalação

```bash
npm install n8n-nodes-ghl-mcp
```

## Configuração

No n8n, adicione credencial "GoHighLevel MCP API":
- MCP Server URL: `https://mcp-github.va1qz0.easypanel.host`
- API Key: Seu token do GHL
- Location ID: Seu Location ID

## Operações

- Criar Contato
- Listar Contatos
- Criar Oportunidade
- Ver Pipelines
- Enviar SMS
```

---

## PRONTO PARA VENDER

Depois de publicar, seus clientes instalam com:

```bash
npm install n8n-nodes-ghl-mcp
```

E só configuram as credenciais deles no n8n. ZERO complicação!

---

## COMANDOS FINAIS

Execute na ordem:

```bash
# 1. Vai pra pasta
cd n8n-nodes-ghl-mcp

# 2. Instala
npm install

# 3. Builda
npm run build

# 4. Publica
npm login
npm publish
```

ACABOU! Node pronto pra vender.
