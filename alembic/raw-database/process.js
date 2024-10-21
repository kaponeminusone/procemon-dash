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
