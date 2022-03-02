(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-25a96801"],{"17cc":function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"dashboard-editor-container"},[a("el-row",{attrs:{gutter:8}},[a("el-col",{staticStyle:{"padding-right":"8px","margin-bottom":"30px"},attrs:{xs:{span:24},sm:{span:24},md:{span:24},lg:{span:24},xl:{span:24}}},[a("h2",[e._v(" "+e._s(e.$t("route.mc"))+" ")]),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:12,lg:3}},[a("div",{staticClass:"label"},[e._v("Fecha en vigencia:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:5}},[a("el-date-picker",{attrs:{type:"month",align:"right",placeholder:e.$t("datePicker.date")},on:{change:function(t){return e.dateChange(t)}},model:{value:e.date,callback:function(t){e.date=t},expression:"date"}})],1),e._v(" "),a("el-col",{attrs:{xs:24,sm:24,lg:8}},[a("el-tag",{attrs:{type:"warning"}},[e._v("\n            Datos actualizados a fecha de "+e._s(e.printLastDate())+"\n          ")])],1),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:3}},[a("div",{staticClass:"label"},[e._v("Consultar por:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:5}},[a("el-select",{attrs:{value:e.$t(e.agent.text),placeholder:e.$t(e.agent.id)},on:{change:function(t){return e.agentChange(t)}}},e._l(e.agents,(function(t){return a("el-option",{key:t.id,attrs:{label:e.$t(t.text),value:t}})})),1)],1)],1),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:12,lg:3}},[a("div",{staticClass:"label"},[e._v("Inicio contrato:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:5}},[a("multiselect",{attrs:{options:e.years,multiple:!0,taggable:!0,placeholder:"Seleccione un año","select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.startingDateChange()},tag:function(t){return e.startingDateChange()}},model:{value:e.sYears,callback:function(t){e.sYears=t},expression:"sYears"}})],1),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:3}},[a("div",{staticClass:"label"},[e._v("Fuente:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:13}},[a("multiselect",{attrs:{options:e.sources,multiple:!0,taggable:!0,placeholder:"Seleccione una fuente","select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.sourceChange()},tag:function(t){return e.sourceChange()}},model:{value:e.sSources,callback:function(t){e.sSources=t},expression:"sSources"}})],1)],1),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:8,lg:3}},[a("div",{staticClass:"label"},[e._v("Agrupar por:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:8,lg:5}},[a("multiselect",{attrs:{options:e.grouping,multiple:!1,taggable:!0,placeholder:"Seleccione agrupación","select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.groupingChange()},tag:function(t){return e.groupingChange()}},model:{value:e.sGrouping,callback:function(t){e.sGrouping=t},expression:"sGrouping"}})],1),e._v(" "),a("el-col",{attrs:{xs:24,sm:8,lg:16}},[a("multiselect",{attrs:{options:e.groupingOptions,multiple:!0,taggable:!0,placeholder:e.groupingText,"select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.groupingOptionChange()},tag:function(t){return e.groupingOptionChange()}},model:{value:e.sGroupingOptions,callback:function(t){e.sGroupingOptions=t},expression:"sGroupingOptions"}})],1)],1),e._v(" "),a("div",{staticClass:"chart-wrapper"},[a("bubble-chart",{attrs:{data:e.list,"value-title":"Valor",agents:e.sAgents,groups:e.sGroups,grouping:e.sGrouping,"s-grouping":e.sGroupingOptions}})],1),e._v(" "),a("div",{staticClass:"chart-wrapper"},[a("transaction-table",{attrs:{data:e.list,"indicator-name":e.indicatorName,"item-title":e.sAgents[0],"description-title":e.sAgents[1],"value-title":"Porcentaje de ventas","value2-title":"Cantidades vendidas",date:e.date,status:e.status,value:e.value}})],1)],1)],1)],1)},s=[],r=(a("96cf"),a("3b8d")),o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"transction-table"},[a("el-row",{style:{height:e.showImage?e.height:"80px",width:e.width}},[a("el-col",{staticClass:"multiselect-box",attrs:{xs:24,sm:24,lg:8}},[e._v("\n      "+e._s(e.agents[0])+" "),a("br"),e._v(" "),a("multiselect",{attrs:{options:e.agents0Keys,multiple:!0,taggable:!0,placeholder:"Seleccione un "+e.agents[0],"select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.showAgent()},tag:function(t){return e.showAgent()}},model:{value:e.agents0,callback:function(t){e.agents0=t},expression:"agents0"}}),e._v(" "),a("div",{directives:[{name:"show",rawName:"v-show",value:e.showAgents1,expression:"showAgents1"}]},[e._v("\n        "+e._s(e.agents[1])+" "),a("br"),e._v(" "),a("multiselect",{attrs:{options:e.agents1Keys,multiple:!0,taggable:!0,placeholder:"Seleccione un "+e.agents[1],"select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.showAgent()},tag:function(t){return e.showAgent()}},model:{value:e.agents1,callback:function(t){e.agents1=t},expression:"agents1"}})],1)],1),e._v(" "),a("el-col",{staticClass:"rcorners",style:{height:e.showImage?e.height:"80px"},attrs:{xs:24,sm:24,lg:16}},[a("div",{staticClass:"chart",attrs:{id:"macarons"}}),e._v(" "),a("div",{staticClass:"chart",attrs:{id:"macarons2"}})])],1)],1)},i=[],l=(a("c5f6"),a("28a5"),a("1c4c"),a("5df3"),a("4f7f"),a("456d"),a("ac6a"),a("313e")),c=a.n(l),u=a("8e5f"),d=a.n(u);a("817d");var p=2e3,b=["#fce654","#91c7ae","#d3dee5","#E56399","#DE6E4B","#d48265","#749f83","#c23531","#ca8622","#bda29a","#7FD1B9","#6e7074","#546570","#c4ccd3","#61a0a8","#7A6563","#E5D4CE"],g={components:{Multiselect:d.a},props:{data:{type:Array,default:function(){return[]}},valueTitle:{type:String,default:"Valor"},className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"700px"},agents:{type:Array,default:function(){return[]}},groups:{type:Array,default:function(){return[]}},grouping:{type:String,default:"Mercado"},sGrouping:{type:Array,default:function(){return[]}}},data:function(){return{chart:null,agents0:[],agents0Keys:[],agents1:[],agents1Keys:[],agents0Data:{},showImage:!1,showAgents1:!1}},watch:{data:function(e){this.agents0Data={},this.agents1Keys=[],this.agents1=[];for(var t=0;t<e.length;t++)this.agents0Data.hasOwnProperty(e[t].names[0])||(this.agents0Data[e[t].names[0]]=[]),this.agents0Data[e[t].names[0]].push([e[t].names[2],e[t].values[0],e[t].values[1],e[t].names[1],e[t].names[0],e[t].names[3],e[t].names[4],e[t].dates[0],e[t].names[5],e[t].values[2]]);this.agents0Keys=Object.keys(this.agents0Data),this.showAgent()}},beforeDestroy:function(){this.chart&&(window.removeEventListener("resize",this.__resizeHandler),this.chart.dispose(),this.chart=null)},methods:{updateAgents1:function(){var e=new Set;if(0===this.groups.length)for(var t=this.agents0.length-1;t>=0;t--)if(this.agents0[t]in this.agents0Data)for(var a=this.agents0Data[this.agents0[t]],n=0;n<a.length;n++)e.add(a[n][3]);else this.agents0.splice(t,1);this.agents1Keys=Array.from(e)},showAgent:function(){this.updateAgents1(),this.showAgents1=!!(this.agents0.length>0&&0===this.groups.length),this.showImage=this.agents0.length>0,this.chart&&(this.chart.dispose(),this.chart=null),this.showImage&&this.initChart()},initChart:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t,a,n,s,r,o,i,l,u,d,g,h,m;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:t=this,this.chart=c.a.init(document.getElementById("macarons")),a=[{name:"Modalidad",index:0,text:"Modalidad"},{name:"Precio",index:1,text:"Precio"},{name:"Cantidad",index:2,text:"Cantidad"},{name:this.agents[1],index:3,text:this.agents[1]},{name:this.agents[0],index:4,text:this.agents[0]},{name:"Fuente",index:5,text:"Fuente"},{name:"Mercado",index:6,text:"Mercado"},{name:"Fecha inicio",index:7,text:"Fecha inicio"},{name:"Sector de consumo",index:8,text:"Sector de consumo"}],console.info("grouping",this.grouping),n=[],this.min=1e9,s=6,e.t0=this.grouping,e.next="Mercado"===e.t0?10:"Modalidad"===e.t0?12:"Sector de consumo"===e.t0?14:16;break;case 10:return s=6,e.abrupt("break",16);case 12:return s=0,e.abrupt("break",16);case 14:return s=8,e.abrupt("break",16);case 16:for(r=0;r<this.sGrouping.length;r++){for(o=[],i={normal:{opacity:.8,shadowBlur:10,shadowOffsetX:0,shadowOffsetY:0,shadowColor:"rgba(0,0,0,0.3)"}},l=0;l<this.agents0.length;l++)for(u=this.agents0Data[this.agents0[l]],d=0;d<u.length;d++)this.sGrouping[r]===u[d][s]&&(g=u[d].slice(),h=g[2],g[2]=g[0],g[0]=h,h=g[9],g[9]=g[2],g[2]=h,0!==s&&(h=g[s],g[s]=g[3],g[3]=h),o.push(g));m={name:this.sGrouping[r],type:"scatter",itemStyle:i,data:o,animationDuration:p,label:{formatter:"{b}:  {d}%"},symbolSize:function(e){return Math.sqrt(e[2])/1.5}},console.log(m),n.push(m)}this.chart.setOption({grid:{x:"7%",x2:160,y:"17%",y2:"7%"},legend:{x:"15%",top:"3%",textStyle:{color:"#000"}},tooltip:{padding:10,backgroundColor:"#222",borderColor:"#777",borderWidth:1,formatter:function(e){var n=e.value;switch(console.info("values:",n),t.grouping){case"Mercado":return'<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">'+a[4].text+"："+n[4]+'</div><div style="font-size: 12px;">'+a[3].text+"："+n[6].split(";").join("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")+"<br>"+a[0].text+"："+n[9]+"<br>"+a[1].text+"："+Number(n[1]).toFixed(2)+"<br>"+a[2].text+"："+Number(n[2]).toFixed(2)+"<br>"+a[5].text+"："+("Secundario"===n[3]?"Secundario":n[5])+"<br>"+a[6].text+"："+n[3]+"<br>"+a[7].text+"："+n[7]+"<br>"+a[8].text+"："+n[8]+"<br></div>";case"Modalidad":return'<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">'+a[4].text+"："+n[4]+'</div><div style="font-size: 12px;">'+a[3].text+"："+n[3].split(";").join("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")+"<br>"+a[0].text+"："+n[9]+"<br>"+a[1].text+"："+Number(n[1]).toFixed(2)+"<br>"+a[2].text+"："+Number(n[2]).toFixed(2)+"<br>"+a[5].text+"："+("Secundario"===n[6]?"Secundario":n[5])+"<br>"+a[6].text+"："+n[6]+"<br>"+a[7].text+"："+n[7]+"<br>"+a[8].text+"："+n[8]+"<br></div>";case"Sector de consumo":return'<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 12px;padding-bottom: 7px;margin-bottom: 7px">'+a[4].text+"："+n[4]+'</div><div style="font-size: 12px;">'+a[3].text+"："+n[8].split(";").join("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")+"<br>"+a[0].text+"："+n[9]+"<br>"+a[1].text+"："+Number(n[1]).toFixed(2)+"<br>"+a[2].text+"："+Number(n[2]).toFixed(2)+"<br>"+a[5].text+"："+("Secundario"===n[6]?"Secundario":n[5])+"<br>"+a[6].text+"："+n[6]+"<br>"+a[7].text+"："+n[7]+"<br>"+a[8].text+"："+n[3]+"<br></div>"}}},xAxis:{axisTick:{alignWithLabel:!0},type:"value",name:"Energía (GBTUD)",min:null,nameLocation:"middle",nameTextStyle:{color:"#000",fontSize:16,padding:10},splitLine:{show:!1},axisLine:{lineStyle:{color:"#000"}}},yAxis:{type:"value",name:"Precio (USD/MBTU)",min:null,nameLocation:"middle",nameTextStyle:{color:"#000",fontSize:16,padding:10},axisLine:{lineStyle:{color:"#000"}},splitLine:{show:!1}},visualMap:[{left:"right",top:"20%",dimension:2,min:0,max:1e5,itemWidth:60,itemHeight:300,calculable:!0,precision:"auto",text:["Volumen"],textGap:30,textStyle:{color:"#000"},inRange:{symbolSize:[10,70]},outOfRange:{symbolSize:[10,70],color:["rgba(255,255,255,0.4)"]},controller:{inRange:{color:["#c23531"]},outOfRange:{color:["#999"]}}}],series:n,color:b});case 18:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}()}},h=g,m=a("2877"),f=Object(m["a"])(h,o,i,!1,null,null,null),v=f.exports,x=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"transction-table"},[a("el-row",{staticStyle:{background:"#fff",padding:"16px 16px 0","margin-bottom":"32px"}},[a("el-col",{attrs:{xs:24,sm:24,lg:24}},[a("el-collapse",[a("el-collapse-item",{attrs:{title:"Descripción del indicador",name:"1"}},[e._v("\n          Corresponde a la contratación de cada productor en función de volumen y precio\n        ")])],1)],1)],1),e._v(" "),a("el-button",{staticStyle:{margin:"0 0 20px 20px"},attrs:{loading:e.downloadLoading,type:"primary",icon:"document"},on:{click:e.handleDownload}},[e._v("\n    "+e._s(e.$t("excel.export"))+" Excel\n  ")]),e._v(" "),a("el-table",{staticClass:"rcorners",staticStyle:{width:"100%","padding-top":"15px"},attrs:{data:e.format(e.data)}},[a("el-table-column",{attrs:{label:e.itemTitle,"min-width":"200",prop:"name0",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name0)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:e.descriptionTitle,"min-width":"200",prop:"name1",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name1)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Modalidad","min-width":"90",prop:"name2",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name2)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Fuente","min-width":"90",prop:"name3",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name3)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Mercado","min-width":"90",prop:"name4",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name4)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Fecha Inicio","min-width":"80",prop:"date0",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.date0)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Precio (USD/MBTU)",width:"80",align:"center",prop:"value",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(Number(t.row.value0).toFixed(2))+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Cantidad (GBTUD)",width:"80",align:"center",prop:"value",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(Number(t.row.value1).toFixed(2))+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:"Sector de consumo",width:"110",align:"center",prop:"value",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name5)+"\n      ")]}}])})],1)],1)},j=[],y=a("c1df"),w=a.n(y),S=["success","warning","danger"],_={filters:{trafficLightStatusFilter:function(e){return S[e]}},props:{data:{type:Array,default:function(){return[]}},indicatorName:{type:String,default:"preofe"},itemTitle:{type:String,default:"Item"},descriptionTitle:{type:String,default:"Descripción"},valueTitle:{type:String,default:"Valor"},value2Title:{type:String,default:"Valor"},units:{type:String,default:"Cantidad"},statusTitle:{type:String,default:"Estado"},date:{type:Date},status:{default:!1},value:{default:0}},data:function(){return{chart:null,showImage:!1,downloadLoading:!1}},methods:{formatJson:function(e,t){return t.map((function(t){return e.map((function(e){return t[e]}))}))},handleDownload:function(){var e=this;this.downloadLoading=!0,Promise.all([a.e("chunk-412797d4"),a.e("chunk-179281af")]).then(a.bind(null,"4bf8d")).then((function(t){var a=["Id",e.itemTitle,e.descriptionTitle,"Modalidad","Precio (USD/MBTU)","Cantidad (GBTUD)"],n=["index","name0","name1","name2","name3","name4","value0","value1"],s=e.format(e.data),r=e.formatJson(n,s);t.export_json_to_excel({header:a,data:r,filename:e.formatDate(w()())+" "+e.indicatorName,autoWidth:e.autoWidth,bookType:e.bookType}),e.downloadLoading=!1}))},format:function(e){for(var t=[],a=0;a<e.length;a++)t.push({index:e[a].id,name0:e[a].names[0],name1:e[a].names[1],name2:e[a].names[2],name3:e[a].names[3],name4:e[a].names[4],value0:e[a].values[0],value1:e[a].values[1],status:e[a].status,date0:e[a].dates[0],name5:e[a].names[5]});return t},formatDate:function(e){return w()(e).format("DD-MM-YYYY")}}},D=_,k=(a("8de1"),Object(m["a"])(D,x,j,!1,null,"fcb7e5e4",null)),O=k.exports,C=a("820e"),A=[{id:"vendedor",text:"indicator.types.groupBySeller"},{id:"comprador",text:"indicator.types.groupByShopper"}],R={vendedor:["precio"],comprador:["precio"]},M=["Mercado","Modalidad","Sector de consumo"],T={Mercado:["Primario","Secundario"],Modalidad:["Firme","Interrumpible"],"Sector de consumo":[]},z={Mercado:"Seleccione un mercado",Modalidad:"Seleccione una modalidad","Sector de consumo":"Seleccione un sector"},G=[{id:null,text:"todos"},{id:"COMERCIALIZADOR",text:"COMERCIALIZADOR"},{id:"PRODUCTOR-COMERCIALIZADOR",text:"PRODUCTOR-COMERCIALIZADOR"},{id:"TRANSPORTADOR",text:"TRANSPORTADOR"},{id:"USUARIO NO REGULADO",text:"USUARIO NO REGULADO"},{id:"COMERCIALIZADOR GAS IMPORTADO",text:"COMERCIALIZADOR GAS IMPORTADO"},{id:"GENERADOR TERMICO",text:"GENERADOR TERMICO"}],I=["Primario","Secundario"],E=2e3,L={name:"DashboardAdmin",components:{BubbleChart:v,TransactionTable:O,Multiselect:d.a},data:function(){return{groups:R["comprador"],sGroups:[],groupingTree:T,grouping:M,sGrouping:M[0],groupingOptions:T["Mercado"],sGroupingOptions:T["Mercado"],groupingText:"Seleccione una agrupación",agents:A,sAgents:["vendedor","comprador"],agent:A[0],roles:G,role:G[2],markets:I,sMarkets:[I[0]],years:[],sYears:[],sources:[],sSources:[],indicatorName:"gpd",date:new Date,list:[],status:!1,value:0}},created:function(){this.getSources(),this.getSectors(),this.fetchLatest()},methods:{fetchLatest:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t,a,n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(C["b"])("gmg");case 3:for(t=e.sent,this.lastDate=new Date(t[1]),this.initDate=new Date(t[0]),this.date=this.lastDate,a=this.lastDate.getFullYear(),this.years=[],n=E;n<=a;n++)this.years.push(n);e.next=15;break;case 12:e.prev=12,e.t0=e["catch"](0),this.date=new Date;case 15:this.getData();case 16:case"end":return e.stop()}}),e,this,[[0,12]])})));function t(){return e.apply(this,arguments)}return t}(),printLastDate:function(){return w()(this.lastDate).format("DD/MM/YYYY")},formatDate:function(e){return w()(e).format("DD-MM-YYYY")},dateChange:function(e){this.getData()},agentChange:function(e){"comprador"===e.id?this.sAgents=["comprador","vendedor"]:this.sAgents=["vendedor","comprador"],this.groups=R[e.id],this.agent=e,this.getData()},groupChange:function(){this.getData()},groupingChange:function(){this.sGroupingOptions=this.groupingTree[this.sGrouping],this.groupingOptions=this.groupingTree[this.sGrouping],this.groupingText=z[this.sGrouping],this.getData()},groupingOptionChange:function(){this.getData()},sourceChange:function(){this.getData()},marketChange:function(){this.getData()},startingDateChange:function(){this.getData()},getSectors:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(C["a"])("sectores");case 3:t=e.sent,t.items&&(this.groupingTree["Sector de consumo"]=t.items),e.next=10;break;case 7:e.prev=7,e.t0=e["catch"](0),console.error("error",e.t0);case 10:case"end":return e.stop()}}),e,this,[[0,7]])})));function t(){return e.apply(this,arguments)}return t}(),getSources:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(C["a"])("fuentes");case 3:t=e.sent,t.items&&(this.sources=t.items),e.next=10;break;case 7:e.prev=7,e.t0=e["catch"](0),console.error("error",e.t0);case 10:case"end":return e.stop()}}),e,this,[[0,7]])})));function t(){return e.apply(this,arguments)}return t}(),getData:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t,a,n,s;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return t=[],a=[],n=[],"Mercado"===this.sGrouping?t=this.sGroupingOptions:"Modalidad"===this.sGrouping?a=this.sGroupingOptions:"Sector de consumo"===this.sGrouping&&(n=this.sGroupingOptions),e.prev=4,e.next=7,Object(C["a"])(this.indicatorName,{fecha:this.formatDate(this.date),agrupar:this.sGroups,fuente:this.sSources,mercado:t,fecha_inicial:this.sYears,tipo_agente:this.agent.id,rol_vendedor:this.role.id,modalidad:a,sector:n});case 7:s=e.sent,s&&(this.list=s.items,this.status=s.status,this.value=s.value),e.next=16;break;case 11:e.prev=11,e.t0=e["catch"](4),console.error(e.t0),this.list=[],this.value=0;case 16:case"end":return e.stop()}}),e,this,[[4,11]])})));function t(){return e.apply(this,arguments)}return t}()}},N=L,F=Object(m["a"])(N,n,s,!1,null,"332a71b0",null);t["default"]=F.exports},4678:function(e,t,a){var n={"./af":"2bfb","./af.js":"2bfb","./ar":"8e73","./ar-dz":"a356","./ar-dz.js":"a356","./ar-kw":"423e","./ar-kw.js":"423e","./ar-ly":"1cfd","./ar-ly.js":"1cfd","./ar-ma":"0a84","./ar-ma.js":"0a84","./ar-sa":"8230","./ar-sa.js":"8230","./ar-tn":"6d83","./ar-tn.js":"6d83","./ar.js":"8e73","./az":"485c","./az.js":"485c","./be":"1fc1","./be.js":"1fc1","./bg":"84aa","./bg.js":"84aa","./bm":"a7fa","./bm.js":"a7fa","./bn":"9043","./bn-bd":"9686","./bn-bd.js":"9686","./bn.js":"9043","./bo":"d26a","./bo.js":"d26a","./br":"6887","./br.js":"6887","./bs":"2554","./bs.js":"2554","./ca":"d716","./ca.js":"d716","./cs":"3c0d","./cs.js":"3c0d","./cv":"03ec","./cv.js":"03ec","./cy":"9797","./cy.js":"9797","./da":"0f14","./da.js":"0f14","./de":"b469","./de-at":"b3eb","./de-at.js":"b3eb","./de-ch":"bb71","./de-ch.js":"bb71","./de.js":"b469","./dv":"598a","./dv.js":"598a","./el":"8d47","./el.js":"8d47","./en-au":"0e6b","./en-au.js":"0e6b","./en-ca":"3886","./en-ca.js":"3886","./en-gb":"39a6","./en-gb.js":"39a6","./en-ie":"e1d3","./en-ie.js":"e1d3","./en-il":"73332","./en-il.js":"73332","./en-in":"ec2e","./en-in.js":"ec2e","./en-nz":"6f50","./en-nz.js":"6f50","./en-sg":"b7e9","./en-sg.js":"b7e9","./eo":"65db","./eo.js":"65db","./es":"898b","./es-do":"0a3c","./es-do.js":"0a3c","./es-mx":"b5b7","./es-mx.js":"b5b7","./es-us":"55c9","./es-us.js":"55c9","./es.js":"898b","./et":"ec18","./et.js":"ec18","./eu":"0ff2","./eu.js":"0ff2","./fa":"8df48","./fa.js":"8df48","./fi":"81e9","./fi.js":"81e9","./fil":"d69a","./fil.js":"d69a","./fo":"0721","./fo.js":"0721","./fr":"9f26","./fr-ca":"d9f8","./fr-ca.js":"d9f8","./fr-ch":"0e49","./fr-ch.js":"0e49","./fr.js":"9f26","./fy":"7118","./fy.js":"7118","./ga":"5120","./ga.js":"5120","./gd":"f6b46","./gd.js":"f6b46","./gl":"8840","./gl.js":"8840","./gom-deva":"aaf2","./gom-deva.js":"aaf2","./gom-latn":"0caa","./gom-latn.js":"0caa","./gu":"e0c5","./gu.js":"e0c5","./he":"c7aa","./he.js":"c7aa","./hi":"dc4d","./hi.js":"dc4d","./hr":"4ba9","./hr.js":"4ba9","./hu":"5b14","./hu.js":"5b14","./hy-am":"d6b6","./hy-am.js":"d6b6","./id":"5038","./id.js":"5038","./is":"0558","./is.js":"0558","./it":"6e98","./it-ch":"6f12","./it-ch.js":"6f12","./it.js":"6e98","./ja":"079e","./ja.js":"079e","./jv":"b540","./jv.js":"b540","./ka":"201b","./ka.js":"201b","./kk":"6d79","./kk.js":"6d79","./km":"e81d","./km.js":"e81d","./kn":"3e92","./kn.js":"3e92","./ko":"22f8","./ko.js":"22f8","./ku":"2421","./ku.js":"2421","./ky":"9609","./ky.js":"9609","./lb":"440c","./lb.js":"440c","./lo":"b29d","./lo.js":"b29d","./lt":"26f9","./lt.js":"26f9","./lv":"b97c","./lv.js":"b97c","./me":"293c","./me.js":"293c","./mi":"688b","./mi.js":"688b","./mk":"6909","./mk.js":"6909","./ml":"02fb","./ml.js":"02fb","./mn":"958b","./mn.js":"958b","./mr":"39bd","./mr.js":"39bd","./ms":"ebe4","./ms-my":"6403","./ms-my.js":"6403","./ms.js":"ebe4","./mt":"1b45","./mt.js":"1b45","./my":"8689","./my.js":"8689","./nb":"6ce3","./nb.js":"6ce3","./ne":"3a39","./ne.js":"3a39","./nl":"facd","./nl-be":"db29","./nl-be.js":"db29","./nl.js":"facd","./nn":"b84c","./nn.js":"b84c","./oc-lnc":"167b","./oc-lnc.js":"167b","./pa-in":"f3ff","./pa-in.js":"f3ff","./pl":"8d57","./pl.js":"8d57","./pt":"f260","./pt-br":"d2d4","./pt-br.js":"d2d4","./pt.js":"f260","./ro":"972c","./ro.js":"972c","./ru":"957c","./ru.js":"957c","./sd":"6784","./sd.js":"6784","./se":"ffff","./se.js":"ffff","./si":"eda5","./si.js":"eda5","./sk":"7be6","./sk.js":"7be6","./sl":"8155","./sl.js":"8155","./sq":"c8f3","./sq.js":"c8f3","./sr":"cf1e9","./sr-cyrl":"13e9","./sr-cyrl.js":"13e9","./sr.js":"cf1e9","./ss":"52bd","./ss.js":"52bd","./sv":"5fbd","./sv.js":"5fbd","./sw":"74dc","./sw.js":"74dc","./ta":"3de5","./ta.js":"3de5","./te":"5cbb","./te.js":"5cbb","./tet":"576c","./tet.js":"576c","./tg":"3b1b","./tg.js":"3b1b","./th":"10e8","./th.js":"10e8","./tk":"5aff","./tk.js":"5aff","./tl-ph":"0f38","./tl-ph.js":"0f38","./tlh":"cf75","./tlh.js":"cf75","./tr":"0e81","./tr.js":"0e81","./tzl":"cf51","./tzl.js":"cf51","./tzm":"c109","./tzm-latn":"b53d","./tzm-latn.js":"b53d","./tzm.js":"c109","./ug-cn":"6117","./ug-cn.js":"6117","./uk":"ada2","./uk.js":"ada2","./ur":"5294","./ur.js":"5294","./uz":"2e8c","./uz-latn":"010e","./uz-latn.js":"010e","./uz.js":"2e8c","./vi":"2921","./vi.js":"2921","./x-pseudo":"fd7e","./x-pseudo.js":"fd7e","./yo":"7f33","./yo.js":"7f33","./zh-cn":"5c3a","./zh-cn.js":"5c3a","./zh-hk":"49ab","./zh-hk.js":"49ab","./zh-mo":"3a6c","./zh-mo.js":"3a6c","./zh-tw":"90ea","./zh-tw.js":"90ea"};function s(e){var t=r(e);return a(t)}function r(e){var t=n[e];if(!(t+1)){var a=new Error("Cannot find module '"+e+"'");throw a.code="MODULE_NOT_FOUND",a}return t}s.keys=function(){return Object.keys(n)},s.resolve=r,e.exports=s,s.id="4678"},"820e":function(e,t,a){"use strict";a.d(t,"a",(function(){return s})),a.d(t,"b",(function(){return r}));var n=a("b775");function s(e,t){return Object(n["a"])({url:"/indicadores/".concat(e),method:"get",params:t})}function r(e){return Object(n["a"])({url:"/indicadores/indicador",method:"get",params:{nombre:e}})}},"8de1":function(e,t,a){"use strict";a("e3e3")},e3e3:function(e,t,a){}}]);