<template>
  <div class="transction-table">

    <div class="dashboard-editor-container rcorners">
      <el-row>
        <table class="table table-striped">
          <tr>
            <td>
              <div :class="{'arrow-black': !status, 'arrow-yellow': status}">
                <v-icon name="circle" scale="2" />
              </div>
            </td>
            <td>Número de días con desviación mayor a 5%: {{ Number(value).toFixed(1) }} </td>
          </tr>
        </table>
      </el-row>
    </div>

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            <ul>
              <li>
                Mide la desviación de energía para el sistema entre la generación programada y la real, identificando variaciones mayores a 5%.
              </li>
            </ul>
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la convecion del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <h3> Desviación (se espera desviación menor o igual a 5%)</h3>
            <table class="table table-striped">
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
                <td>Se cumple la métrica</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
                <td>Se incumple la métrica un día hasta tres días bandera amarilla</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-red" /></td>
                <td>Se incumple la métrica por más de tres días seguidos bandera roja</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>

    <line-chart :data="data" value-title="Valor" />

    <br>

    <el-tooltip class="item" effect="dark" content="Haga click para descargar la información en archivo excel" placement="bottom-end">
      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
        {{ $t('excel.export') }} Excel
      </el-button>
    </el-tooltip>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column :label="statusTitle" width="100" align="center" prop="status" sortable>
        <template slot-scope="scope">
          <div
            :class="{'arrow-black': scope.row.status === 0,
                     'arrow-yellow': scope.row.status === 1,
                     'arrow-red': scope.row.status === 2}"
          >
            <v-icon name="circle" scale="2" />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="descriptionTitle" min-width="200" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="valueTitle" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value).toFixed(2) }}  %
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import moment from 'moment'
import LineChart from './LineChart'
const TRAFFIC_LIGHT_OPTIONS = ['success', 'warning', 'danger']

export default {
  components: {
    LineChart
  },
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
    indicatorName: {
      type: String,
      default: 'preofe'
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
    units: {
      type: String,
      default: 'Cantidad'
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
        const tHeader = [this.statusTitle, this.itemTitle, this.valueTitle]
        const filterVal = ['status', 'name0', 'value']
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
      for (var i = 0; i < data.length; i++) {
        formatedData.push({
          index: data[i].id,
          name0: data[i].dates[0].split(' ')[0],
          name1: data[i].names[0],
          value: data[i].values[0],
          status: data[i].status
        })
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
