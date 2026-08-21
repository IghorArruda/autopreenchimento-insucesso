# ⚡ AutoPreenchimento - Insucesso de Atividades

Aplicacao web desenvolvida para **automatizar a formatacao de insucessos de atividades de campo**, eliminando o trabalho manual de reescrever informacoes e reduzindo o tempo de execucao em ate **80%**.

> 🔒 **Nota:** Este e um projeto de portfolio. Todos os dados de demonstracao sao ficticios.

---

## 🎯 Problema Resolvido

Profissionais de campo precisam, diariamente, converter textos brutos de rotas em mensagens formatadas para comunicacao (WhatsApp). Esse processo:
- Levava **5-10 minutos** por ocorrencia
- Gerava erros de digitacao e omissao de dados
- Nao tinha padronizacao entre tecnicos

**Resultado:** App que extrai dados automaticamente e gera o texto formatado em **segundos**.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|------------|-----|
| Python | Logica de negocio e parse de dados |
| Streamlit | Interface web responsiva |
| Regex | Extracao automatica de informacoes do texto bruto |
| Session State | Gerenciamento de estado da aplicacao |

---

## ⚡ Funcionalidades

- **📋 Seletor de Modelo:** Chamado, Chamado Modem, Preventiva, Instalacao, Retirada
- **📥 Parse Automatico:** Cola o texto da rota e o app extrai data, cliente, PC, chamado, SAP, modelo, endereco, etc.
- **✏️ Campos Manuais:** Solicitante, motivo, contato no local e confirmacao de ligacao
- **📋 Geracao Instantanea:** Texto formatado pronto para copiar e colar no WhatsApp
- **🎨 Interface Visual:** Cards, badges de status e preview estilizado

---

## 🚀 Como Executar

```bash
git clone https://github.com/IghorArruda/autopreenchimento-insucesso.git
cd autopreenchimento-insucesso
pip install -r requirements.txt
streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
autopreenchimento-insucesso/
├── app.py              # Aplicacao principal
├── requirements.txt    # Dependencias
└── README.md           # Documentacao
```

---

## 📫 Contato

- 💼 [LinkedIn](https://www.linkedin.com/in/ighor-arruda-77877824/)
- 🌐 [Portfolio](https://ighorarruda.github.io)
- 📧 ighor_arruda@hotmail.com

---

**Desenvolvido por:** Ighor Arruda
