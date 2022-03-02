<template>
  <div class="transction-table">
    <el-row :style="{height: showImage ? height : '80px', width: width}">
      <el-col :xs="24" :sm="24" :lg="8" class="multiselect-box">
        {{ agents[0] }} <br>
        <multiselect
          v-model="agents0"
          :options="agents0Keys"
          :multiple="true"
          :taggable="true"
          :placeholder="'Seleccione un ' + agents[0]"
          select-label="Seleccionar"
          deselect-label="Remover"
          selected-label="Seleccionado"
          @input="showAgent()"
          @tag="showAgent()"
        />
        <div v-show="showAgents1">
          {{ agents[1] }} <br>
          <multiselect
            v-model="agents1"
            :options="agents1Keys"
            :multiple="true"
            :taggable="true"
            :placeholder="'Seleccione un ' + agents[1]"
            select-label="Seleccionar"
            deselect-label="Remover"
            selected-label="Seleccionado"
            @input="showAgent()"
            @tag="showAgent()"
          />
        </div>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="16" :style="{height: showImage ? height : '80px'}" class="rcorners">
        <div id="macarons" class="chart" />
        <div id="macarons2" class="chart" />
      </el-col>
    </el-row>

  </div>
</template>

<script>
import echarts from 'echarts'
import Multiselect from 'vue-multiselect'
require('echarts/theme/macarons')

const animationDuration = 2000
const colors = ['#fce654', '#91c7ae', '#d3dee5', '#E56399', '#DE6E4B', '#d48265', '#749f83', '#c23531', '#ca8622', '#bda29a', '#7FD1B9', '#6e7074', '#546570', '#c4ccd3', '#61a0a8', '#7A6563', '#E5D4CE']

export default {
  components: { Multiselect },
  props: {
    data: {
      type: Array,
      default: function() { return [] }
    },
    valueTitle: {
      type: String,
      default: 'Valor'
    },
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '700px'
    },
    agents: {
      type: Array,
      default: function() { return [] }
    },
    groups: {
      type: Array,
      default: function() { return [] }
    },
    grouping: {
      type: String,
      default: 'Mercado'
    },
    sGrouping: {
      type: Array,
      default: function() { return [] }
    }
  },
  data() {
    return {
      chart: null,
      agents0: [],
      agents0Keys: [],
      agents1: [],
      agents1Keys: [],
      agents0Data: {},
      showImage: false,
      showAgents1: false
    }
  },
  watch: {
    data: function(data) {
      this.agents0Data = {}
      this.agents1Keys = []
      this.agents1 = []
      for (var i = 0; i < data.length; i++) {
        if (!this.agents0Data.hasOwnProperty(data[i].names[0])) {
          this.agents0Data[data[i].names[0]] = []
        }
        this.agents0Data[data[i].names[0]].push([
          data[i].names[2],
          data[i].values[0],
          data[i].values[1],
          data[i].names[1],
          data[i].names[0],
          data[i].names[3],
          data[i].names[4],
          data[i].dates[0],
          data[i].names[5],
          data[i].values[2]
        ])
      }
      this.agents0Keys = Object.keys(this.agents0Data)
      this.showAgent()
    }

  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    window.removeEventListener('resize', this.__resizeHandler)
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    updateAgents1() {
      var agents1Set = new Set()
      if (this.groups.length === 0) {
        for (var i = this.agents0.length - 1; i >= 0; i--) {
          if (this.agents0[i] in this.agents0Data) {
            var selectedSeller = this.agents0Data[this.agents0[i]]
            for (var j = 0; j < selectedSeller.length; j++) {
              agents1Set.add(selectedSeller[j][3])
            }
          } else {
            this.agents0.splice(i, 1)
          }
        }
      }
      this.agents1Keys = Array.from(agents1Set)
    },
    showAgent() {
      this.updateAgents1()
      this.showAgents1 = !!((this.agents0.length > 0 && this.groups.length === 0))
      this.showImage = this.agents0.length > 0
      if (this.chart) {
        this.chart.dispose()
        this.chart = null
      }
      if (this.showImage) {
        this.initChart()
      }
    },
    async initChart() {
      var self = this

      this.chart = echarts.init(document.getElementById('macarons'))

      var schema = [
        { name: 'Modalidad', index: 0, text: 'Modalidad' },
        { name: 'Precio', index: 1, text: 'Precio' },
        { name: 'Cantidad', index: 2, text: 'Cantidad' },
        { name: this.agents[1], index: 3, text: this.agents[1] },
        { name: this.agents[0], index: 4, text: this.agents[0] },
        { name: 'Fuente', index: 5, text: 'Fuente' },
        { name: 'Mercado', index: 6, text: 'Mercado' },
        { name: 'Fecha inicio', index: 7, text: 'Fecha inicio' },
        { name: 'Sector de consumo', index: 8, text: 'Sector de consumo' }
      ]

      console.info('grouping', this.grouping)

      var series = []
      this.min = 1000000000

      var gRow = 6
      switch (this.grouping) {
        case 'Mercado':
          gRow = 6
          break
        case 'Modalidad':
          gRow = 0
          break
        case 'Sector de consumo':
          gRow = 8
          break
      }

      for (var k = 0; k < this.sGrouping.length; k++) {
        var filteredAgents0Data = []
        var itemStyle = {
          normal: {
            opacity: 0.8,
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            shadowColor: 'rgba(0,0,0,0.3)'
          }
        }
        for (var i = 0; i < this.agents0.length; i++) {
          var agents0Data = this.agents0Data[this.agents0[i]]
          for (var j = 0; j < agents0Data.length; j++) {
            if (this.sGrouping[k] === agents0Data[j][gRow]) {
              var rowCopy = agents0Data[j].slice()
              var tmp = rowCopy[2]
              rowCopy[2] = rowCopy[0]
              rowCopy[0] = tmp

              tmp = rowCopy[9]
              rowCopy[9] = rowCopy[2]
              rowCopy[2] = tmp

              if (gRow !== 0) {
                tmp = rowCopy[gRow]
                rowCopy[gRow] = rowCopy[3]
                rowCopy[3] = tmp
              }

              filteredAgents0Data.push(rowCopy)
            }
          }
        }
        var serie = {
          name: this.sGrouping[k],
          type: 'scatter',
          itemStyle: itemStyle,
          data: filteredAgents0Data,
          animationDuration,
          label: {
            formatter: '{b}:  {d}%'
          },
          symbolSize: function(data) {
            return Math.sqrt(data[2]) / 1.5
          }
        }
        console.log(serie)
        series.push(serie)
      }
      this.chart.setOption({
        grid: {
          x: '7%',
          x2: 160,
          y: '17%',
          y2: '7%'
        },
        legend: {
          x: '15%',
          top: '3%',
          textStyle: {
            color: '#000'
          }
        },
        tooltip: {
          padding: 10,
          backgroundColor: '#222',
          borderColor: '#777',
          borderWidth: 1,
          formatter: function(obj) {
            var value = obj.value
            console.info('values:', value)
            switch (self.grouping) {
              case 'Mercado':
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">' +
                  schema[4].text + '：' + value[4] +
                  '</div>' + '<div style="font-size: 12px;">' +
                  schema[3].text + '：' + value[6].split(';')
                  .join('<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;') + '<br>' +
                  schema[0].text + '：' + value[9] + '<br>' +
                  schema[1].text + '：' + Number(value[1]).toFixed(2) + '<br>' +
                  schema[2].text + '：' + Number(value[2]).toFixed(2) + '<br>' +
                  schema[5].text + '：' + ((value[3] === 'Secundario') ? 'Secundario' : value[5]) + '<br>' +
                  schema[6].text + '：' + value[3] + '<br>' +
                  schema[7].text + '：' + value[7] + '<br>' +
                  schema[8].text + '：' + value[8] + '<br>' +
                  '</div>'

              case 'Modalidad':
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">' +
                  schema[4].text + '：' + value[4] +
                  '</div>' + '<div style="font-size: 12px;">' +
                  schema[3].text + '：' + value[3].split(';')
                  .join('<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;') + '<br>' +
                  schema[0].text + '：' + value[9] + '<br>' +
                  schema[1].text + '：' + Number(value[1]).toFixed(2) + '<br>' +
                  schema[2].text + '：' + Number(value[2]).toFixed(2) + '<br>' +
                  schema[5].text + '：' + ((value[6] === 'Secundario') ? 'Secundario' : value[5]) + '<br>' +
                  schema[6].text + '：' + value[6] + '<br>' +
                  schema[7].text + '：' + value[7] + '<br>' +
                  schema[8].text + '：' + value[8] + '<br>' +
                  '</div>'

              case 'Sector de consumo':
                return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">' +
                  schema[4].text + '：' + value[4] +
                  '</div>' + '<div style="font-size: 12px;">' +
                  schema[3].text + '：' + value[8].split(';')
                  .join('<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;') + '<br>' +
                  schema[0].text + '：' + value[9] + '<br>' +
                  schema[1].text + '：' + Number(value[1]).toFixed(2) + '<br>' +
                  schema[2].text + '：' + Number(value[2]).toFixed(2) + '<br>' +
                  schema[5].text + '：' + ((value[6] === 'Secundario') ? 'Secundario' : value[5]) + '<br>' +
                  schema[6].text + '：' + value[6] + '<br>' +
                  schema[7].text + '：' + value[7] + '<br>' +
                  schema[8].text + '：' + value[3] + '<br>' +
                  '</div>'
            }
          }
        },
        xAxis: {
          axisTick: {
            alignWithLabel: true
          },
          type: 'value',
          name: 'Energía (GBTUD)',
          min: null,
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#000',
            fontSize: 16,
            padding: 10
          },
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Precio (USD/MBTU)',
          min: null,
          nameLocation: 'middle',
          nameTextStyle: {
            color: '#000',
            fontSize: 16,
            padding: 10
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          splitLine: {
            show: false
          }
        },
        visualMap: [
          {
            left: 'right',
            top: '20%',
            dimension: 2,
            min: 0,
            max: 100000,
            itemWidth: 60,
            itemHeight: 300,
            calculable: true,
            precision: 'auto',
            text: ['Volumen'],
            textGap: 30,
            textStyle: {
              color: '#000'
            },
            inRange: {
              symbolSize: [10, 70]
            },
            outOfRange: {
              symbolSize: [10, 70],
              color: ['rgba(255,255,255,0.4)']
            },
            controller: {
              inRange: {
                color: ['#c23531']
              },
              outOfRange: {
                color: ['#999']
              }
            }
          }
        ],
        series: series,
        color: colors
      })
    }
  }
}
</script>

<style>
</style>
