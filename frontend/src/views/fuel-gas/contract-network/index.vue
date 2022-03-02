<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 24 }"
        :lg="{ span: 24 }"
        :xl="{ span: 24 }"
        style="padding-right: 8px; margin-bottom: 30px"
      >
        <div class="chart-wrapper">
          <h2>{{ $t("route.contractNetwork") }}</h2>
          <el-row :gutter="32">

            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-date-picker
                v-model="dateValue"
                type="daterange"
                align="right"
                unlink-panels
                range-separator=" - "
                :start-placeholder="$t('datePicker.startDate')"
                :end-placeholder="$t('datePicker.endDate')"
                @change="dateChange($event)"
              />
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Agente:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione un agente" placement="bottom-end">
                <el-select :value="agent.text" :placeholder="agent.id" @change="agentChange($event)">
                  <el-option v-for="item in agents" :key="item.id" :label="item.text" :value="item" />
                </el-select>
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Modalidad:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-tooltip class="item" effect="dark" content="Seleccione un modalidad" placement="bottom-end">
                <el-select :value="modality.text" :placeholder="modality.id" @change="modalityChange($event)">
                  <el-option v-for="item in modalities" :key="item.id" :label="item.text" :value="item" />
                </el-select>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>

        <div class="chart-wrapper">
          <graph-chart
            :data="list"
            :public_conf="public_conf"
            value-title="Índice"
          />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="list"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import GraphChart from './components/GraphChart'
import TransactionTable from './components/TransactionTable'
import { getIndicator, getLastDate } from '@/api/remoteSearch'

const MOADLITIES = [
  { 'id': 'Firme', 'text': 'Firme' },
  { 'id': 'Con Interrupciones', 'text': 'Con Interrupciones' }
]

export default {
  name: 'DashboardAdmin',
  components: {
    TransactionTable,
    GraphChart
  },
  data() {
    return {
      public_conf: process.env.VUE_APP_PUBLIC === 'true',
      indicatorName: 'contract_network',
      end: new Date(),
      start: new Date(),
      lastDate: new Date(),
      dateValue: [],
      list: {},
      value: [],
      agents: [],
      modalities: MOADLITIES,
      modality: MOADLITIES[0],
      agent: {
        id: null,
        text: 'Selecione un agente'
      }
    }
  },
  created() {
    this.fetchLatest()
    this.getData()
  },
  methods: {
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    dateChange(event) {
      if (event) {
        this.start = event[0]
        this.end = event[1]
        this.agent = {
          id: null,
          text: 'Selecione un agente'
        }
        this.getData()
      }
    },
    agentChange(event) {
      this.agent = event
      this.getData()
    },
    modalityChange(event) {
      this.modality = event
      this.getData()
    },
    async fetchLatest() {
      try {
        var range_dates = await getLastDate('gmg')
        this.lastDate = new Date(range_dates[1])
        this.initDate = new Date(range_dates[0])
        this.end = this.lastDate
        this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 30)
        this.dateValue = [this.start, this.end]
      } catch (error) {
        this.end = new Date()
        this.start = new Date()
        console.error(error)
      }
    },
    async getData() {
      if (this.end > this.lastDate || this.end < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      } else if (this.start > this.lastDate || this.start < this.initDate) {
        this.end = this.lastDate
        this.start = new Date(2019, 0, 1)
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha_inicial: this.formatDate(this.start),
          fecha_final: this.formatDate(this.end),
          agente: this.agent.id,
          modalidad: this.modality.id
        })
        console.info('result:', result)
        if (result) {
          this.list = result.items
          this.agents = result.items.agents
        }
      } catch (error) {
        console.info('error:', error)
        this.list = []
        this.value = 0
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
