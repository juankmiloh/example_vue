<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-collapse-item title="Descripción del indicador" name="1">
          <ul>
            <li>
              Corresponde al porcentaje de participación de cada productor sobre la contratación en firme total del mercado.
            </li>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column :label="descriptionTitle" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="value2Title" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value1) }}
        </template>
      </el-table-column>
      <el-table-column :label="valueTitle" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value0).toFixed(2) }}  %
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
    value2Title: {
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
        const tHeader = [this.descriptionTitle, this.value2Title, this.valueTitle]
        const filterVal = ['index', 'value1', 'value0']
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
          value0: data[i].values[0],
          value1: data[i].values[1],
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
