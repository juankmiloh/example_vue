<template>
  <div class="transction-table">
    <el-row style="background: #fff; padding: 16px 16px 0; margin-bottom: 16px">
      <el-tooltip
        class="item"
        effect="dark"
        content="Haga click para mostrar u ocultar la descripción del indicador"
        placement="bottom-end"
      >
        <el-collapse>
          <el-collapse-item title="Descripción del indicador" name="1">
            <b>Índice de comparación de obligaciones en energía firme: </b> Este
            indicador ayuda a identificar los recursos de generación que
            posiblemente no estén en capacidad de respaldar las OEF asumidas en
            caso de ser requeridas en el despacho durante un periodo crítico en
            el mercado mayorista.<br>
          </el-collapse-item>
        </el-collapse>
      </el-tooltip>
    </el-row>
    <el-tooltip
      class="item"
      effect="dark"
      content="Haga click para descargar la información en archivo excel"
      placement="bottom-end"
    >
      <el-button
        :loading="downloadLoading"
        style="margin: 0 0 20px 20px"
        type="primary"
        icon="document"
        @click="handleDownload"
      >
        {{ $t("excel.export") }} Excel
      </el-button>
    </el-tooltip>
    <el-table
      :data="data"
      style="width: 100%; padding-top: 15px"
      class="rcorners"
    >
      <el-table-column
        v-for="column in columns"
        :key="column.id"
        :label="column.name"
        align="center"
        prop="value"
        sortable
      >
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
      default: ''
    },
    valueTitle: {
      type: String,
      default: 'ICOEF'
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
      return jsonData.map((v) =>
        filterVal.map((j) => {
          return v[j]
        })
      )
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then((excel) => {
        if (this.data && this.data.length > 0) {
          const header = Object.keys(this.data[0])
          const data = this.formatJson(header, this.data)
          header[0] = 'periodo'
          header[1] = 'planta'
          excel.export_json_to_excel({
            header: header,
            data: data,
            filename: this.formatDate(moment()) + ' ' + this.indicatorName,
            autoWidth: this.autoWidth,
            bookType: this.bookType
          })
        }
        this.downloadLoading = false
      })
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>
