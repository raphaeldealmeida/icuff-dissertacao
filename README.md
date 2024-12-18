
## Dissertação

# IMPACTO DE DE MOCKS NO TESTE DE SOFTWARE

## Resumo
Diante da crescente complexidade dos sistemas de software e da diversidade de linguagens de programação, a qualidade do código torna-se um fator crucial para o sucesso de projetos. O uso de testes de software, em especial a prática de mocking, é fundamental para garantir a confiabilidade e a eficiência dos sistemas, permitindo isolar unidades de código e simular comportamentos de componentes externos. Este trabalho investiga o uso de ferramentas de mocking em quatro linguagens de programação, com o objetivo de compreender as tendências e práticas associadas a essa técnica de teste. Foram formuladas cinco questões de pesquisa que abordam desde a identificação das ferramentas mais utilizadas por linguagem até o impacto do uso de mocks na cobertura de código. A metodologia envolveu a análise de projetos open-source hospedados no GitHub, coletando dados sobre as ferramentas de mocking empregadas, frequência de uso, tipos de dependências simuladas e métricas de cobertura. Os resultados indicam que as ferramentas mais populares são o unittest para Python, Mocha para JavaScript, PHPUnit para PHP e Mockito para Java. Observou-se também que certas ferramentas são adotadas em conjunto, sugerindo sinergias entre elas. Notou-se uma alta frequência de uso de mocks em PHP, Java e JavaScript, enquanto em Python o uso não é proporcional ao número de testes, apontando para práticas de teste distintas. Além disso, constatou-se uma preferência por simular dependências externas, especialmente em projetos JavaScript, e que não há correlação significativa entre o uso de mocks e a cobertura de código. As implicações deste estudo são relevantes para desenvolvedores, que podem aprimorar suas práticas de teste, para mantenedores de ferramentas, que podem focar em funcionalidades demandadas, e para pesquisadores, que têm oportunidades para explorar novas métricas de qualidade e eficácia dos testes. Conclui-se que a compreensão aprofundada das práticas de mocking contribui significativamente para a melhoria da qualidade e eficiência dos testes de software.

## Instalação das dependências
```
pip install -r requirements.txt --user
```
## Uso

Alterar a variável ```PROG_LANG``` ao executar o script.

create_final_list.py
cloner.py
count_test_files.py
test_tool_by_descriptor.py
search_mock_use.py
dep_origins.py
graphics.py