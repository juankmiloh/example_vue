<template>
  <div class="rcorners">
    <div id="chartoc" :style="{height:height,width:width}" />
    <div class="current-inventory">Nivel de inventario {{ this.plant.text }} <span :class="resultClass">{{ level }}%</span></div>
  </div>
</template>

<script>
import moment from 'moment'
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import {
  debounce
} from '@/utils'

const animationDuration = 500

export default {
  props: {
    referenceDate: {
      type: Date,
      default: function() {
        new Date()
      }
    },
    plant: {
      type: Object,
      default: function() {
        return {}
      }
    },
    plants: {
      type: Object,
      default: function() {
        return {}
      }
    },
    data: {
      type: Array,
      default: function() {
        return []
      }
    },
    injectionData: {
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
    }
  },
  data() {
    return {
      publicConf: process.env.VUE_APP_PUBLIC === 'true',
      chart: null,
      levels: [
        { value: 100, color: '#4C9900' },
        { value: 80, color: '#F1C40F' },
        { value: 50, color: '#FF0000' },
        { value: 0, color: '#000000' }
      ],
      level: 0,
      resultClass: 'result-1'
    }
  },
  watch: {
    plant: function(newVal, oldVal) {
      console.info('event')
      this.initChart(this.data)
      this.__resizeHandler = debounce(() => {
        if (this.chart) {
          this.chart.resize()
          this.chart.setOption({
            grid: this.getGridOptions()
          })
        }
      }, 100)
      window.addEventListener('resize', this.__resizeHandler)
    },
    injectionData: function(newVal, oldVal) {
      console.info('event')
      this.initChart(this.data)
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
          top: '110px',
          left: '50px',
          right: '50px',
          bottom: '80px',
          containLabel: true
        }
      }
      return {
        top: '145px',
        left: '5px',
        right: '5px',
        bottom: '80px',
        containLabel: true

      }
    },
    getTitle() {
      if (this.plant.id === 'ToTal') {
        return 'Inventarios por planta (GBTUD)'
      }
      return `Inventario ${this.plant.text} (GBTUD)`
    },
    initChart(data) {
      const series = []
      let items = []
      var referenceDateValueStart = moment(this.referenceDate).format('YYYY-MM-DD')
      var referenceDateValueEnd = referenceDateValueStart
      var referenceDateIndex = 0
      this.chart = echarts.init(document.getElementById('chartoc'), 'macarons')
      this.chart.clear()

      var full = (this.plant.id === 'Total')

      var yAxis1 = {
        name: 'Volumen inyectado\n(GBTUD)',
        nameTextStyle: {
          fontSize: this.getFontSize()
        },
        splitArea: {
          show: false
        },
        axisLine: {
          lineStyle: {
            color: '#000'
          }
        },
        axisLabel: {
          interval: 0,
          show: true,
          textStyle: {
            fontSize: this.getFontSize()
          }
        }
      }
      var yAxis2 = {
        name: 'Inventario GNL\n(GBTUD)',
        nameTextStyle: {
          fontSize: this.getFontSize()
        },
        splitArea: {
          show: false
        },
        axisLine: {
          lineStyle: {
            color: '#000'
          }
        },
        axisLabel: {
          interval: 0,
          show: true,
          textStyle: {
            fontSize: this.getFontSize()
          }
        }
      }

      for (let i = 0; i < data.length; i++) {
        if (i === 0) {
          items = data[0].dates
          referenceDateIndex = items.indexOf(referenceDateValueStart)
          if (referenceDateIndex === -1) {
            referenceDateValueStart = items[items.length - 1]
            referenceDateIndex = items.length - 1
          }
          referenceDateValueEnd = items[items.length - 1]
          if (full) {
            this.level = (data[i].values.slice(-1)[0] * 100 / data[i].operational_values.max).toFixed(0)
            for (let j = 0; j < this.levels.length - 1; j++) {
              if (this.level > this.levels[j + 1].value) {
                this.resultClass = `result-${j}`
              }
            }
            series.push({
              color: '#ed7d31',
              name: 'Volumen inyectado',
              type: 'line',
              step: 'start',
              smooth: false,
              data: this.injectionData[0].values,
              animationDuration,
              symbol: 'circle',
              yAxisIndex: 0,
              symbolSize: 3,
              zlevel: 10,
              lineStyle: {
                width: 2
              }
            })

            if (this.publicConf) {
              series.push({
                name: this.plants[data[i].id].text,
                color: this.plants[data[i].id].color,
                type: 'line',
                step: 'start',
                areaStyle: {},
                data: Array.from(data[i].values, x => x.toFixed(2)),
                smooth: false,
                animationDuration,
                symbolSize: 1,
                yAxisIndex: full ? 1 : 0,
                Z: 1,
                symbol: 'circle',
                stack: '0',
                markArea: {
                  data: [
                    [{
                      name: referenceDateValueStart < referenceDateValueEnd ? 'Valores estimados' : '',
                      xAxis: referenceDateValueStart
                    }, {
                      xAxis: referenceDateValueEnd
                    }]
                  ]
                }
              })
            } else {
              series.push({
                color: this.plants[data[i].id].color,
                name: this.plants[data[i].id].text,
                type: 'line',
                step: 'start',
                data: Array.from(data[i].values, x => x.toFixed(2)),
                smooth: false,
                animationDuration,
                symbolSize: 2,
                yAxisIndex: full ? 1 : 0,
                zlevel: 2,
                symbol: 'circle',
                stack: '0',
                markArea: {
                  data: [
                    [{
                      name: referenceDateValueStart < referenceDateValueEnd ? 'Valores estimados' : '',
                      xAxis: referenceDateValueStart
                    }, {
                      xAxis: referenceDateValueEnd
                    }]
                  ]
                }
              })
            }
          }
        }
        if (data[i].id !== 'Total') {
          if (this.plant.id === 'Total' || data[i].id === this.plant.id) {
            series.push({
              color: this.plants[data[i].id].color,
              name: this.plants[data[i].id].text,
              type: 'line',
              step: 'start',
              areaStyle: {},
              data: Array.from(data[i].values, x => x.toFixed(2)),
              smooth: false,
              animationDuration,
              symbolSize: 1,
              yAxisIndex: full ? 1 : 0,
              zlevel: 2,
              symbol: 'circle',
              stack: '1',
              markArea: {
                data: [
                  [{
                    name: referenceDateValueStart < referenceDateValueEnd ? 'Valores estimados' : '',
                    xAxis: referenceDateValueStart
                  }, {
                    xAxis: referenceDateValueEnd
                  }]
                ]
              }
            })
            if (!full) {
              const op_max = data[i].operational_values.max
              this.level = (data[i].values.slice(-1)[0] * 100 / op_max).toFixed(0)
              for (let j = 0; j < this.levels.length - 1; j++) {
                if (this.level >= this.levels[j + 1].value) {
                  this.resultClass = `result-${j}`
                  break
                }
              }
              for (let j = 0; j < this.levels.length - 1; j++) {
                series.push({
                  color: this.levels[j].color,
                  name: `[ ${op_max * this.levels[j].value / 100} - ${op_max * this.levels[j + 1].value / 100}]`,
                  type: 'line',
                  step: 'start',
                  data: Array(items.length).fill(op_max * this.levels[j].value / 100),
                  animationDuration,
                  symbol: 'box',
                  symbolSize: 1,
                  yAxisIndex: full ? 1 : 0,
                  zlevel: 10,
                  lineStyle: {
                    width: 3,
                    type: 'dashed'
                  }
                })
              }
            }
          }
        }
      }

      if (full) {
        const op_max = data[0].operational_values.max
        for (var i = 0; i < this.levels.length - 1; i++) {
          series.push({
            color: this.levels[i].color,
            name: `[ ${op_max * this.levels[i].value / 100} - ${op_max * this.levels[i + 1].value / 100}]`,
            type: 'line',
            step: 'start',
            data: Array(items.length).fill(op_max * this.levels[i].value / 100),
            animationDuration,
            symbol: 'box',
            symbolSize: 1,
            yAxisIndex: full ? 1 : 0,
            zlevel: 10,
            lineStyle: {
              width: 3,
              type: 'dashed'
            }
          })
        }

        series.push({
          color: '#76448A ',
          name: 'Mínimo operativo',
          type: 'line',
          step: 'start',
          data: Array(items.length).fill(data[0].operational_values.min),
          animationDuration,
          symbol: 'box',
          symbolSize: 1,
          yAxisIndex: full ? 1 : 0,
          zlevel: 10,
          lineStyle: {
            width: 3,
            type: 'dashed'
          }
        })
      }
      this.chart.setOption({
        title: {
          left: 'center',
          text: this.getTitle(),
          textStyle: {
            color: '#000'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          top: '30px',
          textStyle: {
            color: '#000',
            fontSize: this.getFontSize()
          }
        },
        grid: this.getGridOptions(),
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
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff'
          },
          borderColor: '#000'
        },
        {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 60
        }
        ],
        xAxis: {
          name: '\n\n\n\n\nFecha',
          nameLocation: 'middle',
          type: 'category',
          silent: false,
          splitLine: {
            show: false
          },
          splitArea: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          axisLabel: {
            interval: items ? Math.floor(items.length / 20) : 10,
            rotate: 50,
            textStyle: {
              fontSize: this.getFontSize()
            }
          },
          data: items
        },
        yAxis: full ? [yAxis1, yAxis2] : [yAxis2],
        series: series
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .result-0 {
      color: #4C9900;
  }
  .result-1 {
      color: #F1C40F;
  }
  .result-2 {
      color: #FF0000;
  }
  .current-inventory {
    font-size: 35px;
    text-align: center;
  }
</style>
