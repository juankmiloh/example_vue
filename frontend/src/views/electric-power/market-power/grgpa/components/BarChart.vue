<template>
  <div :class="className" :style="{height:height,width:width}" class="rcorners" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'

const animationDuration = 3000

export default {
  props: {
    data: {
      type: Array,
      default: function() { return [] }
    },
    itemTitle: {
      type: String,
      default: 'agente'
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
            yAxis: {
              axisLabel: {
                textStyle: {
                  fontSize: this.getFontSize()
                }
              }
            }
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
    getFontSize() {
      const width = document.getElementById('chart').offsetWidth
      return (width >= 700) ? '13' : '6'
    },
    initChart(data) {
      this.chart = echarts.init(this.$el, 'macarons')

      if (!data) return
      var items = []
      var values = []
      for (var i = 0; i < data.length; i++) {
        items.push(data[i].names[0].length > 45 ? (data[i].names[0].substring(0, 45) + '..') : data[i].names[0])
        values.push(data[i].values[0])
      }

      this.chart.setOption({
        title: {
          left: 'center',
          text: 'Desviación en generación por ' + this.itemTitle,
          textStyle: {
            color: '#000',
            fontSize: '22'
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
          right: '4%',
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
          },
          axisLabel: {
            interval: 0,
            show: true,
            textStyle: {
              fontSize: this.getFontSize()
            },
            formatter: function(obj) {
              const width = document.getElementById('chart').offsetWidth
              var str = ''
              if (width >= 700) {
                str = obj.trim().replace(/(.{1,50})(?:\n|$| )/g, '$1\n')
              } else {
                str = obj.trim().replace(/(.{1,15})(?:\n|$| )/g, '$1\n')
              }

              return str.substring(0, str.length - 1)
            }
          }
        }],
        xAxis: [{
          name: '%',
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
