<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.rc') }} </h2>
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
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="data" value-title="Costo" :reference-date="initDate" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="formatedData" :columns="columns" :indicator-name="$t('route.rc')" />
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

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    TransactionTable
  },
  data() {
    var self = this
    return {
      lastDate: new Date(),
      initDate: new Date(),
      data: [],
      data2: [],
      injectionData: [],
      formatedData: [],
      columns: [],
      indicatorName: 'rc',
      start: new Date(),
      end: new Date(),
      sGroups: [],
      groups: [],
      sNits: [],
      nits: [],
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
    printLastDate() {
      return moment(this.lastDate).utc().format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('rc')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        this.end = new Date(range_data[1])
        this.start = new Date(range_data[0])
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      await this.getData()
      // this.format()
      this.format_rc()
    },
    async getData() {
      this.data = []
      if (this.initDate > this.start || this.lastDate < this.start) {
        this.start = this.initDate
      }
      if (this.initDate > this.end || this.lastDate < this.end) {
        this.end = this.lastDate
      }
      this.dateValue = [this.start, this.end]
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha_inicial: this.formatDate(this.start),
          fecha_final: this.formatDate(this.end)
        })
        if (result) {
          this.data = result.items
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
    },
    async format_rc() {
      var data = this.data
      if (!data[0]) {
        return []
      }
      this.columns = [{
        id: 'agent',
        name: 'Planta'
      },
      {
        id: 'cost',
        name: 'Costo regasificación'
      },
      {
        id: 'quantity',
        name: 'Cantidad regasificación'
      }
      ]

      var formatedData = []
      var rows = data
      for (const i in rows) {
        for (const d in rows[i].dates) {
          var row = {
            'date': rows[i].dates[d],
            agent: rows[i].names,
            cost: rows[i].values[d],
            quantity: rows[i].values2[d].toFixed(2)
          }
          formatedData.push(row)
        }
      }
      this.formatedData = formatedData
    },
    dateChange(event) {
      this.start = event[0]
      this.end = event[1]
      this.getData()
      this.format_rc()
    },
    groupChange(envet) {
      this.getData()
      this.format_rc()
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
.el-tag {
    background-color: rgb(48, 65, 86);
    color: #fff;
    font-size: 14px;
}

.dashboard-editor-container {
    padding: 32px;
    background-color: rgb(254, 254, 254);

    .chart-wrapper {
        background: #fff;
        padding: 16px 16px 0;
        margin-bottom: 32px;
    }
}

.el-date-editor.el-input,
.el-date-editor.el-input__inner {
    width: 100% !important;
}

.el-select {
    width: 100% !important;
}

.transction-table .chart {
    width: 100%;
    padding-top: 15px;
    height: 660px;
}

.el-tag {
    background-color: rgb(48, 65, 86);
    color: #fff;
    font-size: 14px;
}
</style>
