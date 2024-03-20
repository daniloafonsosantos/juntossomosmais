# JUNTOSSOMOSMAIS
Repositório do Teste da Juntos somos Mais


Criado Autenticação por JWT 

Fiz a importação das duas formas pelo csv, pelo json ou das duas formas simultaneamente.

Notei que os dois arquivos possuem os mesmo dados, então não faz muito sentido importar os dois simultaneamente,

porém se houver algum caso com infomações diferentes, já está pronto também ;) ...

*** Pensei em fazer um SET (Coleções), para remover os registros duplicados nesses casos, 
    convertendo para coleções, depois voltaria para a mesma lista, mas achei melhor deixar os dados brutos ***


Depois de instalar as dependencia e executar a aplicação ir para o endereço com Swagger >>

http://127.0.0.1:8000/api/docs


Ir para Login User e acessar o unico endpoint POST /api/token e informar o Json para login abaixo:

{
"username": "juntossomosmais@juntossomosmais.com.br",
"password": "123"
}

ao copia o access_token retornado, to topo da página existe um botão Authorize, clique nesse botão,
abrirá uma tela, cole o Token em value e em seguida clique no botão Authorize, pronto, todos seus endpoint's foram autenticados com sucesso ;)


Finalmente clique em Eligibles no endpoint /api/eligibles/

Ao clicar em Try it out, ele preencherá alguns valores default's que poderão serem alterados a qualquer momento.

