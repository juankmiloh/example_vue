<template>
  <div>
    <div id="chartoc" :style="{height:height,width:'100%'}" class="rcorners" />
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'
import 'echarts-gl'

export default {
  props: {
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
      if (data.length === 0) {
        return
      }
      this.series = []
      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      var schema = [
        { name: 'x', index: 0, text: 'Hora' },
        { name: 'y', index: 1, text: 'IOR' },
        { name: 'z', index: 2, text: 'Día' }
      ]

      this.chart.setOption({
        tooltip: {
          padding: 10,
          backgroundColor: '#222',
          borderColor: '#777',
          borderWidth: 1,
          formatter: function(obj) {
            var value = obj.value
            return (
              '<div style="font-size: 18px;">' +
              obj.seriesName +
              ': ' +
              value[2] +
              '<br>' +
              schema[0].text +
              '：' +
              value[0] +
              '<br>' +
              schema[2].text +
              '：' +
              data[0].dates[value[1]]
            )
          }
        },
        title: {
          text: 'Índice de Oferta Residual',
          left: 'center',
          x: '20',
          top: '20',
          textStyle: {
            color: '#000',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#000',
            fontSize: '16'
          }
        },
        visualMap: {
          show: false,
          min: 1,
          max: 5,
          inRange: {
            color: ['#a50026', '#fee090', '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027']
          }
        },
        xAxis3D: {
          type: 'category',
          data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 22, 23, 24],
          name: 'Hora'
        },
        yAxis3D: {
          type: 'category',
          data: data[0].dates,
          name: '         Día'
        },
        zAxis3D: {
          type: 'value',
          max: 3,
          min: 0,
          name: 'IOR'
        },
        grid3D: {
          viewControl: {
            // projection: 'orthographic'
          },
          boxWidth: 140,
          boxDepth: 100,
          axisLine: {
            lineStyle: { color: '#000' }
          },
          axisPointer: {
            lineStyle: { color: '#000' }
          },
          light: {
            main: {
              shadow: true,
              quality: 'ultra',
              intensity: 1.5
            }
          }
        },
        series: [{
          name: 'IOR',
          type: 'bar3D',
          data: data[0].values,
          shading: 'lambert',
          label: {
            formatter: function(param) {
              return param.value[2].toFixed(1)
            }
          }
        }
        ]
      }
      )
    }
  }
}
</script>
