<template>
  <div class="dashboard-editor-container">

    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> Índice Hirschman Herfindahl - {{ title }} </h2>
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
                Datos actualizados a fecha de {{ printCurrentDate() }}
              </el-tag>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="list"
            :chart-title="title"
            :indicator-name="indicatorName"
            item-title="Planta"
            description-title="Agente"
            value-title="Cuota de Mercado"
            status-title="Estado"
            :descriptions="descriptions"
            :date="date"
            :status="status"
            :value="value"
          />
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
  props: {
    title: {
      type: String,
      default: ''
    },
    indicador: {
      type: String,
      default: ''
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
      date: new Date(),
      ihhCapacityLastDate: new Date(),
      ihhGenerationLastDate: new Date(),
      list: [],
      status: false,
      value: 0
    }
  },
  created() {
    this.fetchLatest()
  },
  methods: {
    async fetchLatest() {
      try {
        var rangeDatesIhhCapacity = await getLastDate('ihh_capacity')
        var rangeDatesIhhGeneration = await getLastDate('ihh_generation')

        this.ihhCapacityLastDate = new Date(rangeDatesIhhCapacity[1])
        this.ihhGenerationLastDate = new Date(rangeDatesIhhGeneration[1])

        this.ihhCapacityInitDate = new Date(rangeDatesIhhCapacity[0])
        this.ihhGenerationInitDate = new Date(rangeDatesIhhGeneration[0])
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    printCurrentDate() {
      var currentDate = this.indicador === 'capacidad' ? this.ihhCapacityLastDate : this.ihhGenerationLastDate
      return moment(currentDate).format('DD/MM/YYYY')
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    dateChange(event) {
      this.getData()
    },
    plantFilterChange(item) {
      this.plantFilter = item
      this.getData()
    },
    async getData() {
      if (this.indicador === 'capacidad') {
        if (this.date < this.ihhCapacityInitDate || this.date > this.ihhCapacityLastDate) {
          this.date = this.ihhCapacityLastDate
        }
      } else if (this.date > this.ihhGenerationLastDate || this.date < this.ihhGenerationInitDate) {
        this.date = this.ihhGenerationLastDate
      }
      if (this.indicador === 'declaredDisponibility') {
        this.plantFilter = FILTERS[1]
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date),
          medida: this.indicador,
          central_dipatch: this.plantFilter.id
        })
        if (result) {
          this.list = _.orderBy(result.items, ['values.0'], ['desc'])
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
