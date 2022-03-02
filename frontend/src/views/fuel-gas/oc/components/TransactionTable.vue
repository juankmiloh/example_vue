<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-collapse-item title="Descripción del indicador" name="1">
          <ul>
            <li>
              Corresponde a la contratación acumulada por productor en función del respectivo nivel de precios.
            </li>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column :label="agentTitle" min-width="200" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column label="Modalida" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row.name1 }}
        </template>
      </el-table-column>
      <el-table-column :label="valueTitle" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          $ {{ Number(scope.row.value) }}
        </template>
      </el-table-column>
      <el-table-column :label="quantityTitle" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.quantity) }}
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
    indicatorName: {
      type: String,
      default: 'preofe'
    },
    agentTitle: {
      type: String,
      default: 'agetn'
    },
    valueTitle: {
      type: String,
      default: 'Precio'
    },
    quantityTitle: {
      type: String,
      default: 'Cantidad'
    },
    statusTitle: {
      type: String,
      default: 'Estado'
    },
    publicConf: {
      type: Boolean,
      default: true
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
        const tHeader = ['Agente', 'Modalidad', 'Precio', 'Cantidad']
        const filterVal = ['name0', 'name1', 'value', 'quantity']
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
      var quantityAcc = 0
      var formatedData = []

      if (!data.length) {
        return []
      }

      quantityAcc = 0

      if (data[0] !== undefined) {
        for (var i = 0; i < data[0].length; i++) {
          if (this.publicConf) {
            quantityAcc += data[0][i].values[1]
            data[0][i].values[1] = quantityAcc
          }
          formatedData.push(this.getFormateData(data[0][i], 'Interrumpible'))
        }
      }

      quantityAcc = 0
      if (data[1] !== undefined) {
        for (i = 0; i < data[1].length; i++) {
          if (this.publicConf) {
            quantityAcc += data[1][i].values[1]
            data[1][i].values[1] = quantityAcc
          }
          formatedData.push(this.getFormateData(data[1][i], 'Firme'))
        }
        return formatedData
      }
    },
    getFormateData(data, modalidad) {
      return {
        index: data.id,
        name0: data.names[0],
        name1: modalidad,
        value: data.values[0],
        quantity: data.values[1],
        status: data.status
      }
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
