<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="24" justify="center">
      <el-col :span="16" :offset="4">
        <img
          width="100%"
          style="padding-top: 20px;"
          :src="imageUmmeg"
        >
        <h1 align="center">Panel de Indicadores UMMEG</h1>
        <p align="justify">
          En busca del fortalecimiento en el ejercicio de vigilancia realizado por la Superintendencia de
          Servicios Públicos Domiciliarios, La Superintendencia Delegada para Energía y Gas Combustible
          con el objetivo de fortalecer su gestión en torno a la vigilancia de los mercados de energía
          eléctrica y gas natural, cuenta con el Panel de indicadores para el
          Monitoreo para los Mercados de Energía y Gas Natural en Colombia. esta herramienta permite
          la detección y mitigación de conductas que afecten la eficiencia o confiabilidad de los
          mercados, así como poder determinar cuando los resultados del mercado afectan a los
          participantes del mercado y/o usuarios finales de este.
        </p>
      </el-col>
    </el-row>
    <el-row :gutter="24" justify="center">
      <el-col :lg=" {span: 8, offset: 8}" :md=" {span: 16, offset: 4}" :sm=" {span: 16, offset: 4}" :xs="{span: 16, offset: 4}">
        <div class="servicio-button" style="width:45%;">
          <router-link to="/electric-power/market-power/ihh_c">
            <img
              style="padding-top: 20px; width:100%;"
              :src="imageEnergia"
            >
          </router-link>
        </div>
        <div class="servicio-button" style="width:45%;">
          <router-link to="fuel-gas/market/pm">
            <img
              style="padding-top: 20px; width:100%;"
              :src="imageGas"
            >
          </router-link>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import imageUmmeg
  from '@/assets/ummeg_horizontal.jpg'
import imageEnergia
  from '@/assets/energia_0.png'
import imageGas
  from '@/assets/gas-combustible_0.png'

export default {
  data() {
    return {
      imageGas: imageGas,
      imageUmmeg: imageUmmeg,
      imageEnergia: imageEnergia
    }
  }
}
</script>

<style scoped>
.servicio-button{
  width: 200px;
  display: inline-block;
  border-radius: 10px;
}

.servicio-button:hover{
  background-color: rgb(169, 205, 229);
}
</style>
