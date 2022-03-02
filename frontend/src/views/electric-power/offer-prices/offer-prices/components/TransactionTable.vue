<template>
  <div class="transction-table">
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            Mostrar y comparar los precios que oferta cada planta, presentando el valor ofertado para cada día.

            Esta información se publica de acuerdo con lo establecido en la Resolución CREG 138 de 2010.
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar las convenciones del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <table class="table table-striped">
              <tr>
                <td><v-icon name="minus-circle" scale="1" class="arrow-blue" /></td>
                <td>Constante</td>
                <td width="50" />
                <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
                <td>Diferencia menor al 10% del valor inicial</td>
              </tr>
              <tr>
                <td><v-icon name="arrow-circle-down" scale="1" class="arrow-blue" /></td>
                <td>Baja</td>
                <td />
                <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
                <td>Diferencia mayor al 10% del valor inicial</td>
              </tr>
              <tr>
                <td><v-icon name="arrow-circle-up" scale="1" class="arrow-blue" /></td>
                <td>Sube</td>
                <td />
                <td><v-icon name="circle" scale="1" class="arrow-red" /></td>
                <td>Diferencia mayor al 20% del valor inicial</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>
    <div v-show="showImage" id="chart" class="chart rcorners" />
    <br>
    <el-tooltip class="item" effect="dark" content="Haga clic para descargar la información en archivo excel" placement="bottom-end">
      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
        {{ $t('excel.export') }} Excel
      </el-button>
    </el-tooltip>
    <el-table :data="formatedData" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column width="100" :render-header="appendControl">
        <template slot-scope="scope">
          <el-tooltip class="item" effect="dark" content="Haga clic para agregar o quitar gráfica" placement="bottom-end">
            <el-checkbox v-model="scope.row.show" border @change="showChart(scope.row.index, scope.row.show)">
              <v-icon name="chart-line" class="svg-icon" />
            </el-checkbox>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column :label="statusTitle" width="100" align="center" prop="status" sortable>
        <template slot-scope="scope">
          <el-tag v-if="statusType === 'trafficLight'" :type="scope.row.status | trafficLightStatusFilter" />
          <div
            :class="{'arrow-black': scope.row.status === 0,
                     'arrow-yellow': scope.row.status === 1,
                     'arrow-red': scope.row.status === 2}"
          >
            <v-icon :name="scope.row.trend | trendStatusFilter" scale="2" />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="itemTitle" min-width="200" prop="name1" sortable>
        <template slot-scope="scope">
          {{ scope.row.name1 }}
        </template>
      </el-table-column>
      <el-table-column :label="descriptionTitle" min-width="200" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="value1Title" width="150" align="center" prop="value0" sortable>
        <template slot-scope="scope">
          {{ scope.row.value0 }}
        </template>
      </el-table-column>
      <el-table-column :label="value2Title" width="150" align="center" prop="value1" sortable>
        <template slot-scope="scope">
          {{ scope.row.value1 }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import echarts from 'echarts'
import { getIndicator } from '@/api/remoteSearch'
import moment from 'moment'

const TRAFFIC_LIGHT_OPTIONS = ['success', 'warning', 'danger']
const TREND_OPTIONS = ['minus-circle', 'arrow-circle-down', 'arrow-circle-up']

export default {
  filters: {
    trafficLightStatusFilter(status) {
      return TRAFFIC_LIGHT_OPTIONS[status]
    },
    trendStatusFilter(status) {
      return TREND_OPTIONS[status]
    }
  },
  props: {
    data: {
      type: Array,
      default: function() { return [] }
    },
    indicatorName: {
      type: String,
      default: 'preofe'
    },
    itemTitle: {
      type: String,
      default: 'Item'
    },
    descriptionTitle: {
      type: String,
      default: 'Descripción'
    },
    value1Title: {
      type: String,
      default: 'Valor'
    },
    units: {
      type: String,
      default: 'Cantidad'
    },
    value2Title: {
      type: String,
      default: 'Valor'
    },
    statusTitle: {
      type: String,
      default: 'Estado'
    },
    trendTitle: {
      type: String,
      default: 'Tendencia'
    },
    statusType: {
      type: String,
      default: 'Trend'
    },
    startDate: {
      type: Date,
      default: new Date()
    },
    endDate: {
      type: Date,
      default: new Date()
    }
  },
  data() {
    return {
      chart: null,
      showImage: false,
      downloadLoading: false,
      idsToShow: new Set(),
      chartData: {},
      formatedData: []
    }
  },
  watch: {
    data: function(newVal, oldVal) {
      this.formatedData = this.format(newVal)
      this.showImage = this.idsToShow.size > 0
      if (this.showImage) {
        this.initChart(Array.from(this.idsToShow))
      }
    }
  },
  methods: {
    isBigSize() {
      const width = document.getElementById('chart').offsetWidth
      return width >= 700
    },
    getFontSize() {
      return this.isBigSize() ? 13 : 9
    },
    getGridOptions() {
      if (this.isBigSize()) {
        return {
          top: '120px',
          left: '20px',
          right: '20px',
          bottom: '80px',
          containLabel: true
        }
      }
      return {
        top: '180px',
        left: '1px',
        right: '1px',
        bottom: '80px',
        containLabel: true

      }
    },
    appendControl(h, { column }) {
      const self = this
      return h('el-tooltip', {
        attrs: {
          effect: 'dark',
          content: 'Deseleccionar todo',
          placement: 'top'
        }
      },
      [h('el-button', {
        on: {
          click: self.dropAllSelections
        }
      },
      [h(
        'v-icon', {
          attrs: {
            name: 'tasks',
            class: 'svg-icon'
          }
        }
      ),
      ' ',
      h(
        'v-icon', {
          attrs: {
            name: 'trash-alt',
            class: 'svg-icon'
          }
        }
      )
      ]
      )
      ]
      )
    },
    dropAllSelections() {
      for (var i = 0; i < this.formatedData.length; i++) {
        this.formatedData[i].show = false
      }
      this.idsToShow.clear()
      this.showImage = false
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = [this.itemTitle, this.descriptionTitle, this.value1Title, this.value2Title, this.statusTitle, this.trendTitle]
        const filterVal = ['name1', 'name0', 'value0', 'value1', 'status', 'trend']
        const list = this.format(this.data)
        const data = this.formatJson(filterVal, list)

        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.formatDate(moment()) + ' ' + 'precios de oferta',
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        this.downloadLoading = false
      })
    },
    format(data) {
      var formatedData = []
      for (var i = 0; i < data.length; i++) {
        formatedData.push({
          index: data[i].index,
          name0: data[i].names[0],
          name1: data[i].names[1],
          value0: data[i].values[0],
          value1: data[i].values[1],
          status: data[i].status,
          trend: data[i].trend
        })
      }

      // Ordenar por status descendiente
      formatedData = formatedData.sort(function(a, b) {
        return b.status - a.status
      })
      return formatedData
    },
    showChart(id, show) {
      if (show) {
        this.idsToShow.add(id)
      } else if (this.idsToShow.has(id)) {
        this.idsToShow.delete(id)
      }
      this.initChart(Array.from(this.idsToShow))
      this.showImage = this.idsToShow.size > 0
    },
    formatDate(date) {
      return moment(date).format('DD-MM-YYYY')
    },
    async getSeries(ids) {
      var series = []
      for (var i = 0; i < ids.length; i++) {
        var result = await getIndicator('preofe', { finicial: this.formatDate(this.startDate),
          ffinal: this.formatDate(this.endDate),
          id: ids[i] })
        if (i === 0) {
          var xData = result.items[0].dates
        }
        var xValues = result.items[0].values

        var serie = {
          name: `${result.items[0].names[1]}`,
          type: 'line',
          symbolSize: 5,
          symbol: 'circle',
          itemStyle: {
            normal: {
              barBorderRadius: 0,
              label: {
                show: true,
                position: 'top',
                formatter(p) {
                  return p.value > 0 ? Number(p.value).toFixed(1) : ''
                }
              }
            }
          },
          data: xValues
        }
        series.push(serie)
      }
      return { 'xData': xData, 'series': series }
    },
    async initChart(ids) {
      this.chartData.series = null
      this.chartData = await this.getSeries(ids)

      this.chart = echarts.init(document.getElementById('chart'))
      this.chart.clear()
      this.chart.setOption({
        title: {
          text: 'Oferta de Precios',
          left: 'center',
          top: '10',
          textStyle: {
            color: '#000',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#000',
            fontSize: '16'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            textStyle: {
              color: '#fff'
            }
          }
        },
        legend: {
          top: '40px',
          textStyle: {
            color: '#000'
          }
        },
        grid: this.getGridOptions(),
        calculable: true,
        xAxis: [{
          name: '\n\n\n\nFecha',
          nameLocation: 'middle',
          axisLine: {
            lineStyle: {
              color: '#000'
            }
          },
          splitLine: {
            show: true
          },
          axisTick: {
            show: true
          },
          splitArea: {
            show: true
          },
          axisLabel: {
            interval: this.chartData.xData ? Math.floor(this.chartData.xData.length / 30) : 10,
            rotate: 45
          },
          data: this.chartData.xData
        }],
        yAxis: [{
          name: '$/kwh',
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
            interval: 0
          },
          splitArea: {
            show: false
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
            color: '#000' },
          borderColor: '#000'

        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        series: this.chartData.series
      })
    }
  }
}
</script>

<style scoped>
.arrow-black {
  color: green;
}
.arrow-yellow {
  color: orange
}
.arrow-red {
  color: red
}
.arrow-blue {
  color: #1890ff
}
</style>
