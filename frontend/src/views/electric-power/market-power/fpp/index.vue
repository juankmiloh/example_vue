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
          <h2>{{ $t("route.fpp") }}</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione un periodo"
                placement="bottom-end"
              >
                <date-picker
                  key="month-picker"
                  v-model="dates"
                  type="day"
                  range
                  placeholder="Seleccione rango de días"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag
                type="warning"
              >Datos actualizados a fecha de {{ printLastDate() }}</el-tag>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Agrupación:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <div class="label">
                <el-switch
                  v-model="agruparPorPlanta"
                  active-text="Planta"
                  inactive-text="Agente"
                  @change="checkChange($event)"
                />
              </div>
              <br>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col v-show="showNoDataMessage" :xs="24" :sm="8" :lg="8">
              <br>
              <el-alert
                title="No se encontraron datos para el filtro seleccionado"
                type="warning"
                effect="light"
                :closable="false"
              />
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bubble-chart :data="data" :agrupar-por-planta="agruparPorPlanta" />
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="data" :agrupar-por-planta="agruparPorPlanta" />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="formatedData"
            :columns="columns"
            :indicator-name="$t('route.fpp')"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import { getIndicator, getLastDate } from '@/api/remoteSearch'
import BarChart from './components/BarChart'
import BubbleChart from './components/BubbleChart'
import TransactionTable from './components/TransactionTable'
import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'

var TOLERANCES = [...Array(101).keys()]
TOLERANCES.shift()

var OPTIONS = [...Array(101).keys()]
OPTIONS.shift()

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    BubbleChart,
    TransactionTable,
    DatePicker
  },
  data() {
    return {
      lastDate: new Date(),
      data: {},
      dates: [],
      formatedData: [],
      indicatorName: 'fpp',
      sGroups: [],
      groups: [],
      agruparPorPlanta: true,

      tolerances: TOLERANCES,
      sTolerances: 10,
      mediasToShow: OPTIONS,
      sMediasToShow: 10,
      topsToShow: OPTIONS,
      sTopsToShow: 10,

      plants: [],
      sPlants: [],
      oldPlants: [],
      agents: [],
      sAgents: [],
      oldAgents: [],
      causes: [],
      sCauses: [],
      oldCauses: [],
      techs: [],
      sTechs: [],
      oldTechs: [],

      columns: [
        { id: 'agente', name: 'Agente' },
        { id: 'planta', name: 'Nombre planta' },
        { id: 'codigo', name: 'Fecha' },
        { id: 'frecuencia', name: 'Número de fijaciones' },
        { id: 'duracion', name: 'Precio promedio de fijación' }
      ],
      showNoDataMessage: false
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
        var range_data = await getLastDate('fpp')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        this.dates = [moment(range_data[1]).subtract(1, 'month').toDate(), new Date(range_data[1])]
        console.info('this.dates: ' + this.dates)
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      await this.getData()
      this.format_rc()
    },
    async getData() {
      if (this.dates[1] > this.lastDate || this.dates[1] < this.initDate) {
        this.dates[0] = this.initDate
        this.dates[1] = this.lastDate
      }
      if (this.dates[0] > this.lastDate || this.dates[0] < this.initDate) {
        this.dates[0] = this.initDate
        this.dates[1] = this.lastDate
      }
      this.data = {}

      var plantIds = []
      for (const i in this.sPlants) {
        plantIds.push(this.sPlants[i].id)
      }
      var agentsIds = []
      for (const i in this.sAgents) {
        agentsIds.push(this.sAgents[i].id)
      }
      var causesIds = []
      for (const i in this.sCauses) {
        causesIds.push(this.sCauses[i].id)
      }
      var techsIds = []
      for (const i in this.sTechs) {
        techsIds.push(this.sTechs[i].id)
      }
      try {
        var result = await getIndicator('fpp', {
          fecha_inicial: this.formatDate(
            this.dates[0]
          ),
          fecha_final: this.formatDate(
            this.dates[1]
          ),
          agrupar_por_planta: this.agruparPorPlanta
        })
        if (result) {
          // return
          this.data = result
          if (result === undefined || result.length === 0) {
            this.showNoDataMessage = true
          } else {
            this.showNoDataMessage = false
          }
        }
      } catch (error) {
        console.error(error)
        this.data = {}
      }
    },
    async format_rc() {
      var formatedData = []
      var rows = this.data.items
      var row = {}
      if (rows === undefined || rows.length === 0) {
        return []
      }
      for (const i in rows) {
        row = {
          agente: rows[i].values[5],
          planta: rows[i].values[6],
          codigo: rows[i].values[0],
          frecuencia: rows[i].values[2],
          duracion: rows[i].values[3]
        }
        formatedData.push(row)
      }
      this.formatedData = formatedData
    },
    async periodChange(event) {
      await this.getData()
      await this.format_rc()
    },
    async toleranceChange() {
      await this.getData()
      await this.format_rc()
    },
    async fetchCategories() {
      var plants = await getIndicator('plantas-generacion')
      var plantGroups = []
      for (const i in plants.items) {
        plantGroups.push({
          id: plants.items[i][0],
          name: plants.items[i][1]
        })
      }
      this.plants = plantGroups

      var agents = await getIndicator('agentes-generacion')
      var agentGroups = []
      for (const i in agents.items) {
        agentGroups.push({
          id: agents.items[i][0],
          name: agents.items[i][1]
        })
      }
      this.agents = agentGroups
    },
    async dateChange(event) {
      this.dates = event
      await this.getData()
      await this.format_rc()
    },
    async checkChange(event) {
      this.agruparPorPlanta = event
      await this.getData()
      await this.format_rc()
    },
    async categoryChange() {
      if ((await this.oldPlants) !== (await this.sPlants)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldPlants = this.sAgents

      if ((await this.oldAgents) !== (await this.sAgents)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldAgents = this.sAgents

      if ((await this.oldCauses) !== (await this.sCauses)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldCauses = this.sCauses

      if ((await this.oldTechs) !== (await this.sTechs)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldTechs = this.sTechs
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
