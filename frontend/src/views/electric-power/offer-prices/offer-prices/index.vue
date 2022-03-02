<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> Precios de oferta </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="2" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="10" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione una fecha" placement="bottom-end">
                <el-date-picker v-model="dateValue" type="daterange" align="right" unlink-panels range-separator=" - " :start-placeholder="$t('datePicker.startDate')" :end-placeholder="$t('datePicker.endDate')" @change="dateChange($event)" />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="10" :lg="7">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="list"
            :indicator-name="indicatorName"
            item-title="Planta"
            description-title="Agente"
            value1-title="Valor Inicial"
            value2-title="Valor Final"
            status-title="Estado"
            trend-title="Tendencia"
            status-type="trend"
            :end-date="end"
            :start-date="start"
          />
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="list" value-title="Valor" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import BarChart from './components/BarChart'
import TransactionTable from './components/TransactionTable'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'
import _ from 'lodash'

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    TransactionTable
  },
  data() {
    return {
      indicatorName: 'preofe',
      start: new Date(),
      end: new Date(),
      list: [],
      lastDate: new Date(),
      initDate: new Date(),
      dateValue: []
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
        const rangeData = await getLastDate('preofe')
        this.lastDate = new Date(rangeData[1])
        this.initDate = new Date(rangeData[0])
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      this.getData()
    },
    async getData() {
      if (this.end > this.lastDate) {
        this.end = this.lastDate
      }
      this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 7)
      this.dateValue = [this.start, this.end]
      try {
        var result = await getIndicator(this.indicatorName, {
          finicial: this.formatDate(this.start),
          ffinal: this.formatDate(this.end)
        })
        if (result) {
          this.list = _.orderBy(result.items, ['status', 'trend'], ['desc', 'desc'])
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
    async dateChange(event) {
      var start = new Date(event[0])
      var end = new Date(event[1])
      if (start < this.initDate || end < this.initDate || start > this.lastDate || end > this.lastDate) {
        this.end = this.lastDate
        this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 7)
        this.dateValue = [this.start, this.end]
      } else {
        this.start = start
        this.end = end
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          finicial: this.formatDate(this.start),
          ffinal: this.formatDate(this.end)
        })
        if (result) {
          this.list = result.items
        }
      } catch (error) {
        this.list = []
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
