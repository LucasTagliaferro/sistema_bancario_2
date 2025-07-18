Sistema Bancário em Python v2

📖 Sobre
Este projeto é a segunda versão de um sistema bancário simples, desenvolvido como parte de um desafio de programação em Python. O objetivo principal foi refatorar um script inicial monolítico, transformando-o em um sistema modularizado e baseado em funções. O desafio também incluiu a implementação de novas funcionalidades e a aplicação de regras específicas na passagem de argumentos para cada função, explorando conceitos como positional-only e keyword-only arguments.

💻 Desafio Proposto
O desenvolvimento foi guiado pelos seguintes requisitos:

Modularização: Separar as operações de saque, depósito e extrato em funções distintas.
Novas Funcionalidades:
Criar Usuário (Cliente): Armazenar usuários em uma lista, impedindo o cadastro de CPFs duplicados.

Criar Conta Corrente: Armazenar contas em uma lista, vinculando cada conta a um usuário. Uma conta pertence a um único usuário, mas um usuário pode ter múltiplas contas.

Regras Específicas para Funções:
Depósito: A função deve receber os argumentos apenas por posição (positional-only).
Saque: A função deve receber os argumentos apenas por nome (keyword-only).
Extrato: A função deve receber argumentos por posição e nome (um argumento posicional e outro nomeado).

✨ Funcionalidades
Depositar: Adiciona valores à conta do usuário.
Sacar: Permite o saque de valores, respeitando um limite de R$ 500,00 por saque e um máximo de 3 saques diários.
Exibir Extrato: Mostra o histórico de transações e o saldo atual da conta.
Criar Novo Usuário: Cadastra um novo cliente com nome, data de nascimento, CPF e endereço.
Criar Nova Conta Corrente: Cria uma nova conta, associada a um usuário já cadastrado. O número da agência é fixo ("0001") e o número da conta é sequencial.
Listar Contas Cadastradas: Exibe uma lista com todas as contas e seus respectivos titulares.

🚀 Como Executar o Projeto
Pré-requisitos
Antes de começar, você vai precisar ter o Python 3 instalado em sua máquina.
