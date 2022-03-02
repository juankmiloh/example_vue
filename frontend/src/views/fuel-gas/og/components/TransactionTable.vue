<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-collapse-item title="Descripción del indicador" name="1">
          <ul>
            <li>
              Corresponde a la producción real diaria por campo, expresada en GBTUD.
            </li>
          </ul>
        </el-collapse-item>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="format(data)" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column label="Procedencia" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.procedencia }}
        </template>
      </el-table-column>
      <el-table-column label="Fecha" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row.date }}
        </template>
      </el-table-column>
      <el-table-column label="GBTUD" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.gbtud) }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import moment from 'moment'
import _ from 'lodash'

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
      default: 'Oferta Gas Natural'
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
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['Procedencia', 'Fecha', 'GBTUD']
        const filterVal = ['procedencia', 'date', 'gbtud']
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

      for (const key in data) {
        var row = data[key].data
        for (const i in row) {
          formatedData.push({
            index: row[i].id,
            procedencia: data[key].name,
            date: row[i].dates[0],
            gbtud: row[i].values
          })
        }
      }
      return _.orderBy(formatedData, ['date'], ['asc'])
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

