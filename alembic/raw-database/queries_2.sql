INSERT INTO entradas (id, nombre, tipo) VALUES
(10, 'Madera', 'type1'),  -- tipo 'int'
(11, 'Piedra', 'type1'),  -- tipo 'int'
(12, 'Plástico', 'type2'), -- tipo 'float'
(13, 'Metal', 'type2'),    -- tipo 'float'
(14, 'Vidrio', 'type1');   -- tipo 'int'

INSERT INTO indicadores (id, nombre, tipo) VALUES
(100, '¿Se encuentra en correcto estado?', 'type2'),  -- tipo 'checkbox'
(101, 'Cantidad de material dañado', 'type1'),        -- tipo 'range'
(102, '¿Requiere mantenimiento?', 'type2'),            -- tipo 'checkbox'
(103, 'Nivel de calidad', 'type3'),                    -- tipo 'criteria'
(104, '¿Es reciclable?', 'type2');                     -- tipo 'checkbox'


