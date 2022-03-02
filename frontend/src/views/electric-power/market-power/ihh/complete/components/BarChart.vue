<template>
  <div id="chartoc" :class="className" :style="{height:height,width:width}" class="rcorners" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'
import moment from 'moment'

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
    chartTitle: {
      type: String,
      default: ''
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
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: 90,
          left: '25px',
          right: '25px',
          bottom: '80',
          containLabel: true
        }
      }
      return {
        top: 180,
        left: '5px',
        right: '5px',
        bottom: '80',
        containLabel: true

      }
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    initChart(data) {
      this.chart = echarts.init(this.$el, 'macarons')
      if (!data) return

      var dates = []
      var series_dis_rea = []
      var series_fij_pre = []
      var series_gen_rea = []
      var series_cap_ins = []
      var series_enficc = []
      var nivel_bajo = []
      var nivel_medio = []
      var nivel_alto = []

      for (var row in data) {
        dates.push(this.formatDate(data[row].date))
        series_dis_rea.push(data[row].dis_rea)
        series_fij_pre.push(data[row].fij_pre)
        series_gen_rea.push(data[row].gen_rea)
        series_cap_ins.push(data[row].cap_ins)
        series_enficc.push(data[row].enficc)
        nivel_bajo.push(1000)
        nivel_medio.push(800)
        nivel_alto.push(2500 - 800 - 1000)
      }

      this.chart.setOption({
        legend: {
          left: 'center',
          textStyle: {
            color: '#000',
            fontSize: 13
          },
          top: '15',
          data: ['HHI Disponibilidad real', 'HHI Generación real', 'HHI Capacidad instalada', 'HHI Fijación de precios', 'HHI ENFICC']
        },
        grid: this.getGridOptions(),
        yAxis: [{
          name: 'IHH',
          type: 'value',
          max: 2500,
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
          name: '\nPeriodo',
          nameLocation: 'middle',
          data: dates,
          splitLine: {
            show: true
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
        series: [{
          name: 'HHI Disponibilidad real',
          type: 'line',
          barWidth: '70%',
          data: series_dis_rea,
          animationDuration,
          color: '#ed7d31',
          showSymbol: false,
          smooth: false
        },
        {
          name: 'HHI Generación real',
          type: 'line',
          barWidth: '70%',
          data: series_gen_rea,
          animationDuration,
          color: 'blue',
          showSymbol: false,
          smooth: false
        },
        {
          name: 'HHI Capacidad instalada',
          type: 'line',
          barWidth: '70%',
          data: series_cap_ins,
          animationDuration,
          color: 'green',
          showSymbol: false,
          smooth: false
        },
        {
          name: 'HHI Fijación de precios',
          type: 'line',
          barWidth: '70%',
          data: series_fij_pre,
          animationDuration,
          color: 'purple',
          showSymbol: false,
          smooth: false
        },
        {
          name: 'HHI ENFICC',
          type: 'line',
          barWidth: '70%',
          data: series_enficc,
          animationDuration,
          color: 'brown',
          showSymbol: false,
          smooth: false
        },
        {
          name: 'Nivel Bajo',
          type: 'line',
          showSymbol: false,
          data: nivel_bajo,
          color: 'rgba(194, 217,	177, 0.3)',
          areaStyle: {
            color: 'rgba(194, 217,	177, 0.3)'
          },
          stack: 'regiones',
          animationDuration,
          smooth: false
        },
        {
          name: 'Nivel Moderado',
          type: 'line',
          showSymbol: false,
          data: nivel_medio,
          color: 'rgba(255, 229, 201, 0.3)',
          areaStyle: {
            color: 'rgba(255, 229, 201, 0.3)'
          },
          stack: 'regiones',
          animationDuration,
          smooth: false
        },
        {
          name: 'Nivel Alto',
          type: 'line',
          showSymbol: false,
          data: nivel_alto,
          color: 'rgba(255, 161, 149, 0.3)',
          areaStyle: {
            color: 'rgba(255, 161, 149, 0.3)'
          },
          stack: 'regiones',
          animationDuration,
          smooth: false
        }],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow' // 'line' | 'shadow'
          }
        }
      })
    }
  }
}
</script>
