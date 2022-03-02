<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <h2> {{ $t('route.oc') }} </h2>
          <el-row :gutter="8">
            <el-col :xs="24" :sm="12" :lg="3">
              <div class="label">Fecha en vigencia:</div>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="5">
              <el-date-picker v-model="date" type="month" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
            </el-col>
            <el-col :xs="24" :sm="24" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="3">
              <div class="label">Consultar por:</div>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="5">
              <el-select :value="$t(agent.text)" :placeholder="$t(agent.id)" @change="agentChange($event)">
                <el-option v-for="item in agents" :key="item.id" :label="$t(item.text)" :value="item" />
              </el-select>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="3">
              <div class="label">Mercado:</div>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="5">
              <multiselect v-model="sMarkets" :options="markets" :multiple="true" :taggable="true" placeholder="Seleccione un mercado" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="marketChange()" @tag="marketChange()" />
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="3">
              <div class="label">Fuente:</div>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="5">
              <multiselect v-model="sSources" :options="sources" :multiple="true" :taggable="true" placeholder="Seleccione una fuente" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="sourceChange()" @tag="sourceChange()" />
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="3">
              <div class="label">Inicio contrato:</div>
            </el-col>
            <el-col v-if="!public_conf" :xs="24" :sm="12" :lg="5">
              <multiselect v-model="sYears" :options="years" :multiple="true" :taggable="true" placeholder="Seleccione un año" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="startingDateChange()" @tag="startingDateChange()" />
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <line-chart :data="list" :public_conf="public_conf" value-title="Valor" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="list" :public_conf="public_conf" :indicator-name="indicatorName" agent-title="Agente" value-title="Precio" quantity-title="Cantidad" :date="date" :status="status" :value="value" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import LineChart from './components/LineChart'
import TransactionTable from './components/TransactionTable'
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import moment from 'moment'
import Multiselect from 'vue-multiselect'

var AGENTS = [{
  id: 'vendedores',
  text: 'indicator.types.groupBySeller'
},
{
  id: 'comprador',
  text: 'indicator.types.groupByShopper'
}
]

var GROUPS = {
  'vendedor': ['precio'],
  'comprador': ['precio']
}

var ROLES = [{
  id: null,
  text: 'todos'
},
{
  id: 'COMERCIALIZADOR',
  text: 'COMERCIALIZADOR'
},
{
  id: 'PRODUCTOR-COMERCIALIZADOR',
  text: 'PRODUCTOR-COMERCIALIZADOR'
},
{
  id: 'TRANSPORTADOR',
  text: 'TRANSPORTADOR'
},
{
  id: 'USUARIO NO REGULADO',
  text: 'USUARIO NO REGULADO'
},
{
  id: 'COMERCIALIZADOR GAS IMPORTADO',
  text: 'COMERCIALIZADOR GAS IMPORTADO'
},
{
  id: 'GENERADOR TERMICO',
  text: 'GENERADOR TERMICO'
}
]

var MARKETS = ['Primario', 'Secundario']
var FIRST_YEAR = 2000
export default {
  name: 'DashboardAdmin',
  components: {
    LineChart,
    TransactionTable,
    Multiselect
  },
  data() {
    return {
      groups: GROUPS['comprador'],
      sGroups: [],
      agents: AGENTS,
      sAgents: ['vendedor', 'comprador'],
      agent: AGENTS[0],
      roles: ROLES,
      role: ROLES[2],
      markets: MARKETS,
      sMarkets: [MARKETS[0]],
      years: [],
      sYears: [],
      sources: [],
      sSources: [],
      indicatorName: 'oc',
      date: new Date(),
      list: [],
      status: false,
      value: 0,
      public_conf: process.env.VUE_APP_PUBLIC === 'true'
    }
  },
  created() {
    if (!this.public_conf) {
      this.getSources()
    }
    this.fetchLatest()
  },
  methods: {
    async fetchLatest() {
      try {
        var range_data = await getLastDate('gmg')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])

        this.date = this.lastDate
        var LAST_YEAR = this.lastDate.getFullYear()
        this.years = []
        for (var i = FIRST_YEAR; i <= LAST_YEAR; i++) {
          this.years.push(i)
        }
      } catch (error) {
        this.date = new Date()
        console.error(error)
      }
      this.getData()
    },
    printLastDate() {
      return moment(this.lastDate).format('DD/MM/YYYY')
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    dateChange(event) {
      this.getData()
    },
    measureChange(item) {
      this.type = item
      this.getData()
    },
    marketChange() {
      this.getData()
    },
    sourceChange() {
      this.getData()
    },
    startingDateChange() {
      this.getData()
    },
    agentChange(item) {
      if (item.id === 'comprador') {
        this.sAgents = ['comprador', 'vendedor']
      } else {
        this.sAgents = ['vendedor', 'comprador']
      }
      this.groups = GROUPS[item.id]
      this.agent = item
      this.getData()
    },
    async getSources() {
      try {
        var result = await getIndicator('fuentes')
        if (result.items) {
          this.sources = result.items
        }
      } catch (error) {
        console.error('error', error)
      }
    },
    async getData() {
      try {
        if (this.date > this.lastDate || this.date < this.initDate) {
          this.date = this.lastDate
        }
        var dateAux = this.date
        var indicador = this.indicatorName + (this.public_conf ? 'pbl' : '')
        var result_Firme = await getIndicator(indicador, {
          fecha: this.formatDate(this.date),
          fuente: this.sSources,
          mercado: this.sMarkets,
          fecha_inicial: this.sYears,
          tipo_agente: this.agent.id,
          rol_vendedor: this.role.id,
          modalidad: 'Firme'
        })

        var result_inter = await getIndicator(indicador, {
          fecha: this.formatDate(dateAux),
          fuente: this.sSources,
          mercado: this.sMarkets,
          fecha_inicial: this.sYears,
          tipo_agente: this.agent.id,
          rol_vendedor: this.role.id,
          modalidad: 'Interrumpible'
        })

        if (!result_Firme && result_inter) {
          this.list = []
          this.value = []
        }

        if (result_Firme || result_inter) {
          this.list = [result_inter.items, result_Firme.items]
          this.status = [result_inter.status, result_Firme.status]
          this.value = [result_inter.value, result_Firme.value]
        }
      } catch (error) {
        console.log(error)
        this.list = []
        this.value = []
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
