<template>
  <div :class="className" :style="{height:height,width:width}" class="rcorners" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'
import _ from 'lodash'

const animationDuration = 3000

export default {
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
      default: '900px'
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
      this.chart = echarts.init(this.$el, 'macarons')

      var valuesCharts = []
      if (!data) return

      for (var i = 0; i < data.length; i++) {
        valuesCharts.push({
          items: data[i].names[1].length > 45 ? (data[i].names[1].substring(0, 45) + '..') : data[i].names[1],
          values: data[i].values[0]
        })
      }
      valuesCharts = _.orderBy(valuesCharts, ['values'], ['asc'])

      var items = []
      var values = []

      for (i = 0; i < valuesCharts.length; i++) {
        items.push(valuesCharts[i].items)
        values.push(valuesCharts[i].values)
      }

      this.chart.setOption({
        title: {
          text: 'Oferta de Precios',
          left: 'center',
          top: '10',
          textStyle: {
            color: '#000',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#000',
            fontSize: '16'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow' // 'line' | 'shadow'
          }
        },
        grid: {
          top: 65,
          left: '2%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: [{
          name: 'Agentes',
          type: 'category',
          data: items,
          axisTick: {
            alignWithLabel: true
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          }
        }],
        xAxis: [{
          name: '$/kWh',
          type: 'value',
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          }
        }],
        series: [{
          name: this.valueTitle,
          type: 'bar',
          stack: 'vistors',
          barWidth: '60%',
          data: values,
          animationDuration
        }],
        color: ['#344b58', '#4cabce', '#e5323e']
      })
    }
  }
}
</script>
