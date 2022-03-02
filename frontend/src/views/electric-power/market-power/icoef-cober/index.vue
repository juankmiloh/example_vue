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
          <h2>{{ $t("route.icoefCober") }}</h2>
          <el-row :gutter="32">
            <el-col :xs="12" :sm="12" :lg="2">
              <div class="label">Periodo:</div>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione un periodo"
                placement="bottom-end"
              >
                <multiselect
                  v-model="sPeriods"
                  :options="periods"
                  :multiple="false"
                  :taggable="false"
                  :allow-empty="false"
                  :show-labels="false"
                  placeholder="Seleccione un periodo"
                  @input="periodChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag
                type="warning"
              >Datos actualizados a fecha de {{ printLastDate() }}</el-tag>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="3">
              <div class="label">Tolerancia (%):</div>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="5">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione una tolerancia"
                placement="bottom-end"
              >
                <el-input-number
                  v-model="sTolerances"
                  :min="1"
                  :max="100"
                  @change="toleranceChange()"
                />
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Plantas:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
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
                  :show-labels="false"
                  placeholder="Seleccione plantas"
                  @input="plantChange($event)"
                />
              </el-tooltip>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Rango del periodo:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="5">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione un periodo"
                placement="bottom-end"
              >
                <date-picker
                  v-if="datePickerType === 'date'"
                  key="date-picker"
                  v-model="dates"
                  type="date"
                  range
                  :placeholder="datePlaceholder"
                  @change="dateChange($event)"
                />
                <date-picker
                  v-else-if="datePickerType === 'week'"
                  key="week-picker"
                  v-model="dates"
                  type="week"
                  range
                  :placeholder="datePlaceholder"
                  @change="dateChange($event)"
                />
                <date-picker
                  v-else-if="datePickerType === 'month'"
                  key="month-picker"
                  v-model="dates"
                  type="month"
                  range
                  :placeholder="datePlaceholder"
                  @change="dateChange($event)"
                />
                <date-picker
                  v-else-if="datePickerType === 'year'"
                  key="year-picker"
                  v-model="dates"
                  type="year"
                  range
                  :placeholder="datePlaceholder"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
          </el-row>
          <el-row :xs="24" :sm="24" :lg="24">
            <el-col v-show="showNoDataMessage" :xs="24" :sm="8" :lg="12">
              <br>
              <el-alert
                title="No se encontraron datos para el filtro seleccionado"
                type="warning"
                effect="light"
                :closable="false"
              />
            </el-col>
            <el-col :xs="24" :sm="24" :lg="24">
              <el-alert
                title="Los resultados de las plantas acogidas a la Resolución CREG 081 de 2014 se ven afectados por la variación en la disponibilidad. No obstante, dichas plantas garantizan su OEF a partir de un combustible diferente al declarado"
                type="info"
                :closable="false"
              />
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bar-chart
            :data="data"
            value-title="Costo"
            :reference-date="initDate"
          />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="formatedData"
            :columns="columns"
            :indicator-name="$t('route.icoef')"
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
import 'vue2-datepicker/index.css'
import DatePicker from 'vue2-datepicker'

var PERIODS = ['Diario', 'Semanal', 'Mensual', 'Anual']

var TOLERANCES = [...Array(101).keys()]
TOLERANCES.shift()

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
      initDate: new Date(),
      data: [],
      data2: [],
      injectionData: [],
      formatedData: [],
      indicatorName: 'icoef',
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
      sTolerances: TOLERANCES[1],

      plants: [],
      sPlants: [],
      oldPlants: [],

      columns: [
        { id: 'plant', name: 'Periodo' },
        { id: 'date', name: 'Planta' },
        { id: 'icoef', name: 'ICOEF' },
        { id: 'icoefas', name: 'ICOEFAS' },
        { id: 'cobertura', name: 'Cobertura (%)' }
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
        const range_data = await getLastDate('icoef')

        const iniDate = new Date(range_data[0])
        const lastDate = new Date(range_data[1])

        this.initDate = iniDate
        this.lastDate = lastDate

        this.start = moment(lastDate).startOf('month').toDate()
        this.end = lastDate

        this.dates = [iniDate, lastDate]
        this.dateValue = [moment(lastDate).startOf('month').toDate(), lastDate]
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      await this.getDataICOEF()
      this.format_rc()
    },
    async getDataICOEF() {
      this.data = []
      if (this.end > this.lastDate || this.end < this.initDate) {
        this.end = this.lastDate
      }
      var sPlants = this.sPlants
      var plantIds = []
      this.dates = [this.start, this.end]

      for (const i in sPlants) {
        plantIds.push(sPlants[i].id)
      }

      try {
        var result = await getIndicator('icoef', {
          fecha_inicial: this.formatDate(this.start),
          fecha_final: this.formatDate(this.end),
          periodo: this.sPeriods,
          beta: this.sTolerances,
          planta: plantIds,
          invertir: true,
          anillado: false,
          cobertura: true,
          no_agrupar: true
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
        for (const d in rows[i].dates) {
          if (this.flip) {
            row = {
              date: rows[i].names,
              plant: rows[i].dates[d],
              icoef: rows[i].values[d],
              icoefas: rows[i].icoefas[d],
              cobertura: rows[i].cobertura[d]
            }
          } else {
            row = {
              date: rows[i].dates[d],
              plant: rows[i].names,
              icoef: rows[i].values[d],
              icoefas: rows[i].icoefas[d],
              cobertura: rows[i].cobertura[d]
            }
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
      await this.getDataICOEF()
      await this.format_rc()
    },
    async toleranceChange() {
      await this.getDataICOEF()
      await this.format_rc()
    },
    async fetchPlants() {
      var plants = await getIndicator('plantas')
      var plantGroups = []
      for (const i in plants.items) {
        plantGroups.push({
          id: plants.items[i][0],
          name: plants.items[i][1]
        })
      }
      this.plants = plantGroups
      // this.sPlants = plants.items
    },
    async dateChange(event) {
      if (event) {
        var start = new Date(event[0])
        var end = new Date(event[1])
        this.end = event
        if (start < this.initDate || end < this.initDate || start > this.lastDate || end > this.lastDate) {
          this.end = this.lastDate
          this.start.setTime(this.end.getTime() - 3600 * 1000 * 24 * 7)
        } else {
          this.start = start
          this.end = end
        }
        this.dateValue = [this.start, this.end]
        await this.getDataICOEF()
        await this.format_rc()
      }
    },
    async plantChange() {
      console.log(JSON.stringify(this.sPlants))
      if ((await this.oldPlants) !== (await this.sPlants)) {
        await this.getDataICOEF()
        await this.format_rc()
      }
      this.oldPlants = this.sPlants
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    async onFlip(value) {
      await this.getDataICOEF()
      await this.format_rc()
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
