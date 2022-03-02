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
          <h2>Indisponibilidad de activos de red</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="5">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione un periodo"
                placement="bottom-end"
              >
                <date-picker
                  key="month-picker"
                  v-model="dates"
                  type="month"
                  range
                  :placeholder="datePlaceholder"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8" style="margin-bottom: 15px">
              <el-tag
                type="warning"
              >Datos actualizados a fecha de {{ printLastDate() }}</el-tag>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="4" style="margin-bottom: 15px">
              <div class="label">Agrupar por agentes:</div>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="4">
              <el-tooltip
                class="item"
                effect="dark"
                content="Haga click para agrupar por agentes"
                placement="bottom-end"
              >
                <div class="label">
                  <el-switch v-model="flip" @change="onFlip($event)" />
                </div>
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="3">
              Número de activos a mostrar:
            </el-col>
            <el-col :xs="24" :sm="12" :lg="5">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione el número de activos a mostrar"
                placement="bottom-end"
              >
                <el-slider
                  v-model="sTolerances"
                  show-input
                  @change="toleranceChange()"
                />
              </el-tooltip>
            </el-col>
            <template v-if="flip">
              <el-col :xs="24" :sm="12" :lg="2">
                <div class="label">Agentes:</div>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="14">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="Seleccione agentes"
                  placement="bottom-end"
                >
                  <multiselect
                    v-model="sAgents"
                    label="name"
                    track-by="id"
                    :options="agents"
                    :multiple="true"
                    :searchable="true"
                    :close-on-select="false"
                    :allow-empty="true"
                    placeholder="Seleccione agentes"
                    @input="plantChange($event)"
                  />
                </el-tooltip>
              </el-col>
            </template>
            <template v-else>
              <el-col :xs="24" :sm="24" :lg="2">
                <div class="label">Activos:</div>
              </el-col>
              <el-col :xs="24" :sm="24" :lg="14">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="Seleccione activos"
                  placement="bottom-end"
                >
                  <multiselect
                    v-model="sPlants"
                    label="name"
                    track-by="id"
                    :options="plants"
                    :multiple="true"
                    :searchable="true"
                    :close-on-select="false"
                    :allow-empty="true"
                    placeholder="Seleccione los activos a filtrar"
                    @input="plantChange($event)"
                  />
                </el-tooltip>
              </el-col>
            </template>
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
          <bar-chart
            :data="data"
            :value-title="activoAgente"
            :reference-date="initDate"
            :tolerances="sTolerances"
          />
        </div>
        <div class="chart-wrapper">
          <area-chart
            :data="data"
            :value-title="activoAgente"
            :reference-date="initDate"
          />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="formatedData"
            :columns="columns"
            :indicator-name="$t('route.iar')"
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
import AreaChart from './components/AreaChart'
import TransactionTable from './components/TransactionTable'
import Multiselect from 'vue-multiselect'
import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'

var PERIODS = ['Diario', 'Semanal', 'Mensual', 'Anual']

var TOLERANCES = [...Array(101).keys()]
TOLERANCES.shift()

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    AreaChart,
    TransactionTable,
    Multiselect,
    DatePicker
  },
  data() {
    return {
      lastDate: new Date(),
      initDate: new Date(),
      data: [],
      data2: [],
      injectionData: [],
      formatedData: [],
      indicatorName: 'iar',
      start: new Date(),
      end: new Date(),
      sGroups: [],
      groups: [],
      sNits: [],
      nits: [],
      list: [],
      dateValue: [],

      periods: PERIODS,
      sPeriods: PERIODS[2],

      tolerances: TOLERANCES,
      sTolerances: 10,

      plants: [],
      sPlants: [],
      oldPlants: [],
      agents: [],
      sAgents: [],
      oldAgents: [],

      activoAgente: 'Activo',
      columns: [
        {
          id: 'value',
          name: 'Activo'
        },
        {
          id: 'hc',
          name: 'Horas de compensación'
        },
        {
          id: 'hid',
          name: 'Horas de indisponibilidad'
        }
      ],

      dates: [],
      datePickerType: 'month',
      datePlaceholder: 'Seleccione rango de meses',

      flip: false,
      flipAcc: false,
      showNoDataMessage: false
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    await this.fetchPlants()
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).utc().format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('iar')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        this.end = new Date(range_data[1])
        this.start = new Date(range_data[0])
        this.dates = [new Date(range_data[0]), new Date(range_data[1])]
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

      this.data = []
      this.dateValue = [this.start, this.end]

      var plantIds = []
      var sPlants = this.sPlants
      if (this.flip) {
        sPlants = this.sAgents
      }
      for (const i in sPlants) {
        plantIds.push(sPlants[i].id)
      }
      try {
        var result = await getIndicator('iar', {
          fecha_inicial: this.formatDate(
            moment(this.dates[0]).startOf('month').toDate()
          ),
          fecha_final: this.formatDate(
            moment(this.dates[1]).startOf('month').add(1, 'month').toDate()
          ),
          periodo: this.sPeriods,
          resultados: this.sTolerances,
          agente: plantIds,
          agrupar_por_agente: this.flip
        })
        if (result) {
          this.data = result.items
          if (result === undefined || result.length === 0) {
            this.showNoDataMessage = true
          } else {
            this.showNoDataMessage = false
          }
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
    },
    async format_rc() {
      var data = this.data
      if (data === undefined || data.length === 0) {
        return []
      }

      var formatedData = []
      var rows = data
      var row = {}
      for (const i in rows) {
        for (const d in rows[i].value) {
          row = {
            value: rows[i].value[d],
            hc: rows[i].hc[d],
            hid: rows[i].hid[d]
          }
          formatedData.push(row)
        }
      }
      this.formatedData = formatedData
    },
    async periodChange(event) {
      this.dates = []
      if (event === 'Diario') {
        this.datePickerType = 'date'
        this.datePlaceholder = 'Seleccione rango de días'
      } else if (event === 'Semanal') {
        this.datePickerType = 'week'
        this.datePlaceholder = 'Seleccione rango de semanas'
      } else if (event === 'Mensual') {
        this.datePickerType = 'month'
        this.datePlaceholder = 'Seleccione rango de meses'
      } else if (event === 'Anual') {
        this.datePickerType = 'year'
        this.datePlaceholder = 'Seleccione rango de años'
      }
      await this.getData()
      await this.format_rc()
    },
    async toleranceChange() {
      await this.getData()
      await this.format_rc()
    },
    async fetchPlants() {
      var plants = await getIndicator('activos')
      var plantGroups = []
      for (const i in plants.items) {
        plantGroups.push({
          id: plants.items[i][0],
          name: plants.items[i][1]
        })
      }
      this.plants = plantGroups

      var agents = await getIndicator('agents')
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
    async plantChange() {
      if ((await this.oldPlants) !== (await this.sPlants)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldAgents = this.sAgents
      if ((await this.oldAgents) !== (await this.sAgents)) {
        await this.getData()
        await this.format_rc()
      }
      this.oldPlants = this.sAgents
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    async onFlip(value) {
      if (value === true) {
        this.activoAgente = 'Agente'
        this.columns[0] = {
          id: 'value',
          name: 'Agente'
        }
      } else {
        this.activoAgente = 'Activo'
        this.columns[0] = {
          id: 'value',
          name: 'Activo'
        }
      }
      await this.getData()
      await this.format_rc()
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
