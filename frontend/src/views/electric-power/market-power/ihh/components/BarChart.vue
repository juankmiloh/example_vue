<template>
  <div id="chart" :class="className" :style="{height:height,width:width}" class="rcorners" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'
import _ from 'lodash'

const animationDuration = 3000

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
      default: 'Valor'
    },
    chartTitle: {
      type: String
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
    getTop20(data) {
      var i = 0
      var items = []
      var values = []
      var otros = 0

      for (i = 0; i < data.length - 19; i++) {
        otros += data[i].values[0]
      }
      items.push('Otros')
      values.push(otros.toFixed(2))
      for (i; i < data.length; i++) {
        items.push(data[i].names[0].length > 45 ? (data[i].names[0].substring(0, 45) + '..') : data[i].names[0])
        values.push(data[i].values[0].toFixed(2))
      }
      return [items, values]
    },
    getFontSize() {
      const width = document.getElementById('chart').offsetWidth
      return (width >= 700) ? '10' : '6'
    },
    initChart(data) {
      this.chart = echarts.init(this.$el, 'macarons')
      if (!data) return

      data = _.orderBy(data, ['values.0'], ['asc'])
      var value = this.getTop20(data)

      var items = value[0]
      var values = value[1]
      var chartTitle = this.chartTitle

      this.chart.setOption({
        title: {
          left: 'center',
          text: 'Cuota de Mercado:\n' + chartTitle,
          textStyle: {
            color: '#000',
            fontSize: '22'
          }
        },
        grid: {
          top: 85,
          left: '2%',
          right: '5%',
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
                str = obj.trim().replace(/(.{1,30})(?:\n|$| )/g, '$1\n')
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
          barWidth: '70%',
          data: values,
          animationDuration
        }],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(obj) {
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 14px;padding-bottom: 7px;margin-bottom: 7px">' +
                            obj[0].name +
                            '</div> <strong>Valor: </strong>' + obj[0].value + '<strong>%</strong>'
          }
        },
        color: ['#344b58', '#4cabce', '#e5323e']
      })
    }
  }
}
</script>
