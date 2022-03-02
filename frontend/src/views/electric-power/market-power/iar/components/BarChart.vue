<template>
  <div>
    <div
      id="chararea"
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
    tolerances: {
      type: Number,
      default: 10
    }
  },
  data() {
    return {
      chart: null,
      height: '450px'
    }
  },
  watch: {
    tolerances: function(newVal, oldVal) {
      this.height = (170 + 40 * this.tolerances) + 'px'
      console.info(this.height)
      this.chart.resize()
    },
    data: function(newVal, oldVal) {
      this.height = (170 + 40 * this.tolerances) + 'px'
      this.initChart(newVal)
      this.chart.resize()
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
      const width = document.getElementById('chararea').offsetWidth
      return width >= 700
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return [
          {
            left: 40,
            right: 40,
            top: '80px',
            containLabel: true
          }
        ]
      }
      return [
        {
          left: 10,
          right: 10,
          top: '80px',
          containLabel: true
        }
      ]
    },
    getFontSize() {
      const width = document.getElementById('chararea').offsetWidth
      return width >= 700 ? '10' : '6'
    },
    initChart(data) {
      const series = []
      let items = []

      this.chart = echarts.init(document.getElementById('chararea'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(data)) {
        return
      }
      items = items.concat(data[0].value)

      series.push({
        name: 'Horas de compensación',
        type: 'bar',
        barGap: 0,
        data: data[0].hc
      })
      series.push({
        name: 'Horas de indisponibilidad',
        type: 'bar',
        barGap: 0,
        data: data[0].hid
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
            left: 'center',
            top: '5px',
            text:
              'Activos (Agentes) de transmisión con más horas de\ndisponibilidad en el periodo de análisis',
            textStyle: {
              color: '#000',
              fontSize: '100%'
            }
          }
        ],
        grid: this.getGridOptions(),
        yAxis: [
          {
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
            axisLabel: {
              interval: 0,
              show: true,
              textStyle: {
                fontSize: this.getFontSize()
              },
              formatter: function(obj) {
                const width = document.getElementById('chararea').offsetWidth
                var str = ''
                if (width >= 700) {
                  str = obj.trim().replace(/(.{1,30})(?:\n|$| )/g, '$1\n')
                } else {
                  str = obj.trim().replace(/(.{1,20})(?:\n|$| )/g, '$1\n')
                }

                return str.substring(0, str.length - 1)
              }
            },
            data: items
          }
        ],
        xAxis: [
          {
            type: 'value',
            name: '\nHoras',
            nameLocation: 'middle',
            min: 0,
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 1
              }
            }
          }
        ],
        series: series,
        color: ['#20699b', '#e84545']
      })
    }
  }
}
</script>
