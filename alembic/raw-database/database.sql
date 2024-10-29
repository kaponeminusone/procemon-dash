-- CREATE DATABASE dashdatav2;

-- Define enum types
CREATE TYPE tipo_enum AS ENUM ('type1', 'type2', 'type3');

-- Tabla Indicadores
CREATE TABLE IF NOT EXISTS Indicadores (
  id bigint PRIMARY KEY,
  nombre text NOT NULL,
  tipo tipo_enum NOT NULL
);

-- Tabla Entradas
CREATE TABLE IF NOT EXISTS Entradas (
  id bigint PRIMARY KEY,
  nombre text,
  tipo tipo_enum
);

-- Tabla Procesos
CREATE TABLE IF NOT EXISTS Procesos (
  id bigint PRIMARY KEY,
  nombre text NOT NULL,
  num_etapas integer
);

-- Tabla Etapas
CREATE TABLE IF NOT EXISTS Etapas (
  id bigint PRIMARY KEY,
  num_etapa bigint NOT NULL,
  id_proceso bigint,
  FOREIGN KEY (id_proceso) REFERENCES Procesos(id)
);

-- Tabla Usuario
CREATE TABLE IF NOT EXISTS Usuario (
  id bigint PRIMARY KEY,
  nombre text NOT NULL,
  email text NOT NULL,
  tipo tipo_enum NOT NULL
);

-- Tabla Etapa_indicadores
CREATE TABLE IF NOT EXISTS Etapa_indicadores (
  id_etapa bigint NOT NULL,
  id_indicador_entrada bigint NOT NULL,
  FOREIGN KEY (id_etapa) REFERENCES Etapas(id),
  FOREIGN KEY (id_indicador_entrada) REFERENCES Indicadores(id)
);

-- Tabla Etapas_entradas
CREATE TABLE IF NOT EXISTS Etapas_entradas (
  id_etapa bigint NOT NULL,
  id_entrada bigint NOT NULL,
  FOREIGN KEY (id_etapa) REFERENCES Etapas(id),
  FOREIGN KEY (id_entrada) REFERENCES Entradas(id)
);

-- Tabla Etapas_salidas
CREATE TABLE IF NOT EXISTS Etapas_salidas (
  id_etapa bigint NOT NULL,
  id_entrada bigint,
  FOREIGN KEY (id_etapa) REFERENCES Etapas(id),
  FOREIGN KEY (id_entrada) REFERENCES Entradas(id)
);

-- Tabla Indicadores_entradas
CREATE TABLE IF NOT EXISTS Indicadores_entradas (
  id bigint PRIMARY KEY,
  id_entrada bigint NOT NULL,
  id_indicador bigint,
  FOREIGN KEY (id_entrada) REFERENCES Entradas(id),
  FOREIGN KEY (id_indicador) REFERENCES Indicadores(id)
);

-- Tabla Registro
CREATE TABLE IF NOT EXISTS Registro (
  id bigint PRIMARY KEY,
  id_usuario bigint NOT NULL,
  descripcion text,
  creado timestamp DEFAULT now(),
  modificado timestamp DEFAULT now(),
  FOREIGN KEY (id_usuario) REFERENCES Usuario(id)
);

-- Tabla Registro_entradas
CREATE TABLE IF NOT EXISTS Registro_entradas (
  id_registro bigint PRIMARY KEY,
  id_entrada bigint,
  FOREIGN KEY (id_entrada) REFERENCES Entradas(id)
);

-- Tabla Registro_indicadores
CREATE TABLE IF NOT EXISTS Registro_indicadores (
  id_registro bigint PRIMARY KEY,
  id_indicador bigint,
  FOREIGN KEY (id_indicador) REFERENCES Indicadores(id)
);

-- Tabla Registro_procesos
CREATE TABLE IF NOT EXISTS Registro_procesos (
  id_registro bigint PRIMARY KEY,
  id_proceso bigint,
  FOREIGN KEY (id_proceso) REFERENCES Procesos(id)
);
