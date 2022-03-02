<template>
  <div>
    <div
      id="chartoc"
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
      default: '450px'
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
    getGridOptions() {
      if (this.isBigSize()) {
        return [
          {
            left: 40,
            right: 40,
            top: '100px',
            containLabel: true
          }
        ]
      }
      return [
        {
          left: 10,
          right: 10,
          top: '100px',
          containLabel: true
        }
      ]
    },
    getFontSize() {
      const width = document.getElementById('chartoc').offsetWidth
      return width >= 700 ? '10' : '6'
    },
    initChart(data) {
      const series = []
      let items2 = []

      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(data)) {
        return
      }
      items2 = items2.concat(data[0].series)

      series.push({
        name: 'Probabilidad acumulada de horas de indisponibilidad',
        type: 'line',
        areaStyle: {},
        barGap: 0,
        data: data[0].acumulado,
        yAxisIndex: 1
      })
      series.push({
        name: 'Probabilidad de horas de indisponibilidad',
        type: 'bar',
        barGap: 0,
        data: data[0].hist,
        yAxisIndex: 0
      })

      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: [
          {
            type: 'scroll',
            top: '50px',
            textStyle: {
              color: '#000',
              fontSize: 13
            }
          }
        ],
        title: [
          {
            top: '10px',
            left: 'center',
            text:
              'Densidad de probabilidad y densidad acumulada de las horas de\nindisponibilidad por activo de transmisión en el periodo de análisis',
            textStyle: {
              color: '#000',
              fontSize: '95%'
            }
          }
        ],
        grid: this.getGridOptions(),
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0
          ],
          bottom: 5,
          start: 0,
          end: 20,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '100%',
          handleStyle: {
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff'
          },
          borderColor: '#000'
        },
        {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 60
        }
        ],
        yAxis: [
          {
            name: 'Probabilidad',
            silent: false,
            splitLine: {
              show: false
            },
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 2
              }
            }
          },
          {
            name: 'Probabilidad acumulada      ',
            silent: false,
            splitLine: {
              show: false
            },
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 2
              }
            }
          }
        ],
        xAxis: [
          {
            name: '\nHoras',
            nameLocation: 'middle',
            type: 'category',
            silent: false,
            splitLine: {
              show: false
            },
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 2
              }
            },
            data: items2
          }
        ],
        series: series,
        color: ['rgba(255, 185, 151, 2)', 'rgba(32, 105, 155, 1)'] // '#ffabb1', '#20699b'
      })
    }
  }
}
</script>
