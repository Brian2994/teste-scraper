-- Cria o banco de dados do projeto (execute apenas uma vez)
CREATE DATABASE teste_movida;

-- Mostra o nome de todas as tabelas salvas no seu banco de dados
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;

-- Consulta para ver se os dados realmente entraram na tabela fato e nas dimensões
SELECT 'fato_veiculos' AS tabela, COUNT(*) AS total_registros FROM fato_veiculos
UNION ALL
SELECT 'dim_marcas', COUNT(*) FROM dim_marcas
UNION ALL
SELECT 'dim_lojas', COUNT(*) FROM dim_lojas
UNION ALL
SELECT 'kpi_resumo_geral', COUNT(*) FROM kpi_resumo_geral;


-- Mostra os 10 primeiros veículos salvos com suas respectivas informações
SELECT id, marca, modelo, preco, quilometragem, loja, uf 
FROM fato_veiculos 
LIMIT 10;
