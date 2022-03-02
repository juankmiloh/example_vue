<template>
  <div>
    <div id="chartoc" class="rcorners" :style="{height:height,width:width}" />
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:10px;">
      Precio promedio Firme: {{ formatterNumber(precioPromedioInter) }} (USD/MBTU)<br>
      Precio promedio Interrumpible: {{ formatterNumber(precioPromedioFirme) }} (USD/MBTU)<br>
    </el-row>
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'

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
    },
    publicConf: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      chart: null,
      precioPromedioFirme: 0,
      precioPromedioInter: 0
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
          top: 70,
          left: '25px',
          right: '25px',
          bottom: '4%',
          containLabel: true
        }
      }
      return {
        top: 70,
        left: '5px',
        right: '5px',
        bottom: '40',
        containLabel: true

      }
    },
    getChartValues(data) {
      var items = []
      var values = []

      var CxDAcc = 0
      var PxCxDAcc = 0
      var cantidadAcc = 0
      var precioPromedio = 0

      if (data === undefined) {
        return [
          [], 0, []
        ]
      }

      for (let i = 0; i < data.length; i++) {
        var name = data[i].names[0]
        var precio = data[i].values[0]
        var cantidad = data[i].values[1]
        var CxD = data[i].values[2]
        var PxCxD = data[i].values[3]

        CxDAcc += CxD
        PxCxDAcc += PxCxD

        cantidadAcc += cantidad

        name = name.length > 35 ? (name.substring(0, 35) + '..') : name

        items.push(name)
        values.push({
          name: name,
          value: [cantidadAcc, precio]
        })
      }
      precioPromedio = PxCxDAcc / CxDAcc

      return [values, precioPromedio, items]
    },
    initChart(data) {
      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.precioPromedioFirme = 0
      this.precioPromedioInter = 0

      if (!data) return

      var data_inter = this.getChartValues(data[0])
      var data_firme = this.getChartValues(data[1])

      var values_firme = data_firme[0]
      var values_inter = data_inter[0]

      this.precioPromedioFirme = data_firme[1]
      this.precioPromedioInter = data_inter[1]

      this.chart.setOption({
        legend: {
          data: ['Interrumpible', 'Firme'],
          textStyle: {
            color: '#000',
            fontSize: 16
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow' // 'line' | 'shadow'
          },
          formatter: function(obj) {
            return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 14px;padding-bottom: 7px;margin-bottom: 7px">' +
                            obj[0].name +
                            '</div>' +
                            '<strong>Precio: </strong>' + obj[0].value[1] + ' USD/MBTU<br>' +
                            '<strong>Cantidad: </strong>' + obj[0].value[0] + ' MBTUD<br>'
          }
        },
        grid: this.getGridOptions(),
        yAxis: [{
          name: '                        Precio (USD/MBTU)',
          type: 'value',
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
          name: '\n\n\nCantidad\n(MBTUD)',
          nameLocation: 'middle',
          type: 'value',
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            rotate: 45,
            textStyle: {
              fontSize: this.getFontSize()
            }
          }
        }],
        series: [{
          name: 'Firme',
          step: 'end',
          type: 'line',
          data: values_firme,
          smooth: false,
          animationDuration
        }, {
          name: 'Interrumpible',
          step: 'end',
          type: 'line',
          data: values_inter,
          smooth: false,
          animationDuration
        }]
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
