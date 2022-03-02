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
            <td>IHH: {{ Number(value).toFixed(1) }} </td>
          </tr>
        </table>
      </el-row>
    </div>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            <ul>
              <li v-for="description in descriptions" :key="description.text">
                {{ description.text }}
              </li>
            </ul>
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la convenciones del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <h3> Índice Herfindahl-Hirschman </h3>
            <table class="table table-striped">
              <tr>
                <td>
                  <v-icon name="circle" scale="1" class="arrow-black" />
                </td>
                <td>IHH no supera el valor de 1800</td>
              </tr>
              <tr>
                <td>
                  <v-icon name="circle" scale="1" class="arrow-yellow" />
                </td>
                <td>IHH supera el valor de 1800</td>
              </tr>
            </table>
            <h3> {{ valueTitle }} </h3>
            <table class="table table-striped">
              <tr>
                <td>
                  <v-icon name="circle" scale="1" class="arrow-black" />
                </td>
                <td>La cuota de mercado de un agente es menor al 25%</td>
              </tr>
              <tr>
                <td>
                  <v-icon name="circle" scale="1" class="arrow-yellow" />
                </td>
                <td>La cuota de mercado de un agente se encuentra en el rango entre el 25% y 30%</td>
              </tr>
              <tr>
                <td>
                  <v-icon name="circle" scale="1" class="arrow-red" />
                </td>
                <td>La cuota de mercado de un agente supera el 30%</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="24">
        <bar-chart :data="data" :chart-title="chartTitle" value-title="Valor" />
      </el-col>
    </el-row>
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
      <el-table-column :label="valueTitle" width="180" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value).toFixed(2) }} %
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import moment from 'moment'
import BarChart from './BarChart'
const TRAFFIC_LIGHT_OPTIONS = ['success', 'warning', 'danger']

export default {
  filters: {
    trafficLightStatusFilter(status) {
      return TRAFFIC_LIGHT_OPTIONS[status]
    }
  },
  components: {
    BarChart
  },
  props: {
    data: {
      type: Array,
      default: function() {
        return []
      }
    },
    chartTitle: {
      type: String,
      default: ''
    },
    descriptions: {
      type: Array,
      default: function() {
        return []
      }
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
              const tHeader = [this.descriptionTitle, this.valueTitle, this.statusTitle]
              const filterVal = ['name0', 'value', 'status']
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
          name0: data[i].names[0],
          name1: data[i].names[1],
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
