<template>
  <div class="transction-table">
    <el-row style="background: #fff; padding: 16px 16px 0; margin-bottom: 16px">
      <el-collapse>
        <el-tooltip
          class="item"
          effect="dark"
          content="Haga click para mostrar u ocultar la descripción del indicador"
          placement="bottom-end"
        >
          <el-collapse-item title="Descripción del indicador" name="1">
            <ul>
              <li v-for="description in descriptions" :key="description.text">
                {{ description.text }}
              </li>
            </ul>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
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
      :data="format(data)"
      style="width: 100%; padding-top: 15px"
      class="rcorners"
    >
      <el-table-column label="Fecha" prop="fecha" sortable>
        <template slot-scope="scope">
          {{ formatDate(scope.row.date) }}
        </template>
      </el-table-column>
      <el-table-column
        label="HHI Disponibilidad real"
        align="center"
        prop="dis_rea"
        sortable
      >
        <template slot-scope="scope">
          {{ Number(scope.row.dis_rea).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column
        label="HHI Fijación de precios"
        align="center"
        prop="fij_pre"
        sortable
      >
        <template slot-scope="scope">
          {{ Number(scope.row.fij_pre).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column
        label="HHI Generación real"
        align="center"
        prop="gen_rea"
        sortable
      >
        <template slot-scope="scope">
          {{ Number(scope.row.gen_rea).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column
        label="HHI Capacidad instalada"
        align="center"
        prop="cap_ins"
        sortable
      >
        <template slot-scope="scope">
          {{ Number(scope.row.cap_ins).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="HHI ENFICC" align="center" prop="enficc" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.enficc).toFixed(2) }}
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
  components: {},
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
      default: 'Fecha'
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
          var header = Object.keys(this.data[0])
          header.shift()
          const data = this.formatJson(header, this.data)
          header = ['Fecha', 'HHI Disponibilidad real', 'HHI Fijación de precios', 'HHI Generación real', 'HHI Capacidad instalada', 'HHI ENFICC']

          excel.export_json_to_excel({
            header: header,
            data,
            filename: this.formatDate(moment()) + ' ' + this.indicatorName,
            autoWidth: this.autoWidth,
            bookType: this.bookType
          })
          this.downloadLoading = false
        }
      })
    },
    format(data) {
      return data
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
  color: orange;
}
.arrow-red {
  color: red;
}
.arrow-blue {
  color: #1890ff;
}
.transction-table .chart {
  width: 100%;
  padding-top: 15px;
  height: 400px;
}
</style>
