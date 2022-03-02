<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">

        <div class="chart-wrapper">
          <h2>Desviación por agente: Generación programada vs generación real - {{ $t(type.text) }} </h2>
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
            <el-col :xs="24" :sm="8" :lg="2">
              <div class="label">Agrupacion:</div>
            </el-col>
            <el-col :xs="24" :sm="8" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione una Agrupacion" placement="bottom-end">
                <el-select :value="$t(type.text)" :placeholder="$t(type.text)" @change="groupChange($event)">
                  <el-option v-for="item in types" :key="item.id" :label="$t(item.text)" :value="item" />
                </el-select>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="listTable"
            :indicator-name="indicatorName"
            :item-title="$t(type.name1)"
            :description-title="$t(type.name2)"
            value-title="Desviación"
            status-title="Estado"
            :date="date"
            :type="type.id"
            :status="status"
            :value="value"
            :start-date="date"
            :loading="loading"
          />
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="list" value-title="Valor" :item-title="$t(type.name1)" />
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

var TYPES = [{
  id: 'agente',
  text: 'indicator.groups.agent',
  name1: 'Agente',
  name2: 'Código agente'
},
{
  id: 'planta',
  text: 'indicator.groups.plant',
  name1: 'Planta',
  name2: 'Código planta'
}
]

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    TransactionTable
  },
  data() {
    return {
      types: TYPES,
      type: TYPES[0],
      indicatorName: 'gpgr',
      date: new Date(),
      lastDate: new Date(),
      list: [],
      listTable: [],
      status: false,
      value: 0,
      loading: false
    }
  },
  created() {
    this.fetchLatest()
  },
  methods: {
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_dates = await getLastDate('gpgr')
        this.lastDate = new Date(range_dates[1])
        this.initDate = new Date(range_dates[0])
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    dateChange(event) {
      this.getData()
    },
    groupChange(item) {
      this.type = item
      this.getData()
    },
    async getData() {
      if (this.date > this.lastDate || this.date < this.initDate) {
        this.date = this.lastDate
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date),
          grupo: this.type.id
        })
        if (result) {
          this.list = _.orderBy(result.items, ['values'], ['asc'])
          this.listTable = _.orderBy(result.items, ['values'], ['desc'])
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
