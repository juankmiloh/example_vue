<template>
  <div>
    <div id="chartoc" :style="{height:height,width:width}" class="rcorners" />
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'

const animationDuration = 400
const THRESHOLD = 1

export default {
  props: {
    pivots: {
      type: Number,
      default: 1
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
          left: '20px',
          right: '20px',
          bottom: '80px',
          containLabel: true
        }
      }
      return {
        top: '180px',
        left: '1px',
        right: '1px',
        bottom: '80px',
        containLabel: true

      }
    },
    initChart(data) {
      const series = []
      let items = []
      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      for (let i = 0; i < data.length; i++) {
        if (i === 0) {
          items = data[0].dates
        }
        if (i === 200) {
          break
        }
        series.push({
          name: data[i].id,
          type: 'scatter',
          data: Array.from(data[i].values, x => x.toFixed(2)),
          smooth: false,
          animationDuration,
          symbolSize: 8,
          symbol: 'circle'
        })
      }

      series.push({
        name: 'Límite',
        type: 'line',
        areaStyle: {},
        data: Array(items.length).fill(THRESHOLD),
        smooth: false,
        animationDuration,
        symbolSize: 1,
        symbol: 'box',
        color: 'rgba(255, 0, 0, 0.2)'
      })

      let legend = null
      let tooltip = null
      if (this.pivots === 1) {
        legend = {
          top: '30px',
          textStyle: {
            // color: '#A0A7Ac',
            fontSize: 10
          }
        }
        tooltip = {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        }
      } else {
        tooltip = {
          formatter: function(value) {
            return value.seriesName + ': ' + value.value
          }
        }
      }

      this.chart.setOption({
        title: {
          text: 'Indice Pivotal de Oferta Residual',
          textStyle: {
            color: '#fff'
          }
        },
        legend: legend,
        tooltip: tooltip,
        // backgroundColor: '#344b58',
        grid: this.getGridOptions(),
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [0],
          bottom: 30,
          start: 0,
          end: 100,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '100%',
          handleStyle: {
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff'
          },
          borderColor: '#90979c'
        },
        {
          type: 'inside',
          show: true,
          height: 15
        }
        ],
        xAxis: {
          name: '\nHora',
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
              // color: '#90979c'
              color: '#000'
            }
          },
          data: items
        },
        yAxis: {
          name: '            Indice pivotal',
          type: 'value',
          splitArea: {
            show: false
          },
          axisLine: {
            lineStyle: {
              // color: '#90979c'
              color: '#000'
            }
          }
        },
        series: series,
        color: ['#fce654', '#c23531', '#000000', '#91c7ae', '#1E90FF', '#ca8622', '#5465a0', '#c4ccd3', '#61a0a8', '#7A6563', '#E5D4CE']
      })
    }
  }
}
</script>
