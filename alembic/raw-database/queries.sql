-- Insertar un nuevo proceso
INSERT INTO Procesos (id, nombre, num_etapas) 
VALUES (1, 'Proceso de Ejemplo', 3);


-- Insertar etapas para el proceso recién creado
INSERT INTO Etapas (id, num_etapa, id_proceso) 
VALUES 
    (1, 1, 1), 
    (2, 2, 1), 
    (3, 3, 1);

-- Insertar entradas para cada etapa
INSERT INTO Entradas (id, nombre, tipo) 
VALUES 
    (1, 'Entrada 1', 'type1'),
    (2, 'Entrada 2', 'type2'),
    (3, 'Entrada 3', 'type3');

-- Asignar entradas a etapas
INSERT INTO Etapas_entradas (id_etapa, id_entrada) 
VALUES 
    (1, 1), -- Asigna Entrada 1 a la Etapa 1
    (2, 2), -- Asigna Entrada 2 a la Etapa 2
    (3, 3); -- Asigna Entrada 3 a la Etapa 3

-- Insertar indicadores
INSERT INTO Indicadores (id, nombre, tipo) 
VALUES 
    (1, 'Indicador A', 'type1'),
    (2, 'Indicador B', 'type2'),
    (3, 'Indicador C', 'type3');

INSERT INTO Indicadores_entradas (id, id_entrada, id_indicador) 
VALUES 
    (1, 1, 1), -- Relaciona Entrada 1 con Indicador A
    (2, 2, 2), -- Relaciona Entrada 2 con Indicador B
    (3, 3, 3); -- Relaciona Entrada 3 con Indicador C

-- Relacionar indicadores a entradas en la tabla Etapa_indicadores
INSERT INTO Etapa_indicadores (id_etapa, id_indicador_entrada) 
VALUES 
    (1, 1), -- Asigna Indicador_Entrada 1 a Etapa 1
    (2, 2), -- Asigna Indicador_Entrada 2 a Etapa 2
    (3, 3); -- Asigna Indicador_Entrada 3 a Etapa 3


-- PROCESO #2

-- Insertar un nuevo proceso
INSERT INTO Procesos (id, nombre, num_etapas) 
VALUES (2, 'Proceso de Ejemplo 2', 2);

-- Insertar etapas para el proceso recién creado
INSERT INTO Etapas (id, num_etapa, id_proceso) 
VALUES 
    (4, 1, 2),  -- Etapa 1 del Proceso 2
    (5, 2, 2);  -- Etapa 2 del Proceso 2

-- Insertar entradas para cada etapa
INSERT INTO Entradas (id, nombre, tipo) 
VALUES 
    (4, 'Entrada 4', 'type1'),
    (5, 'Entrada 5', 'type2');

-- Asignar entradas a etapas
INSERT INTO Etapas_entradas (id_etapa, id_entrada) 
VALUES 
    (4, 4), -- Asigna Entrada 4 a la Etapa 1
    (5, 5); -- Asigna Entrada 5 a la Etapa 2

-- Insertar indicadores
INSERT INTO Indicadores (id, nombre, tipo) 
VALUES 
    (4, 'Indicador D', 'type1'),
    (5, 'Indicador E', 'type2');

-- Relacionar entradas con indicadores
INSERT INTO Indicadores_entradas (id, id_entrada, id_indicador) 
VALUES 
    (4, 4, 1), -- Relaciona Entrada 4 con Indicador D
    (5, 5, 1); -- Relaciona Entrada 5 con Indicador E

-- Relacionar indicadores a entradas en la tabla Etapa_indicadores
INSERT INTO Etapa_indicadores (id_etapa, id_indicador_entrada) 
VALUES 
    (4, 4), -- Asigna Indicador_Entrada 4 a Etapa 1
    (5, 5); -- Asigna Indicador_Entrada 5 a Etapa 2


SELECT 
    p.id AS proceso_id,
    p.nombre AS proceso_nombre,
    e.num_etapa AS etapa_numero,
    i.nombre AS indicador_nombre
FROM 
    Procesos p
JOIN 
    Etapas e ON p.id = e.id_proceso
JOIN 
    Etapa_indicadores ei ON e.id = ei.id_etapa
JOIN 
    Indicadores_entradas ie ON ei.id_indicador_entrada = ie.id
JOIN 
    Indicadores i ON ie.id_indicador = i.id
WHERE 
    i.nombre = 'Indicador A';
