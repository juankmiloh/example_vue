<template>
  <div class="transction-table">
    <el-row style="background: #fff; padding: 16px 16px 0; margin-bottom: 16px">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            Permite verificar si las plantas de un agente son necesarias para
            cubrir la demanda del sistema. En caso de que sean estrictamente
            necesarias, el agente estaría en la capacidad de ejercer poder de
            mercado.
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>
    <el-tooltip class="item" effect="dark" content="Haga click para descargar la información en archivo excel" placement="bottom-end">
      <el-button :loading="downloadLoading" style="margin: 0 0 20px 20px" type="primary" icon="document" @click="handleDownload">
        {{ $t("excel.export") }} Excel
      </el-button>
    </el-tooltip>
    <el-table :data="data" style="width: 100%; padding-top: 15px" class="rcorners">
      <el-table-column label="Fecha" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row.Fecha }}
        </template>
      </el-table-column>

      <el-table-column label="Mínimo" width="90" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row['Mínimo'].toFixed(2) }}
        </template>
      </el-table-column>

      <el-table-column v-for="column in columns" :key="column.toString()" :label="(column + 1).toString()" width="50" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row[column + 1].toFixed(2) }}
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
      default: function() {
        return []
      }
    },
    columns: {
      type: Array,
      default: function() {
        return []
      }
    },
    indicatorName: {
      type: String,
      default: 'Índice de oferta residual por agente'
    },
    valueTitle: {
      type: String,
      default: 'Precio'
    },
    publicConf: {
      type: Boolean,
      default: true
    },
    agente: {
      type: String,
      default: 'agente'
    },
    startDate: {
      type: Date,
      default: new Date()
    }
  },
  data() {
    return {
      downloadLoading: false
    }
  },
  methods: {
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) =>
        filterVal.map((j) => {
          return v[j]
        })
      )
    },
    handleDownload() {
      this.downloadLoading = true
            import('@/vendor/Export2Excel').then((excel) => {
              let headers = []
              let data = []
              if (this.data && this.data.length > 0) {
                headers = Object.keys(this.data[0])
                data = this.formatJson(headers, this.data)
              }
              excel.export_json_to_excel({
                header: headers,
                data,
                filename: this.formatDate(this.startDate) + ' ' + this.indicatorName + ' - ' + this.agente,
                autoWidth: this.autoWidth,
                bookType: this.bookType
              })
              this.downloadLoading = false
            })
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>
