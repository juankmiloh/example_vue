<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 24 }"
        :lg="{ span: 24 }"
        :xl="{ span: 24 }"
        style="padding-right: 8px; margin-bottom: 30px"
      >
        <div class="chart-wrapper">
          <h2>Índice Hirschman Herfindahl acumulado</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione un periodo"
                placement="bottom-end"
              >
                <el-date-picker
                  v-model="date"
                  type="daterange"
                  start-placeholder="Fecha inicial"
                  end-placeholder="Fecha final"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag class="el-tag--dark">
                Datos actualizados a fecha de {{ printCurrentDate() }}
              </el-tag>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="list" chart-title="IHH" value-title="Valor" />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="list"
            chart-title="IHH"
            indicator-name="ihh"
            item-title="Planta"
            description-title="Agente"
            value-title="Mercado"
            status-title="Fecha"
            :descriptions="description"
            :status="false"
            :value="value"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import TransactionTable from './components/TransactionTable'
import BarChart from './components/BarChart'
import { getIndicator, getLastDate } from '@/api/remoteSearch'
import moment from 'moment'

var FILTERS = [
  {
    id: false,
    text: 'Todo'
  },
  {
    id: true,
    text: 'Despachado centralmente'
  }
]

export default {
  name: 'DashboardAdmin',
  components: {
    TransactionTable,
    BarChart
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    indicador: {
      type: String,
      default: 'ihh'
    },
    descriptions: {
      type: Array,
      default: function() {
        return []
      }
    }
  },
  data() {
    return {
      plantFilters: FILTERS,
      plantFilter: FILTERS[0],
      indicatorName: 'ihh',
      date: [new Date(), new Date()],
      initDate: new Date(),
      lastDate: new Date(),
      ihhGenerationInitDate: new Date(),
      ihhGenerationLastDate: new Date(),
      list: [],
      status: false,
      value: 0,
      description: [
        {
          text:
            'Índice Herfindall Hirschman, mide el nivel de concentración en el mercado de generación real, considerando el portafolio de plantas de generación de cada uno de los agentes.'
        },
        {
          text:
            'Permite observar la evolución de estos indicadores durante el periodo de análisis y la región donde se encuentran, identificando el grado de concentración de los distintos mercados.'
        }
      ]
    }
  },
  created() {
    this.fetchLatest()
  },
  methods: {
    async fetchLatest() {
      try {
        const range_dates = await getLastDate('ihh')
        this.date = [
          moment(range_dates[1]).startOf('month').toDate(),
          new Date(range_dates[1])
        ]
        this.initDate = new Date(range_dates[0])
        this.lastDate = new Date(range_dates[1])
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    printCurrentDate() {
      var currentDate = this.lastDate
      return moment(currentDate).format('DD/MM/YYYY')
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    dateChange(event) {
      if (event) {
        this.getData()
      }
    },
    plantFilterChange(item) {
      this.plantFilter = item
      this.getData()
    },
    async getData() {
      if (this.date[1] > this.lastDate || this.date[1] < this.initDate) {
        this.date[0] = moment(this.lastDate).startOf('month').toDate()
        this.date[1] = this.lastDate
      }
      if (this.date[0] > this.lastDate || this.date[0] < this.initDate) {
        this.date[0] = moment(this.lastDate).startOf('month').toDate()
        this.date[1] = this.lastDate
      }

      try {
        var result = await getIndicator(this.indicatorName, {
          fecha_inicial: this.formatDate(this.date[0]),
          fecha_final: this.formatDate(this.date[1]),
          medida: this.indicador
        })
        if (result) {
          this.list = result.items
        }
      } catch (error) {
        this.list = []
        this.value = 0
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
