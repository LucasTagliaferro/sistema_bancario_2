Sistema Bancário em Python (V3 - Orientado a Objetos)
📜 Descrição do Projeto
Este projeto é uma simulação de um sistema bancário interativo via terminal, desenvolvido em Python. O sistema evoluiu de uma abordagem puramente procedural para uma arquitetura robusta e modular utilizando os princípios da Programação Orientada a Objetos (POO).

O objetivo é demonstrar a aplicação de conceitos de POO como classes, objetos, herança, encapsulamento e abstração para criar um software mais organizado, reutilizável e fácil de manter.

✨ Funcionalidades Principais
O sistema permite que os usuários realizem as seguintes operações:

Gestão de Clientes e Contas:

[nu] - Criar novos usuários (clientes).

[nc] - Criar novas contas correntes, que são automaticamente vinculadas a um usuário existente.

[lc] - Listar todas as contas cadastradas no sistema.

Operações Bancárias:

[d] - Realizar depósitos em contas.

[s] - Efetuar saques, com validações de saldo, limite por saque e número máximo de saques diários.

[e] - Exibir um extrato detalhado com todas as transações realizadas e o saldo atual da conta.

Configurações da Conta:

[al] - (Nova Funcionalidade) - Permitir que o cliente altere seu próprio limite de valor por saque.

🚀 Novidades na Versão 3
Esta versão representa uma refatoração completa do sistema, focando na implementação de um modelo orientado a objetos. As principais atualizações são:

Refatoração para POO: O código foi reestruturado com classes para modelar as entidades do sistema:

Cliente e PessoaFisica: Para representar os usuários do banco.

Conta e ContaCorrente: Para encapsular os dados (saldo, agência, etc.) e os comportamentos (sacar, depositar) de uma conta.

Historico: Uma classe dedicada a gerenciar o histórico de transações de cada conta.

Transacao, Saque, Deposito: Classes que utilizam abstração para modelar os diferentes tipos de transações.

Nova Funcionalidade - Alterar Limite de Saque: Foi adicionada a opção [al] ao menu, permitindo ao usuário definir um novo valor para seu limite de saque, dando mais flexibilidade e controle sobre a conta.

Código Mais Limpo e Escalável: A lógica de negócios agora está encapsulada dentro dos métodos das classes, tornando a função main e as funções auxiliares mais limpas e focadas em orquestrar as interações entre os objetos.

🛠️ Tecnologias Utilizadas
Python 3: Linguagem principal do projeto.

Módulos Nativos:

textwrap: Para formatação do menu de texto.

datetime: Para registrar a data e hora de cada transação.

abc: Para a criação de Classes Base Abstratas (Transacao).

⚙️ Como Executar
1 Certifique-se de ter o Python 3 instalado em sua máquina.

2 Clone este repositório ou baixe o arquivo sistema_bancario_v3.py.

3 Abra um terminal ou prompt de comando na pasta onde o arquivo está localizado.

4 Execute o seguinte comando:

Bash

python sistema_bancario_v3.py

5 Siga as instruções apresentadas no menu interativo.