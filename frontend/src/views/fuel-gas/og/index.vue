<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.og') }} </h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-date-picker v-model="dateValue" type="daterange" align="right" unlink-panels range-separator=" - " :start-placeholder="$t('datePicker.startDate')" :end-placeholder="$t('datePicker.endDate')" @change="dateChange($event)" />
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Region:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <multiselect v-model="sRegions" :options="regions" :multiple="false" :taggable="true" placeholder="Seleccione region" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="regionChange()" @tag="regionChange()" />
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Procedencia:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="22">
              <multiselect v-model="sGroups" :options="groups" :multiple="true" :taggable="true" placeholder="Seleccione agrupación" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="groupChange()" @tag="groupChange()" />
            </el-col>
          </el-row>
        </div>
        <div v-if="sGroups.length" class="chart-wrapper">
          <line-chart :data="list" value-title="Valor" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import Multiselect from 'vue-multiselect'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import LineChart from './components/LineChart'
import TransactionTable from './components/TransactionTable'

export default {
  name: 'DashboardAdmin',
  components: {
    LineChart,
    Multiselect,
    TransactionTable
  },
  data() {
    var self = this
    return {
      indicatorName: 'og',
      start: new Date(),
      end: new Date(),
      sRegions: [],
      regions: [],
      dict_regions: {},
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

    this.fetchGrups()
    this.fetchRegions()
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var rangeData = await getLastDate('gmg_og')
        this.lastDate = new Date(rangeData[1])
        this.initDate = new Date(rangeData[0])
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      this.getData()
    },
    async fetchGrups() {
      var grupos = await getIndicator('fuentes')
      this.groups = grupos.items
    },
    async fetchRegions() {
      var regions = await getIndicator('regiones')
      for (var i in regions.items) {
        var fuente = regions.items[i][0]
        var region = regions.items[i][1]
        if (!this.regions.includes(region)) {
          this.regions.push(region)
          this.dict_regions[region] = []
        }
        this.dict_regions[region].push(fuente)
      }
    },
    async getData() {
      var aux = []
      this.list = []

      if (this.end > this.lastDate || this.end < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      } else if (this.start > this.lastDate || this.start < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      }

      this.dateValue = [this.start, this.end]

      try {
        for (const key in this.sGroups) {
          var result = await getIndicator(this.indicatorName, {
            fecha_incial: this.formatDate(this.start),
            fecha_final: this.formatDate(this.end),
            grupo: this.sGroups[key],
            region: this.sRegions
          })
          if (result) {
            aux.push({
              name: this.sGroups[key],
              data: result.items
            })
          }
        }
        this.list = aux
      } catch (error) {
        this.list = []
      }
    },
    dateChange(event) {
      this.start = event[0]
      this.end = event[1]

      this.getData()
    },
    groupChange(envet) {
      this.sRegions = []
      this.getData()
    },
    regionChange(envet) {
      if (this.sRegions) {
        this.sGroups = this.dict_regions[this.sRegions]
      }

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
