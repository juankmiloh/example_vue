<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.daggi') }} </h2>
          <el-row :gutter="32">
            <el-col key="fecha-label" :xs="24" :sm="12" :lg="2">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col key="fecha-input" :xs="24" :sm="12" :lg="6">
              <el-date-picker v-model="date" type="date" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
            </el-col>
            <el-col key="fecha-update" :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
          <h5>Definir porcentajes de la capacidad de generación:</h5>
          <el-row :gutter="32">
            <template v-for="(name, index) in names">
              <el-col :key="name" :xs="12" :sm="12" :lg="4">
                {{ name }}
              </el-col>
              <el-col :key="index" :xs="12" :sm="12" :lg="4">
                <el-input-number v-model="percentages[index]" :step="5" :min="0" :max="100" size="mini" step-strictly @change="dateChange($event)" />
                %<br><br><br>
              </el-col>
            </template>
          </el-row>
          <el-row :gutter="32">
            <template v-if="percentages.includes(0)">
              <br>
              <el-alert
                :title="'Los porcentajes en 0 indican que no se ha consumido gas importado durante los ultimos ' + days.toString() + ' días'"
                type="info"
              />
            </template>
          </el-row>
          <h5>Calcular porcentajes por promedio de generación:</h5>
          <el-row :gutter="32">
            <el-col :xs="12" :sm="12" :lg="4">
              <div class="label">
                <el-switch
                  v-model="utilizarOEF"
                  active-text="OEF"
                  inactive-text="Consumo máximo"
                />
              </div>
              <br>
            </el-col>
            <el-col :xs="12" :sm="12" :lg="4">
              <div class="label">
                <el-switch
                  v-model="utilizarGN"
                  active-text="Mixto"
                  inactive-text="Sólo importado"
                />
              </div>
              <br>
            </el-col>
            <el-col key="dias-input-label" :xs="12" :sm="12" :lg="4">
              <div class="label">Días de cálculo</div>
            </el-col>
            <el-col key="dias-input" :xs="12" :sm="12" :lg="4">
              <el-input-number v-model="days" :step="5" :min="0" :max="120" size="mini" step-strictly />
            </el-col>
            <el-col key="dias-input-action" :xs="24" :sm="12" :lg="4">
              <el-button plain @click="getByAverage(false)">Calcular</el-button>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <gauge-chart :data="list" value-title="Valor" :thresholds="thresholds" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" :indicator-name="indicatorName" item-title="Planta" description-title="Agente" value-title="Días" :date="date" :thresholds="thresholds" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import GaugeChart from './components/GaugeChart'
import TransactionTable from './components/TransactionTable'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'

export default {
  components: {
    GaugeChart,
    TransactionTable
  },
  data() {
    return {
      indicatorName: 'daggi',
      date: new Date(),
      list: [],
      thresholds: [0, 8, 15, 20],
      names: [],
      percentages: [],
      days: 7,
      utilizarOEF: true,
      utilizarGN: true
    }
  },
  created() {
    this.fetchLatest()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    dateChange(event) {
      this.getData()
    },
    async fetchLatest() {
      try {
        var rangeDate = await getLastDate(this.indicatorName)
        this.lastDate = new Date(rangeDate[1])
        this.initDate = new Date(rangeDate[0])
        this.date = this.lastDate
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getByAverage(true)
    },
    async getByAverage(updateNames) {
      await this.getPercentages(updateNames)
      await this.getData()
    },
    async getPercentages(updateNames) {
      try {
        if (this.date > this.lastDate || this.date < this.initDate) {
          this.date = this.lastDate
        }

        var result = await getIndicator('daggi_percentage', {
          fecha: this.formatDate(this.date),
          dias: this.days,
          utilizar_oef: this.utilizarOEF,
          utilizar_gn: this.utilizarGN
        })
        this.percentages = []
        var list = result.items
        if (list && list[0]) {
          if (updateNames) {
            this.names = [...list[0].names]
          }
          for (var i = 0; i < this.names.length; i++) {
            if (list[0].names.includes(this.names[i])) {
              this.percentages.push(Math.ceil(list[0].values[list[0].names.indexOf(this.names[i])] * 100))
            } else {
              this.percentages.push(0.0)
            }
          }
        }
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
    },
    async getData() {
      try {
        if (this.date > this.lastDate || this.date < this.initDate) {
          this.date = this.lastDate
        }
        var percentages = []
        for (var i = 0; i < this.percentages.length; i++) {
          percentages.push(this.percentages[i] / 100.0)
        }
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.date),
          porcentaje: percentages,
          utilizar_oef: this.utilizarOEF,
          utilizar_gn: this.utilizarGN
        })
        if (result) {
          this.list = result.items
        }
      } catch (error) {
        this.list = []
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
