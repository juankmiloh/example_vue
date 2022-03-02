<template>
  <ihh
    indicador="declaredDisponibility"
    title="Disponibilidad declarada"
    :descriptions="description"
  />
</template>
<script>
import ihh from '../ihh'
export default {
  components: {
    ihh
  }, data() {
    return {
      description: [
        { text: 'Índice Herfindall Hirschman, mide el nivel de concentración sobre en el mercado de disponibilidad declarada, considerando el portafolio de plantas de generación de cada uno de los agentes.' },
        { text: 'Cuota de mercado, mide la participación de cada uno de los agentes en el mercado de disponibilidad declarada, considerando su portafolio de plantas de generación.' }
      ]

    }
  }
}
</script>
