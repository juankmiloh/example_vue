<template>
  <div>
    <div id="chartoc" :style="{ height: height, width: width }" class="rcorners" />
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
      type: Array,
      default: function() {
        return []
      }
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
      default: '600px'
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
      const width = document.getElementById('chartoc').offsetWidth
      return width >= 700
    },
    getFontSize() {
      return this.isBigSize() ? 13 : 9
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: '120px',
          left: '50px',
          right: '120px',
          bottom: '30px',
          containLabel: true
        }
      }
      return {
        top: '165px',
        left: '5px',
        right: '15px',
        bottom: '30px',
        containLabel: true

      }
    },
    initChart(data) {
      var legends = []
      var series = []
      var vals = []

      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(data)) {
        return
      }

      for (const i in data) {
        vals = []
        for (const j in data[i].values) {
          vals.push([
            data[i].values[j][8],
            data[i].values[j][7],
            data[i].values[j][6],
            data[i].values[j][0],
            data[i].values[j][1],
            data[i].values[j][2],
            data[i].values[j][3],
            data[i].values[j][4],
            data[i].values[j][5]
          ])
        }
        console.log(JSON.stringify(vals))
        legends.push(data[i].names)
        series.push({
          name: data[i].names,
          type: 'scatter',
          data: vals,
          label: {
            show: true,
            position: 'right',
            formatter: '{@[3]}'
          },
          symbolSize: function(data) {
            return Math.sqrt(data[2]) / 2e-1
          }
        })
      }

      var schema = [
        { name: 'planta', index: 0, text: 'Nombre de la planta' },
        { name: 'agente', index: 1, text: 'Nombre del agente' },
        { name: 'capacidad', index: 2, text: 'Capacidad Efectiva Neta' },
        { name: 'duracion', index: 3, text: 'Duración Media en horas' },
        { name: 'frecuencia', index: 4, text: 'Frecuencia en número de veces' },
        { name: 'causa', index: 5, text: 'Causa' },
        { name: 'tecnologia', index: 6, text: 'Tecnología de generación' }
      ]

      this.chart.setOption({
        color: [
          '#fce654',
          '#91c7ae',
          '#E56399',
          '#DE6E4B',
          '#d48265',
          '#749f83',
          '#c23531',
          '#ca8622',
          '#bda29a',
          '#7FD1B9',
          '#61a0a8',
          '#7A6563',
          '#E5D4CE'
        ],
        legend: {
          top: 10,
          data: legends,
          textStyle: {
            color: '#000',
            fontSize: 16
          }
        },
        visualMap: [
          {
            left: 'right',
            top: '150px',
            dimension: 2,
            itemWidth: 45,
            itemHeight: 200,
            calculable: true,
            precision: 0.1,
            text: ['Capacidad\nEfectiva Neta'],
            textGap: 15,
            textStyle: {
              color: '#000'
            },
            inRange: {
              symbolSize: [10, 70]
            },
            outOfRange: {
              symbolSize: [10, 70],
              color: ['rgba(255,255,255,.2)']
            },
            controller: {
              inRange: {
                color: ['rgba(52,75,88,.7)']
              },
              outOfRange: {
                color: ['rgba(230,230,230,.3)']
              }
            }
          }
        ],
        grid: this.getGridOptions(),
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
              ': ' +
              value[3] +
              '<br>' +
              schema[6].text +
              '：' +
              value[6] +
              '<br>' +
              schema[5].text +
              '：' +
              value[7] +
              '<br>' +
              schema[2].text +
              '：' +
              value[2] +
              '<br>' +
              schema[3].text +
              '：' +
              value[1] +
              '<br>' +
              schema[4].text +
              '：' +
              value[0]
            )
          }
        },
        xAxis: {
          type: 'value',
          name: 'Frecuencia [número de veces]',
          nameLocation: 'middle',
          nameGap: 30,
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
          }
        },
        yAxis: {
          type: 'value',
          name: 'Duración media [horas]',
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
        },
        series: series
      })
    }
  }
}
</script>
