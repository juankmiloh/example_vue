<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-collapse>
        <el-collapse-item title="Descripción del indicador" name="1">
          <b>Inventario GNL:</b> Corresponde a las cantidades existentes de gas natural licuado (GNL) en GBTU que se encuentran almacenadas en la Planta de Regasificación de Cartagena.<br>
          <b>Volumen inyectado:</b> Corresponde a la cantidad regasificada diario en GBTU que ingresa al Sistema Nacional de Transporte.
        </el-collapse-item>
      </el-collapse>
    </el-row>

    <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
      {{ $t('excel.export') }} Excel
    </el-button>

    <el-table :data="data" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column label="Fecha" width="150" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row.date }}
        </template>
      </el-table-column>

      <el-table-column v-for="column in columns" :key="column.id" :label="column.name" width="250" align="center" prop="value" sortable>
        <template slot-scope="scope">
          {{ scope.row[column.id] }}
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
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const header = ['Fecha']
        const filter = ['date']

        for (const key in this.columns) {
          console.info(key, this.columns[key])
          filter.push(this.columns[key].id)
          header.push(this.columns[key].name)
        }
        const data = this.formatJson(filter, this.data)
        excel.export_json_to_excel({
          header: header,
          data: data,
          filename: this.formatDate(moment()) + ' ' + this.indicatorName,
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

