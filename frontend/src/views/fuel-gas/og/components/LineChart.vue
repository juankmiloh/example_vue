<template>
  <div>
    <div id="chartoc" class="rcorners" :style="{height:height,width:width}" />
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'
import _ from 'lodash'

const animationDuration = 1000

export default {
  props: {
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
      chart: null,
      series: []
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
          top: '75px',
          left: '50px',
          right: '50px',
          bottom: '75',
          containLabel: true
        }
      }
      return {
        top: '145px',
        left: '5px',
        right: '5px',
        bottom: '75',
        containLabel: true

      }
    },
    initChart(data) {
      this.series = []
      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      for (const key in data) {
        var data_group = data[key].data
        data_group = _.orderBy(data_group, ['dates'], ['asc'])
        if (!data_group) continue

        var values = []
        var items = []

        for (let i = 0; i < data_group.length; i++) {
          values.push(data_group[i].values[0])
          items.push(data_group[i].dates[0])
        }
        this.series.push({
          name: data[key].name,
          type: 'line',
          stack: 'gas',
          areaStyle: {},
          data: values.slice(),
          smooth: false,
          large: true,
          animationDuration
        })
      }
      this.chart.setOption({
        title: {
          left: 'center',
          text: 'Produccion de Gas por Campo (GBTUD)',
          textStyle: {
            color: '#000',
            fontSize: 16
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow' // 'line' | 'shadow'
          }
        },
        legend: {
          top: '23px',
          textStyle: {
            color: '#000',
            fontSize: 16
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
        xAxis: {
          name: '\n\n\n\nFecha',
          nameLocation: 'middle',
          data: items,
          type: 'category',
          silent: false,
          splitLine: {
            show: true
          },
          splitArea: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            interval: items ? Math.floor(items.length / 20) : 10,
            rotate: 45,
            textStyle: {
              fontSize: this.getFontSize()
            }
          }
        },
        yAxis: {
          name: 'GBTUD',
          splitArea: {
            show: true
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            interval: 0,
            show: true,
            textStyle: {
              fontSize: this.getFontSize()
            }
          }
        },
        series: this.series
      })
    },
    formatterNumber(number) {
      if (!number) {
        return 0
      }

      return number.toFixed(2)
    }
  }
}
</script>
