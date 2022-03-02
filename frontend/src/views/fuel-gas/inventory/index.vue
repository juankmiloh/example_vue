<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.gasInventory') }} </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-date-picker v-model="dateValue" type="daterange" align="right" unlink-panels range-separator=" - " :start-placeholder="$t('datePicker.startDate')" :end-placeholder="$t('datePicker.endDate')" @change="dateChange($event)" />
            </el-col>
            <el-col :xs="24" :sm="12" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <template v-if="!publicConf">
              <el-col :xs="24" :sm="12" :lg="2">
                <div class="label">Planta:</div>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="6">
                <el-tooltip class="item" effect="dark" content="Seleccione una Planta" placement="bottom-end">
                  <el-select :value="plant.text" :placeholder="plant.text" @change="plantChange($event)">
                    <el-option v-for="item in plants" :key="item.id" :label="$t(item.text)" :value="item" />
                  </el-select>
                </el-tooltip>
              </el-col>
            </template>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="data" :injection-data="injectionData" value-title="Valor" :reference-date="lastDate" :plant="plant" :plants="plantsD" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="formatedData" :columns="columns" :indicator-name="$t('route.gasInventory')" />
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
import BarChart from './components/BarChart'
import TransactionTable from './components/TransactionTable'
import _ from 'lodash'

var PLANTS = [
  { id: 'Total', text: 'Total' },
  { id: 'Termobarranquilla S.A.', text: 'Tebsa' },
  { id: 'Prime Termoflores S.A.', text: 'Flores' },
  { id: 'Termocandelaria S.C.A.', text: 'Candelaria' }
]

var PLANTS_D = {
  'Total': { text: 'Total', color: '#000' },
  'Termobarranquilla S.A.': { text: 'Tebsa', color: '#1E90FF' },
  'Prime Termoflores S.A.': { text: 'Flores', color: '#91c7ae' },
  'Termocandelaria S.C.A.': { text: 'Candelaria', color: '#A0A0A0' }
}

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    TransactionTable
  },
  data() {
    var self = this
    return {
      plants: PLANTS,
      plantsD: PLANTS_D,
      publicConf: process.env.VUE_APP_PUBLIC === 'true',
      plant: PLANTS[0],
      lastDate: new Date(),
      data: [],
      injectionData: [],
      formatedData: [],
      columns: [],
      indicatorName: 'gmg-inventory',
      start: new Date(),
      end: new Date(),
      sGroups: [],
      groups: [],
      list: [],
      pickerOptions: {
        shortcuts: [{
          text: this.$t('datePicker.lastWeek'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        }, {
          text: this.$t('datePicker.lastMonth'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        }, {
          text: this.$t('datePicker.last3Days'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 3)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        }, {
          text: this.$t('datePicker.last2Days'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 2)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        }]
      },
      dateValue: []
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    this.fetchLatest()
  },
  methods: {
    plantChange(item) {
      this.plant = item
    },
    printLastDate() {
      return moment(this.lastDate).utc().format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('gmg_inventory')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      await this.getData()
      await this.getInjectionData()
      this.format()
    },
    async getInjectionData() {
      try {
        var result = await getIndicator('gmg-injection', {
          fecha_inicial: this.formatDate(this.start),
          fecha_final: this.formatDate(this.end)
        })
        if (result) {
          this.injectionData = result.items
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
    },
    async getData() {
      this.data = []
      if (this.end > this.lastDate || this.end < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      } else if (this.start > this.lastDate || this.start < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      }
      this.dateValue = [this.start, this.end]
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha_inicial: this.formatDate(this.start),
          fecha_final: this.formatDate(this.end)
        })
        if (result) {
          this.data = _.sortBy(result.items, function(item) {
            return item.id === 'Total' ? 0 : 1
          })
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
    },
    async format() {
      var data = this.data
      if (!data[0]) {
        return []
      }
      this.columns = []
      this.columns.push({
        id: 'injectionData',
        name: 'Volumen inyectado'
      })
      for (const key in data) {
        this.columns.push({
          id: key,
          name: data[key].id
        })
      }
      var formatedData = []
      var rows = data[0].dates
      for (const i in rows) {
        var row = {
          'date': rows[i],
          injectionData: this.injectionData[0].values[i]
        }
        for (const key in data) {
          row[key] = data[key].values[i]
        }
        formatedData.push(row)
      }
      this.formatedData = formatedData
    },
    async dateChange(event) {
      this.start = event[0]
      this.end = event[1]
      await this.getData()
      await this.getInjectionData()
      this.format()
    },
    groupChange(envet) {
      this.getData()
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
.transction-table .chart {
    width: 100%;
    padding-top: 15px;
    height: 660px;
}
</style>
