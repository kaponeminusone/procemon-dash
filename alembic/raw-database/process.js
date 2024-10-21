proceso = 
{
  "nombre": "Proceso de Producción",
  "etapas": [
    {
      "num_etapa": 1,
      "entradas": [
        {
          "id": 10  // Madera
        }
      ],
      "indicadores": [
        {
          "id": 100,  // Indicador 1
          "entrada_id": 10  // Madera
        },
        {
          "id": 101,  // Indicador 1
          "entrada_id": 10  // Madera
        }
      ],
      "salidas": [
        {
          "id": 11  // Suponiendo que tienes una salida con id 11
        }
      ]
    },
    {
      "num_etapa": 2,
      "entradas": [
        {
          "id": 11  // Piedra
        }
      ],
      "indicadores": [
        {
          "id": 101,  // Indicador 2
          "entrada_id": 11  // Piedra
        }
      ],
      "salidas": [
        {
          "id": 12  // Suponiendo que tienes una salida con id 12
        }
      ]
    },
    {
      "num_etapa": 3,
      "entradas": [
        {
          "id": 12  // Metal
        }
      ],
      "indicadores": [
        {
          "id": 100,  // Indicador 1
          "entrada_id": 12  // Metal
        }
      ],
      "salidas": [
        {
          "id": 13  // Suponiendo que tienes una salida con id 13
        }
      ]
    }
  ]
}

proceso_submited = 
{
  "id_proceso": 1,
  "etapas": [
    {
      "num_etapa": 1,
      "entradas": [
        {
          "id": 10,
          "value": 320
        }
      ],
      "indicadores": [
        {
          "id": 100,
          "entrada_id": 10,
          "chekbox": true,
          "range": "10-50"
        },
        {
          "id": 101,
          "entrada_id": 10,
          "checkbox": true,
          "criteria": ">300"
        }
      ],
      "salidas": [
        {
          "id": 11,
          "value": 40.0
        }
      ]
    },
    {
      "num_etapa": 2,
      "entradas": [
        {
          "id": 11,
          "value": 100.5
        }
      ],
      "indicadores": [
        {
          "id": 101,
          "entrada_id": 11,
          "chekbox": true,
        }
      ],
      "salidas": [
        {
          "id": 12,
          "value": 20
        }
      ]
    },
    {
      "num_etapa": 3,
      "entradas": [
        {
          "id": 12,
          "value": 10
        }
      ],
      "indicadores": [
        {
          "id": 100,
          "entrada_id": 12,
          "criteria": "=10"
        }
      ],
      "salidas": [
        {
          "id": 13,
          "value": 1
        }
      ]
    }
  ]
}



proceso_executed = 
{
  "id_proceso_ejecutado": 12,
  "id_proceso": 1,
  "no_conformes": 100,
  "conformes": 200,
  "num_etapas": 3,
  "etapas": [
    {
      "num_etapa": 1,
      "conformes": 20,
      "no_conformes": 100,
      "state": false,
      "entradas": [
        {
          "id": 10,
          "value": 320
        }
      ],
      "indicadores": [
        {
          "id": 100,
          "entrada_id": 10,
          "chekbox": true, //Puede o no tener este campo
          "range": "10-50",   // Puede o no tener este campo
          "state": false
        },
        {
          "id": 101,
          "entrada_id": 10,
          "checkbox": true, //Puede o no tener este campo
          "criteria": ">300",   //Puede o no tener este campo
          "state": true
        }
      ],
      "salidas": [
        {
          "id": 11,
          "value": 40.0
        }
      ]
    },
    {
      "num_etapa": 2,
      "conformes": 50,
      "no_conformes": 1,
      "state": true,
      "entradas": [
        {
          "id": 11,
          "value": 100.5
        }
      ],
      "indicadores": [
        {
          "id": 101,
          "entrada_id": 11,
          "chekbox": true, //Puede o no tener este campo
          "state": true,
        }
      ],
      "salidas": [
        {
          "id": 12,
          "value": 20
        }
      ]
    },
    {
      "num_etapa": 3,
      "conformes": 300,
      "no_conformes": 13,
      "state": true,
      "entradas": [
        {
          "id": 12,
          "value": 10
        }
      ],
      "indicadores": [
        {
          "id": 100,
          "entrada_id": 12,
          "criteria": "=10", //Puede o no tener este campo
          "status": false
        }
      ],
      "salidas": [
        {
          "id": 13,
          "value": 1
        }
      ]
    }
  ]
}

