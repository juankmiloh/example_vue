<template>
  <div class="rcorners">
    <div id="chart" :style="{height:height,width:width}" />
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <table class="table table-striped">
        <tr v-if="statisticsNew">
          <td v-if="statisticsNew">
            <v-icon
              v-if="statisticsNew.avg > statisticsOld.avg"
              name="arrow-circle-up"
              scale="1"
              class="arrow-blue"
            />
            <v-icon
              v-else
              name="arrow-circle-down"
              scale="1"
              class="arrow-blue"
            />
          </td>
          <td>PB ({{ months[statisticsNew.moth] }})</td>
          <td width="50" />
          <td>{{ statisticsNew.avg.toFixed(2) }}</td>
        </tr>
        <tr v-if="statisticsOld">
          <td />
          <td>PB ({{ months[statisticsOld.moth] }})</td>
          <td width="50" />
          <td>{{ statisticsOld.avg.toFixed(2) }}</td>
        </tr>
      </table>
    </el-row>
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import { debounce } from '@/utils'

const months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

export default {
  props: {
    year: {
      type: Number,
      default: 2020
    },
    data: {
      type: Array,
      default: function() { return [] }
    },
    reference: {
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
      chart: null,
      statisticsNew: null,
      statisticsOld: null,
      months: months
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
      this.averages(newVal)
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
      const width = document.getElementById('chart').offsetWidth
      return width >= 700
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: 70,
          left: '25px',
          right: '25px',
          bottom: '80',
          containLabel: true
        }
      }
      return {
        top: 140,
        left: '5px',
        right: '5px',
        bottom: '80',
        containLabel: true

      }
    },
    averages(data) {
      if (data.length && data.length > 0) {
        let key = 0
        let lastKey = 0
        const statistics = []
        const refYear = data[0]
        for (let i = 0; i < refYear.dates.length; i++) {
          lastKey = parseInt(refYear.dates[i].split('/')[0])
          if (lastKey !== key) {
            statistics[lastKey] = { 'avg': refYear.values[i], 'count': 1 }
          } else {
            statistics[lastKey].avg = (statistics[lastKey].count * statistics[lastKey].avg + refYear.values[i]) / ++statistics[lastKey].count
          }
          key = lastKey
        }
        this.statisticsNew = statistics[lastKey]
        this.statisticsNew['moth'] = lastKey - 1
        if (lastKey > 1) {
          this.statisticsOld = statistics[lastKey - 1]
          this.statisticsOld['moth'] = lastKey - 2
        }
      }
    },
    initChart(data) {
      var series = []
      for (let i = 0; i < this.reference.length; i++) {
        series.push({
          name: this.$t(`indicator.reference.${this.reference[i].id}`) + ' (' + this.year + ')',
          type: 'line',
          step: 'start',
          symbolSize: 2,
          symbol: 'box',
          data: Array.from(this.reference[i].values, x => x.toFixed(2))
        })
      }
      for (let i = 0; i < data.length; i++) {
        series.push({
          name: data[i].id,
          type: 'line',
          symbolSize: 5,
          symbol: 'circle',
          data: Array.from(data[i].values, x => x.toFixed(2))
        })
      }
      var xData = data[0].dates
      var xReference = months.slice(0, parseInt(data[0].dates.slice(-1)[0].split('/')[0]))

      this.chart = echarts.init(document.getElementById('chart'))
      this.chart.clear()
      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            textStyle: {
              color: '#000'
            }
          }
        },
        legend: {
          top: '20',
          textStyle: {
            color: '#000'
          }
        },
        grid: this.getGridOptions(),
        xAxis: [{
          boundaryGap: true,
          name: '\n\nFecha',
          nameLocation: 'middle',
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          splitLine: {
            show: true
          },
          axisTick: {
            show: true,
            alignWithLabel: true
          },
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: 5,
            rotate: 45,
            fontSize: 16
          },
          data: xData
        },
        {
          type: 'category',
          name: 'Mes\n',
          nameLocation: 'middle',
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: true,
            alignWithLabel: true
          },
          splitArea: {
            show: false
          },
          axisLabel: {
            interval: 0,
            fontSize: 16
          },
          data: xReference
        }
        ],
        yAxis: [{
          name: '$/kwh\n',
          type: 'value',
          axisTick: {
            alignWithLabel: true
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          splitLine: {
            show: true
          },
          axisLabel: {
            fontSize: 16
          }
        }],
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0, 1
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
        series: series,
        color: ['#ed7d31', '#51a75e', '#a3aea5', '#344b58', '#c23531', '#E5D4CE']
      })
    }
  }
}
</script>
