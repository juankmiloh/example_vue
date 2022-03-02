<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{ span: 24 }" :sm="{ span: 24 }" :md="{ span: 24 }" :lg="{ span: 24 }" :xl="{ span: 24 }" style="padding-right: 8px; margin-bottom: 30px">
        <div class="chart-wrapper">
          <h2>{{ $t("route.pivotal3d") }}</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="16" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="16" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione un periodo" placement="bottom-end">
                <el-date-picker v-model="dateValue" type="daterange" align="right" unlink-panels range-separator=" - " :start-placeholder="$t('datePicker.startDate')" :end-placeholder="$t('datePicker.endDate')" @change="dateChange($event)" />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="16" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col :xs="24" :sm="16" :lg="2">
              <div class="label">Agente:</div>
            </el-col>
            <el-col :xs="24" :sm="16" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione un agente" placement="bottom-end">
                <el-select :value="agent.text" :placeholder="agent.id" @change="agentChange($event)">
                  <el-option v-for="item in agents" :key="item.id" :label="item.text" :value="item" />
                </el-select>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
        <div v-if="agent.id !== null && data.length === 0" class="chart-wrapper">
          <div class="note rcorners">
            <h3>
              <v-icon name="info-circle" class="svg-icon" />
              No hay datos para el agente y el rango de fechas seleccionados
            </h3>
          </div>
        </div>
        <div v-show="data.length !== 0" class="chart-wrapper">
          <line-chart :data="data" value-title="Valor" />
        </div>
        <div v-if="agent.id === null" class="chart-wrapper">
          <div class="note rcorners">
            <h3>
              <v-icon name="info-circle" class="svg-icon" /> Debe seleccionar un agente
            </h3>
          </div>
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="formatedData" :columns="columns" :agente="agent.text" :start-date="start" />
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
import LineChart from './components/Bar3dChart'
import TransactionTable from './components/TransactionTable'

export default {
  name: 'DashboardAdmin',
  components: {
    LineChart,
    TransactionTable
  },
  data() {
    var self = this
    return {
      indicatorName: 'pivotal3d',
      start: new Date(),
      end: new Date(),
      agents: [],
      agent: {
        id: null,
        text: 'Selecione un agente'
      },
      data: [],
      formatedData: [],
      columns: [],
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
        },
        {
          text: this.$t('datePicker.lastMonth'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        },
        {
          text: this.$t('datePicker.last3Days'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 3)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        },
        {
          text: this.$t('datePicker.last2Days'),
          onClick(picker) {
            self.end = new Date()
            self.start = new Date()
            self.start.setTime(self.start.getTime() - 3600 * 1000 * 24 * 2)
            picker.$emit('pick', [self.start, self.end])
            self.dateChange([self.start, self.end])
          }
        }
        ]
      },
      dateValue: []
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    this.fetchLatest()
    this.fetchAgents()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var rangeData = await getLastDate('pivotal3d')
        this.lastDate = new Date(rangeData[1])
        this.initDate = new Date(rangeData[0])
        this.end = this.lastDate
        this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 7)
        this.dateValue = [this.start, this.end]
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      this.getData()
    },
    async fetchAgents() {
      var agents = await getIndicator('agentes')
      this.agents = agents.items
    },
    async getData() {
      if (this.dateValue === null) {
        this.end = this.lastDate
        this.start = this.initDate
        this.dateValue = [this.start, this.end]
      }

      if (this.dateValue[1] > this.lastDate || this.dateValue[1] < this.initDate) {
        this.end = this.lastDate
        this.dateValue[1] = this.lastDate
      }
      if (this.dateValue[0] > this.lastDate || this.dateValue[0] < this.initDate) {
        this.start = this.initDate
        this.dateValue[0] = this.initDate
      }

      if (this.agent.id == null) {
        this.data = []
        return
      }

      try {
        var result = await getIndicator(this.indicatorName, {
          finicial: this.formatDate(this.start),
          ffinal: this.formatDate(this.end),
          id: this.agent.id
        })
        if (result) {
          if ('items' in result) {
            this.data = result.items
          } else {
            this.data = []
          }
          this.format(this.data)
        }
      } catch (error) {
        this.data = []
      }
    },
    format(data) {
      var formatedData = []
      this.columns = [...Array(24).keys()]
      if (this.data.length !== 0) {
        for (var i in data[0].table) {
          var row = {
            'Fecha': data[0].dates[i]
          }
          row['Mínimo'] = data[0].table[i][0]
          for (var j = 1; j < 25; j++) {
            row[j] = data[0].table[i][j]
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
    },
    agentChange(event) {
      this.agent = event
      this.getData()
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
.note {
    text-align: center;
}
</style>
