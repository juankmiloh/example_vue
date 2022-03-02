<template>
  <div class="transction-table">

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-col :xs="24" :sm="24" :lg="24">
        <el-collapse>
          <el-collapse-item title="Descripción del indicador" name="1">
            Corresponde a la contratación de cada productor en función de volumen y precio
          </el-collapse-item>
        </el-collapse>
      </el-col>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column :label="itemTitle" min-width="200" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="descriptionTitle" min-width="200" prop="name1" sortable>
        <template slot-scope="scope">
          {{ scope.row.name1 }}
        </template>
      </el-table-column>
      <el-table-column label="Modalidad" min-width="90" prop="name2" sortable>
        <template slot-scope="scope">
          {{ scope.row.name2 }}
        </template>
      </el-table-column>
      <el-table-column label="Fuente" min-width="90" prop="name3" sortable>
        <template slot-scope="scope">
          {{ scope.row.name3 }}
        </template>
      </el-table-column>
      <el-table-column label="Mercado" min-width="90" prop="name4" sortable>
        <template slot-scope="scope">
          {{ scope.row.name4 }}
        </template>
      </el-table-column>
      <el-table-column label="Fecha Inicio" min-width="80" prop="date0" sortable>
        <template slot-scope="scope">
          {{ scope.row.date0 }}
        </template>
      </el-table-column>
      <el-table-column label="Precio (USD/MBTU)" width="80" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value0).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="Cantidad (GBTUD)" width="80" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value1).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="Sector de consumo" width="110" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row.name5 }}
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
        const tHeader = ['Id', this.itemTitle, this.descriptionTitle, 'Modalidad', 'Precio (USD/MBTU)', 'Cantidad (GBTUD)']
        const filterVal = ['index', 'name0', 'name1', 'name2', 'name3', 'name4', 'value0', 'value1']
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
          name2: data[i].names[2],
          name3: data[i].names[3],
          name4: data[i].names[4],
          value0: data[i].values[0],
          value1: data[i].values[1],
          status: data[i].status,
          date0: data[i].dates[0],
          name5: data[i].names[5]
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
