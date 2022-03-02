<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            <b>Indice Pivotal:</b>
            Permite verificar si las plantas de un agente son necesarias para cubrir
            la demanda del sistema. En caso de que sean estrictamente necesarias, el agente estaría en
            la capacidad de ejercer poder de mercado.<br><br>

            <b>Indice Bipivotal:</b>
            Permite verificar si las ofertas combinadas de dos agentes son necesarias para atender la demanda
            del sistema. En caso de que sean necesarias, la combinación de agentes estarían en la capacidad de
            ejercer poder de mercado.<br><br>

            <b>Indice Tripivotal:</b>
            Permite verificar si las plantas de tres agentes son necesarias para atender la demanda del sistema.
            En caso de que sean estrictamente necesarias, la combinación de agentes estarían en la capacidad de
            ejercer poder de mercado.
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar las convenciones del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <table class="table table-striped">
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
                <td>El agente o combinación de agentes no estaría en la capacidad de ejercer poder de mercado en ninguna hora del día</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-red" /></td>
                <td>El agente o combinación de agentes estaría en la capacidad de ejercer poder de mercado en algúna hora del día</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="data.slice(0, 200)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column v-for="(column, index) in columns" :key="index" :label="column" :width="getWidth(index)" align="center" :prop="index.toString()" sortable>
        <template slot-scope="scope">
          <template v-if="index === 0">
            <div
              :class="{'arrow-black': scope.row[0] === 0,
                       'arrow-red': scope.row[0] === 1}"
            >
              <v-icon name="circle" scale="2" />
            </div>
          </template>
          <template v-else>
            {{ scope.row[index] }}
          </template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import moment from 'moment'

const TRAFFIC_LIGHT_OPTIONS = ['success', 'warning', 'danger']

export default {
  filters: {
    trafficLightStatusFilter(status) {
      return TRAFFIC_LIGHT_OPTIONS[status]
    }
  },
  props: {
    data: {
      type: Array,
      default: function() { return [] }
    },
    columns: {
      type: Array,
      default: function() { return [] }
    },
    indicatorName: {
      type: String,
      default: ''
    },
    valueTitle: {
      type: String,
      default: 'Precio'
    },
    publicConf: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      downloadLoading: false
    }
  },
  methods: {
    getWidth(index) {
      if (index > 3) {
        return 50
      }
      if (index === 3 && this.publicConf) {
        return 50
      }
      if (index === 2 && !this.publicConf) {
        return 200
      }
      return 70
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        excel.export_json_to_excel({
          header: this.columns,
          data: this.data,
          filename: this.formatDate(moment()) + ' ' + this.indicatorName,
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        this.downloadLoading = false
      })
    }
  }
}
</script>

<style scoped>
  .arrow-black {
    color: green;
  }
  .arrow-red {
    color: red
  }
</style>
