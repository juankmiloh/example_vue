<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">

        <div class="chart-wrapper">
          <el-row :gutter="32">
            <el-col :xs="24" :sm="2" :lg="1">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col :xs="24" :sm="10" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione una fecha" placement="bottom-end">
                <el-date-picker v-model="date" type="date" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="10" :lg="7">
              <el-tag class="el-tag--dark">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
          <h2> Índice Herfindahl-Hirschman - {{ $t('route.trsd') }} </h2>
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" :indicator-name="indicatorName" item-title="Agente" description-title="Agente" value-title="Cuota de mercado (porcentaje de fijación de precios)" status-title="Estado" :date="date" :status="status" :value="value" />
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import TransactionTable from './components/TransactionTable'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'

export default {
  name: 'DashboardAdmin',
  components: {
    TransactionTable
  },
  data() {
    return {
      indicatorName: 'trsd',
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
    async fetchLatest() {
      try {
        var range_dates = await getLastDate('trsd')
        this.lastDate = new Date(range_dates[1])
        this.initDate = new Date(range_dates[0])
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
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
    async getData() {
      if (this.date > this.lastDate || this.date < this.initDate) {
        this.date = this.lastDate
      }
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
</style>
