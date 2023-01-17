DROP TABLE IF EXISTS post;

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    usuario TEXT NOT NULL
);

DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nome TEXT NOT NULL,
    atuacao TEXT,
    endereco TEXT,
    telefone TEXT,
    descricao TEXT,
    nascimento TEXT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);