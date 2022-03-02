<template>
  <div class="transction-table">

    <div class="dashboard-editor-container">

      <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
        <table class="table table-striped">
          <tr>
            <td>
              <div
                :class="{'arrow-black': !status,
                         'arrow-yellow': status}"
              >
                <v-icon name="circle" scale="2" />
              </div>
            </td>
            <td>IHH: {{ Number(value).toFixed(1) }}  </td>
          </tr>
        </table>
      </el-row>
    </div>

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-collapse-item title="Descripción del indicador" name="1">
          Determina el número de agentes que participan de manera mayoritaria en
          la fijación del precio de bolsa en cada mes.
        </el-collapse-item>
        <el-collapse-item title="Convenciones" name="2">

          <h3> Índice Herfindahl-Hirschman </h3>

          <table class="table table-striped">
            <tr>
              <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
              <td>IHH no supera el valor de 1800</td>
            </tr>
            <tr>
              <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
              <td>IHH supera el valor de 1800</td>
            </tr>
          </table>
          <h3> {{ valueTitle }} </h3>
          <table class="table table-striped">
            <tr>
              <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
              <td>IHH no supera el valor de 1800</td>
            </tr>
            <tr>
              <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
              <td>IHH supera el valor de 1800 y el agente hace parte de los 5 agentes que participan de manera mayoritaria en la fijación del precio de bolsa en cada mes
              </td>
            </tr>
          </table>
        </el-collapse-item>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;">
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
          {{ Number(scope.row.value).toFixed(1) }}  %
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
      type: Date
    },
    status: {
      default: false
    },
    value: {
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
        const tHeader = ['Id', this.itemTitle, this.descriptionTitle, this.valueTitle, this.statusTitle]
        // const filterVal = ['index', 'name1', 'name0', 'value', 'status']
        const filterVal = ['index', 'name0', 'value', 'status']
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
