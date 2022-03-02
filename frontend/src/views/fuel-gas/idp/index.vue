<template>
  <div class="dashboard-editor-container">
    <el-row :gutter="8">
      <el-col :xs="{span: 24}" :sm="{span: 24}" :md="{span: 24}" :lg="{span: 24}" :xl="{span: 24}" style="padding-right:8px;margin-bottom:30px;">
        <div class="chart-wrapper">
          <el-row :gutter="32">
            <el-col :xs="24" :sm="247" :lg="24">
              <h2> {{ $t('route.idp') }} </h2>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="2">
              <div class="label">Fecha:</div>
            </el-col>
            <el-col :key="name" :xs="24" :sm="12" :lg="6">
              <el-date-picker v-model="dateValue" type="month" align="right" :placeholder="$t('datePicker.date')" @change="dateChange($event)" />
            </el-col>
            <el-col :key="name" :xs="24" :sm="12" :lg="8">
              <el-tag type="warning">
                Datos actualizados a fecha de {{ printLastDate() }}
              </el-tag>
            </el-col>
          </el-row>
          <h3>Numerador</h3>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="6">
              Mercados:<br>
              <multiselect v-model="sMarketsNum" :options="marketsNum" :multiple="true" :taggable="true" placeholder="Seleccione un mercado" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="marketChange()" @tag="marketChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteNumMarkets">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectNumMarkets">Todos</el-button>
              </el-button-group>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Modalidades:<br>
              <multiselect v-model="sModalitiesNum" :options="modalitiesNum" :multiple="true" :taggable="true" placeholder="Seleccione una modalidad" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="modalityChange()" @tag="modalityChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteNumModalities">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectNumModalities">Todos</el-button>
              </el-button-group>
              <br><br>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Sectores:<br>
              <multiselect v-model="sSectorsNum" :options="sectorsNum" :multiple="true" :taggable="true" placeholder="Seleccione un sector" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="sectorNomChange()" @tag="sectorNomChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteNumSectors">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectNumSectors">Todos</el-button>
              </el-button-group>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Fuentes:<br>
              <multiselect v-model="sSourcesNum" :options="sourcesNum" :multiple="true" :taggable="true" placeholder="Seleccione una fuente" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="sourceNomChange()" @tag="sourceNomChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteNumSources">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectNumSources">Todos</el-button>
              </el-button-group>
            </el-col>
          </el-row>
          <br>
          <h3>Denominador</h3>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" :lg="6">
              Mercados:<br>
              <multiselect v-model="sMarketsDenom" :options="marketsDenom" :multiple="true" :taggable="true" placeholder="Seleccione un mercado" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="marketChange()" @tag="marketChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteDenomMarkets">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectDenomMarkets">Todos</el-button>
              </el-button-group>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Modalidades:<br>
              <multiselect v-model="sModalitiesDenom" :multiple="true" :options="modalitiesDenom" :taggable="true" deselect-label="Remover" placeholder="Seleccione una modalidad" select-label="Seleccionar" selected-label="Seleccionado" @input="modalityChange()" @tag="modalityChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteDenomModalities">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectDenomModalities">Todos</el-button>
              </el-button-group>
              <br><br>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Sectores:<br>
              <multiselect v-model="sSectorsDenom" :options="sectorsDenom" :multiple="true" :taggable="true" placeholder="Seleccione un sector" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="sectorDenomChange()" @tag="sectorDenomChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteDenomSectors">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectDenomSectors">Todos</el-button>
              </el-button-group>
            </el-col>
            <el-col :xs="24" :sm="12" :lg="6">
              Fuentes:<br>
              <multiselect v-model="sSourcesDenom" :options="sourcesDenom" :multiple="true" :taggable="true" placeholder="Seleccione un sector" select-label="Seleccionar" deselect-label="Remover" selected-label="Seleccionado" @input="sourceDenomChange()" @tag="sourceDenomChange()" />
              <el-button-group style="margin:5px 5px 5px 5px;">
                <el-button type="primary" size="mini" icon="el-icon-close" @click="deleteDenomSources">Ninguno</el-button>
                <el-button type="primary" size="mini" icon="el-icon-check" @click="selectDenomSources">Todos</el-button>
              </el-button-group>
            </el-col>
          </el-row>
          <br>
          <br>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="24" :lg="16">
              <el-button :loading="loadingData" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleLoadingData">
                Agregar nueva comparación
              </el-button>
              <el-button style="margin:0 0 20px 20px;" type="primary" icon="document" @click="deleteData">
                Borrar datos
              </el-button>
              <el-button style="margin:0 0 20px 20px;" type="danger" icon="el-icon-delete" plain @click="clearFilters">
                Quitar filtros
              </el-button>
              <el-button style="margin:0 0 20px 20px;" type="primary" icon="document" @click="selectAll">
                Seleccionar todo
              </el-button>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :xs="24" :sm="24" :lg="24">
              <el-alert v-show="showNoDataMessage" title="No se encontraron datos para los filtros seleccionados" type="warning" :closable="false" />
            </el-col>
          </el-row>
        </div>
        <div class="chart-wrapper">
          <bar-chart :data="formatedData" value-title="Dispersión" :reference-date="initDate" />
        </div>
        <div class="chart-wrapper">
          <transaction-table :data="formatedData" :columns="columns" :indicator-name="$t('route.idp')" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import {
  getIndicator,
  getLastDate
} from '@/api/remoteSearch'
import BarChart from './components/BarChart'
import TransactionTable from './components/TransactionTable'

import moment from 'moment'
import Multiselect from 'vue-multiselect'

var MARKETS = ['Primario', 'Secundario']
var MODALITIES = ['Firme', 'Interrumpible']
var SECTORS = []
var SOURCES = ['BALLENA', 'LISAMA', 'MANA'] // Nombres probablemente malos

export default {
  name: 'DashboardAdmin',
  components: {
    BarChart,
    TransactionTable,
    Multiselect
  },
  data() {
    return {
      lastDate: new Date(),
      initDate: new Date(),
      data: [],
      data2: [],
      date: new Date(),
      injectionData: [],
      formatedData: [],
      indicatorName: 'dp',
      start: new Date(),
      end: new Date(),
      sGroups: [],
      groups: [],
      sNits: [],
      nits: [],
      list: [],

      marketsDenom: MARKETS,
      marketsNum: MARKETS,
      sMarketsDenom: MARKETS,
      sMarketsNum: MARKETS,

      modalitiesDenom: MODALITIES,
      modalitiesNum: MODALITIES,
      sModalitiesDenom: MODALITIES,
      sModalitiesNum: MODALITIES,

      sectorsDenom: SECTORS,
      sectorsNum: SECTORS,
      sSectorsDenom: SECTORS,
      sSectorsNum: SECTORS,

      sourcesDenom: SOURCES,
      sourcesNum: SOURCES,
      sSourcesDenom: SOURCES,
      sSourcesNum: SOURCES,

      showNoDataMessage: false,

      columns: [{
        id: 'numerator',
        name: 'Numerador'
      },
      {
        id: 'denominator',
        name: 'Denominador'
      },
      {
        id: 'weigthed_avg_numerator',
        name: 'Promedio ponderado (Numerador)'
      },
      {
        id: 'weigthed_avg_denominator',
        name: 'Promedio ponderado (Denominador)'
      },
      {
        id: 'index',
        name: 'índice'
      }
      ],

      dateValue: [],

      loadingData: false
    }
  },
  async created() {
    this.end = new Date()
    this.start = new Date()
    await this.fetchLatest()
    await this.fetchSectors()
    await this.fetchSources()
    await this.getData()
    await this.format_rc()
  },
  methods: {
    printLastDate() {
      return moment(this.lastDate).utc().format('DD/MM/YYYY')
    },
    async fetchLatest() {
      try {
        var range_data = await getLastDate('dp')
        this.lastDate = new Date(range_data[1])
        this.initDate = new Date(range_data[0])
        this.end = new Date(range_data[1])
        this.start = new Date(range_data[0])
        this.dateValue = new Date(range_data[1])
      } catch (error) {
        this.end = new Date()
        console.error(error)
      }
    },
    async getData() {
      this.loadingData = true
      this.data = []
      try {
        var result = await getIndicator(this.indicatorName, {
          fecha: this.formatDate(this.dateValue),
          mercados_numerador: this.sMarketsNum,
          mercados_denominador: this.sMarketsDenom,
          modalidades_numerador: this.sModalitiesNum,
          modalidades_denominador: this.sModalitiesDenom,
          sectores_numerador: this.sSectorsNum,
          sectores_denominador: this.sSectorsDenom,
          fuentes_numerador: this.sSourcesNum,
          fuentes_denominador: this.sSourcesDenom
        })
        if (result) {
          this.data = result.items[0]
        }
      } catch (error) {
        console.error(error)
        this.data = []
      }
      this.loadingData = false
    },
    async fetchSectors() {
      var sectors = await getIndicator('sectores')
      this.sectorsDenom = sectors.items
      this.sectorsNum = sectors.items
      this.sSectorsDenom = sectors.items
      this.sSectorsNum = sectors.items
    },
    async fetchSources() {
      var sources = await getIndicator('fuentes')
      this.sourcesDenom = sources.items
      this.sourcesNum = sources.items
      this.sSourcesDenom = sources.items
      this.sSourcesNum = sources.items
    },
    async format_rc() {
      var data = this.data
      if (data === undefined || data.weigthed_avg_denominator === 0 || data.weigthed_avg_numerator === 0) {
        this.showNoDataMessage = true
        return []
      }
      this.showNoDataMessage = false

      var row = {
        date: this.formatDate(this.dateValue),
        denominator: 'Mercados: ' + this.sMarketsDenom + '. Modalidades: ' + this.sModalitiesDenom + '. Sectores: ' + this.sSectorsDenom + '. Fuentes: ' + this.sSourcesDenom,
        numerator: 'Mercados: ' + this.sMarketsNum + '. Modalidades: ' + this.sModalitiesNum + '. Sectores: ' + this.sSectorsNum + '. Fuentes: ' + this.sSourcesNum,
        denominator_numerator: 'Numerador:\n      Mercados: ' + this.sMarketsNum.map(x => x.substring(0, 3)) + ' \n      Modalidades: ' + this.sMarketsNum.map(x => x.substring(0, 3)) + '\n      Sectores: ' + this.sSectorsNum.map(x => x.substring(0, 3)) + '\n      Fuentes: ' + this.sSourcesNum.map(x => x.substring(0, 3)) + '\n' +
                    '\nDenominador:\n      Mercados: ' + this.sMarketsDenom.map(x => x.substring(0, 3)) + '\n      Modalidades: ' + this.sMarketsDenom.map(x => x.substring(0, 3)) + '\n      Sectores: ' + this.sSectorsDenom.map(x => x.substring(0, 3)) + '\n      Fuentes: ' + this.sSourcesDenom.map(x => x.substring(0, 3)),
        weigthed_avg_denominator: data.weigthed_avg_denominator,
        weigthed_avg_numerator: data.weigthed_avg_numerator,
        index: data.index
      }
      this.formatedData.push(row)
    },
    async dateChange(event) {

    },
    async groupChange(envet) {

    },
    async marketChange() {

    },
    async modalityChange() {

    },
    async sectorDenomChange() {

    },
    async sectorNomChange() {

    },
    async sourceDenomChange() {

    },
    async sourceNomChange() {

    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    async handleLoadingData() {
      await this.getData()
      this.format_rc()
    },
    deleteData() {
      this.data = []
      this.formatedData = []
    },
    clearFilters() {
      this.sMarketsDenom = []
      this.sMarketsNum = []
      this.sModalitiesDenom = []
      this.sModalitiesNum = []
      this.sSectorsDenom = []
      this.sSectorsNum = []
      this.sSourcesDenom = []
      this.sSourcesNum = []
    },
    selectAll() {
      this.sMarketsDenom = MARKETS
      this.sMarketsNum = MARKETS
      this.sModalitiesDenom = MODALITIES
      this.sModalitiesNum = MODALITIES
      this.sSectorsDenom = this.sectorsDenom
      this.sSectorsNum = this.sectorsNum
      this.sSourcesDenom = this.sourcesDenom
      this.sSourcesNum = this.sourcesDenom
    },
    deleteNumMarkets() {
      this.sMarketsNum = []
    },
    selectNumMarkets() {
      this.sMarketsNum = MARKETS
    },
    deleteNumModalities() {
      this.sModalitiesNum = []
    },
    selectNumModalities() {
      this.sModalitiesNum = MODALITIES
    },
    deleteNumSectors() {
      this.sSectorsNum = []
    },
    selectNumSectors() {
      this.sSectorsNum = this.sectorsNum
    },
    deleteNumSources() {
      this.sSourcesNum = []
    },
    selectNumSources() {
      this.sSourcesNum = this.sourcesNum
    },
    deleteDenomMarkets() {
      this.sMarketsDenom = []
    },
    selectDenomMarkets() {
      this.sMarketsDenom = MARKETS
    },
    deleteDenomModalities() {
      this.sModalitiesDenom = []
    },
    selectDenomModalities() {
      this.sModalitiesDenom = MODALITIES
    },
    deleteDenomSectors() {
      this.sSectorsDenom = []
    },
    selectDenomSectors() {
      this.sSectorsDenom = this.sectorsDenom
    },
    deleteDenomSources() {
      this.sSourcesDenom = []
    },
    selectDenomSources() {
      this.sSourcesDenom = this.sourcesDenom
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
