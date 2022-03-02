<template>
  <div>
    <div
      id="chartoc"
      :style="{ height: height, width: width }"
      class="rcorners"
    />
  </div>
</template>

<script>
import echarts from 'echarts'
import _ from 'lodash'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'

export default {
  props: {
    referenceDate: {
      type: Date,
      default: function() {
        new Date()
      }
    },
    data: {
      type: Object,
      default: function() {
        return {}
      }
    },
    agruparPorPlanta: {
      type: Boolean,
      default: true
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
      default: '850px'
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
    getFontSize() {
      return this.isBigSize() ? 13 : 9
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return [
          {
            left: 40,
            right: 40,
            top: '140px',
            containLabel: true
          }
        ]
      }
      return [
        {
          left: 10,
          right: 10,
          top: '220px',
          containLabel: true
        }
      ]
    },
    initChart(data) {
      var series = []
      var vals = []
      var scatter = data.scatter
      var items = data.items

      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      if (_.isEmpty(items)) {
        return
      }

      for (const i in scatter) {
        vals = [
          scatter[i].values[0],
          scatter[i].values[1],
          scatter[i].values[2],
          scatter[i].values[3],
          scatter[i].values[4],
          scatter[i].values[5],
          scatter[i].values[6],
          30
        ]
        series.push({
          name: scatter[i].names,
          type: 'scatter',
          data: [vals],
          symbol: 'rect',
          itemStyle: itemStyle
        })
      }

      var itemStyle = {
        opacity: 0.8,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }

      this.chart.setOption({
        title: [
        ],
        color: [
          '#c23531',
          '#ca8622',
          '#bda29a',
          '#7FD1B9',
          '#61a0a8',
          '#7A6563',
          '#E5D4CE'
        ],
        legend: [
          {
            top: 50,
            textStyle: {
              color: '#000',
              fontSize: 16
            }
          }
        ],
        tooltip: {},
        visualMap: [
          {
            left: 'right',
            top: '10%',
            dimension: 7,
            show: false,
            itemWidth: 30,
            itemHeight: 120,
            calculable: true,
            precision: 0.1,
            textGap: 30,
            textStyle: {
              color: '#344B58'
            },
            inRange: {
              symbolSize: [20, 20]
            },
            outOfRange: {
              symbolSize: [20, 20],
              color: ['rgba(255,255,255,.2)']
            }
          }
        ],
        grid: this.getGridOptions(),
        xAxis: [
          {
            type: 'category',
            name: '\n\n\n\nFecha',
            nameLocation: 'middle',
            nameGap: 30,
            nameTextStyle: {
              color: '#000',
              fontSize: 14
            },
            splitLine: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#000'
              }
            },
            axisLabel: {
              rotate: 90,
              interval: 0,
              showMinLabel: true,
              showMaxLabel: true,
              formatter: function(value) {
                return value.replaceAll('-', '/')
              }
            }
          }
        ],
        yAxis: [
          {
            type: 'value',
            name: 'Hora',
            nameLocation: 'middle',
            nameGap: 40,
            nameTextStyle: {
              color: '#000',
              fontSize: 16
            },
            axisLine: {
              lineStyle: {
                color: '#000'
              }
            },
            splitLine: {
              show: false
            }
          }
        ],
        series: series
      })
    }
  }
}
</script>
