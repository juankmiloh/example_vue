<template>
  <div class="sidebar-logo-container" :class="{'collapse':collapse}">
    <transition name="sidebarLogoFade">
      <router-link v-if="collapse" key="collapse" class="sidebar-logo-link" to="/">
        <img v-if="logo" :src="logo" class="sidebar-logo">
        <h1 v-else class="sidebar-title">{{ title }} </h1>
      </router-link>
      <router-link v-else key="expand" class="sidebar-logo-link" to="/">
        <img v-if="logo" :src="logo" class="sidebar-logo">
        <h1 class="sidebar-title">{{ title }} </h1>
      </router-link>
    </transition>
  </div>
</template>

<script>

import logo_sspd
  from '@/assets/logo_super.png'

export default {
  name: 'SidebarLogo',
  props: {
    collapse: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      title: 'Panel de Indicadores UMMEG',
      logo: logo_sspd
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  position: relative;
  width: 100%;
  height: 50px;
  line-height: 50px;
  //background:  rgb(255, 255, 255);
  background: rgb(48,65,86);
  text-align: center;
  overflow: hidden;
  border-bottom-color: rgb(42, 57, 76);
  border-bottom-style: solid;
  border-bottom-width: 1px;
  //border-right-color: rgb(243, 243, 243);
  border-right-color: rgb(48,65,86);
  border-right-style: solid;
  border-right-width: 5px;
  border-left-color: rgb(48,65,86);
  border-left-style: solid;
  border-left-width: 5px;
  border-top-color: rgb(48,65,86);
  border-top-style: solid;
  border-top-width: 2px;

  & .sidebar-logo-link {
    height: 100%;
    width: 100%;
    background: #fff;
    border-radius: 10px;
    border: 2px solid rgb(48,65,86);

    & .sidebar-logo {
      width: 30px;
      height: 30px;
      vertical-align: middle;
      margin-right: 8px;
    }

    & .sidebar-title {
      display: inline-block;
      margin: 0;
      color: rgb(48,65,86);
      font-weight: 600px;
      line-height: 50px;
      font-size: 14px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
    }
  }

  &.collapse {
    .sidebar-logo {
      margin-right: 0px;
    }
  }
}
</style>
