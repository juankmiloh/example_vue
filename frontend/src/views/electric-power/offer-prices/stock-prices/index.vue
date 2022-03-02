<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> Precios de bolsa </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="1">
              <div class="label">Año:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="15">
              <multiselect
                v-model="sYears"
                :options="years"
                :multiple="true"
                :taggable="true"
                placeholder="Seleccione un año"
                select-label="Seleccionar"
                deselect-label="Remover"
                selected-label="Seleccionado"
                :allow-empty="false"
                @input="startingDateChange()"
                @tag="startingDateChange()"
              />
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
          <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
            <el-collapse>
              <el-tooltip class="item" effect="dark" content="Haga clic para mostrar u ocultar la descripción del indicador" placement="bottom-end">
                <el-collapse-item title="Descripción del indicador" name="1">
                  <ul>
                    <li>
                      Muestra la evolución con periodicidad diaria del precio de bolsa, presentando para cada día el valor promedio, el valor máximo y el precio de escasez de activación.
                    </li>
                    <li>
                      Este indicador se puede comparar con otros años de interés.
                    </li>
                    <li>
                      El precio de bolsa para cada fecha publicada corresponde con la última versión disponible por el ASIC, de acuerdo con las fechas respectivas de publicación y modificación.
                    </li>
                    <br>
                  </ul>
                </el-collapse-item>
              </el-tooltip>
            </el-collapse>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <line-chart :data="data" :reference="reference" value-title="Valor" :year="lastYear" />
        </div>
        <div class="chart-wrapper">
          <el-row>
            <el-col>
              <el-tooltip class="item" effect="dark" content="Haga clic para descargar la información en archivo excel" placement="bottom-end">
                <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
                  {{ $t('excel.export') }} Excel
                </el-button>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LineChart from './components/LineChart'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'
import Multiselect from 'vue-multiselect'

var FIRST_YEAR = 2010
var REFERENCE_YEARS = []

export default {
  name: 'DashboardAdmin',
  components: {
    LineChart,
    Multiselect
  },
  data() {
    return {
      years: [],
      sYears: [],
      lastYear: 2020,
      list: [],
      reference: [],
      data: [],
      downloadLoading: false,
      indicatorName: 'precios_de_bolsa'
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        const rangeData = await getLastDate('trsd')
        this.lastDate = new Date(rangeData[1])
        this.initDate = new Date(rangeData[0])

        console.info('this.lastDate', this.lastDate)
        this.date = this.lastDate
        this.lastYear = this.lastDate.getFullYear()
        this.years = []
        this.sYears = REFERENCE_YEARS.concat(this.lastYear)
        for (var i = this.lastYear; i >= FIRST_YEAR; i--) {
          this.years.push(i)
        }
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      this.getData()
    },
    startingDateChange() {
      if (Array.isArray(this.sYears) && this.sYears.length) {
        this.lastYear = [this.lastYear]
      }
      this.lastYear = this.sYears[0]
      this.getData()
    },
    async getData() {
      if (this.end > this.lastDate) {
        this.end = this.lastDate
      }
      this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 7)
      try {
        var reference = await getIndicator('pme140', {
          year: this.lastYear
        })
        var data = await getIndicator('pb', {
          years: this.sYears
        })
        if (data) {
          this.reference = reference.items
          this.data = data.items
        }
      } catch (error) {
        console.error(error)
        this.list = []
      }
    },
    daysDifference(date2, date1) {
      var diffTime = Math.abs(date2.getTime() - date1.getTime())
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    format(data, tHeader) {
      var formatedData = []
      for (let i = 0; i < data.length; i++) {
        var row = [data[i].id]
        for (let j = 0; j < tHeader.length - 1; j++) {
          row.push(data[i].values[j])
        }
        formatedData.push(row)
      }
      return formatedData
    },
    handleDownload() {
      this.downloadLoading = true
            import('@/vendor/Export2Excel').then(excel => {
              var tHeader = ['Año']
              tHeader = tHeader.concat(this.data[0].dates)
              const table = this.format(this.data, tHeader)

              // Transponer datos
              var headersT = [tHeader[0], table[0][0], table[1][0]]
              var tableT = []
              for (let j = 1; j < tHeader.length - 1; j++) {
                tableT.push([
                  tHeader[j],
                  table[0][j],
                  table[1][j]
                ])
              }

              excel.export_json_to_excel({
                header: headersT,
                data: tableT,
                filename: this.formatDate(moment()) + ' ' + this.indicatorName,
                autoWidth: this.autoWidth,
                bookType: this.bookType
              })
              this.downloadLoading = false
            })
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
