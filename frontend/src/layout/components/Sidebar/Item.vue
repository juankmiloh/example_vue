<script>

export default {
  name: 'MenuItem',
  functional: true,
  props: {
    icon: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
    fa: {
      type: Boolean,
      default: false
    }
  },
  render(h, context) {
    const { icon, title, fa } = context.props
    const vnodes = []

    if (icon) {
      if (fa) {
        vnodes.push(<v-icon name={icon} class='svg-icon'/>)
      } else {
        vnodes.push(<svg-icon icon-class={icon}/>)
      }
    }
    if (title) {
      // vnodes.push(<span slot='title'>{(title)}<br/>{(title)}</span>)
      vnodes.push(<span slot='title'>{(title)}</span>)
    }
    return vnodes
  }
}

</script>
