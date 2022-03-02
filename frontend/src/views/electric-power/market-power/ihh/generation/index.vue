<template>
  <ihh
    indicador="generacion"
    title="Generación real"
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
        { text: 'Índice Herfindall Hirschman, mide el nivel de concentración en el mercado de generación real, considerando el portafolio de plantas de generación de cada uno de los agentes.' },
        { text: 'Cuota de mercado, mide la participación de cada uno de los agentes en el mercado de generación, considerando los recursos de su portafolio.' }
      ]

    }
  }
}
</script>
