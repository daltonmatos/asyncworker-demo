# Asyncworker Content Negotiation Demo

Prova de conceito da uma implementação de suporte a Content Negotiation
para handlers HTTP Asyncworker.

## O que funciona

Um `Resource` pode ser declarado como sendo o Resource princial, que é o que o handler retorna.

Esse resource declara quais versões ele possui, através do método `media_types()`, que retorna um dict
com pares `(<media_type>, <ResoouorceClass>)`.

## O que falta

* Poder associar um Resource com um status code
* Poder definir uma config que rejeita um request se o header `Accept` não estiver presente
    - Essa mesma opção poder também retornar o Resource principal caso esse header não exista
