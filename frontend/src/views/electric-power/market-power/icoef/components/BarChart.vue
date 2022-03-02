<template>
  <div>
    <div id="chartoc" :style="{height:height,width:width}" class="rcorners" />
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
      default: function() { new Date() }
    },
    data: {
      type: Array,
      default: function() { return [] }
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
    initChart(data) {
      const series = []
      let items = []
      const plants = []

      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(data)) {
        return
      }
      for (const i in data) {
        if (data[i].dates.length > items.length) {
          items = data[i].dates
        }
      }

      for (let i = 0; i < data.length; i++) {
        plants.push(data[i].names)
        series.push({
          name: data[i].names,
          type: 'bar',
          barGap: 0,
          data: data[i].values
        })
      }

      plants.sort()
      series.sort((a, b) => (a.name > b.name) ? 1 : -1)

      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          type: 'scroll',
          top: 30,
          right: 30,
          left: 30,
          textStyle: {
            color: '#000',
            fontSize: 13
          }
        },
        grid: {
          top: '120px',
          left: '50px',
          right: '85px',
          bottom: '65',
          containLabel: true
        },
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
          neme: 'Periodo',
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
            // interval: items ? Math.floor(items.length / 30) : 10,
            rotate: 45
          },
          data: items
        },
        yAxis: [
          {
            name: 'Días (No. días)',
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 1
              }
            }
          },
          {
            name: '',
            splitArea: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000',
                width: 1
              }
            },
            splitLine: {
              show: false
            }
          }
        ],
        series: series
        // color: ['#CA9523', '#F5871E', '#91d7ae', '#8DCA38', '#4475f0', '#1E90FF']
      })
    }
  }
}
</script>
