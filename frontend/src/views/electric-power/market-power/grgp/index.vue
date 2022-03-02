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
          <h2>Desviación en el sistema: Generación programada vs generación real</h2>
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" :indicator-name="indicatorName" item-title="Fecha" description-title="Fecha" value-title="Desviación" status-title="Estado" :date="date" :type="type.id" :status="status" :value="value" />
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
import _ from 'lodash'

var TYPES = [{
  id: 'capacidad',
  text: 'indicator.types.capacity'
},
{
  id: 'generacion',
  text: 'indicator.types.generation'
}
]

var FILTERS = [{
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
    TransactionTable
  },
  data() {
    return {
      types: TYPES,
      type: TYPES[0],
      plantFilters: FILTERS,
      plantFilter: FILTERS[0],
      indicatorName: 'gpgr',
      date: new Date(),
      lastDate: new Date(),
      list: [],
      status: false,
      value: 0
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
    dateChange(event) {
      this.getData()
    },
    measureChange(item) {
      this.type = item
      this.getData()
    },
    plantFilterChange(item) {
      this.plantFilter = item
      this.getData()
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
    async getData() {
      if (this.date > this.lastDate || this.date < this.initDate) {
        this.date = this.lastDate
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date),
          medida: this.type.id,
          central_dipatch: this.plantFilter.id
        })
        if (result) {
          this.list = _.orderBy(result.items, ['dates'], ['asc'])
          this.status = Boolean(result.status)
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
