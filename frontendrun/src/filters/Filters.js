import Vue from 'vue'

// format number to given decimal points
Vue.filter('number', (value, decimals=2) => {
  return value.toFixed(decimals)
})
// convert meters to miles or km
Vue.filter('distance', (value, units='imperial', decimals=2) => {
  if (units === 'imperial') {
    return (value * 0.000621371).toFixed(decimals)
  }
  return (value / 1000).toFixed(decimals)
})
// add the units to the value
Vue.filter('units', (value, units='imperial') => {
  if (units === 'imperial') {
    return `${value} miles`
  }
  return `${value} km`
})
// format the date using C standard format codes and locale
Vue.filter('date', (value, opts='', locale='en-us') => {
  let o = opts.split('%')
  let options = {}
  o.forEach(v => {
    switch (v) {
      case 'a':
        options['weekday'] = 'short'
        break
      case 'A': 
        options['weekday'] = 'long'
        break
      case 'b':
        options['month'] = 'short'
        break
      case 'B':
        options['month'] = 'long'
        break
      case 'm':
        options['month'] = 'numeric'
        break
      case 'y':
        options['year'] = '2-digit'
        break
      case 'Y':
        options['year'] = 'numeric'
        break
      case 'd':
        options['day'] = 'numeric'
        break
    }
  })
  return value.toLocaleDateString(locale, options)
})
// format time with 00H00M. rounds to integers.
Vue.filter('time', (value) => {
  let m = value / 60
  let h = 0
  if (m > 60) {
    h = m / 60
    m = m % 60
  }
  return `${Math.round(h)}H${Math.round(m)}M`
})
