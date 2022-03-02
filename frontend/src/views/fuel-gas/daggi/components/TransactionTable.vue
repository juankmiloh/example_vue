<template>
  <div class="transction-table">

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            Corresponde al número de días que las plantas térmicas que tienen acceso a la planta
            de regasificación de Cartagena podrían generar con el gas importado que se encuentra
            disponible como inventario en la fecha de consulta. El número de días dependerá del
            escenario de generación que se escoja.
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la convenciones del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <table class="table table-striped">
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
                <td><b>{{ thresholds[2] }} días o más.</b>  Riesgo bajo de abastecimiento en caso de una indisponibilidad</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
                <td><b>Entre {{ thresholds[1] }} y {{ thresholds[2] }} días.</b>  Riesgo medio de abastecimiento en caso de una indisponibilidad</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-red" /></td>
                <td><b>Menos de {{ thresholds[1] }} días.</b> En caso de llegar a una indisponibilidad del sistema estaríamos en problemas de tener una generación permanente.</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>

    <el-button
      :loading="downloadLoading"
      style="margin:0 0 20px 20px;"
      type="primary"
      icon="document"
      @click="handleDownload"
    >
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column :label="statusTitle" width="100" align="center" prop="value0" sortable>
        <template slot-scope="scope">
          <div
            :class="{'arrow-red': scope.row.value0 < thresholds[1],
                     'arrow-yellow': scope.row.value0 >= thresholds[1] && scope.row.value0 < thresholds[2],
                     'arrow-black': scope.row.value0 >= thresholds[2]}"
          >
            <v-icon name="circle" scale="2" />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="descriptionTitle" min-width="150" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="valueTitle" width="230" align="center" prop="value0" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value0).toFixed(1) }}
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
    thresholds: {
      type: Array,
      default: function() { return [] }
    },
    itemTitle: {
      type: String,
      default: 'Item'
    },
    descriptionTitle: {
      type: String,
      default: 'Descripción'
    },
    valueTitle: {
      type: String,
      default: 'Valor'
    },
    value2Title: {
      type: String,
      default: 'Valor'
    },
    indicatorName: {
      type: String,
      default: ''
    },
    statusTitle: {
      type: String,
      default: 'Estado'
    },
    date: {
      type: Date,
      default: new Date()
    },
    status: {
      type: Boolean,
      default: false
    },
    value: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      chart: null,
      showImage: false,
      downloadLoading: false
    }
  },
  methods: {
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = [this.descriptionTitle, this.valueTitle]
        const filterVal = ['name0', 'value0']
        const list = this.format(this.data)
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.formatDate(moment()) + ' ' + this.indicatorName,
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        this.downloadLoading = false
      })
    },
    format(data) {
      var formatedData = []
      if (data && data[0]) {
        for (var i = 0; i < data[0].names.length; i++) {
          formatedData.push({
            name0: data[0].names[i],
            value0: data[0].values[i]
          })
        }
      }
      return formatedData
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style scoped>
.arrow-black {
  color: green;
}
.arrow-yellow {
  color: orange
}
.arrow-red {
  color: red
}
.arrow-blue {
  color: #1890ff
}
.transction-table .chart {
  width: 100%;
  padding-top: 15px;
  height: 400px;
}
</style>
