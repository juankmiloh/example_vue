<template>
  <div>
    <div id="chartoc" key="" :style="{height:height,width:width}" class="rcorners" />
  </div>
</template>

<script>
import echarts from 'echarts'
import _ from 'lodash'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'

const animationDuration = 500

export default {
  props: {
    referenceDate: {
      type: Date,
      default: function() { new Date() }
    },
    data: {
      type: Array,
      default: function() { return [] }
    },
    valueTitle: {
      type: String,
      default: 'Dispersión de precios'
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
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: '190px',
          left: '25px',
          right: '25px',
          bottom: '90px',
          containLabel: true
        }
      }
      return {
        top: '190px',
        left: '5px',
        right: '5px',
        bottom: '90px',
        containLabel: true

      }
    },
    initChart(data) {
      const series = []
      const items = []

      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(data) || data.length === 0) {
        return
      }
      const fData = []
      for (let i = 0; i < data.length; i++) {
        items.push(data[i].date)
        fData.push(data[i].index)
      }

      series.push({
        name: data[0].denominator_numerator,
        type: 'line',
        data: fData,
        smooth: false,
        animationDuration,
        symbol: 'circle',
        yAxisIndex: 0,
        symbolSize: 10,
        lineStyle: {
          width: 3
        }
      })

      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          top: '15px',
          textStyle: {
            color: '#000',
            fontSize: 11
          }
        },
        grid: this.getGridOptions(),
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0
          ],
          bottom: 30,
          start: 0,
          end: 100,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '100%',
          handleStyle: {
            color: '#000'

          },
          textStyle: {
            color: '#000'
          },
          borderColor: '#000'
        },
        {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 60
        }],
        xAxis: {
          type: 'category',
          name: '\n\n\n\nFecha',
          nameLocation: 'middle',
          silent: false,
          splitLine: {
            show: true
          },
          splitArea: {
            show: true
          },
          axisLine: {
            lineStyle: {
              color: '#000',
              width: 2
            }
          },
          axisLabel: {
            interval: items ? Math.floor(items.length / 30) : 10,
            rotate: 45
          },
          data: items
        },
        yAxis: [
          {
            name: '           índice de dispersión',
            nameLocation: 'end',
            offset: 0,
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 1
              }
            }
          }
        ],
        series: series,
        color: ['#CA9523', '#F5871E', '#91d7ae', '#8DCA38', '#4475f0', '#1E90FF']
      })
    }
  }
}
</script>
