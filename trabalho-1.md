# INE5429 Trabalho 1

<center>**Aluno**: Gabriel Sartori Rangel (22100617)</center>

<center>Florianópolis, 28 de agosto de 2026</center>

# Análise de Segurança do Sistema de Autenticação da Google

A empresa Google oferece um serviço de autenticação de usuários para uma extensa lista de serviços próprios e terceirizados. Dentre os múltiplos serviços disponibilizados, esta análise se centrará em torno de:

- Autenticação para acesso de dados armazenados por usuários [1]
- Autenticação em aplicações de terceiros [1]
- Armazenamento em nuvem [1]
- Transações financeiras [1]

## Ativos

Dado que a empresa oferece seus serviços para diversas outras aplicações externas, além de se propor a armazenar dados arbitrários de usuários, nota-se que a empresa possui tanto ativos tangíveis quanto intangíveis para proteger.

O mais importante desses ativos é a sua reputação. A Google domina significativamente a área de manegamento e rastreamento de usuários pela internet. Desde o manejo interno para aprimoramento dos próprios serviços até o serviço de coletar e análisar os dados que descrevem como pessoas navegam pela internet. O domínio da empresa nessa área depende essencialmente da confiança depositada em sua capacidade de lidar com essas informações de forma responsável.

Além disso, a empresa oferece diversas formas de armazenamento de dados, como emails, fotos e arquivos genéricos. Esse grande volume de dados é privado para seus respectivos usuários e deve estar consistentemente disponível. Dessa forma, a privacidade e integridade dos sistemas são ativos de suma importância para o funcionamento da empresa.

Por fim, o serviço de gerenciar transações financeiras evidencia os dados e recursos econômicos de seus usuários como ativos valiosos. É preciso garantir que os dados sensíveis como detalhes de cartões de crédito não sejam compartilhados, além de manter a consistência com os valores monetários em posse dos usuários.

## Adversários

Ao observar a grande lista de ativos sob controle da empresa, diversos agentes possuem interesse para explorar falhas se segurança no sistema de forma a abusar ou alterar as informações armazenadas.

Um principal grupo de possíveis atacantes são indivíduos que buscam coletar informações sensíveis de usuários da internet. O acesso indevido a esse tipo de informação pode levar à sua venda para entidades mal intecionadas ou à prática de fraude diretamente.

Outro grupo relevante consiste de usuários mal intencionados, que buscam acessar as informações pessoais de outros usuários indevidamente. Dessa forma, os ativos de propriedade direta dos usuários da plataforma entra em risco de serem vazados. Isso pode levar a ocorrência de crimes em direção à vitima do vazamento, como assédio ou chantagem.

Também há uma pequena parcela de usuários a serem considerados: funcionários internos da empresa. Apesar de estarem em número reduzido e controlado pela própria empresa, indíviduos com acesso direto ao sistema podem causar danos mais significativos antes que contramedidas consigam entrar em prática. Este grupo normalmente está motivado pela busca por autorizações indevidas ou até mesmo um crime organizado com outras entidades.

## Gerenciamento de Risco

Visto o quão importante é a reputação da empresa para garantir sua influência no mercado, a segurança dos dados manejados é de absoluta importância. Isso pois, a perca da reputação resultaria na diminuição do uso da plataforma e redução na influência e domínio da empresa na internte. Esse é um custo indireto altíssimo, que coloca em risco todo o valor da empresa.

Além do custo indireto, é necessário considerar custos diretos como indenizações a usuários lesados por vazamentos de dados. Por examplo, milhões de dólares foram pagos em indenizações após a empresa admitir que bugs em seu sistema levaram ao vazamento de dados pessoais como nomes completos e endereços em 2018 [2].

Dessa forma, a atenção à integridade e proteção dos dados manejados pela empresa é essencial. Ela deve ser aplicada continuamente ao longo de todas as partes do sistema, desde os funcionários que mantém seu funcionamento até à interface de acesso dos usuários.

## Contramedidas

De forma a garantir a segurança da informação, a empresa aplica diversos métodos para validar a identidade dos usuários e assegurar funcionamento correto de suas plataformas.

A contramedida mais conhecida pelos usuários engloba as diversas etapadas envolvidas na autenticação de um usuário. O uso da autenticação de dois fatores e a atenção para senhas fracas ou velhas são exemplos de ações tomadas no lado do usuário para previnir acesso indevido à sua conta.

Por outro lado, os servidores da empresa precisam estar sob constante monitoramento para identificar atividade suspeita. O acesso a contas vindo de dispositivos desconhecidos é um possível identificador de que algo está errado. A Google mantém diversas formas de rastrear e identificar atividade suspeita, principalmente com o uso de machine learning.

Outra forma da empresa se proteger é por meio de sua arquitetura de zero confiança [3]. Nenhum dispositivo da empresa possui privilégio de acesso inerente. Para que os funcionários possam desempenhar suas funções, a atenticação deve ser feita por meio de seus usuários e outros elementos contextuais, como horário e localização do dispositivo. Dessa forma, o mero acesso físico a um dispositivo não permite que um agente mal intencionado aja de forma anonima internamente.

## Custo Benefício

A Google é pioneira no desenvolvimento de técnicas de segurança computacional. Esse pioneirismo tem um custo que tem se mostrado suficientemente rentável para que a empresa se torne uma gigante multinacional.

Tanto o custo direto para desenvolvimento dessas técnicas como o custo indireto para manter o funcionamento dos mecanismos de segurança desenvolvidos devem ser enxergados como uma despesa no mercado que a empresa busca se consolidar. É importante considerar que agentes mal intencionados possuem outros incentivos para não agirem em certos cenários além da resiliência de seu alvo. Por exemplo, no caso do ataque de insiders, é necessário levar em conta que o fácil rastreamento do crime e a consequência jurídica associada servem como camadas de proteção que não envolvem custo em segurança computacional, facilitando o processo.

Porém, é evidente que a reputação da empresa se mantém sobre o gerenciamento seguro de informações, fazendo com que o gasto com segurança seja, na verdade, um investimento.

## Bibliografia

1. Produtos e Serviços do Google. Disponível em: https://about.google/intl/pt_ALL/products/
1. **CISO MAG.** Google Agrees to Pay US$ 7.5M Over Google+ Data Breaches, 10 jan. 2020. Disponível em Google Agrees to Pay US$ 7.5M Over Google+ Data Breaches
1. Segurança Corporativa de Confiança Zero do BeyondCorp. Disponível em https://cloud.google.com/beyondcorp?hl=pt-BR

