-- 1. Criar a tabela clientes
CREATE TABLE clientes (
  id SERIAL PRIMARY KEY,
  nome TEXT
);

-- 2. Inserir dados fictícios (250.000 "Mario" e 250.000 "João")
INSERT INTO clientes (nome)
SELECT 'Mario' FROM generate_series(1, 250000);

INSERT INTO clientes (nome)
SELECT 'João' FROM generate_series(1, 250000);

-- 3. Verificar o plano de execução ANTES de criar o índice
EXPLAIN ANALYZE
SELECT * FROM clientes WHERE nome = 'João';

-- 4. Criar índice no campo nome
CREATE INDEX idx_nome ON clientes(nome);

-- 5. Verificar o plano de execução DEPOIS de criar o índice
EXPLAIN ANALYZE
SELECT * FROM clientes WHERE nome = 'João';
