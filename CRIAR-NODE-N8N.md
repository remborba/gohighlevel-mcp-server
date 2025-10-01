# Criar Node Community do n8n para GoHighLevel MCP

## O Que Vamos Criar

Um node do n8n que qualquer pessoa instala e usa, conectando no SEU servidor MCP.

**Vantagens:**
- Instala com `npm install n8n-nodes-ghl-mcp`
- Aparece como node nativo no n8n
- Cada usuário configura suas credenciais
- Usa o servidor MCP que você já tem rodando

---

## Estrutura do Projeto

Crie uma nova pasta chamada `n8n-nodes-ghl-mcp` ao lado da pasta `gohighlevel-mcp`.

```
n8n-nodes-ghl-mcp/
├── package.json
├── tsconfig.json
├── .npmignore
├── README.md
├── nodes/
│   └── GhlMcp/
│       ├── GhlMcp.node.ts
│       └── GhlMcp.node.json
└── credentials/
    └── GhlMcpApi.credentials.ts
```

---

## Arquivos Para Criar

### 1. package.json

```json
{
  "name": "n8n-nodes-ghl-mcp",
  "version": "1.0.0",
  "description": "n8n node to connect to GoHighLevel MCP Server",
  "keywords": [
    "n8n-community-node-package",
    "gohighlevel",
    "mcp"
  ],
  "license": "MIT",
  "homepage": "https://github.com/remborba/n8n-nodes-ghl-mcp",
  "author": {
    "name": "Remborba",
    "email": "seu@email.com"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/remborba/n8n-nodes-ghl-mcp.git"
  },
  "main": "index.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch"
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
    "@types/node": "^18.16.0",
    "n8n-workflow": "^1.0.0",
    "typescript": "^5.0.0"
  },
  "peerDependencies": {
    "n8n-workflow": "*"
  }
}
```

### 2. tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2019",
    "module": "commonjs",
    "lib": ["ES2019"],
    "outDir": "./dist",
    "rootDir": "./",
    "declaration": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["nodes/**/*", "credentials/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 3. .npmignore

```
src/
tsconfig.json
*.ts
!dist/**/*.d.ts
node_modules/
```

### 4. credentials/GhlMcpApi.credentials.ts

```typescript
import {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class GhlMcpApi implements ICredentialType {
	name = 'ghlMcpApi';
	displayName = 'GoHighLevel MCP API';
	documentationUrl = 'https://github.com/remborba/n8n-nodes-ghl-mcp';
	properties: INodeProperties[] = [
		{
			displayName: 'MCP Server URL',
			name: 'mcpServerUrl',
			type: 'string',
			default: 'https://mcp-github.va1qz0.easypanel.host',
			required: true,
			description: 'URL do servidor MCP (deixe o padrão se for usar o servidor público)',
		},
		{
			displayName: 'GHL API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
			description: 'Seu GoHighLevel API Key',
		},
		{
			displayName: 'GHL Location ID',
			name: 'locationId',
			type: 'string',
			default: '',
			required: true,
			description: 'Seu GoHighLevel Location ID',
		},
	];

	test: ICredentialTestRequest = {
		request: {
			baseURL: '={{$credentials.mcpServerUrl}}',
			url: '/mcp',
			method: 'POST',
			body: {
				method: 'get_contacts',
				params: { limit: 1 },
			},
		},
	};
}
```

### 5. nodes/GhlMcp/GhlMcp.node.json

```json
{
  "node": "n8n-nodes-base.ghlMcp",
  "nodeVersion": "1.0",
  "codexVersion": "1.0",
  "categories": ["CRM"],
  "resources": {
    "primaryDocumentation": [
      {
        "url": "https://github.com/remborba/n8n-nodes-ghl-mcp"
      }
    ]
  }
}
```

### 6. nodes/GhlMcp/GhlMcp.node.ts

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
		icon: 'file:ghl.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Interact with GoHighLevel via MCP Server',
		defaults: {
			name: 'GoHighLevel MCP',
		},
		inputs: ['main'],
		outputs: ['main'],
		credentials: [
			{
				name: 'ghlMcpApi',
				required: true,
			},
		],
		properties: [
			// Resource
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Contact',
						value: 'contact',
					},
					{
						name: 'Opportunity',
						value: 'opportunity',
					},
					{
						name: 'SMS',
						value: 'sms',
					},
				],
				default: 'contact',
			},

			// CONTACT OPERATIONS
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['contact'],
					},
				},
				options: [
					{
						name: 'Create',
						value: 'create',
						description: 'Create a new contact',
						action: 'Create a contact',
					},
					{
						name: 'Get Many',
						value: 'getAll',
						description: 'Get many contacts',
						action: 'Get many contacts',
					},
				],
				default: 'create',
			},

			// Contact - Create Fields
			{
				displayName: 'First Name',
				name: 'firstName',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['contact'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Email',
				name: 'email',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['contact'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'phone',
				type: 'string',
				displayOptions: {
					show: {
						resource: ['contact'],
						operation: ['create'],
					},
				},
				default: '',
			},

			// Contact - Get Many
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				displayOptions: {
					show: {
						resource: ['contact'],
						operation: ['getAll'],
					},
				},
				typeOptions: {
					minValue: 1,
					maxValue: 100,
				},
				default: 10,
			},

			// OPPORTUNITY OPERATIONS
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['opportunity'],
					},
				},
				options: [
					{
						name: 'Create',
						value: 'create',
						description: 'Create an opportunity',
						action: 'Create an opportunity',
					},
					{
						name: 'Get Many',
						value: 'getAll',
						description: 'Get many opportunities',
						action: 'Get many opportunities',
					},
					{
						name: 'Get Pipelines',
						value: 'getPipelines',
						description: 'Get all pipelines',
						action: 'Get all pipelines',
					},
				],
				default: 'create',
			},

			// Opportunity - Create
			{
				displayName: 'Contact Name',
				name: 'contactName',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['opportunity'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Phone',
				name: 'phone',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['opportunity'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Pipeline Name',
				name: 'pipelineName',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['opportunity'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Stage Name',
				name: 'stageName',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['opportunity'],
						operation: ['create'],
					},
				},
				default: '',
			},
			{
				displayName: 'Value',
				name: 'value',
				type: 'number',
				displayOptions: {
					show: {
						resource: ['opportunity'],
						operation: ['create'],
					},
				},
				default: 0,
			},

			// SMS OPERATIONS
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				displayOptions: {
					show: {
						resource: ['sms'],
					},
				},
				options: [
					{
						name: 'Send',
						value: 'send',
						description: 'Send an SMS',
						action: 'Send an SMS',
					},
				],
				default: 'send',
			},

			// SMS - Send
			{
				displayName: 'Contact ID',
				name: 'contactId',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['sms'],
						operation: ['send'],
					},
				},
				default: '',
			},
			{
				displayName: 'Message',
				name: 'message',
				type: 'string',
				required: true,
				displayOptions: {
					show: {
						resource: ['sms'],
						operation: ['send'],
					},
				},
				default: '',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: IDataObject[] = [];
		const resource = this.getNodeParameter('resource', 0) as string;
		const operation = this.getNodeParameter('operation', 0) as string;

		const credentials = await this.getCredentials('ghlMcpApi');
		const mcpServerUrl = credentials.mcpServerUrl as string;

		for (let i = 0; i < items.length; i++) {
			try {
				let method = '';
				let params: IDataObject = {};

				if (resource === 'contact') {
					if (operation === 'create') {
						method = 'create_contact';
						params = {
							firstName: this.getNodeParameter('firstName', i),
							email: this.getNodeParameter('email', i),
							phone: this.getNodeParameter('phone', i),
						};
					} else if (operation === 'getAll') {
						method = 'get_contacts';
						params = {
							limit: this.getNodeParameter('limit', i),
						};
					}
				}

				if (resource === 'opportunity') {
					if (operation === 'create') {
						method = 'create_opportunity_natural';
						params = {
							nome: this.getNodeParameter('contactName', i),
							telefone: this.getNodeParameter('phone', i),
							pipeline_name: this.getNodeParameter('pipelineName', i),
							stage_name: this.getNodeParameter('stageName', i),
							valor: this.getNodeParameter('value', i),
						};
					} else if (operation === 'getAll') {
						method = 'get_opportunities';
						params = {};
					} else if (operation === 'getPipelines') {
						method = 'get_pipelines';
						params = {};
					}
				}

				if (resource === 'sms') {
					if (operation === 'send') {
						method = 'send_sms';
						params = {
							contactId: this.getNodeParameter('contactId', i),
							message: this.getNodeParameter('message', i),
						};
					}
				}

				const response = await this.helpers.request({
					method: 'POST',
					url: `${mcpServerUrl}/mcp`,
					body: {
						method,
						params,
					},
					json: true,
				});

				returnData.push(response.data || response);
			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({ error: error.message });
					continue;
				}
				throw error;
			}
		}

		return [this.helpers.returnJsonArray(returnData)];
	}
}
```

### 7. README.md

```markdown
# n8n-nodes-ghl-mcp

Node community do n8n para integração com GoHighLevel via servidor MCP.

## Instalação

```bash
npm install n8n-nodes-ghl-mcp
```

Ou no n8n self-hosted:

```bash
cd ~/.n8n/nodes
npm install n8n-nodes-ghl-mcp
```

Reinicie o n8n.

## Configuração

1. No n8n, adicione credencial "GoHighLevel MCP API"
2. Configure:
   - **MCP Server URL:** `https://mcp-github.va1qz0.easypanel.host` (ou sua URL)
   - **GHL API Key:** Seu token do GoHighLevel
   - **GHL Location ID:** Seu Location ID

## Recursos

### Contacts
- Create: Criar novo contato
- Get Many: Listar contatos

### Opportunities
- Create: Criar oportunidade
- Get Many: Listar oportunidades
- Get Pipelines: Ver pipelines

### SMS
- Send: Enviar SMS

## Como Publicar

```bash
npm run build
npm publish
```

## Licença

MIT
```

---

## Como Usar

### 1. Criar o Projeto

```bash
# Criar pasta
mkdir n8n-nodes-ghl-mcp
cd n8n-nodes-ghl-mcp

# Copiar todos os arquivos acima
# Criar as pastas nodes/GhlMcp e credentials

# Instalar dependências
npm install
```

### 2. Build

```bash
npm run build
```

### 3. Testar Localmente no n8n

```bash
# No seu n8n self-hosted
cd ~/.n8n/nodes  # Linux/Mac
# ou
cd %USERPROFILE%\.n8n\nodes  # Windows

# Link o node
npm link ../caminho/para/n8n-nodes-ghl-mcp

# Reinicia n8n
```

### 4. Publicar no npm

```bash
npm login
npm publish
```

---

## Distribuir

Depois de publicar, qualquer pessoa instala com:

```bash
npm install n8n-nodes-ghl-mcp
```

E usa normalmente no n8n, só configurando as credenciais deles!

---

## Quer que Eu Crie os Arquivos Agora?

Posso criar tudo isso pra você, ou prefere fazer manualmente seguindo o guia?
