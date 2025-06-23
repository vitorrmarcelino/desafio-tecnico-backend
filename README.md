# Desafio Pipeline de Dados EX-001

## Visão Geral
Este desafio prático visa validar competências de:

1. **Modelagem de Banco de Dados** (PostgreSQL)
2. **Ingestão de Dados via MQTT** com Python (broker MQTT configurado para MQTT)
3. **Visualização de KPIs** em Grafana (ou Power BI)

Os dados de operação da máquina **EX-001** são transmitidos automaticamente a cada 5 minutos por um ambiente MQTT em nuvem. Seu trabalho é **processar** essas informações e **criar** o dashboard de OEE (e demais KPIs).

Você receberá credenciais (host, porta, usuário e senha) para esse ambiente MQTT, que publica mensagens no tópico `ECOPLUS/EX-001/dados`. Seu objetivo é:

- Consumir essas mensagens JSON
- Persisti-las em PostgreSQL
- Criar dashboards com os KPIs abaixo:
  - **Disponibilidade**
  - **Performance** (meta: 100 peças/hora)
  - **Qualidade**
  - **OEE**
  - **Total de peças produzidas**
  - **Total de peças defeituosas**

Para testar e depurar a conexão MQTT, recomendamos instalar o [**MQTT Explorer**](https://mqtt-explorer.com) ou qualquer outro cliente de sua preferência.

## Estrutura do Repositório

```
├── README.md
├── .env.example
├── docker-compose.yml
├── ingestion/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
├── db/
│   └── init.sql
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── datasources.yml
│   │   └── dashboards/
│   │       └── dashboard_oee.json
└── docs/
├── architecture_diagram.png
└── architecture_diagram.md
```

## Requisitos
- Docker e Docker Compose instalados
- Acesso ao broker MQTT (credenciais serão fornecidas)
- Git
- MQTT Client (opcional, para debug)

## Configuração
1. Copie o arquivo de exemplo de variáveis de ambiente:
    ```bash
    cp .env.example .env
    ```

2. Preencha `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER` e `MQTT_PASS` com as credenciais do broker MQTT:
    ```
    - MQTT_HOST = mqtt.ecoplus-apps.com
    - MQTT_PORT = 1883
    - MQTT_USER = ecoplus-teste:temp_user
    - MQTT_PASS = u9JJ8d8DOp
    ```

## Preparação do ambiente

```bash
# Na raiz do projeto
docker-compose up --build
```

Isso irá:

* Iniciar o serviço PostgreSQL e executar o script de criação de tabelas (`db/init.sql`).
* Subir o serviço Python de ingestão, que se conecta ao broker MQTT via MQTT e persiste os dados no banco.
* Executar o Grafana com provisionamento automático de data source.

## Execução

1. Abra o MQTT Client e conecte-se usando as credenciais definidas em `.env`;
2. Confirme o recebimento de mensagens JSON no tópico `ECOPLUS/EX-001/dados`, por exemplo:

   ```json
   {
     "id_maquina": 1,
     "datahora": "2025-01-01T12:00:00-03:00",
     "ligada": true,
     "operacao": true,
     "manutencao_corretiva": false,
     "manutencao_preventiva": false,
     "pecas_produzidas": 9,
     "pecas_defeituosas": 1
   }
   ```
3. Verifique nos logs do container `ingestion` e banco de dados `postgres` se a mensagem foi processada e inserida;
4. Acesse o Grafana em `http://localhost:3000` (usuário/senha: `admin`/`admin`);
5. Crie o dashboard **OEE** com os KPIs especificados na próximo tópico;
6. Aplique seleção de tempo `time picker` nas queries SQL configuradas nos painéis, como no exemplo abaixo:
```sql
SELECT *
FROM dados_maquina
WHERE $__timeFilter(datahora)
```
7. Documente os passos da criação e execução da solução em um arquivo Markdown de forma clara e objetiva;
8. Documente também o resultado final do dashboard (prints e arquivo `.json` de import são bem vindos) e os registros de dados, da forma que preferir;

## KPIs considerados

### A partir dos dados aferidos e registrados, crie um dashboard com os seguintes indicadores:

* **Disponibilidade**: % de tempo em que a máquina esteve pronta para operar (sem paradas, desligamentos e manutenções).
* **Performance**: (peças boas produzidas/hora) ÷ (meta de produção) × 100
* **Qualidade**: (peças boas ÷ peças produzidas) × 100
* **OEE**: Disponibilidade × Performance × Qualidade
* **Total de peças produzidas**: soma de `pecas_produzidas` no intervalo.
* **Total de peças defeituosas**: soma de `pecas_defeituosas` no intervalo.
> Obs: Meta de produção = 100 peças/hora.

#### Mais informações sobre indicadores em [OEE Factors](https://www.oee.com/oee-factors).

---
 
### Demonstre sua capacidade de resolução de problemas e análise de dados com a criação desse dashboard e nos envie os resultados! 
### Encaminhe seu projeto para o seu contato da ECO+, com cópia para rh@ecoautomacao.com.br. 
## Boa sorte!
