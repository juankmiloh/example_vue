<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.pivotal') }} </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="8" :lg="2">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col :xs="24" :sm="8" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione una fecha" placement="bottom-end">
                <el-date-picker v-model="date" type="date" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="8" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col :xs="24" :sm="8" :lg="4">
              <div class="label">Número de pivotes:</div>
            </el-col>
            <el-col :xs="24" :sm="8" :lg="4">
              <el-tooltip class="item" effect="dark" content="Seleccione un indicador" placement="bottom-end">
                <el-select :value="$t(sPivots.text)" :placeholder="$t(sPivots.text)" @change="pivotsChange($event)">
                  <el-option v-for="item in pivots" :key="item.value" :label="$t(item.text)" :value="item" />
                </el-select>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <scatter-chart :data="data" value-title="Valor" :pivots="sPivots.value" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="formatedData" :columns="columns" :indicator-name="$t('route.pivotal')" :public-conf="publicConf" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import ScatterChart from './components/ScatterChart'
import TransactionTable from './components/TransactionTable'
import _ from 'lodash'

const THRESHOLD = 1

var PIVOTS = [{
  value: 1,
  text: 'Pivotal'
},
{
  value: 2,
  text: 'Bipivotal'
},
{
  value: 3,
  text: 'Tripivotal'
}
]

export default {
  name: 'DashboardAdmin',
  components: {
    ScatterChart,
    TransactionTable
  },
  data() {
    return {
      data: [],
      formatedData: [],
      columns: [],
      indicatorName: 'pivotal',
      start: new Date(),
      end: new Date(),
      list: [],
      date: new Date(),
      pivots: PIVOTS,
      sPivots: PIVOTS[0],
      publicConf: process.env.VUE_APP_PUBLIC === 'true'
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
        var rangeDate = await getLastDate('pivotal')
        var lastDate = new Date(rangeDate[1])
        // lastDate.setDate(lastDate.getDate() - 2)
        this.lastDate = lastDate
        this.initDate = new Date(rangeDate[0]).addDays(5)
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    async getData() {
      this.data = []
      if (this.date > this.lastDate || this.date < this.initDate) {
        this.date = this.lastDate
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date),
          pivotes: this.sPivots.value
        })
        if (result) {
          this.data = _.orderBy(result.items, ['names.2'], ['asc'])
          this.format(this.data)
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
    },
    async format(data) {
      if (!data[0]) {
        return []
      }
      if (this.publicConf) {
        this.columns = ['Estado', 'Agente(s)', 'Mínimo']
      } else {
        this.columns = ['Estado', 'Código', 'Agente(s)', 'Mínimo']
      }
      this.columns = this.columns.concat(Array.from(data[0].dates, x => x.toString()))
      var formatedData = []
      for (const i in data) {
        var row = []
        if (this.publicConf) {
          row = [Number(data[i].names[2]) < THRESHOLD ? 1 : 0, data[i].names[1], data[i].names[2].toFixed(2)]
        } else {
          row = [Number(data[i].names[2]) < THRESHOLD ? 1 : 0, data[i].names[0], data[i].names[1], data[i].names[2].toFixed(2)]
        }
        row = row.concat(Array.from(data[i].values, x => x.toFixed(2)))
        formatedData.push(row)
      }
      this.formatedData = formatedData
    },
    pivotsChange(item) {
      this.sPivots = item
      this.getData()
    },
    dateChange(event) {
      this.start = event[0]
      this.end = event[1]
      this.getData()
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
