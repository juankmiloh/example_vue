<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">

        <div class="block">
          <el-date-picker v-model="date" type="month" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
        </div>

        <h2> {{ $t('route.pm') }} </h2>

        <transaction-table :data="list" :indicator-name="indicatorName" item-title="Planta" description-title="Agente" value-title="Cuota de mercado (porcentaje de fijación de precios)" status-title="Estado" :date="date" :status="status" :value="value" />
      </el-col>
    </el-row>

    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="24">
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
  getIndicator
} from '@/api/remoteSearch'
import moment from 'moment'

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
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
    this.date = new Date('01-01-2019') // TODO drop
    // this.date = new Date() // TODO uncomment
    this.getData()
  },
  methods: {
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
    async getData() {
      try {
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
.dashboard-editor-container {
    padding: 32px;
    background-color: rgb(254, 254, 254);

    .chart-wrapper {
        background: #fff;
        padding: 16px 16px 0;
        margin-bottom: 32px;
    }
}
</style>
