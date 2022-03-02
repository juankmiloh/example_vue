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
          <h2>{{ $t("route.icoef") }}</h2>
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
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Tolerancia (%):</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="5">
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
                content="Seleccione plantas"
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
                  @close="plantChange($event)"
                >
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__title">{{
                        truncateString(props.option.name, 30)
                      }}</span>
                    </div>
                  </template>
                </multiselect>
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
            <el-col :xs="12" :sm="12" :lg="3">
              <div class="label">Agrupar por plantas:</div>
            </el-col>
            <el-col :xs="6" :sm="6" :lg="1">
              <div class="label">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="Seleccione para agrupar por plantas"
                  placement="bottom-end"
                >
                  <el-switch v-model="flip" @change="onFlip($event)" />
                </el-tooltip>
              </div>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="2">
              <div class="label">ICOEFAS:</div>
            </el-col>
            <el-col :xs="6" :sm="6" :lg="2">
              <div class="label">
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="Seleccione para obtener el ICOEF anillado"
                  placement="bottom-end"
                >
                  <el-switch v-model="flipAcc" @change="onFlip($event)" />
                </el-tooltip>
              </div>
            </el-col>
          </el-row>
          <el-row :xs="24" :sm="24" :lg="24">
            <el-col v-show="showNoDataMessage" :xs="24" :sm="8" :lg="8">
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
                style="margin-top: 15px"
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
import DatePicker from 'vue2-datepicker'
import 'vue2-datepicker/index.css'

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
        {
          id: 'plant',
          name: 'Planta'
        },
        {
          id: 'date',
          name: 'Periodo'
        },
        {
          id: 'icoef',
          name: 'ICOEF'
        },
        {
          id: 'icoefas',
          name: 'ICOEFAS'
        },
        {
          id: 'cobertura',
          name: 'cobertura'
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
    truncateString(str, num) {
      if (str.length > num) {
        return str.slice(0, num) + '...'
      } else {
        return str
      }
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('icoef')

        var ini_date = new Date(range_data[1])
        ini_date = moment(ini_date)
          .startOf('month')
          .subtract(1, 'month')
          .toDate()
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        this.end = new Date(range_data[1])
        this.start = new Date(range_data[0])
        this.dates = [ini_date, new Date(range_data[1])]
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
      await this.getData()
      this.format_rc()
    },
    async getData() {
      this.data = []
      var sPlants = this.sPlants
      var plantIds = []
      if (this.dates[1] > this.lastDate || this.dates[1] < this.initDate) {
        this.end = this.lastDate
        this.dates[1] = this.lastDate
      }
      if (this.dates[0] > this.lastDate || this.dates[0] < this.initDate) {
        var ini_date = this.initDate
        ini_date = moment(ini_date)
          .startOf('month')
          .subtract(2, 'month')
          .toDate()
        this.start = this.initDate
        this.dates[0] = ini_date
      }

      for (const i in sPlants) {
        plantIds.push(sPlants[i].id)
      }
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha_inicial: this.formatDate(this.dates[0]),
          fecha_final: this.formatDate(this.dates[1]),
          periodo: this.sPeriods,
          beta: this.sTolerances,
          planta: plantIds,
          invertir: this.flip,
          anillado: this.flipAcc
        })
        if (result) {
          var rows = result.items
          var date = ''
          for (const i in rows) {
            for (const d in rows[i].dates) {
              if (rows[i].values[d] !== 0) {
                if (this.flip) {
                  date = rows[i].names
                } else {
                  date = rows[i].dates[d]
                }
                if (this.datePickerType === 'month') {
                  date = moment(date).format('MMM')
                } else if (this.datePickerType === 'week') {
                  date = moment(date).format('W')
                } else if (this.datePickerType === 'year') {
                  date = moment(date).format('YYYY')
                }
                if (date !== 'Invalid date') {
                  if (this.flip) {
                    rows[i].names = date
                  } else {
                    rows[i].dates[d] = date
                  }
                }
              }
            }
          }
          this.data = rows
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
    async getDataICOEF() {
      this.data = []
      var sPlants = this.sPlants
      var plantIds = []
      if (this.dates[1] > this.lastDate || this.dates[1] < this.initDate) {
        this.end = this.lastDate
        this.dates[1] = this.lastDate
      }
      if (this.dates[0] > this.lastDate || this.dates[0] < this.initDate) {
        var ini_date = this.lastDate
        ini_date = moment(ini_date)
          .startOf('month')
          .subtract(1, 'month')
          .toDate()
        this.start = this.initDate
        this.dates[0] = ini_date
      }

      for (const i in sPlants) {
        plantIds.push(sPlants[i].id)
      }
      try {
        var result = await getIndicator('icoef', {
          fecha_inicial: this.formatDate(this.dates[0]),
          fecha_final: this.formatDate(this.dates[1]),
          periodo: this.sPeriods,
          beta: this.sTolerances,
          planta: plantIds,
          invertir: this.flip,
          anillado: this.flipAcc
        })
        if (result) {
          var rows = result.items
          for (const i in rows) {
            for (const d in rows[i].dates) {
              if (rows[i].values[d] !== 0) {
                var date = ''
                if (this.flip) {
                  date = rows[i].names
                } else {
                  date = rows[i].dates[d]
                }
                if (this.datePickerType === 'month') {
                  date = moment(date).format('MMM')
                } else if (this.datePickerType === 'week') {
                  date = moment(date).format('W')
                } else if (this.datePickerType === 'year') {
                  date = moment(date).format('YYYY')
                }
                if (date !== 'Invalid date') {
                  if (this.flip) {
                    rows[i].names = date
                  } else {
                    rows[i].dates[d] = date
                  }
                }
              }
            }
          }
          this.data = rows

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
          if (rows[i].values[d] !== 0) {
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
      this.start = event[0]
      this.end = event[1]
      if (event[0] !== null && event[1] !== null) {
        await this.getDataICOEF()
        await this.format_rc()
      }
    },
    async plantChange() {
      if ((await this.oldPlants) !== (await this.sPlants)) {
        await this.getData()
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
