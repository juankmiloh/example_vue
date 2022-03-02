(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-daae4034"],{"0bfd":function(e,t,a){"use strict";a.r(t);var n=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"dashboard-editor-container"},[a("el-row",{attrs:{gutter:8}},[a("el-col",{staticStyle:{"padding-right":"8px","margin-bottom":"30px"},attrs:{xs:{span:24},sm:{span:24},md:{span:24},lg:{span:24},xl:{span:24}}},[a("div",{staticClass:"chart-wrapper"},[a("h2",[e._v(e._s(e.$t("route.gpin")))]),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:24,lg:8}},[a("el-tag",{attrs:{type:"warning"}},[e._v("\n              Datos actualizados a fecha de "+e._s(e.printLastDate())+"\n            ")])],1)],1),e._v(" "),a("br"),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:12,lg:2}},[a("div",{staticClass:"label"},[e._v("Fecha:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:6}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"Seleccione una fecha",placement:"bottom-end"}},[a("el-date-picker",{attrs:{type:"date",align:"right",placeholder:e.$t("datePicker.date")},on:{change:function(t){return e.dateChange(t)}},model:{value:e.date,callback:function(t){e.date=t},expression:"date"}})],1)],1)],1),e._v(" "),a("br"),e._v(" "),a("el-row",{attrs:{gutter:32}},[a("el-col",{attrs:{xs:24,sm:12,lg:2}},[a("div",{staticClass:"label"},[e._v("Procedencia:")])]),e._v(" "),a("el-col",{attrs:{xs:24,sm:12,lg:22}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"Seleccione una procedencia",placement:"bottom-end"}},[a("multiselect",{attrs:{options:e.groups,multiple:!0,taggable:!0,placeholder:"Seleccione agrupación","select-label":"Seleccionar","deselect-label":"Remover","selected-label":"Seleccionado"},on:{input:function(t){return e.groupChange()},tag:function(t){return e.groupChange()}},model:{value:e.sGroups,callback:function(t){e.sGroups=t},expression:"sGroups"}})],1)],1)],1)],1),e._v(" "),a("div",{staticClass:"chart-wrapper"},[a("line-chart",{attrs:{data:e.list,public_conf:e.public_conf,"value-title":"Índice"}})],1),e._v(" "),a("div",{staticClass:"chart-wrapper"},[a("transaction-table",{attrs:{data:e.list,public_conf:e.public_conf,"indicator-name":e.indicatorName,"source-title":"Fuente","price-title":"Precio Nacional Ponderado","ratio-title":"Índice","group-name":e.groupName,value:e.value}})],1)])],1)],1)},s=[],r=(a("ac6a"),a("96cf"),a("3b8d")),i=a("c1df"),c=a.n(i),o=a("8e5f"),l=a.n(o),d=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"rcorners",style:{height:e.height,width:e.width},attrs:{id:"chartgpin"}})])},u=[],f=(a("7f7f"),a("313e")),p=a.n(f),b=a("ed08");a("817d");var h=3e3,m={props:{data:{type:Array,default:function(){return[]}},valueTitle:{type:String,default:"Índice"},className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"600px"},publicConf:{type:Boolean,default:!0}},data:function(){return{chart:null,series:[],xAxis:[]}},watch:{data:function(e,t){var a=this;this.initChart(e),this.__resizeHandler=Object(b["b"])((function(){a.chart&&(a.chart.resize(),a.chart.setOption({grid:a.getGridOptions()}))}),100),window.addEventListener("resize",this.__resizeHandler)}},beforeDestroy:function(){this.chart&&(window.removeEventListener("resize",this.__resizeHandler),this.chart.dispose(),this.chart=null)},methods:{isBigSize:function(){var e=document.getElementById("chartgpin").offsetWidth;return e>=700},getGridOptions:function(){return this.isBigSize()?{top:"120px",left:"50px",right:"50px",bottom:"40px",containLabel:!0}:{top:"170px",left:"5px",right:"5px",bottom:"40px",containLabel:!0}},initChart:function(e){var t=[];if(this.series=[],this.chart=p.a.init(document.getElementById("chartgpin"),"macarons"),this.chart.clear(),e){var a={rotate:0,align:"center",verticalAlign:"middle",position:"top",distance:15},n={normal:{show:!0,rotate:a.rotate,align:a.align,verticalAlign:a.verticalAlign,position:a.position,distance:a.distance,formatter:"{a} \n {c}",fontSize:15}};for(var s in e){var r=[];t.push(e[s].name),r.push(e[s].data[0].values[1].toFixed(2)),this.series.push({name:e[s].name,label:n,step:"end",type:"bar",data:r,smooth:!1,large:!0,animationDuration:h})}this.chart.setOption({legend:{data:t,textStyle:{color:"#000",fontSize:16}},grid:this.getGridOptions(),yAxis:[{name:"Índice",type:"value",axisTick:{alignWithLabel:!0},axisLine:{lineStyle:{color:"#000"}}}],xAxis:[{name:"Fuente",type:"category",nameLocation:"middle",axisTick:{show:!1},axisLine:{lineStyle:{color:"#000"}}}],series:this.series,tooltip:{trigger:"item",axisPointer:{type:"shadow"}}})}},formatterNumber:function(e){return e?e.toFixed(2):0}}},j=m,g=a("2877"),v=Object(g["a"])(j,d,u,!1,null,null,null),x=v.exports,y=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"transction-table"},[a("el-row",{staticStyle:{background:"#fff",padding:"16px 16px 0","margin-bottom":"16px"}},[a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"Haga click para mostrar u ocultar la descripción del indicador",placement:"bottom-end"}},[a("el-collapse",[a("el-collapse-item",{attrs:{title:"Descripción del indicador",name:"1"}},[a("b",[e._v("Precio nacional vs precio importado: ")]),e._v(" Comparación entre el\n          precio de gas de cada campo y el precio del gas que se está\n          importando al mercado colombiano. Se calcula como el cociente entre\n          el precio promedio ponderado para cada fuente de suministro y el\n          precio promedio ponderado de las importaciones físicas de gas para\n          el periodo seleccionado."),a("br")])],1)],1)],1),e._v(" "),a("el-tooltip",{staticClass:"item",attrs:{effect:"dark",content:"Haga click para descargar la información en archivo excel",placement:"bottom-end"}},[a("el-button",{staticStyle:{margin:"0 0 20px 20px"},attrs:{loading:e.downloadLoading,type:"primary",icon:"document"},on:{click:e.handleDownload}},[e._v("\n      "+e._s(e.$t("excel.export"))+" Excel\n    ")])],1),e._v(" "),a("el-table",{staticClass:"rcorners",staticStyle:{width:"100%","padding-top":"15px"},attrs:{data:e.format(e.data)}},[a("el-table-column",{attrs:{label:e.sourceTitle,prop:"name",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(t.row.name)+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:e.priceTitle,align:"center",prop:"weightedPrice",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        $ "+e._s(Number(t.row.weightedPrice))+"\n      ")]}}])}),e._v(" "),a("el-table-column",{attrs:{label:e.ratioTitle,align:"center",prop:"ratio",sortable:""},scopedSlots:e._u([{key:"default",fn:function(t){return[e._v("\n        "+e._s(Number(t.row.ratio))+"\n      ")]}}])})],1)],1)},w=[],k={props:{data:{type:Array,default:function(){return[]}},indicatorName:{type:String,default:"gpin"},sourceTitle:{type:String,default:"Fuente"},priceTitle:{type:String,default:"Precio"},ratioTitle:{type:String,default:"Índice"}},data:function(){return{chart:null,showImage:!1,downloadLoading:!1}},methods:{formatJson:function(e,t){return t.map((function(t){return e.map((function(e){return t[e]}))}))},handleDownload:function(){var e=this;this.downloadLoading=!0,Promise.all([a.e("chunk-412797d4"),a.e("chunk-179281af")]).then(a.bind(null,"4bf8d")).then((function(t){var a=[e.sourceTitle,e.priceTitle,e.ratioTitle],n=["name","weightedPrice","ratio"],s=e.format(e.data),r=e.formatJson(n,s);t.export_json_to_excel({header:a,data:r,filename:e.formatDate(c()())+" precio_naciona_vs_importado",autoWidth:e.autoWidth,bookType:e.bookType}),e.downloadLoading=!1}))},format:function(e){var t=[];for(var a in e){var n=e[a].data;for(var s in n)t.push({index:n[s].id,name:e[a].name,weightedPrice:n[s].values[0].toFixed(2),ratio:n[s].values[1].toFixed(2)})}return t},formatDate:function(e){return c()(e).format("DD-MM-YYYY")}}},_=k,D=(a("3e14"),Object(g["a"])(_,y,w,!1,null,"7cc53f9e",null)),z=D.exports,S=a("820e"),C={name:"DashboardAdmin",components:{TransactionTable:z,Multiselect:l.a,LineChart:x},data:function(){return{public_conf:!1,indicatorName:"gpin",date:new Date,lastDate:new Date,list:[],value:[],groupName:"",sGroups:[],groups:[]}},created:function(){this.fetchLatest(),this.fetchGroups()},methods:{formatDate:function(e){return c()(e).format("DD-MM-YYYY")},printLastDate:function(){return c()(this.lastDate).format("DD/MM/YYYY")},dateChange:function(e){e&&this.getData()},measureChange:function(e){this.type=e,this.getData()},fetchLatest:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,Object(S["b"])("gmg");case 3:t=e.sent,this.lastDate=new Date(t[1]),this.initDate=new Date(t[0]),e.next=12;break;case 8:e.prev=8,e.t0=e["catch"](0),this.date=new Date,console.error(e.t0);case 12:case"end":return e.stop()}}),e,this,[[0,8]])})));function t(){return e.apply(this,arguments)}return t}(),fetchGroups:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,Object(S["a"])("fuentes",{no_guajira_costa:!0});case 2:t=e.sent,this.groups=t.items,this.sGroups=t.items,this.getData();case 6:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),groupChange:function(e){this.getData()},getData:function(){var e=Object(r["a"])(regeneratorRuntime.mark((function e(){var t,a,n;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:t=[],(this.date>this.lastDate||this.date<this.initDate)&&(this.date=this.lastDate),e.prev=2,e.t0=regeneratorRuntime.keys(this.sGroups);case 4:if((e.t1=e.t0()).done){e.next=12;break}return a=e.t1.value,e.next=8,Object(S["a"])(this.indicatorName,{fecha:this.formatDate(this.date||this.lastDate),fuente:this.sGroups[a]});case 8:n=e.sent,n&&(n.items&&t.push({name:this.sGroups[a],data:n.items}),this.value=n.value),e.next=4;break;case 12:this.list=t,e.next=19;break;case 15:e.prev=15,e.t2=e["catch"](2),this.list=[],this.value=0;case 19:case"end":return e.stop()}}),e,this,[[2,15]])})));function t(){return e.apply(this,arguments)}return t}()}},O=C,L=Object(g["a"])(O,n,s,!1,null,"28a786b4",null);t["default"]=L.exports},"3e14":function(e,t,a){"use strict";a("4d99")},4678:function(e,t,a){var n={"./af":"2bfb","./af.js":"2bfb","./ar":"8e73","./ar-dz":"a356","./ar-dz.js":"a356","./ar-kw":"423e","./ar-kw.js":"423e","./ar-ly":"1cfd","./ar-ly.js":"1cfd","./ar-ma":"0a84","./ar-ma.js":"0a84","./ar-sa":"8230","./ar-sa.js":"8230","./ar-tn":"6d83","./ar-tn.js":"6d83","./ar.js":"8e73","./az":"485c","./az.js":"485c","./be":"1fc1","./be.js":"1fc1","./bg":"84aa","./bg.js":"84aa","./bm":"a7fa","./bm.js":"a7fa","./bn":"9043","./bn-bd":"9686","./bn-bd.js":"9686","./bn.js":"9043","./bo":"d26a","./bo.js":"d26a","./br":"6887","./br.js":"6887","./bs":"2554","./bs.js":"2554","./ca":"d716","./ca.js":"d716","./cs":"3c0d","./cs.js":"3c0d","./cv":"03ec","./cv.js":"03ec","./cy":"9797","./cy.js":"9797","./da":"0f14","./da.js":"0f14","./de":"b469","./de-at":"b3eb","./de-at.js":"b3eb","./de-ch":"bb71","./de-ch.js":"bb71","./de.js":"b469","./dv":"598a","./dv.js":"598a","./el":"8d47","./el.js":"8d47","./en-au":"0e6b","./en-au.js":"0e6b","./en-ca":"3886","./en-ca.js":"3886","./en-gb":"39a6","./en-gb.js":"39a6","./en-ie":"e1d3","./en-ie.js":"e1d3","./en-il":"73332","./en-il.js":"73332","./en-in":"ec2e","./en-in.js":"ec2e","./en-nz":"6f50","./en-nz.js":"6f50","./en-sg":"b7e9","./en-sg.js":"b7e9","./eo":"65db","./eo.js":"65db","./es":"898b","./es-do":"0a3c","./es-do.js":"0a3c","./es-mx":"b5b7","./es-mx.js":"b5b7","./es-us":"55c9","./es-us.js":"55c9","./es.js":"898b","./et":"ec18","./et.js":"ec18","./eu":"0ff2","./eu.js":"0ff2","./fa":"8df48","./fa.js":"8df48","./fi":"81e9","./fi.js":"81e9","./fil":"d69a","./fil.js":"d69a","./fo":"0721","./fo.js":"0721","./fr":"9f26","./fr-ca":"d9f8","./fr-ca.js":"d9f8","./fr-ch":"0e49","./fr-ch.js":"0e49","./fr.js":"9f26","./fy":"7118","./fy.js":"7118","./ga":"5120","./ga.js":"5120","./gd":"f6b46","./gd.js":"f6b46","./gl":"8840","./gl.js":"8840","./gom-deva":"aaf2","./gom-deva.js":"aaf2","./gom-latn":"0caa","./gom-latn.js":"0caa","./gu":"e0c5","./gu.js":"e0c5","./he":"c7aa","./he.js":"c7aa","./hi":"dc4d","./hi.js":"dc4d","./hr":"4ba9","./hr.js":"4ba9","./hu":"5b14","./hu.js":"5b14","./hy-am":"d6b6","./hy-am.js":"d6b6","./id":"5038","./id.js":"5038","./is":"0558","./is.js":"0558","./it":"6e98","./it-ch":"6f12","./it-ch.js":"6f12","./it.js":"6e98","./ja":"079e","./ja.js":"079e","./jv":"b540","./jv.js":"b540","./ka":"201b","./ka.js":"201b","./kk":"6d79","./kk.js":"6d79","./km":"e81d","./km.js":"e81d","./kn":"3e92","./kn.js":"3e92","./ko":"22f8","./ko.js":"22f8","./ku":"2421","./ku.js":"2421","./ky":"9609","./ky.js":"9609","./lb":"440c","./lb.js":"440c","./lo":"b29d","./lo.js":"b29d","./lt":"26f9","./lt.js":"26f9","./lv":"b97c","./lv.js":"b97c","./me":"293c","./me.js":"293c","./mi":"688b","./mi.js":"688b","./mk":"6909","./mk.js":"6909","./ml":"02fb","./ml.js":"02fb","./mn":"958b","./mn.js":"958b","./mr":"39bd","./mr.js":"39bd","./ms":"ebe4","./ms-my":"6403","./ms-my.js":"6403","./ms.js":"ebe4","./mt":"1b45","./mt.js":"1b45","./my":"8689","./my.js":"8689","./nb":"6ce3","./nb.js":"6ce3","./ne":"3a39","./ne.js":"3a39","./nl":"facd","./nl-be":"db29","./nl-be.js":"db29","./nl.js":"facd","./nn":"b84c","./nn.js":"b84c","./oc-lnc":"167b","./oc-lnc.js":"167b","./pa-in":"f3ff","./pa-in.js":"f3ff","./pl":"8d57","./pl.js":"8d57","./pt":"f260","./pt-br":"d2d4","./pt-br.js":"d2d4","./pt.js":"f260","./ro":"972c","./ro.js":"972c","./ru":"957c","./ru.js":"957c","./sd":"6784","./sd.js":"6784","./se":"ffff","./se.js":"ffff","./si":"eda5","./si.js":"eda5","./sk":"7be6","./sk.js":"7be6","./sl":"8155","./sl.js":"8155","./sq":"c8f3","./sq.js":"c8f3","./sr":"cf1e9","./sr-cyrl":"13e9","./sr-cyrl.js":"13e9","./sr.js":"cf1e9","./ss":"52bd","./ss.js":"52bd","./sv":"5fbd","./sv.js":"5fbd","./sw":"74dc","./sw.js":"74dc","./ta":"3de5","./ta.js":"3de5","./te":"5cbb","./te.js":"5cbb","./tet":"576c","./tet.js":"576c","./tg":"3b1b","./tg.js":"3b1b","./th":"10e8","./th.js":"10e8","./tk":"5aff","./tk.js":"5aff","./tl-ph":"0f38","./tl-ph.js":"0f38","./tlh":"cf75","./tlh.js":"cf75","./tr":"0e81","./tr.js":"0e81","./tzl":"cf51","./tzl.js":"cf51","./tzm":"c109","./tzm-latn":"b53d","./tzm-latn.js":"b53d","./tzm.js":"c109","./ug-cn":"6117","./ug-cn.js":"6117","./uk":"ada2","./uk.js":"ada2","./ur":"5294","./ur.js":"5294","./uz":"2e8c","./uz-latn":"010e","./uz-latn.js":"010e","./uz.js":"2e8c","./vi":"2921","./vi.js":"2921","./x-pseudo":"fd7e","./x-pseudo.js":"fd7e","./yo":"7f33","./yo.js":"7f33","./zh-cn":"5c3a","./zh-cn.js":"5c3a","./zh-hk":"49ab","./zh-hk.js":"49ab","./zh-mo":"3a6c","./zh-mo.js":"3a6c","./zh-tw":"90ea","./zh-tw.js":"90ea"};function s(e){var t=r(e);return a(t)}function r(e){var t=n[e];if(!(t+1)){var a=new Error("Cannot find module '"+e+"'");throw a.code="MODULE_NOT_FOUND",a}return t}s.keys=function(){return Object.keys(n)},s.resolve=r,e.exports=s,s.id="4678"},"4d99":function(e,t,a){},"820e":function(e,t,a){"use strict";a.d(t,"a",(function(){return s})),a.d(t,"b",(function(){return r}));var n=a("b775");function s(e,t){return Object(n["a"])({url:"/indicadores/".concat(e),method:"get",params:t})}function r(e){return Object(n["a"])({url:"/indicadores/indicador",method:"get",params:{nombre:e}})}}}]);