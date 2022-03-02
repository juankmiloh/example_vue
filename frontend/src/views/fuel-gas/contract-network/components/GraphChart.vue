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

export default {
  props: {
    data: {
      type: Object,
      default: function() {
        return null
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
      default: '700px'
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
      this.chart = echarts.init(
        document.getElementById('chartgpin'),
        'macarons'
      )
      this.chart.clear()

      this.chart.setOption({
        title: {
          text: 'Graph'
        },

        legend: [{
          data: data.categories.map(function(a) {
            return a.name
          })
        }],

        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',

        tooltip: {},
        series: [
          {
            name: 'Red de contratación - TEBSA',
            type: 'graph',
            layout: 'force',
            force: {
              repulsion: 2500,
              layoutAnimation: false
            },
            categories: data.categories,

            // symbolSize: 60,
            color: ['#3CAEA3', '#20639B', '#EA5455'],
            roam: true,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
              fontSize: 20
            },
            data: data.nodes,
            links: data.links,
            lineStyle: {
              // opacity: 0.6,
              width: 3,
              curveness: 0.2,
              color: 'source'
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 6
              }
            },
            label: {
              show: true,
              /* position: 'right',*/
              formatter: '{b}'
            }
            /*
            scaleLimit: {
              min: 0.4,
              max: 20
            */
          }
        ]
      }
      )
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
