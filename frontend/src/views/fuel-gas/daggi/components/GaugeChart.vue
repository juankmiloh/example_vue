<template>
  <div :class="className" class="rcorners" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'

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
      default: '700px'
    },
    thresholds: {
      type: Array,
      default: function() {
        return []
      }
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
      var self = this
      this.chart = echarts.init(this.$el, 'macarons')
      if (!data && data.length > 0) return
      var names = data[0].names
      var values = data[0].values
      var offset = 50
      var series = []
      var colors = ['#5465a0', '#7A6563', '#b4bcb3', '#d3dee5', '#61a0a9', '#ca8622']

      for (var i = 0; i < names.length; i++) {
        var generatteformatter = function() {
          var name = names[i]
          return function formatter(value) {
            return name + ': ' + Number(value).toFixed(1) + ' días'
          }
        }

        var serie = {
          name: names[i],
          type: 'gauge',
          data: [{
            value: values[i],
            name: ''
          }],
          axisLine: {
            lineStyle: {
              color: [
                [(self.thresholds[3] - self.thresholds[2]) / self.thresholds[3].toFixed(2), '#71a78e'],
                [(self.thresholds[3] - self.thresholds[1]) / self.thresholds[3].toFixed(2), '#fea500'],
                [(self.thresholds[3] - self.thresholds[0]) / self.thresholds[3].toFixed(2), '#cb5754']
              ],
              'width': 40
            }
          },
          pointer: {
            width: 8
          },
          radius: '70%',
          axisTick: {
            lineStyle: {
              color: '#fff',
              width: 3
            },
            length: 40,
            splitNumber: 1
          },
          axisLabel: {
            distance: 20,
            textStyle: {
              color: '#888',
              fontSize: 14
            }
          },
          splitNumber: self.thresholds[3],
          min: self.thresholds[3],
          max: self.thresholds[0],
          startAngle: 200,
          endAngle: -20,
          itemStyle: {
            normal: {
              color: colors[i]
            }
          },
          detail: {
            formatter: generatteformatter(),
            offsetCenter: [0, (offset + i * 22) + '%'],
            textStyle: {
              fontSize: 20
            },
            borderWidth: 2,
            borderRadius: 5,
            borderColor: colors[i]
          }
        }

        if (i === 0) {
          serie.axisLabel = {
            distance: -125,
            textStyle: {
              fontSize: 20
            },
            formatter: function(v) {
              switch (v) {
                case self.thresholds[1] - 2:
                  return 'Menos de \n' + self.thresholds[1] + ' días  '
                case self.thresholds[2] - 2:
                  return 'Entre ' + self.thresholds[1] + ' y\n' + self.thresholds[2] + ' días  '
                case self.thresholds[3] - 2:
                  return 'Mayor a \n' + self.thresholds[2] + ' días  '
              }
            }
          }
          serie.axisTick = {
            lineStyle: {
              color: '#61a0a9',
              width: 3
            },
            length: -8,
            splitNumber: 1
          }
        }
        series.push(serie)
      }

      this.chart.setOption({
        title: {
          text: 'DAGGI',
          textStyle: {
            color: '#000',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#90979c',
            fontSize: '16'
          }
        },
        grid: {
          top: 200,
          bottom: 50
        },
        legend: {
          top: '4%'
        },
        tooltip: {
          formatter: function(data) {
            return data.seriesName + ': ' + Number(data.value).toFixed(1) + ' días'
          }
        },
        series: series
      })
    }
  }
}
</script>
