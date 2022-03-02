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
      if (!data) return
      var items = []
      var values = []
      for (var i = 0; i < data.length; i++) {
        items.push(data[i].dates[0].split(' ')[0])
        values.push(data[i].values[0].toFixed(2))
      }

      this.chart.setOption({
        title: {
          left: 'center',
          text: 'Desviación en generación',
          textStyle: {
            color: '#000',
            fontSize: '22'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          top: 65,
          left: '3%',
          right: '5%',
          bottom: '85',
          containLabel: true
        },
        xAxis: [{
          name: '\n\n\n\nFecha',
          nameLocation: 'middle',
          data: items,
          splitLine: {
            show: true
          },
          axisTick: {
            alignWithLabel: true
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            rotate: 45
          }
        }],
        yAxis: [{
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
            color: '#000' },
          borderColor: '#000'

        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        color: ['#2f4554', '#F5871E', '#91d7ae', '#8DCA38', '#4475f0', '#1E90FF'],
        series: [{
          name: 'Desviación',
          type: 'line',
          barWidth: '60%',
          data: values,
          animationDuration,
          itemStyle: {
            normal: {
              barBorderRadius: 0,
              label: {
                show: true,
                position: 'top',
                formatter(p) {
                  return Number(p.value).toFixed(2) + ' %'
                }
              }
            }
          }
        }]
      })
    }
  }
}
</script>
