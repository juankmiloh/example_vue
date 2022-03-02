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
            <b>Precio nacional vs precio importado: </b> Comparación entre el
            precio de gas de cada campo y el precio del gas que se está
            importando al mercado colombiano. Se calcula como el cociente entre
            el precio promedio ponderado para cada fuente de suministro y el
            precio promedio ponderado de las importaciones físicas de gas para
            el periodo seleccionado.<br>
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
      :data="format(data)"
      style="width: 100%; padding-top: 15px"
      class="rcorners"
    >
      <el-table-column :label="sourceTitle" prop="name" sortable>
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column
        :label="priceTitle"
        align="center"
        prop="weightedPrice"
        sortable
      >
        <template slot-scope="scope">
          $ {{ Number(scope.row.weightedPrice) }}
        </template>
      </el-table-column>
      <el-table-column :label="ratioTitle" align="center" prop="ratio" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.ratio) }}
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
    indicatorName: {
      type: String,
      default: 'gpin'
    },
    sourceTitle: {
      type: String,
      default: 'Fuente'
    },
    priceTitle: {
      type: String,
      default: 'Precio'
    },
    ratioTitle: {
      type: String,
      default: 'Índice'
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
        const tHeader = [this.sourceTitle, this.priceTitle, this.ratioTitle]
        const filterVal = ['name', 'weightedPrice', 'ratio']
        const list = this.format(this.data)
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.formatDate(moment()) + ' ' + 'precio_naciona_vs_importado',
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
            name: data[key].name,
            weightedPrice: row[i].values[0].toFixed(2),
            ratio: row[i].values[1].toFixed(2)
          })
        }
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
.transction-table .chart {
  width: 100%;
  padding-top: 15px;
  height: 400px;
}
</style>
