# Descrição das url's

Os métodos principais são `/api/{modelo}` e `/api/{modelo}/id:{primary_key}/`. Nos campos entre chaves (`{ }`) devem ser substituidos strings que conferem o acesso a cada uma das tabelas apresentadas acima. A relação completa de url's é:
* [/api/veiculos/](http://localhost:8000/api/veiculos/): url associada à tabela de veiculos. 
* [/api/linhas/](http://localhost:8000/api/linhas/): url associada à tabela de linhas. 
* [/api/paradas/](http://localhost:8000/api/paradas/): url associada à tabela de paradas. 
* [/api/posicaoveiculos/](http://localhost:8000/api/posicaoveiculos/): url associada à tabela de posição dos veiculos. 
	* Todas as url's acima suportam as operações de `GET` (lista todas as insâncias da tabela), `POST` (insere novas instâncias na base de dados), `DELETE` (deleta todas as instancias da tabela)

Se qualquer uma das url's descritas acima forem acompanhadas de um `id`, é possível fazer uma das operações dentre `GET`, `PUT`, `PATCH` e `DELETE`. Por exemplo, a operação de `GET` sobre `/api/veiculos/id:1/` retorna a instância contida na tabela `api_veiculo` descrita pelo `id` igual a 1.

A API também conta com três outros métodos além dos que já foram descritos. Estes são:
* [/api/paradaslinhas/](http://localhost:8000/api/paradaslinhas/): url que provê acesso às paradas, acompanhadas de todas as linhas associadas.
* [/api/linhasveiculos/](http://localhost:8000/api/linhasveiculos/): url que provê acesso às linhas, acompanhadas de todas os veiculos associados.
	* As duas url's acima suportam a operação 'GET' (listagem de todas as instnâcias)
	* O acesso à instâncias específicas pode ser feito pelas urls `/api/paradaslinhas/id:{parada_id}/` ou `/api/linhasveiculos/id:{linha_id}`. Estes métodos suportam as operações `GET` (acesso à isntância), `PUT` (atualização de toda a instância) e `PATCH` (atualização apenas de campos específicos)
* `/api/paradasposicao/{lat}:{lon}/`: url que retorna as três paradas mais próximas às coordenadas passadas
	* Caso deseje-se acessar as `N` paradas mais próximas às coordenadas, utiliza-se a url `/api/paradasposicao/{lat}:{lon}/n:{n_paradas}/`

