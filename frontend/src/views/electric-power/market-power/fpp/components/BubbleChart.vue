<template>
  <div>
    <div
      id="charbubble"
      :style="{ height: height, width: width }"
      class="rcorners"
    />
  </div>
</template>

<script>
import echarts from 'echarts'
import _ from 'lodash'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'

export default {
  props: {
    referenceDate: {
      type: Date,
      default: function() {
        new Date()
      }
    },
    data: {
      type: Object,
      default: function() {
        return {}
      }
    },
    agruparPorPlanta: {
      type: Boolean,
      default: true
    },
    valueTitle: {
      type: String,
      default: 'Precio'
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
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    data: function(newVal, oldVal) {
      this.initChart(newVal)
      this.__resizeHandler = debounce(() => {
        if (this.chart) {
          this.chart.resize()
          this.chart.setOption({
            grid: this.getGridOptions()
          })
        }
      }, 100)
      window.addEventListener('resize', this.__resizeHandler)
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
    isBigSize() {
      const width = document.getElementById('charbubble').offsetWidth
      return width >= 700
    },
    getFontSize() {
      return this.isBigSize() ? 13 : 9
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return [
          {
            left: 40,
            right: 100,
            top: '140px',
            containLabel: true
          }
        ]
      }
      return [
        {
          left: 10,
          right: 10,
          top: '220px',
          containLabel: true
        }
      ]
    },
    initChart(data) {
      var series = []
      var vals = []
      var items = data.items

      this.chart = echarts.init(document.getElementById('charbubble'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(items)) {
        return
      }

      for (const i in items) {
        vals = [
          items[i].values[0],
          items[i].values[3],
          items[i].values[2] * 10,
          items[i].values[1],
          items[i].values[4],
          items[i].values[5],
          items[i].values[6],
          items[i].values[2] * 10
        ]
        series.push({
          name: items[i].names,
          type: 'scatter',
          data: [vals],
          itemStyle: itemStyle,
          tooltip: {
            padding: 10,
            backgroundColor: '#222',
            borderColor: '#777',
            borderWidth: 1,
            formatter: function(obj) {
              var value = obj.value
              return (
                '<div style="font-size: 18px;">' +
                schema[0].text +
                '：' +
                value[5] +
                '<br>' +
                schema[1].text +
                '：' +
                value[6] +
                '<br>' +
                schema[2].text +
                '：' +
                value[0] +
                '<br>' +
                schema[3].text +
                '：' +
                value[2] / 10 +
                '<br>' +
                schema[4].text +
                '：' +
                value[1] * 1.0
              )
            }
          }
        })
      }

      var schema = [
        { name: 'agente', index: 0, text: 'Agente' },
        { name: 'planta', index: 1, text: 'Nombre planta' },
        { name: 'codigo', index: 2, text: 'Fecha' },
        { name: 'frecuencia', index: 3, text: 'Número de fijaciones' },
        { name: 'duracion', index: 4, text: 'Precio promedio de fijación' }
      ]
      var itemStyle = {
        opacity: 0.8,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
      var agrupacion = this.agruparPorPlanta ? 'planta' : 'agente'
      this.chart.setOption({
        title: [
          {
            top: '5px',
            left: 'center',
            text:
              'Fijación de precios diario por ' + agrupacion,
            textStyle: {
              color: '#000'
            }
          }
        ],
        color: [
          '#c23531',
          '#ca8622',
          '#bda29a',
          '#7FD1B9',
          '#61a0a8',
          '#7A6563',
          '#E5D4CE'
        ],
        legend: [
          {
            top: 50,
            textStyle: {
              color: '#000',
              fontSize: 16
            }
          }
        ],
        tooltip: {},
        visualMap: [
          {
            left: 'right',
            top: '130px',
            dimension: 7,
            show: true,
            itemWidth: 30,
            itemHeight: 120,
            calculable: true,
            precision: 0.1,
            text: ['Número de\nfijaciones'],
            textGap: 30,
            textStyle: {
              color: '#344B58'
            },
            inRange: {
              symbolSize: [5, 30]
            },
            outOfRange: {
              symbolSize: [5, 30],
              color: ['rgba(255,255,255,.2)']
            },
            controller: {
              inRange: {
                color: ['#344B58']
              },
              outOfRange: {
                color: ['#444']
              }
            }
          }
        ],
        grid: this.getGridOptions(),
        xAxis: [
          {
            type: 'category',
            name: '\n\nFecha',
            nameLocation: 'middle',
            nameGap: 60,
            nameTextStyle: {
              color: '#000',
              fontSize: 14
            },
            splitLine: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000'
              }
            },
            axisLabel: {
              interval: 0,
              rotate: 90,
              formatter: function(value) {
                return value.replaceAll('-', '/')
              }
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: 'Precio marginal [COP]',
            nameLocation: 'middle',
            nameGap: 40,
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
          }
        ],
        series: series
      })
    }
  }
}
</script>
