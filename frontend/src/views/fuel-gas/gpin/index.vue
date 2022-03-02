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
          <h2>{{ $t("route.gpin") }}</h2>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
          <br>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione una fecha"
                placement="bottom-end"
              >
                <el-date-picker
                  v-model="date"
                  type="date"
                  align="right"
                  :placeholder="$t('datePicker.date')"
                  @change="dateChange($event)"
                />
              </el-tooltip>
            </el-col>
          </el-row>
          <br>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Procedencia:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="22">
              <el-tooltip
                class="item"
                effect="dark"
                content="Seleccione una procedencia"
                placement="bottom-end"
              >
                <multiselect
                  v-model="sGroups"
                  :options="groups"
                  :multiple="true"
                  :taggable="true"
                  placeholder="Seleccione agrupación"
                  select-label="Seleccionar"
                  deselect-label="Remover"
                  selected-label="Seleccionado"
                  @input="groupChange()"
                  @tag="groupChange()"
                />
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <line-chart
            :data="list"
            :public_conf="public_conf"
            value-title="Índice"
          />
        </div>
        <div class="chart-wrapper">
          <transaction-table
            :data="list"
            :public_conf="public_conf"
            :indicator-name="indicatorName"
            source-title="Fuente"
            price-title="Precio Nacional Ponderado"
            ratio-title="Índice"
            :group-name="groupName"
            :value="value"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import moment from 'moment'
import Multiselect from 'vue-multiselect'
import LineChart from './components/LineChart'
import TransactionTable from './components/TransactionTable'
import { getIndicator, getLastDate } from '@/api/remoteSearch'

export default {
  name: 'DashboardAdmin',
  components: {
    TransactionTable,
    Multiselect,
    LineChart
  },
  data() {
    return {
      public_conf: process.env.VUE_APP_PUBLIC === 'true',
      indicatorName: 'gpin',
      date: new Date(),
      lastDate: new Date(),
      list: [],
      value: [],
      groupName: '',
      sGroups: [],
      groups: []
    }
  },
  created() {
    this.fetchLatest()
    this.fetchGroups()
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
        this.getData()
      }
    },
    measureChange(item) {
      this.type = item
      this.getData()
    },
    async fetchLatest() {
      try {
        var range_dates = await getLastDate('gmg')
        this.lastDate = new Date(range_dates[1])
        this.initDate = new Date(range_dates[0])
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
    },
    async fetchGroups() {
      var grupos = await getIndicator('fuentes', {
        no_guajira_costa: true
      })
      this.groups = grupos.items
      this.sGroups = grupos.items
      this.getData()
    },
    groupChange(envet) {
      this.getData()
    },
    async getData() {
      var aux = []
      if (this.date > this.lastDate || this.date < this.initDate) {
        this.date = this.lastDate
      }
      try {
        for (var index in this.sGroups) {
          var result = await getIndicator(this.indicatorName, {
            fecha: this.formatDate(this.date || this.lastDate),
            fuente: this.sGroups[index]
          })
          if (result) {
            if (result.items) {
              aux.push({
                name: this.sGroups[index],
                data: result.items
              })
            }
            this.value = result.value
          }
        }
        this.list = aux
      } catch (error) {
        this.list = []
        this.value = 0
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
