<template>
  <div class="transction-table">

    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:16px;">
      <el-collapse>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la descripción del indicador" placement="bottom-end">
          <el-collapse-item title="Descripción del indicador" name="1">
            <ul>
              <li>
                Mide la desviación de energía por agente entre la generación programada y la real, identificando variaciones mayores a 5%.
              </li>
            </ul>
          </el-collapse-item>
        </el-tooltip>
        <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar las convenciones del indicador" placement="bottom-end">
          <el-collapse-item title="Convenciones" name="2">
            <table class="table table-striped">
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-black" /></td>
                <td>Desviación menor o igual a 5%</td>
              </tr>
              <tr>
                <td><v-icon name="circle" scale="1" class="arrow-yellow" /></td>
                <td>Desviación mayor al 5%</td>
              </tr>
            </table>
          </el-collapse-item>
        </el-tooltip>
      </el-collapse>
    </el-row>

    <el-tooltip class="item" effect="dark" content="Haga click para descargar la información en archivo excel" placement="bottom-end">
      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="document" @click="handleDownload">
        {{ $t('excel.export') }} Excel
      </el-button>
    </el-tooltip>

    <div v-show="showImage" id="chart" class="chart rcorners" />

    <el-table :data="formatedData" style="width: 100%;padding-top: 15px;" class="rcorners">
      <el-table-column width="100" :render-header="appendControl">
        <template slot-scope="scope">
          <el-tooltip class="item" effect="dark" content="Haga click para mostrar u ocultar la grafica" placement="bottom-end">
            <el-checkbox v-model="scope.row.show" border @change="showChart(scope.row.index, scope.row.show)">
              <v-icon name="chart-line" class="svg-icon" />
            </el-checkbox>
          </el-tooltip>
        </template>

      </el-table-column>
      <el-table-column :label="statusTitle" width="100" align="center" prop="status" sortable>
        <template slot-scope="scope">
          <div
            :class="{'arrow-black': scope.row.status === 0,
                     'arrow-yellow': scope.row.status === 1}"
          >
            <v-icon name="circle" scale="2" />
          </div>
        </template>
      </el-table-column>
      <el-table-column :label="itemTitle" min-width="200" prop="name1" sortable>
        <template slot-scope="scope">
          {{ scope.row.name0 }}
        </template>
      </el-table-column>
      <el-table-column :label="descriptionTitle" min-width="200" prop="name0" sortable>
        <template slot-scope="scope">
          {{ scope.row.name1 }}
        </template>
      </el-table-column>
      <el-table-column :label="value1Title" width="150" align="center" prop="value0" sortable>
        <template slot-scope="scope">
          {{ Number(scope.row.value0).toFixed(2) }} %
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

import echarts from 'echarts'
import { getIndicator } from '@/api/remoteSearch'
import moment from 'moment'

export default {
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
      default: null
    },
    endDate: {
      type: Date,
      default: null
    },
    type: {
      type: String,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
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
    loading: function(val) {
      if (!val) {
        this.resetData()
      }
    },
    data: function(val) {
      this.resetData()
    },
    itemTitle: function(val) {
      this.dropAllSelections()
      this.resetData()
    }
  },
  methods: {
    appendControl(h, { column }) {
      const self = this
      return h('el-tooltip', {
        attrs: {
          effect: 'dark',
          content: 'Limpiar seleccion',
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
    resetData() {
      this.chart = null
      this.showImage = false
      this.downloadLoading = false
      this.idsToShow = new Set()
      this.chartData = {}
      this.formatedData = this.format(this.data)
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        return v[j]
      }))
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = [this.statusTitle, this.descriptionTitle, this.itemTitle, this.value1Title]
        const filterVal = ['status', 'name1', 'name0', 'value0']
        const list = this.format(this.data)
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.formatDate(moment()) + ' ' + this.indicatorName,
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
          index: data[i].id,
          name0: data[i].names[0],
          name1: data[i].names[1],
          value0: data[i].values[0],
          status: data[i].status[0]
        })
      }
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
        var result = await getIndicator('gpgr', { fecha: this.formatDate(this.startDate),
          grupo: this.type,
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
                  return Number(p.value).toFixed(2) + ' %'
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
          left: 'center',
          text: 'Desviación en generación por agente',
          x: '20',
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
              color: '#000'
            }
          }
        },
        legend: {
          x: '5%',
          top: '45px',
          textStyle: {
            color: '#000'
          }
        },
        grid: {
          left: '5px',
          right: '5px',
          borderWidth: 0,
          top: 100,
          bottom: 140,
          textStyle: {
            color: '#000'
          }
        },
        calculable: true,
        xAxis: [{
          name: '\n\n\n\nFecha',
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
            show: false
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
          name: '%',
          type: 'value',
          splitLine: {
            show: true
          },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          axisTick: {
            show: false
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
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff' },
          borderColor: '#90979c'

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
.transction-table .chart {
  width: 100%;
  height: 500px;
}
</style>
