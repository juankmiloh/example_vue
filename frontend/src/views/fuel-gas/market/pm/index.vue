<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.pm') }} </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col :key="name" :xs="24" :sm="12" :lg="6">
              <el-date-picker v-model="date" type="month" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
            </el-col>
            <el-col :key="name" :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <pie-chart :data="list" value-title="Valor" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" :indicator-name="indicatorName" item-title="Planta" description-title="Agente" value-title="Porcentaje en participacion" value2-title="Cantidades contratadas" :date="date" :status="status" :value="value" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import PieChart from './components/PieChart'
import TransactionTable from './components/TransactionTable'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'

export default {
  name: 'DashboardAdmin',
  components: {
    PieChart,
    TransactionTable
  },
  data() {
    return {
      indicatorName: 'gmp',
      date: new Date(),
      list: [],
      status: false,
      value: 0
    }
  },
  created() {
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    dateChange(event) {
      this.getData()
    },
    measureChange(item) {
      this.type = item
      this.getData()
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('gmg')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        // this.lastDate = new Date('01-01-2019')
        this.date = this.lastDate
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    async getData() {
      try {
        if (this.date > this.lastDate || this.date < this.initDate) {
          this.date = this.lastDate
        }

        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date)
        })
        if (result) {
          this.list = result.items
          this.status = result.status
          this.value = result.value
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
