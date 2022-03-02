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
            <b>Indisponibilidad por eventos de generación: </b> Muestra las
            indisponibilidades de los activos de generación eléctrica.<br>
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

export default {
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
      default: 'iag'
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
        const header = []
        const filter = []

        for (const key in this.columns) {
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
