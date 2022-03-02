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
          data[i].names[2] === 'Firme' ? 0 : 1,
          data[i].values[0],
          data[i].values[1],
          data[i].names[1],
          data[i].names[0],
          data[i].names[3],
          data[i].names[4],
          data[i].dates[0]
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
      this.chart = echarts.init(document.getElementById('macarons'))

      var schema = [
        { name: 'Modalidad', index: 0, text: 'Modalidad' },
        { name: 'Precio', index: 1, text: 'Precio' },
        { name: 'Cantidad', index: 2, text: 'Cantidad' },
        { name: this.agents[1], index: 3, text: this.agents[1] },
        { name: this.agents[0], index: 4, text: this.agents[0] },
        { name: 'Fuente', index: 5, text: 'Fuente' },
        { name: 'Mercado', index: 6, text: 'Mercado' },
        { name: 'Fecha inicio', index: 7, text: 'Fecha inicio' }
      ]

      var agents1Set = new Set(this.agents1)
      var series = []
      this.min = 1000000000
      for (var i = 0; i < this.agents0.length; i++) {
        var itemStyle = {
          normal: {
            opacity: 0.7,
            shadowBlur: 5,
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            borderColor: colors[i % (colors.length - 1)],
            borderWidth: 2
          }
        }

        var filteredAgents0Data = []
        var agents0Data = this.agents0Data[this.agents0[i]]
        for (var j = 0; j < agents0Data.length; j++) {
          if (agents1Set.size === 0 || agents1Set.has(agents0Data[j][3])) {
            filteredAgents0Data.push(agents0Data[j])
          }
        }

        var serie = {
          name: this.agents0[i],
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
        series.push(serie)
      }
      this.chart.setOption({
        grid: {
          x: '5%',
          x2: 160,
          y: '17%',
          y2: '5%'
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
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">' +
                    schema[4].text + '：' + value[4] +
                    '</div>' + '<div style="font-size: 12px;">' +
                    schema[3].text + '：' + value[3].split(';')
              .join('<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;') + '<br>' +
                    schema[0].text + '：' + (value[0] === 0 ? 'Firme' : 'Interrumpible') + '<br>' +
                    schema[1].text + '：' + value[1] + '<br>' +
                    schema[2].text + '：' + value[2] + '<br>' +
                    schema[5].text + '：' + value[5] + '<br>' +
                    schema[6].text + '：' + value[6] + '<br>' +
                    schema[7].text + '：' + value[7] + '<br>' +
                    '</div>'
          }
        },
        xAxis: {
          axisTick: {
            alignWithLabel: true
          },
          type: 'category',
          name: 'Modalidad',
          data: ['Firme', 'Interrumpible'],
          nameGap: 16,
          nameTextStyle: {
            color: '#000',
            fontSize: 16
          },
          max: 1,
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
          name: 'Precio',
          min: null,
          nameLocation: 'end',
          nameGap: 20,
          nameTextStyle: {
            color: '#000',
            fontSize: 16
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
            max: 150000,
            itemWidth: 60,
            itemHeight: 300,
            calculable: true,
            precision: 0.1,
            text: ['Cantidad   \ntransada   '],
            textGap: 30,
            textStyle: {
              color: '#000'
            },
            outOfRange: {
              symbolSize: [1, 2],
              color: ['rgba(0,0,0,0.5)']
            },
            controller: {
              outOfRange: {
                color: ['#444']
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
