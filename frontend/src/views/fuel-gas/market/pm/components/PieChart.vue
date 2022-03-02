<template>
  <div :class="className" class="rcorners" :style="{height:height,width:width}" />
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
      var values = []
      for (var i = 0; i < data.length; i++) {
        values.push({ value: data[i].values[0], name: data[i].names[0] })
      }

      this.chart.setOption({
        series: [{
          name: this.valueTitle,
          type: 'pie',
          stack: 'vistors',
          radius: '70%',
          data: values,
          animationDuration,
          label: {
            formatter: '{b}:  {d}%'
          }
        }]
      })
    }
  }
}
</script>
