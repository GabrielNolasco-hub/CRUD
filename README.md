# Relatório CRUD

Este projeto implementa uma aplicação desktop para gerenciamento de produtos utilizando Python e Tkinter. A estrutura foi organizada de maneira modular, inspirada no padrão MVC, permitindo fácil manutenção e expansão.

## Estrutura do Projeto

O sistema foi dividido em três componentes principais:

### Model — Produto
Representa cada item cadastrado, contendo:
- id
- nome
- preço
- quantidade

### Controller — ProdutoController
Centraliza toda a lógica de funcionamento:
- Mantém a lista de produtos em memória
- Controla a geração automática de IDs
- Executa as operações de adicionar, listar, atualizar e remover
- Realiza busca de produtos por nome
- Inclui funções auxiliares para tratar valores monetários no formato brasileiro.

### View — ProdutoView
Interface gráfica construída com Tkinter:
- Campos de entrada
- Botões para cada operação
- Tabela Treeview para exibição dos produtos
- Filtro de busca em tempo real
- Botão "Limpar campos" para reiniciar o formulário rapidamente

## Métodos do CRUD

### Adicionar
Lê os dados digitados, valida as informações, cria um novo produto e o envia ao controller. O ID é gerado automaticamente. Após isso, a tabela é atualizada.

### Listar Todos
Recarrega toda a tabela, removendo dados anteriores e exibindo todos os produtos cadastrados.

### Atualizar
Permite editar um produto selecionado na tabela. O controller substitui os dados antigos pelos novos e a interface atualiza a exibição.

### Remover
Remove o produto selecionado após confirmação do usuário. A tabela é atualizada logo em seguida.

### Funcionalidades Extras
- Filtro de busca que filtra produtos pelo nome enquanto o usuário digita
- Botão "Limpar campos" para desfazer seleções rapidamente
- Tratamento de preços no formato brasileiro, aceitando vírgula ou ponto

## Decisões de Design

Algumas decisões foram tomadas para garantir organização e boa experiência de uso:

- Separação clara entre Model, View e Controller
- Uso de IDs automáticos para evitar erros e duplicações
- Implementação de Treeview para visualização mais organizada dos produtos
- Preenchimento automático dos campos ao selecionar um item na tabela
- Filtro de busca em tempo real para melhorar a navegação
- Funções auxiliares para garantir consistência no tratamento de valores numéricos

