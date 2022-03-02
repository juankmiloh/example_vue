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
          <h2>{{ $t("route.iag") }}</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="9">
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
                  placeholder="Seleccione rango de meses"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="12">
              <el-tag
                type="warning"
              >Datos actualizados a fecha de {{ printLastDate() }}</el-tag>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Agentes:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="9">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione los agentes"
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
                  placeholder="Seleccione los agentes a filtrar"
                  @input="categoryChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Tecnología de generación:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="9">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione las técnologías"
                placement="bottom-end"
              >
                <multiselect
                  v-model="sTechs"
                  label="name"
                  track-by="id"
                  :options="techs"
                  :multiple="true"
                  :searchable="true"
                  :close-on-select="false"
                  :allow-empty="true"
                  placeholder="Seleccione las tecnologías de generación a filtrar"
                  @input="categoryChange($event)"
                />
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Plantas:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="9">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione las plantas"
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
                  :option-height="80"
                  placeholder="Seleccione las plantas a filtrar"
                  @input="categoryChange($event)"
                >
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__title">{{ props.option.name }}</span>
                    </div>
                  </template>
                </multiselect>
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Causa:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="9">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione las plantas"
                placement="bottom-end"
              >
                <multiselect
                  v-model="sCauses"
                  label="name"
                  track-by="id"
                  :options="causes"
                  :multiple="true"
                  :searchable="true"
                  :close-on-select="false"
                  :allow-empty="true"
                  placeholder="Seleccione las causas a filtrar"
                  @input="categoryChange($event)"
                />
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="24" :lg="6">
              Número de plantas con mayor duración media de indisponibilidad a
              mostrar:
            </el-col>

            <el-col :xs="24" :sm="24" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione el número de plantas con mayor duración media a mostrar"
                placement="bottom-end"
              >
                <el-slider
                  v-model="sMediasToShow"
                  show-input
                  @change="toleranceChange()"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="6">
              Número de plantas con mayor tiempo de indisponibilidad a mostrar:
            </el-col>
            <el-col :xs="24" :sm="24" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione el número de plantas con mayor tiempo de indisponibilidad a mostrar"
                placement="bottom-end"
              >
                <el-slider
                  v-model="sTolerances"
                  show-input
                  @change="toleranceChange()"
                />
              </el-tooltip>
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
          <bar-chart :data="data" />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="formatedData"
            :columns="columns"
            :indicator-name="$t('route.iag')"
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
import TransactionTable from './components/TransactionTable'
import Multiselect from 'vue-multiselect'
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
    TransactionTable,
    Multiselect,
    DatePicker
  },
  data() {
    return {
      lastDate: new Date(),
      data: [],
      dates: [],
      formatedData: [],
      indicatorName: 'iag',
      sGroups: [],
      groups: [],

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
        { id: 'planta', name: 'Planta' },
        { id: 'codigo', name: 'Código Planta' },
        { id: 'tecnologia', name: 'Tecnología de generación' },
        { id: 'causa', name: 'Causa' },
        { id: 'especifica', name: 'Causa Especifica' },
        { id: 'capacidad', name: 'Capacidad Efectiva Neta' },
        { id: 'duracion', name: 'Duración Media en horas' },
        { id: 'frecuencia', name: 'Frecuencia en número de veces' }
      ],

      showNoDataMessage: false
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    await this.fetchCategories()
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).utc().format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('iag')
        this.initDate = new Date(range_data[0])
        this.lastDate = new Date(range_data[1])
        this.dates = [new Date(range_data[1]), new Date(range_data[1])]
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
        var result = await getIndicator('iag', {
          fecha_inicial: this.formatDate(
            moment(this.dates[0]).startOf('month').toDate()
          ),
          fecha_final: this.formatDate(
            moment(this.dates[1]).startOf('month').add(1, 'month').toDate()
          ),
          medias_a_mostrar: this.sMediasToShow,
          top_a_mostrar: this.sTopsToShow,
          causas: causesIds,
          tecnologias: techsIds,
          agentes: agentsIds,
          plantas: plantIds
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
      var formatedData = []
      var rows = this.data
      var row = {}
      if (rows === undefined || rows.length === 0) {
        return []
      }
      for (const i in rows) {
        for (const d in rows[i].values) {
          row = {
            agente: rows[i].values[d][0],
            planta: rows[i].values[d][1],
            codigo: rows[i].values[d][2],
            causa: rows[i].values[d][4],
            tecnologia: rows[i].values[d][3],
            especifica: rows[i].values[d][5],
            capacidad: rows[i].values[d][6],
            duracion: rows[i].values[d][7],
            frecuencia: rows[i].values[d][8]
          }
          formatedData.push(row)
        }
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

      var causes = await getIndicator('causas')
      var causesGroups = []
      for (const i in causes.items) {
        causesGroups.push({
          id: causes.items[i][0],
          name: causes.items[i][1]
        })
      }
      this.causes = causesGroups

      var techs = await getIndicator('tecnologias')
      var techsGroups = []
      for (const i in techs.items) {
        techsGroups.push({
          id: techs.items[i][0],
          name: techs.items[i][1]
        })
      }
      this.techs = techsGroups
    },
    async dateChange(event) {
      this.dates = event
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
