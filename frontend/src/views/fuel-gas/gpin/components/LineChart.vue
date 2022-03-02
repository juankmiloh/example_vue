<template>
  <div>
    <div
      id="chartgpin"
      :style="{ height: height, width: width }"
      class="rcorners"
    />
  </div>
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
      default: function() {
        return []
      }
    },
    valueTitle: {
      type: String,
      default: 'Índice'
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
      series: [],
      xAxis: []
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
      const width = document.getElementById('chartgpin').offsetWidth
      return width >= 700
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: '120px',
          left: '50px',
          right: '50px',
          bottom: '40px',
          containLabel: true
        }
      }
      return {
        top: '170px',
        left: '5px',
        right: '5px',
        bottom: '40px',
        containLabel: true
      }
    },
    initChart(data) {
      var items = []
      this.series = []
      this.chart = echarts.init(
        document.getElementById('chartgpin'),
        'macarons'
      )
      this.chart.clear()
      if (!data) return

      var config = {
        rotate: 0,
        align: 'center',
        verticalAlign: 'middle',
        position: 'top',
        distance: 15
      }

      var labelOption = {
        normal: {
          show: true,
          rotate: config.rotate,
          align: config.align,
          verticalAlign: config.verticalAlign,
          position: config.position,
          distance: config.distance,
          formatter: '{a} \n {c}',
          fontSize: 15
        }
      }

      for (const key in data) {
        var values = []

        items.push(data[key].name)
        values.push(data[key].data[0].values[1].toFixed(2))

        this.series.push({
          name: data[key].name,
          label: labelOption,
          step: 'end',
          type: 'bar',
          data: values,
          smooth: false,
          large: true,
          animationDuration
        })
      }

      this.chart.setOption({
        legend: {
          data: items,
          textStyle: {
            color: '#000',
            fontSize: 16
          }
        },
        grid: this.getGridOptions(),
        yAxis: [
          {
            name: 'Índice',
            type: 'value',
            axisTick: {
              alignWithLabel: true
            },
            axisLine: {
              lineStyle: {
                color: '#000'
              }
            }
          }
        ],
        xAxis: [
          {
            name: 'Fuente',
            type: 'category',
            nameLocation: 'middle',
            axisTick: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000'
              }
            }
          }
        ],
        series: this.series,
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow' // 'line' | 'shadow'
          }
        }
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
