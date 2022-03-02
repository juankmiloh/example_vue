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
          <el-collapse-item title="Descripción del indicador" name="1" />
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
      <el-table-column label="Vendedor" prop="seller" sortable>
        <template slot-scope="scope">
          {{ scope.row.seller }}
        </template>
      </el-table-column>
      <el-table-column label="Comprador" prop="buyer" sortable>
        <template slot-scope="scope">
          {{ scope.row.buyer }}
        </template>
      </el-table-column>
      <el-table-column label="Cantidad (GBTUD)" prop="amount" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.amount) }}
        </template>
      </el-table-column>
      <el-table-column label="Precio (USD/MBTU)" prop="price" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.price) }}
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
      type: Object,
      default: function() {
        return null
      }
    },
    indicatorName: {
      type: String,
      default: ''
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
          filename: this.formatDate(moment()) + ' ' + this.indicatorName,
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        this.downloadLoading = false
      })
    },
    format(data) {
      var formatedData = []
      console.info('data.links', data.links)
      if (data && data.links) {
        for (const i in data.links) {
          formatedData.push({
            index: data.links[i].id,
            seller: data.agents[data.links[i].source + 1].text,
            buyer: data.agents[data.links[i].target + 1].text,
            amount: data.links[i].amount,
            price: data.links[i].price
          })
        }
      }
      console.info('formatedData:', formatedData)
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
